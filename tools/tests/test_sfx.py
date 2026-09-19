import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import asset_workflow as assets
import sfx_workflow as sfx


class SfxTests(unittest.TestCase):
    def setUp(self):
        scratch = sfx.ROOT / '.codex-temp/tests'
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.settings = {'roots': {key: str(self.root / key) for key in ('sfx', 'live', 'vortex', 'vortexTextures')}}
        self.data = {'schemaVersion': 1, 'runtimeRoot': '.', 'groups': [
            {'id': 'effects', 'scope': 'sfx', 'package': 'main', 'files': ['sfx/effects.dcx'],
             'editor': {'root': 'sfx', 'stripPrefix': 'sfx', 'base': ''}}],
            'sources': [{'id': 'sfx-sources', 'repo': 'src/sfx', 'editorRoot': 'sfx', 'editor': 'loose'}]}
        assets.save(self.root / 'asset-catalog.json', self.data)
        self.target = self.root / 'sfx/effects.dcx'
        self.target.parent.mkdir()
        self.target.write_bytes(b'old packed')
        self.source = self.root / 'sfx/loose'
        self.source.mkdir()
        (self.source / 'effect.fxr').write_bytes(b'edited source')
        directory = self.root / '.codex-temp/sfx-builds/fixture'
        directory.mkdir(parents=True)
        self.candidate = directory / 'effects.dcx'
        self.candidate.write_bytes(b'new packed')
        tool = self.root / 'tool'
        tool.write_bytes(b'qualified tool')
        self.receipt = directory / 'receipt.json'
        assets.save(self.receipt, {'kind': 'sfx-build', 'sourceRole': 'editor', 'status': 'candidate',
            'baselineFile': str(self.target), 'sourceHash': assets.checksum(self.target),
            'catalogHash': assets.fingerprint(self.data), 'settingsHash': assets.fingerprint(self.settings),
            'candidate': str(self.candidate), 'sha256': assets.checksum(self.candidate),
            'toolFiles': {str(tool): assets.checksum(tool)}})
        assets.save(directory / 'complete-source.json', {'root': str(self.source), 'files': sfx.formats.tree(self.source)})

    def test_build_save_and_restore_preserve_hardlink_peer_and_source(self):
        peer = self.root / 'peer.dcx'
        os.link(self.target, peer)
        receipt = sfx.save_build(self.root, self.settings, self.receipt)
        self.assertEqual(self.target.read_bytes(), b'new packed')
        self.assertEqual(peer.read_bytes(), b'old packed')
        self.assertEqual((receipt.parent / 'before.bin').read_bytes(), b'old packed')
        self.assertEqual((receipt.parent / 'after.bin').read_bytes(), b'new packed')
        sfx.validate_saved(self.root, self.settings, receipt)
        sfx.restore(self.root, self.settings, receipt)
        self.assertEqual(self.target.read_bytes(), b'old packed')
        self.assertEqual((self.source / 'effect.fxr').read_bytes(), b'edited source')

    def test_new_source_or_changed_tool_prevents_packed_replacement(self):
        (self.source / 'new.fxr').write_bytes(b'new source')
        with self.assertRaisesRegex(ValueError, 'source membership'):
            sfx.save_build(self.root, self.settings, self.receipt)
        (self.source / 'new.fxr').unlink()
        (self.root / 'tool').write_bytes(b'updated tool')
        with self.assertRaisesRegex(ValueError, 'tools changed'):
            sfx.save_build(self.root, self.settings, self.receipt)
        self.assertEqual(self.target.read_bytes(), b'old packed')

    def test_later_source_edit_invalidates_handoff_and_packed_edit_blocks_restore(self):
        receipt = sfx.save_build(self.root, self.settings, self.receipt)
        (self.source / 'effect.fxr').write_bytes(b'later source')
        with self.assertRaisesRegex(ValueError, 'source changed'):
            sfx.validate_saved(self.root, self.settings, receipt)
        self.target.write_bytes(b'later packed')
        with self.assertRaisesRegex(ValueError, 'later edits'):
            sfx.restore(self.root, self.settings, receipt)
        self.assertEqual(self.target.read_bytes(), b'later packed')


if __name__ == '__main__':
    unittest.main()
