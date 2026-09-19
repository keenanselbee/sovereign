from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import asset_workflow as assets
import event_workflow as events
import propagate_workflow as propagate


class EventTests(unittest.TestCase):
    def setUp(self):
        scratch = events.core.ROOT / '.codex-temp/tests'
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.data = {'schemaVersion': 1, 'runtimeRoot': 'mod', 'groups': [
            {'id': 'events', 'scope': 'events', 'package': 'main', 'files': ['event/common.emevd.dcx'],
             'editor': {'root': 'editor', 'stripPrefix': 'event', 'base': 'src'}}],
            'sources': [{'id': 'event-sources', 'scope': 'events', 'repo': 'src/events',
                         'editorRoot': 'editor', 'editor': 'src', 'patterns': ['*.js', '*.emevd.dcx']}]}
        assets.save(self.root / 'asset-catalog.json', self.data)
        self.settings = {'roots': {k: str(self.root / k) for k in ('editor', 'live', 'vortex', 'vortexTextures')},
                         'tools': {'darkscript': str(self.root / 'compiler.exe')}}
        for name in ('mod/event/common.emevd.dcx', 'src/events/common.emevd.dcx',
                     'src/events/common.emevd.dcx.js', 'editor/src/common.emevd.dcx',
                     'editor/src/common.emevd.dcx.js', 'src/events/common_func.emevd.dcx.js',
                     'editor/src/common_func.emevd.dcx.js'):
            self.write(name, b'old')
        for patch in (mock.patch.object(events.core, 'ROOT', self.root),
                      mock.patch.object(events, 'tool_hashes', return_value={'compiler': 'v1'}),
                      mock.patch.object(events.core, 'build_inspector', return_value=(self.root, {})),
                      mock.patch.object(events.core, 'event_data', side_effect=lambda p, *a: {'Events': [{'ID': 1, 'data': p.read_text()}]})):
            patch.start(); self.addCleanup(patch.stop)
        def compile_sources(args, *unused):
            source = Path(args[args.index('-indir') + 1])
            output = Path(args[args.index('-outdir') + 1])
            for path in source.glob('*.js'):
                (output / path.name[:-3]).write_bytes(path.read_bytes())
            return mock.Mock(stdout=b'', stderr=b'')
        patch = mock.patch.object(events.core, 'run_process', side_effect=compile_sources)
        self.compiler = patch.start(); self.addCleanup(patch.stop)

    def write(self, relative, contents):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(contents)
        return path

    def test_uncompiled_editor_script_blocks_propagation_and_direct_handoff(self):
        self.write('editor/src/common.emevd.dcx.js', b'new')
        with mock.patch.object(propagate.vdb, 'project'):
            with self.assertRaisesRegex(ValueError, 'Saved event binaries are stale'):
                propagate.prepare(self.root, self.settings, 'events', 'editor', 'main', '1.0.0-dev.test')
        with self.assertRaisesRegex(ValueError, 'Saved event binaries are stale'):
            assets.prepare_handoff(self.root, self.settings, 'events', 'editor')
        self.assertEqual((self.root / 'src/events/common.emevd.dcx.js').read_bytes(), b'old')
        self.assertFalse((self.root / '.sovereign/handoffs').exists())

    def test_saved_edit_qualifies_and_handoff_preserves_authoring_only_common_func(self):
        self.write('editor/src/common.emevd.dcx.js', b'new')
        self.write('editor/src/common.emevd.dcx', b'new')
        receipt = assets.prepare_handoff(self.root, self.settings, 'events', 'editor')
        assets.apply_handoff(self.root, self.settings, receipt)
        self.assertEqual((self.root / 'mod/event/common.emevd.dcx').read_bytes(), b'new')
        self.assertEqual((self.root / 'src/events/common.emevd.dcx.js').read_bytes(), b'new')
        self.assertFalse((self.root / 'mod/event/common_func.emevd.dcx').exists())

    def test_reuse_requires_unchanged_sources_membership_and_tools(self):
        proof = events.qualify(self.root, self.settings, 'editor')
        self.assertEqual(events.qualify(self.root, self.settings, 'editor'), proof)
        self.assertEqual(self.compiler.call_count, 1)
        with mock.patch.object(events, 'tool_hashes', return_value={'compiler': 'v2'}):
            with self.assertRaisesRegex(ValueError, 'changed'):
                events.validate(self.root, self.settings, 'editor', proof)
        self.write('editor/src/new.emevd.dcx.js', b'new')
        with self.assertRaisesRegex(ValueError, 'changed'):
            events.validate(self.root, self.settings, 'editor', proof)

    def test_source_changes_after_plan_block_acceptance(self):
        self.write('editor/src/common.emevd.dcx.js', b'new')
        self.write('editor/src/common.emevd.dcx', b'new')
        receipt = assets.prepare_handoff(self.root, self.settings, 'events', 'editor')
        self.write('editor/src/common.emevd.dcx.js', b'later')
        with self.assertRaisesRegex(ValueError, 'changed'):
            assets.apply_handoff(self.root, self.settings, receipt)
        self.assertEqual((self.root / 'mod/event/common.emevd.dcx').read_bytes(), b'old')

    def test_repo_runtime_and_source_companion_must_agree(self):
        self.write('mod/event/common.emevd.dcx', b'other')
        with self.assertRaisesRegex(ValueError, 'companion differs'):
            events.qualify(self.root, self.settings, 'repo')
        self.compiler.assert_not_called()


if __name__ == '__main__':
    unittest.main()
