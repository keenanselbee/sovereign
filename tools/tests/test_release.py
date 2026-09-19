import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import release_workflow as release


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        scratch = release.ROOT / '.codex-temp/tests'
        scratch.mkdir(parents=True, exist_ok=True)
        temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root / 'mod.json').write_text(json.dumps({'version': '1.0.0', 'releaseReady': False}))
        self.history = self.root / 'changelog.txt'
        self.history.write_text('Version 1.0.0\nAdded forging.\n')

    def test_version_commands_use_regular_target_without_changing_files(self):
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        for command in ('target-version', 'dev-version'):
            with mock.patch.object(release, 'ROOT', self.root), \
                    mock.patch.object(sys, 'argv', ['release_workflow.py', command]), \
                    mock.patch('builtins.print') as output:
                release.main()
                output.assert_called_once_with('1.0.0')
        self.assertFalse(release.check(self.root)['releaseReady'])
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})

    def test_mismatch_and_missing_history_rejected(self):
        self.history.write_text('Version 1.0.1\nFixed reward.\n')
        with self.assertRaisesRegex(ValueError, 'differ'):
            release.check(self.root)
        self.history.unlink()
        with self.assertRaises(OSError):
            release.check(self.root)

    def test_rejects_malformed_repeated_or_out_of_order_history(self):
        for text in ('', 'Version 1.0.0\n\nAdded forging.',
                     'Version 1.0.0\n- Added forging.', 'Version 1.0.0\nAdded.\nAdded.',
                     'Version 1.0.0\nAdded.\n\nVersion 1.0.0\nFixed.',
                     'Version 1.0.0\nAdded.\n\nVersion 1.0.1\nFixed.'):
            with self.subTest(text=text):
                self.history.write_text(text)
                with self.assertRaises(ValueError):
                    release.check(self.root)

    def test_release_numbering_matches_grailwright(self):
        for version in ('1.0', '01.0.0', '1.10.0', '1.0.10', '1.0.0-dev.1'):
            with self.subTest(version=version), self.assertRaises(ValueError):
                release.check(self.root, {'version': version})
        self.history.write_text('Version 11.1.1\nFixed.\n\nVersion 1.0.0\nAdded.\n')
        self.assertEqual(release.check(self.root, {'version': '11.1.1'})['historyVersions'], ['11.1.1', '1.0.0'])


if __name__ == '__main__':
    unittest.main()
