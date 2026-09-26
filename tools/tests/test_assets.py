import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import asset_workflow as assets


class AssetTests(unittest.TestCase):
    def setUp(self):
        scratch = Path(__file__).resolve().parents[2] / '.codex-temp/tests'
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.settings = {'roots': {key: str(self.root / key) for key in ('editor', 'live', 'vortex', 'vortexTextures')}}
        self.data = {'schemaVersion': 1, 'runtimeRoot': 'mod', 'sources': [], 'groups': [
            {'id': 'maps', 'scope': 'maps', 'package': 'main', 'files': ['event/a.dcx', 'event/b.dcx'],
             'editor': {'root': 'editor', 'stripPrefix': 'event', 'base': ''}},
            {'id': 'icons', 'scope': 'textures', 'package': 'textures', 'files': ['menu/icons.bin']}]}
        self.write('asset-catalog.json', json.dumps(self.data).encode())
        for name in ('a', 'b'):
            self.write(f'mod/event/{name}.dcx', b'new-' + name.encode())
            self.write(f'editor/{name}.dcx', b'old-' + name.encode())

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def test_retired_runtime_copy_is_reported_after_layout_migration(self):
        self.write('mod.json', json.dumps({'runtimePatterns': ['event/*.dcx']}).encode())
        self.write('event/a.dcx', b'old script recreated this')
        findings = assets.inventory_review(self.root, self.settings)
        self.assertIn({'location': 'repo-retired', 'file': 'event/a.dcx',
                       'state': 'Uncatalogued', 'owner': None}, findings)

    def plan(self):
        return assets.prepare_handoff(self.root, self.settings, 'maps', 'repo')

    def test_package_ownership_optional_editor_and_runtime_root(self):
        rows = list(assets.locations(self.root, self.settings, self.data))
        self.assertEqual(rows[0]['paths']['repo'], self.root / 'mod/event/a.dcx')
        self.assertEqual(rows[-1]['paths']['vortex'], self.root / 'vortexTextures/menu/icons.bin')
        self.assertNotIn('editor', rows[-1]['paths'])
        self.assertEqual(len(rows), 3)

    def test_status_names_build_editor_and_missing_sides(self):
        self.write('live/event/a.dcx', b'new-a')
        self.write('vortex/event/a.dcx', b'new-a')
        rows = assets.status(self.root, self.settings, 'maps')
        self.assertEqual(rows[0]['comparisons'], {'repoVsSelectedBuild': 'Match',
                                                   'repoVsSavedEditor': 'Differ'})
        self.assertEqual(rows[1]['comparisons']['repoVsSelectedBuild'], 'Missing selected build')
        (self.root / 'mod/event/b.dcx').unlink()
        rows = assets.status(self.root, self.settings, 'maps')
        self.assertEqual(rows[1]['comparisons']['repoVsSavedEditor'], 'Missing repo')

    def test_source_status_compares_saved_editor_without_build(self):
        self.data['sources'] = [{'id': 'event-source', 'scope': 'maps', 'repo': 'src/events',
                                 'editorRoot': 'editor', 'editor': 'src', 'patterns': ['*.js']}]
        self.write('asset-catalog.json', json.dumps(self.data).encode())
        self.write('src/events/common.js', b'repository source')
        self.write('editor/src/common.js', b'saved editor source')
        source = next(row for row in assets.status(self.root, self.settings, 'maps', include_sources=True)
                      if row['kind'] == 'source')
        self.assertEqual(source['comparisons'], {'repoVsSavedEditor': 'Differ'})

    def test_accept_and_restore_do_not_modify_hardlink_peer(self):
        os.link(self.root / 'editor/a.dcx', self.root / 'live-peer')
        receipt = self.plan()
        result = assets.apply_handoff(self.root, self.settings, receipt)
        self.assertEqual(result['status'], 'complete')
        self.assertEqual((self.root / 'live-peer').read_bytes(), b'old-a')
        self.assertEqual((self.root / 'editor/a.dcx').read_bytes(), b'new-a')
        assets.restore_handoff(self.root, self.settings, receipt)
        self.assertEqual((self.root / 'editor/a.dcx').read_bytes(), b'old-a')

    def test_all_inputs_checked_before_first_destination_write(self):
        receipt = self.plan()
        self.write('mod/event/b.dcx', b'newer')
        with self.assertRaisesRegex(ValueError, 'changed since plan'):
            assets.apply_handoff(self.root, self.settings, receipt)
        self.assertEqual((self.root / 'editor/a.dcx').read_bytes(), b'old-a')

    def test_unchanged_companion_drift_is_detected(self):
        self.write('editor/b.dcx', b'new-b')
        receipt = self.plan()
        self.write('mod/event/b.dcx', b'newer')
        with self.assertRaisesRegex(ValueError, 'changed since plan'):
            assets.apply_handoff(self.root, self.settings, receipt)

    def test_restore_refuses_later_manual_edits(self):
        receipt = self.plan()
        assets.apply_handoff(self.root, self.settings, receipt)
        self.write('editor/b.dcx', b'manual')
        with self.assertRaisesRegex(ValueError, 'changed after handoff'):
            assets.restore_handoff(self.root, self.settings, receipt)
        self.assertEqual((self.root / 'editor/a.dcx').read_bytes(), b'new-a')

    def test_partial_accept_has_recoverable_independent_backups(self):
        receipt = self.plan()
        original = assets.os.replace
        def fail_second(src, dst):
            if str(dst) == str(self.root / 'editor/b.dcx'):
                raise OSError('simulated interruption')
            return original(src, dst)
        with mock.patch.object(assets.os, 'replace', side_effect=fail_second):
            with self.assertRaisesRegex(OSError, 'simulated'):
                assets.apply_handoff(self.root, self.settings, receipt)
        self.assertEqual(assets.read(receipt)['status'], 'interrupted')
        assets.restore_handoff(self.root, self.settings, receipt)
        self.assertEqual((self.root / 'editor/a.dcx').read_bytes(), b'old-a')
        self.assertEqual((self.root / 'editor/b.dcx').read_bytes(), b'old-b')

    def test_receipt_rejects_wrong_mapped_pair_and_backup_traversal(self):
        receipt = self.plan()
        document = assets.read(receipt)
        document['entries'][0]['destination'] = str(self.root / 'editor/b.dcx')
        assets.save(receipt, document)
        with self.assertRaisesRegex(ValueError, 'pair'):
            assets.apply_handoff(self.root, self.settings, receipt)
        receipt = self.plan()
        assets.apply_handoff(self.root, self.settings, receipt)
        document = assets.read(receipt)
        document['entries'][0]['backup'] = '../../outside'
        assets.save(receipt, document)
        with self.assertRaisesRegex(ValueError, 'contained'):
            assets.restore_handoff(self.root, self.settings, receipt)

    def test_duplicate_paths_and_complex_handoffs_fail_closed(self):
        self.data['groups'][0]['files'].append('EVENT/A.DCX')
        self.write('asset-catalog.json', json.dumps(self.data).encode())
        with self.assertRaisesRegex(ValueError, 'colliding'):
            assets.catalog(self.root)
        self.data['groups'][0]['files'].pop()
        self.write('asset-catalog.json', json.dumps(self.data).encode())
        for scope in ('all', 'hks', 'animations', 'talk'):
            with self.subTest(scope=scope), self.assertRaises(ValueError):
                assets.prepare_handoff(self.root, self.settings, scope, 'repo')

    def test_compiled_source_duplicate_requires_consistency(self):
        self.data['sources'] = [{'id': 'sources', 'scope': 'maps', 'repo': 'src/events',
                                'editorRoot': 'editor', 'editor': '', 'patterns': ['*.dcx']}]
        self.write('asset-catalog.json', json.dumps(self.data).encode())
        self.write('src/events/a.dcx', b'new-a')
        self.write('src/events/b.dcx', b'new-b')
        self.assertEqual(len(assets.read(self.plan())['entries']), 2)
        self.write('src/events/b.dcx', b'outdated compile')
        with self.assertRaisesRegex(ValueError, 'Conflicting'):
            self.plan()
        self.write('editor/a.dcx', b'new-a')
        self.write('src/events/a.dcx', b'stale-source-copy')
        with self.assertRaisesRegex(ValueError, 'Conflicting'):
            self.plan()

    def test_overlay_does_not_import_full_editor_extraction(self):
        self.data['sources'] = [{'id': 'overrides', 'scope': 'sfx', 'mode': 'overlay',
                                'repo': 'src/sfx', 'editorRoot': 'editor', 'editor': 'sfx', 'patterns': ['**/*']}]
        self.write('src/sfx/custom.fxr', b'custom')
        self.write('editor/sfx/custom.fxr', b'custom')
        self.write('editor/sfx/vanilla.fxr', b'vanilla')
        rows = [row for row in assets.locations(self.root, self.settings, self.data, True) if row['kind'] == 'source']
        self.assertEqual([row['file'] for row in rows], ['src/sfx/custom.fxr'])

    def talk_proof(self):
        self.data['groups'][0]['scope'] = 'talk'
        self.write('asset-catalog.json', json.dumps(self.data).encode())
        files = {str(row['paths']['repo']): assets.checksum(row['paths']['repo'])
                 for row in assets.locations(self.root, self.settings, self.data, True) if row['scope'] == 'talk'}
        proof = {'kind': 'talk-roundtrip', 'status': 'qualified', 'files': files, 'tools': {},
                 'catalogHash': assets.fingerprint(self.data), 'settingsHash': assets.fingerprint(self.settings)}
        return self.write('.codex-temp/talk-qualifications/test/receipt.json', json.dumps(proof).encode())

    def test_talk_proof_required_and_current_inputs_checked(self):
        proof = self.talk_proof()
        for source in ('repo', 'editor'):
            with self.assertRaises(ValueError):
                assets.prepare_handoff(self.root, self.settings, 'talk', source)
        receipt = assets.prepare_handoff(self.root, self.settings, 'talk', 'repo', proof)
        self.write('mod/event/b.dcx', b'later source')
        with self.assertRaisesRegex(ValueError, 'Talk inputs'):
            assets.apply_handoff(self.root, self.settings, receipt)
        self.assertEqual((self.root / 'editor/a.dcx').read_bytes(), b'old-a')

    def test_qualified_talk_restore_survives_scratch_cleanup(self):
        proof = self.talk_proof()
        receipt = assets.prepare_handoff(self.root, self.settings, 'talk', 'repo', proof)
        assets.apply_handoff(self.root, self.settings, receipt)
        proof.unlink()
        assets.restore_handoff(self.root, self.settings, receipt)
        self.assertEqual((self.root / 'editor/a.dcx').read_bytes(), b'old-a')


if __name__ == '__main__':
    unittest.main()
