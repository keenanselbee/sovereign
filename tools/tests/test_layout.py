from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import asset_workflow as assets
import layout_workflow as layout


class LayoutTests(unittest.TestCase):
    def setUp(self):
        scratch = layout.ROOT / '.codex-temp/tests'
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.data = {'schemaVersion': 1, 'runtimeRoot': '.', 'groups': [
            {'id': 'events', 'scope': 'events', 'package': 'main', 'files': ['event/a.dcx']},
            {'id': 'icons', 'scope': 'textures', 'package': 'textures', 'files': ['menu/hi/a.tpf']}],
            'sources': [{'id': 'event-sources', 'scope': 'events', 'repo': 'event/src'}]}
        assets.save(self.root / 'asset-catalog.json', self.data)
        self.original_catalog = (self.root / 'asset-catalog.json').read_bytes()
        for name, content in [('event/a.dcx', b'event'), ('menu/hi/a.tpf', b'texture'),
                              ('event/src/a.js', b'source'), ('unrelated.txt', b'keep')]:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)

    def test_migrate_and_restore_exact_bytes_with_independent_backups(self):
        receipt = layout.plan(self.root)
        result = layout.apply(self.root, receipt)
        self.assertEqual(result['status'], 'complete')
        self.assertEqual(assets.catalog(self.root)['runtimeRoot'], 'mod')
        self.assertEqual((self.root / 'packages/textures/mod/menu/hi/a.tpf').read_bytes(), b'texture')
        self.assertEqual((self.root / 'src/events/a.js').read_bytes(), b'source')
        for row in result['moves']:
            self.assertFalse((self.root / row['before']).exists())
            self.assertEqual(assets.checksum(receipt.parent / 'backup' / row['before']), row['sha256'])
        layout.restore(self.root, receipt)
        self.assertEqual((self.root / 'asset-catalog.json').read_bytes(), self.original_catalog)
        self.assertEqual((self.root / 'event/a.dcx').read_bytes(), b'event')
        self.assertEqual((self.root / 'unrelated.txt').read_bytes(), b'keep')

    def test_new_source_rejects_plan_before_any_move(self):
        receipt = layout.plan(self.root)
        (self.root / 'event/src/later.js').write_bytes(b'later')
        with self.assertRaisesRegex(ValueError, 'membership changed'):
            layout.apply(self.root, receipt)
        self.assertTrue((self.root / 'event/a.dcx').exists())
        self.assertFalse((self.root / 'mod').exists())

    def test_partial_rename_interruption_can_be_restored(self):
        receipt = layout.plan(self.root)
        original = Path.rename
        calls = []
        def fail_second(source, target):
            calls.append(source)
            if len(calls) == 2:
                raise OSError('injected interruption')
            return original(source, target)
        with mock.patch.object(Path, 'rename', fail_second):
            with self.assertRaisesRegex(OSError, 'injected'):
                layout.apply(self.root, receipt)
        self.assertEqual(assets.read(receipt)['status'], 'interrupted')
        layout.restore(self.root, receipt)
        self.assertEqual((self.root / 'event/a.dcx').read_bytes(), b'event')
        self.assertEqual((self.root / 'menu/hi/a.tpf').read_bytes(), b'texture')

    def test_restore_refuses_later_edits_before_moving_any_file(self):
        receipt = layout.plan(self.root)
        layout.apply(self.root, receipt)
        (self.root / 'mod/event/a.dcx').write_bytes(b'new user edit')
        with self.assertRaisesRegex(ValueError, 'Later edit'):
            layout.restore(self.root, receipt)
        self.assertEqual((self.root / 'mod/event/a.dcx').read_bytes(), b'new user edit')
        self.assertFalse((self.root / 'event/a.dcx').exists())
        self.assertEqual(assets.catalog(self.root)['runtimeRoot'], 'mod')

    def test_tampered_target_and_missing_runtime_entry_are_rejected(self):
        receipt = layout.plan(self.root)
        doc = assets.read(receipt)
        doc['moves'][0]['after'] = 'unrelated.txt'
        assets.save(receipt, doc)
        with self.assertRaisesRegex(ValueError, 'outside its catalog'):
            layout.apply(self.root, receipt)
        doc['moves'].pop(0)
        assets.save(receipt, doc)
        with self.assertRaisesRegex(ValueError, 'Incomplete'):
            layout.apply(self.root, receipt)
        self.assertEqual((self.root / 'unrelated.txt').read_bytes(), b'keep')


if __name__ == '__main__':
    unittest.main()
