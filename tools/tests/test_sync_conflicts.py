from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import asset_workflow as assets
import propagate_workflow as propagate


class SyncConflictTests(unittest.TestCase):
    def setUp(self):
        scratch = Path(__file__).resolve().parents[2] / '.codex-temp/tests'
        scratch.mkdir(parents=True, exist_ok=True)
        temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.settings = {'roots': {k: str(self.root / k) for k in ('editor', 'live', 'vortex', 'vortexTextures')}}
        assets.save(self.root / 'asset-catalog.json', {'schemaVersion': 1, 'runtimeRoot': 'mod',
            'sources': [], 'groups': [{'id': 'params', 'scope': 'params', 'package': 'main',
                'files': ['regulation.bin'], 'editor': {'root': 'editor', 'stripPrefix': '', 'base': ''}}]})
        self.repo, self.editor = self.root / 'mod/regulation.bin', self.root / 'editor/regulation.bin'
        for p in (self.repo, self.editor):
            p.parent.mkdir(); p.write_bytes(b'common baseline')
        assets.record_sync_baseline(self.root, self.settings)

    def propagate(self, source):
        with mock.patch.object(propagate.vdb, 'project'):
            return propagate.prepare(self.root, self.settings, 'params', source, 'main', '1.0.1')

    def test_one_sided_edits_work_in_both_directions_and_update_baseline(self):
        for role, p, other in [('editor', self.editor, self.repo), ('repo', self.repo, self.editor)]:
            p.write_bytes(role.encode())
            plan = assets.read(self.propagate(role))
            assets.apply_handoff(self.root, self.settings, plan['handoff'])
            self.assertEqual(other.read_bytes(), role.encode())
            pair = assets.sync_state(self.root)['pairs'][assets.sync_pair(self.repo, self.editor)]
            self.assertEqual(pair['sha256'], assets.checksum(p))

    def test_stale_source_and_independent_edits_are_rejected_without_writes(self):
        self.repo.write_bytes(b'new repo')
        with self.assertRaisesRegex(ValueError, 'selected source is stale'):
            self.propagate('editor')
        self.editor.write_bytes(b'new editor')
        for role in ('repo', 'editor'):
            with self.assertRaisesRegex(ValueError, 'both sides changed'):
                self.propagate(role)
        self.assertEqual(self.repo.read_bytes(), b'new repo')
        self.assertEqual(self.editor.read_bytes(), b'new editor')
        self.assertFalse((self.root / '.sovereign/handoffs').exists())

    def test_unknown_divergence_requires_reviewed_handoff_not_automatic_selection(self):
        (self.root / '.sovereign/editor-sync.json').unlink()
        self.editor.write_bytes(b'unknown edit')
        with self.assertRaisesRegex(ValueError, 'No shared sync baseline'):
            self.propagate('editor')
        receipt = assets.prepare_handoff(self.root, self.settings, 'params', 'editor')
        assets.apply_handoff(self.root, self.settings, receipt)
        self.assertEqual(self.repo.read_bytes(), b'unknown edit')

    def test_baseline_capture_skips_divergence_and_never_changes_assets(self):
        self.editor.write_bytes(b'new editor')
        before = assets.sync_state(self.root)
        result = assets.record_sync_baseline(self.root, self.settings)
        self.assertEqual(result['recorded'], 0)
        self.assertEqual(result['skipped'], ['regulation.bin'])
        self.assertEqual(assets.sync_state(self.root), before)

    def test_reviewed_resolution_still_refuses_changes_after_plan(self):
        self.repo.write_bytes(b'repo edit'); self.editor.write_bytes(b'editor edit')
        with self.assertRaisesRegex(ValueError, 'both sides changed'):
            assets.prepare_handoff(self.root, self.settings, 'params', 'repo')
        receipt = assets.prepare_handoff(self.root, self.settings, 'params', 'repo', resolve_conflicts=True)
        self.editor.write_bytes(b'later editor edit')
        with self.assertRaisesRegex(ValueError, 'changed since plan'):
            assets.apply_handoff(self.root, self.settings, receipt)
        receipt = assets.prepare_handoff(self.root, self.settings, 'params', 'repo', resolve_conflicts=True)
        assets.apply_handoff(self.root, self.settings, receipt)
        self.assertEqual(self.editor.read_bytes(), b'repo edit')

    def test_no_change_propagation_records_current_agreement(self):
        self.repo.write_bytes(b'agreed edit'); self.editor.write_bytes(b'agreed edit')
        receipt = self.propagate('editor')
        with mock.patch.object(propagate.vdb, 'prepare', side_effect=ValueError('stage unavailable')), \
                mock.patch.object(propagate, 'unchanged_stage', return_value=None):
            with self.assertRaisesRegex(ValueError, 'stage unavailable'):
                propagate.apply(self.root, self.settings, receipt)
        self.editor.write_bytes(b'next edit')
        self.propagate('editor')  # Shared baseline is now agreed edit, not the initial bytes.

    def test_restore_does_not_relabel_divergent_contents_as_synced(self):
        self.repo.write_bytes(b'repo edit')
        receipt = assets.prepare_handoff(self.root, self.settings, 'params', 'repo')
        assets.apply_handoff(self.root, self.settings, receipt)
        assets.restore_handoff(self.root, self.settings, receipt)
        with self.assertRaisesRegex(ValueError, 'both sides changed|selected source is stale'):
            self.propagate('repo')

    def test_sfx_run_checks_conflict_before_editor_build(self):
        data = assets.catalog(self.root)
        data['groups'][0]['scope'] = 'sfx'
        assets.save(self.root / 'asset-catalog.json', data)
        (self.root / 'tools').mkdir()
        assets.save(self.root / 'tools/eldenring-paths.local.json', self.settings)
        self.repo.write_bytes(b'repo edit')
        with mock.patch.object(propagate.core, 'ROOT', self.root), \
                mock.patch.object(sys, 'argv', ['propagate_workflow.py', 'run', '--scope', 'sfx',
                                             '--from', 'editor', '--version', '1.0.1']), \
                mock.patch('finish_workflow.compatible_client'), \
                mock.patch('sfx_workflow.build_and_save') as build:
            with self.assertRaisesRegex(ValueError, 'selected source is stale'):
                propagate.main()
            build.assert_not_called()


if __name__ == '__main__':
    unittest.main()
