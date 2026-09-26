import copy
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import asset_workflow as assets
import recovered_sources as recovered


class RecoveredSourceTests(unittest.TestCase):
    def setUp(self):
        parent = Path(__file__).resolve().parents[2] / '.codex-temp/tests'
        parent.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.settings = {'roots': {name: str(self.root / name) for name in ('editor', 'live', 'vortex')}}
        self.data = {'schemaVersion': 1, 'runtimeRoot': 'mod', 'sources': [], 'groups': [
            {'id': 'menu', 'scope': 'models', 'package': 'main', 'recipe': 'binary',
             'files': ['menu/a.gfx'], 'editor': {'root': 'editor', 'base': '', 'stripPrefix': 'menu'}}],
            'recoveredSources': {'manifest': 'src/extracted-members.json'}}
        assets.save(self.root / 'asset-catalog.json', self.data)
        for name in ['mod/menu/a.gfx', 'editor/a.gfx', 'src/menu/a.gfx']:
            self.write(name, b'old')
        self.manifest = {'schemaVersion': 1, 'archives': [{
            'runtime': 'mod/menu/a.gfx', 'sha256': assets.checksum(self.root / 'mod/menu/a.gfx'),
            'kind': 'direct GFX binary', 'baselineAvailable': True, 'outputs': [{
                'source': 'src/menu/a.gfx', 'sha256': assets.checksum(self.root / 'src/menu/a.gfx'), 'size': 3}]}]}
        assets.save(self.root / 'src/extracted-members.json', self.manifest)
        self.export = mock.patch.object(recovered, 'export_archive', side_effect=self.fake_export)
        self.export.start()
        self.addCleanup(self.export.stop)

    def write(self, name, data):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        return p

    def fake_export(self, settings, binary, archive, directory):
        output = directory / 'output'
        output.mkdir(parents=True)
        candidate = output / '00000.bin'
        candidate.write_bytes(Path(binary).read_bytes())
        sha = assets.checksum(candidate)
        updated = copy.deepcopy(archive)
        updated['sha256'] = sha
        entry = updated['outputs'][0]
        entry.update(sha256=sha, size=candidate.stat().st_size)
        return {'archive': updated, 'files': [dict(entry, candidate=candidate.name)]}, output

    def plan(self, source='editor'):
        return assets.prepare_handoff(self.root, self.settings, 'models', source)

    def test_fresh_missing_edited_and_archive_drift_are_distinct(self):
        self.assertEqual(recovered.issues(self.root), [])
        self.write('src/menu/a.gfx', b'edit')
        self.assertIn('Edited recovered source', recovered.issues(self.root)[0])
        (self.root / 'src/menu/a.gfx').unlink()
        self.assertIn('Missing recovered source', recovered.issues(self.root)[0])
        self.write('mod/menu/a.gfx', b'new')
        self.assertIn('need reviewed handoff', recovered.issues(self.root)[0])
        self.assertEqual(recovered.issues(self.root, []), [])

    def test_editor_accept_refreshes_and_restores_runtime_source_and_manifest(self):
        self.write('editor/a.gfx', b'new')
        receipt = self.plan()
        self.assertEqual((self.root / 'src/menu/a.gfx').read_bytes(), b'old')
        plan = assets.read(receipt)
        self.assertEqual(len(plan['entries']), 3)
        assets.apply_handoff(self.root, self.settings, receipt)
        self.assertEqual((self.root / 'mod/menu/a.gfx').read_bytes(), b'new')
        self.assertEqual((self.root / 'src/menu/a.gfx').read_bytes(), b'new')
        self.assertEqual(recovered.issues(self.root), [])
        self.assertEqual(len(assets.sync_state(self.root)['pairs']), 1)
        assets.restore_handoff(self.root, self.settings, receipt)
        self.assertEqual((self.root / 'src/menu/a.gfx').read_bytes(), b'old')
        self.assertEqual(assets.read(self.root / 'src/extracted-members.json'), self.manifest)

    def test_independent_source_edit_blocks_even_explicit_editor_conflict_override(self):
        self.write('editor/a.gfx', b'new')
        self.write('src/menu/a.gfx', b'other independent edit')
        with self.assertRaisesRegex(ValueError, 'Independent recovered source'):
            assets.prepare_handoff(self.root, self.settings, 'models', 'editor', resolve_conflicts=True)
        self.assertEqual((self.root / 'mod/menu/a.gfx').read_bytes(), b'old')

    def test_source_edit_matching_packed_output_can_be_accepted(self):
        self.write('mod/menu/a.gfx', b'new')
        self.write('src/menu/a.gfx', b'new')
        assets.apply_handoff(self.root, self.settings, self.plan('repo'))
        self.assertEqual(recovered.issues(self.root), [])

    def test_source_edit_without_matching_output_is_rejected(self):
        self.write('src/menu/a.gfx', b'new')
        with self.assertRaisesRegex(ValueError, 'Independent recovered source'):
            self.plan('repo')

    def test_source_drift_after_plan_stops_before_any_runtime_write(self):
        self.write('editor/a.gfx', b'new')
        receipt = self.plan()
        self.write('src/menu/a.gfx', b'late edit')
        with self.assertRaisesRegex(ValueError, 'changed since plan'):
            assets.apply_handoff(self.root, self.settings, receipt)
        self.assertEqual((self.root / 'mod/menu/a.gfx').read_bytes(), b'old')

    def test_changed_manifest_after_plan_is_rejected(self):
        self.write('editor/a.gfx', b'new')
        receipt = self.plan()
        self.manifest['note'] = 'independent manifest edit'
        assets.save(self.root / 'src/extracted-members.json', self.manifest)
        with self.assertRaisesRegex(ValueError, 'changed since plan'):
            assets.apply_handoff(self.root, self.settings, receipt)

    def test_no_editor_mapping_can_refresh_reviewed_repo_snapshot(self):
        del self.data['groups'][0]['editor']
        assets.save(self.root / 'asset-catalog.json', self.data)
        self.write('mod/menu/a.gfx', b'new')
        with self.assertRaisesRegex(ValueError, 'No configured editor'):
            self.plan('editor')
        assets.apply_handoff(self.root, self.settings, self.plan('repo'))
        self.assertEqual(recovered.issues(self.root), [])

    def test_stale_sources_block_package_gate(self):
        recovered.require_fresh(self.root, 'main')
        self.write('src/menu/a.gfx', b'new')
        with self.assertRaisesRegex(ValueError, 'freshness blocks packaging'):
            recovered.require_fresh(self.root, 'main')
        recovered.require_fresh(self.root, 'textures')

    def test_manifest_cannot_name_non_source_destination(self):
        self.manifest['archives'][0]['outputs'][0]['source'] = 'mod/menu/a.gfx'
        assets.save(self.root / 'src/extracted-members.json', self.manifest)
        self.assertIn('Invalid or duplicate recovered source', recovered.issues(self.root)[0])

    def test_partial_failure_uses_existing_handoff_recovery(self):
        self.write('editor/a.gfx', b'new')
        receipt = self.plan()
        actual = assets.os.replace
        count = 0
        def fail_once(src, dst):
            nonlocal count
            if str(dst).endswith('src\\menu\\a.gfx') or str(dst).endswith('src/menu/a.gfx'):
                count += 1
                if count == 1:
                    raise OSError('simulated source publication failure')
            return actual(src, dst)
        with mock.patch.object(assets.os, 'replace', side_effect=fail_once):
            with self.assertRaises(OSError):
                assets.apply_handoff(self.root, self.settings, receipt)
        self.assertEqual(assets.read(receipt)['status'], 'interrupted')
        assets.restore_handoff(self.root, self.settings, receipt)
        self.assertEqual((self.root / 'mod/menu/a.gfx').read_bytes(), b'old')
        self.assertEqual(recovered.issues(self.root), [])


if __name__ == '__main__':
    unittest.main()
