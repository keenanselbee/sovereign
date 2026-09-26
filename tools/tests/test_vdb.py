import json
import shutil
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import asset_workflow as assets
import vdb_workflow as vdb


class VdbTests(unittest.TestCase):
    def test_stable_staging_root_resolves_old_completed_receipt(self):
        receipt, target = self.completed_stage()
        settings = {'roots': {'vortexStaging': str(self.root)}}
        self.assertEqual(vdb.staged_source(self.root, settings, receipt)[0], target)
        vdb.select(self.root, settings, receipt)
        self.assertEqual(vdb.package_source(self.root, settings, 'main'), target)
        (target / 'mod/regulation.bin').write_bytes(b'drift')
        with self.assertRaisesRegex(ValueError, 'differs'):
            vdb.package_source(self.root, settings, 'main')

    def test_stable_staging_requires_selection_even_if_legacy_folder_exists(self):
        settings = {'roots': {**self.settings['roots'], 'vortexStaging': str(self.root)}}
        with self.assertRaisesRegex(ValueError, 'No verified selected VDB stage'):
            vdb.package_source(self.root, settings, 'main')

    def test_doctor_accepts_compatible_client_versions_and_rejects_unknown_protocol(self):
        for protocol in (1, 2, 3, 4):
            data = {'protocolVersion': protocol, 'clientVersion': '0.1.1',
                    'vortex': {'protocolVersion': 1, 'stale': False}}
            with mock.patch.object(vdb, 'invoke', return_value={'exitCode': 0, 'result': data}):
                if protocol in (1, 2, 3):
                    self.assertEqual(vdb.doctor({'version': '0.1.1'}), data)
                else:
                    with self.assertRaisesRegex(ValueError, 'client/protocol'):
                        vdb.doctor({'version': '0.1.1'})

    def test_doctor_still_requires_fresh_extension_status(self):
        data = {'protocolVersion': 2, 'clientVersion': '0.1.1',
                'vortex': {'protocolVersion': 1, 'stale': True}}
        with mock.patch.object(vdb, 'invoke', return_value={'exitCode': 0, 'result': data}), \
                self.assertRaisesRegex(ValueError, 'unavailable/stale'):
            vdb.doctor({'version': '0.1.1'})

    def setUp(self):
        scratch = vdb.ROOT / '.codex-temp/tests'
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.settings = {'roots': {'vortex': str(self.root / 'stage/mod'), 'vortexTextures': str(self.root / 'textures/mod')}}
        for name in ('vdb.json', 'mod.json'):
            self.write(name, (vdb.ROOT / name).read_bytes())
        self.write('asset-catalog.json', json.dumps({'schemaVersion': 1, 'runtimeRoot': 'mod', 'sources': [],
                   'groups': [{'id': 'params', 'scope': 'params', 'package': 'main', 'files': ['regulation.bin']},
                              {'id': 'icons', 'scope': 'textures', 'package': 'textures', 'files': ['menu/hi/header', 'menu/hi/data']}]}).encode())
        self.write('stage/mod/regulation.bin', b'old params')
        self.write('stage/mod/src/source.js', b'not runtime')
        self.write('stage/mods/dependency.dll', b'dependency')
        self.write('mod/regulation.bin', b'accepted params')
        self.write('textures/mod/menu/hi/header', b'header')
        self.write('textures/mod/menu/hi/data', b'data')

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value)

    def test_prepare_preserves_selected_source_and_dependency_layout(self):
        receipt = vdb.prepare(self.root, self.settings, 'main', '0.0.0-test', 'repo')
        payload = receipt.parent / 'payload'
        self.assertEqual((payload / 'mod/regulation.bin').read_bytes(), b'accepted params')
        self.assertEqual((payload / 'mods/dependency.dll').read_bytes(), b'dependency')
        self.assertFalse((payload / 'mod/src').exists())
        self.assertEqual((self.root / 'stage/mod/regulation.bin').read_bytes(), b'old params')
        vdb.load_prepared(self.root, self.settings, receipt)
        (payload / 'mod/regulation.bin').write_bytes(b'drift')
        with self.assertRaisesRegex(ValueError, 'changed'):
            vdb.load_prepared(self.root, self.settings, receipt)

    def test_missing_texture_companion_and_unknown_main_file_rejected(self):
        (self.root / 'textures/mod/menu/hi/data').unlink()
        with self.assertRaisesRegex(ValueError, 'companion'):
            vdb.prepare(self.root, self.settings, 'textures', '0.0.0-test', 'vortex')
        self.write('stage/mod/unowned.bin', b'unowned')
        with self.assertRaisesRegex(ValueError, 'membership'):
            vdb.prepare(self.root, self.settings, 'main', '0.0.0-test', 'vortex')

    def test_stage_queued_is_not_completed_and_cannot_be_replayed(self):
        receipt = vdb.prepare(self.root, self.settings, 'main', '0.0.0-test', 'vortex')
        with mock.patch.object(vdb, 'client', return_value={'path': 'fixture'}), mock.patch.object(vdb, 'doctor'), \
                mock.patch.object(vdb, 'invoke', side_effect=[{'exitCode': 0, 'result': {}},
                    {'exitCode': 0, 'result': {'status': 'queued', 'id': 'request', 'buildId': 'build'}}]) as invoke:
            vdb.stage(self.root, self.settings, receipt)
            self.assertNotIn('--profile', invoke.call_args.args[1])
            self.assertEqual(assets.read(receipt)['status'], 'queued')
            with self.assertRaisesRegex(ValueError, 'already submitted'):
                vdb.stage(self.root, self.settings, receipt)
            self.assertEqual(invoke.call_count, 2)

    def test_source_drift_during_prepare_rejects_candidate(self):
        original = vdb.shutil.copyfileobj
        def changing(source, destination):
            original(source, destination)
            if Path(source.name).name == 'regulation.bin':
                self.write('stage/mod/regulation.bin', b'later edit')
        with mock.patch.object(vdb.shutil, 'copyfileobj', side_effect=changing):
            with self.assertRaisesRegex(ValueError, 'changed'):
                vdb.prepare(self.root, self.settings, 'main', '0.0.0-test', 'vortex')

    def test_project_rejects_automatic_activation_and_wrong_game(self):
        original = assets.read(self.root / 'vdb.json')
        original['packages'][0]['activation'] = 'replace-enabled-version'
        self.write('vdb.json', json.dumps(original).encode())
        with self.assertRaisesRegex(ValueError, 'stage-only'):
            vdb.project(self.root)

    def test_project_checks_both_confirmed_nexus_groups(self):
        doc = assets.read(self.root / 'vdb.json')
        self.assertEqual({p['id']: p['nexus']['groupId'] for p in vdb.project(self.root)['packages']},
                         {'main': '7949853', 'textures': '893965'})
        doc['packages'][1]['nexus']['groupId'] = '7949853'
        assets.save(self.root / 'vdb.json', doc)
        with self.assertRaisesRegex(ValueError, 'Nexus identity'):
            vdb.project(self.root)

    def test_confirmed_mapping_preserves_submitted_receipts_only(self):
        path, target = self.completed_stage()
        doc = assets.read(path)
        legacy = vdb.project(self.root)
        packages = {p['id']: p for p in legacy['packages']}
        packages['main']['nexus']['groupId'] = '893965'
        del packages['textures']['nexus']
        doc['projectHash'] = assets.fingerprint(legacy)
        assets.save(path, doc)
        self.assertEqual(vdb.staged_source(self.root, self.settings, path)[0], target)
        for status in ('queued', 'pending', 'running', 'submitting'):
            doc['status'] = status
            assets.save(path, doc)
            vdb.load_prepared(self.root, self.settings, path)
        doc['status'] = 'prepared'
        assets.save(path, doc)
        with self.assertRaisesRegex(ValueError, 'configuration changed'):
            vdb.load_prepared(self.root, self.settings, path)
        doc['status'] = 'completed'
        legacy['packages'][0]['logicalFileName'] = 'unrelated change'
        doc['projectHash'] = assets.fingerprint(legacy)
        assets.save(path, doc)
        with self.assertRaisesRegex(ValueError, 'configuration changed'):
            vdb.load_prepared(self.root, self.settings, path)

    def completed_stage(self, version='0.0.0-test'):
        path = vdb.prepare(self.root, self.settings, 'main', version, 'vortex')
        receipt = assets.read(path)
        receipt.update(status='completed', buildId='a' * 24, requestId='request', client={'path': 'fixture'})
        receipt['requests'] = [{'result': {'status': 'completed', 'operation': 'stage',
            'projectId': 'sovereign', 'packageId': 'main', 'result': {'buildId': receipt['buildId']}}}]
        assets.save(path, receipt)
        target = self.root / ('vdb-sovereign-main-' + receipt['buildId'])
        shutil.copytree(path.parent / 'payload', target)
        return path, target

    def test_same_version_reuses_completed_stage_without_bridge_submission(self):
        original, target = self.completed_stage('1.0.0')
        candidate = vdb.prepare(self.root, self.settings, 'main', '1.0.0', 'vortex')
        with mock.patch.object(vdb, 'invoke') as invoke:
            vdb.stage(self.root, self.settings, candidate)
            invoke.assert_not_called()
        self.assertEqual(assets.read(candidate)['buildId'], assets.read(original)['buildId'])
        self.assertEqual(vdb.staged_source(self.root, self.settings, candidate)[0], target)

    def test_changed_version_payload_rejected_before_bridge_and_new_version_allowed(self):
        self.completed_stage('1.0.0')
        candidate = vdb.prepare(self.root, self.settings, 'main', '1.0.0', 'repo')
        with mock.patch.object(vdb, 'invoke') as invoke:
            with self.assertRaisesRegex(ValueError, 'different contents'):
                vdb.stage(self.root, self.settings, candidate)
            invoke.assert_not_called()
        candidate = vdb.prepare(self.root, self.settings, 'main', '1.0.1', 'repo')
        with mock.patch.object(vdb, 'client', return_value={}), mock.patch.object(vdb, 'doctor'), \
                mock.patch.object(vdb, 'invoke', side_effect=[{'exitCode': 0, 'result': {}},
                    {'exitCode': 0, 'result': {'status': 'queued', 'id': 'next', 'buildId': 'b' * 24}}]) as invoke:
            vdb.stage(self.root, self.settings, candidate)
            self.assertEqual(invoke.call_count, 2)

    def test_pending_stage_reuses_request_and_interrupted_submission_blocks_retry(self):
        original = vdb.prepare(self.root, self.settings, 'main', '1.0.0', 'repo')
        with mock.patch.object(vdb, 'client', return_value={}), mock.patch.object(vdb, 'doctor'), \
                mock.patch.object(vdb, 'invoke', side_effect=[{'exitCode': 0, 'result': {}},
                    {'exitCode': 0, 'result': {'status': 'queued', 'id': 'pending', 'buildId': 'b' * 24}}]):
            vdb.stage(self.root, self.settings, original)
        candidate = vdb.prepare(self.root, self.settings, 'main', '1.0.0', 'repo')
        with mock.patch.object(vdb, 'invoke') as invoke:
            vdb.stage(self.root, self.settings, candidate)
            self.assertEqual(assets.read(candidate)['requestId'], 'pending')
            invoke.assert_not_called()
        doc = assets.read(original)
        doc['status'] = 'submitting'
        assets.save(original, doc)
        candidate = vdb.prepare(self.root, self.settings, 'main', '1.0.0', 'repo')
        with mock.patch.object(vdb, 'invoke') as invoke:
            with self.assertRaisesRegex(ValueError, 'inspection'):
                vdb.stage(self.root, self.settings, candidate)
            invoke.assert_not_called()

    def test_missing_or_corrupt_retained_payload_fails_closed(self):
        original, _ = self.completed_stage('1.0.0')
        candidate = vdb.prepare(self.root, self.settings, 'main', '1.0.0', 'vortex')
        (original.parent / 'payload/mod/regulation.bin').write_bytes(b'corrupt')
        with mock.patch.object(vdb, 'invoke') as invoke:
            with self.assertRaisesRegex(ValueError, 'changed'):
                vdb.stage(self.root, self.settings, candidate)
            invoke.assert_not_called()

    def test_reserved_receipt_cannot_disappear_and_payload_membership_cannot_change(self):
        original, _ = self.completed_stage('1.0.0')
        with assets.lock(self.root):
            vdb.reserve_version(self.root, self.settings, original, assets.read(original))
        candidate = vdb.prepare(self.root, self.settings, 'main', '1.0.0', 'vortex')
        original_doc = assets.read(original)
        for files in ({}, {**original_doc['files'], 'mod/new.bin': {'size': 1, 'sha256': 'new'}}):
            with self.subTest(files=files), assets.lock(self.root):
                with self.assertRaisesRegex(ValueError, 'different contents'):
                    vdb.reserve_version(self.root, self.settings, candidate, {**original_doc, 'files': files})
        original.unlink()
        with mock.patch.object(vdb, 'invoke') as invoke:
            with self.assertRaises(FileNotFoundError):
                vdb.stage(self.root, self.settings, candidate)
            invoke.assert_not_called()

    def test_version_reservations_are_separate_for_textures(self):
        original, _ = self.completed_stage('1.0.0')
        with assets.lock(self.root):
            vdb.reserve_version(self.root, self.settings, original, assets.read(original))
            texture = vdb.prepare(self.root, self.settings, 'textures', '1.0.0', 'vortex')
            self.assertIsNone(vdb.reserve_version(self.root, self.settings, texture, assets.read(texture)))

    def release_fixture(self):
        import nexus_workflow as workflow
        path, target = self.completed_stage('1.0.0')
        vdb.select(self.root, self.settings, path)
        manifest = assets.read(self.root / 'mod.json')
        manifest.update(version='1.0.0', releaseReady=True, dependencies=[{'verified': True}])
        run = self.root / 'output'
        run.mkdir()
        with mock.patch.object(workflow, 'ROOT', self.root):
            archive = workflow.build_vortex_package(target, manifest, run, '1.0.0', False, self.settings)
        return path, target, manifest, archive

    def test_release_retry_returns_exact_retained_zip_and_publisher_verifies_binding(self):
        import release_artifact
        import nexus_workflow as workflow
        import nexus_publish as publisher
        path, target, manifest, archive = self.release_fixture()
        before = archive.read_bytes()
        run = self.root / 'second-output'
        run.mkdir()
        with mock.patch.object(workflow, 'ROOT', self.root), mock.patch.object(workflow, 'write_vortex_package') as writer:
            self.assertEqual(workflow.build_vortex_package(target, manifest, run, '1.0.0', False, self.settings), archive)
            writer.assert_not_called()
        self.assertEqual(archive.read_bytes(), before)
        with mock.patch.object(publisher.core, 'ROOT', self.root), mock.patch.object(publisher.core, 'config', return_value=self.settings):
            self.assertEqual(publisher.verified_archive(archive, manifest)[0], archive)
        receipt = assets.read(archive.parent / 'receipt.json')
        self.assertEqual(receipt['stage']['buildId'], 'a' * 24)
        self.assertEqual(receipt['stage']['stageReceipt'], str(path))
        archive.write_bytes(b'changed ZIP')
        with self.assertRaisesRegex(ValueError, 'contents changed'):
            release_artifact.verify(self.root, self.settings, archive, manifest)

    def test_release_rejects_dev_stage_and_missing_selection(self):
        import release_artifact
        path, target = self.completed_stage()
        with self.assertRaisesRegex(ValueError, 'selected VDB stage'):
            release_artifact.selected_stage(self.root, self.settings, '1.0.0')
        vdb.select(self.root, self.settings, path)
        with self.assertRaisesRegex(ValueError, 'stage version differs'):
            release_artifact.selected_stage(self.root, self.settings, '1.0.0')

    def test_release_rejects_stage_switch_and_legacy_scratch_archive(self):
        import release_artifact
        path, target, manifest, archive = self.release_fixture()
        with self.assertRaisesRegex(ValueError, 'retained VDB release ZIP'):
            release_artifact.verify(self.root, self.settings, self.root / 'output' / archive.name, manifest)
        doc = assets.read(path)
        doc['buildId'] = 'b' * 24
        doc['requests'][0]['result']['result']['buildId'] = doc['buildId']
        assets.save(path, doc)
        changed_target = self.root / ('vdb-sovereign-main-' + doc['buildId'])
        shutil.copytree(target, changed_target)
        vdb.select(self.root, self.settings, path)
        with self.assertRaisesRegex(ValueError, 'identity or contents changed'):
            release_artifact.verify(self.root, self.settings, archive, manifest)
        doc['version'] = '1.0.1'
        assets.save(path, doc)
        with self.assertRaisesRegex(ValueError, 'stage version differs'):
            release_artifact.verify(self.root, self.settings, archive, manifest)

    def test_release_rejects_inventory_filter_changes_and_partial_retention(self):
        import release_artifact
        path, target, manifest, archive = self.release_fixture()
        manifest['package']['excludeDirectories'].append('mods')
        with self.assertRaisesRegex(ValueError, 'inventory differs'):
            release_artifact.verify(self.root, self.settings, archive, manifest)
        (archive.parent / 'receipt.json').unlink()
        with self.assertRaises(FileNotFoundError):
            release_artifact.package(self.root, self.settings, target, manifest, self.root / 'output', '1.0.0')

    def test_selected_stage_is_verified_and_drift_blocks_packaging(self):
        path, target = self.completed_stage()
        vdb.select(self.root, self.settings, path)
        self.assertEqual(vdb.selected_source(self.root, self.settings, 'main'), target)
        (target / 'mods/dependency.dll').write_bytes(b'changed dependency')
        with self.assertRaisesRegex(ValueError, 'differs'):
                vdb.selected_source(self.root, self.settings, 'main')

    def test_new_runtime_requires_verified_baseline_and_matching_scope(self):
        path, target = self.completed_stage()
        vdb.select(self.root, self.settings, path)
        data = assets.read(self.root / 'asset-catalog.json')
        data['groups'].append({'id': 'talk', 'scope': 'talk', 'package': 'main', 'files': ['script/talk/new.dcx']})
        assets.save(self.root / 'asset-catalog.json', data)
        self.write('mod/script/talk/new.dcx', b'new dialogue')
        with self.assertRaisesRegex(ValueError, 'every added file'):
            vdb.prepare(self.root, self.settings, 'main', '0.0.0-test', 'repo', 'params')
        candidate = vdb.prepare(self.root, self.settings, 'main', '0.0.0-test', 'repo', 'talk')
        self.assertEqual(assets.read(candidate)['addedRuntimePaths'], ['mod/script/talk/new.dcx'])
        self.assertEqual((candidate.parent / 'payload/mod/regulation.bin').read_bytes(), b'old params')
        self.assertEqual((candidate.parent / 'payload/mod/script/talk/new.dcx').read_bytes(), b'new dialogue')
        (self.root / '.vdb/selected.json').unlink()
        with self.assertRaisesRegex(ValueError, 'verified selected stage'):
            vdb.prepare(self.root, self.settings, 'main', '0.0.0-test', 'repo', 'talk')

    def test_status_uses_selected_stage_instead_of_retired_vortex_folder(self):
        path, target = self.completed_stage()
        vdb.select(self.root, self.settings, path)
        self.write('mod/regulation.bin', b'old params')
        self.write('live/regulation.bin', b'old params')
        self.write('stage/mod/regulation.bin', b'retired bytes')
        self.write('stage/mod/obsolete.dcx', b'retired file')
        self.settings['roots']['live'] = str(self.root / 'live')
        rows = assets.status(self.root, self.settings, 'params')
        self.assertEqual(rows[0]['state'], 'Match')
        self.assertEqual(Path(rows[0]['paths']['vortex']), target / 'mod/regulation.bin')
        self.assertFalse(any(row['file'] == 'obsolete.dcx' for row in assets.inventory_review(self.root, self.settings)))
        (target / 'mod/regulation.bin').write_bytes(b'selected drift')
        with self.assertRaisesRegex(ValueError, 'immutable receipt'):
            assets.status(self.root, self.settings, 'params')

    def test_wrong_active_profile_never_submits_a_deployment(self):
        path, target = self.completed_stage()
        with mock.patch.object(vdb, 'client', return_value={}), mock.patch.object(vdb, 'doctor',
                return_value={'vortex': {'activeGameId': 'taintedgrailthefallofavalon', 'activeProfileId': 'other'}}), \
                mock.patch.object(vdb, 'invoke') as invoke:
            with self.assertRaisesRegex(ValueError, 'profile'):
                vdb.operate(self.root, self.settings, path, 'deploy', 'requested')
            invoke.assert_not_called()
            self.assertFalse((self.root / '.vdb/operations').exists())

    def test_scoped_prepare_keeps_other_selected_stage_bytes(self):
        data = assets.read(self.root / 'asset-catalog.json')
        data['groups'].append({'id': 'text', 'scope': 'text', 'package': 'main', 'files': ['msg/item.dcx']})
        self.write('asset-catalog.json', json.dumps(data).encode())
        self.write('stage/mod/msg/item.dcx', b'accepted text')
        self.write('mod/msg/item.dcx', b'unreviewed text edit')
        path = vdb.prepare(self.root, self.settings, 'main', '0.0.0-test', 'repo', 'params')
        self.assertEqual((path.parent / 'payload/mod/regulation.bin').read_bytes(), b'accepted params')
        self.assertEqual((path.parent / 'payload/mod/msg/item.dcx').read_bytes(), b'accepted text')
        self.assertEqual(assets.read(path)['replacedRuntimePaths'], ['mod/regulation.bin'])

    def test_item_file_staging_preserves_selected_menu_bytes(self):
        data = assets.read(self.root / 'asset-catalog.json')
        data['groups'].append({'id': 'text', 'scope': 'text', 'recipe': 'fmg', 'package': 'main',
                               'files': ['msg/item.dcx', 'msg/menu.dcx']})
        assets.save(self.root / 'asset-catalog.json', data)
        for name in ('item', 'menu'):
            self.write(f'stage/mod/msg/{name}.dcx', b'selected ' + name.encode())
            self.write(f'mod/msg/{name}.dcx', b'repo ' + name.encode())
        path = vdb.prepare(self.root, self.settings, 'main', '0.0.0-test', 'repo', 'file:msg/item.dcx')
        self.assertEqual((path.parent / 'payload/mod/msg/item.dcx').read_bytes(), b'repo item')
        self.assertEqual((path.parent / 'payload/mod/msg/menu.dcx').read_bytes(), b'selected menu')
        self.assertEqual(assets.read(path)['replacedRuntimePaths'], ['mod/msg/item.dcx'])

    def test_legacy_duplicates_block_deployment_but_allow_readonly_verification(self):
        state = {'activeGameId': 'eldenring', 'activeProfileId': 'requested',
                 'activeMods': [{'id': 'Sovereign'}, {'id': 'another mod'}]}
        with mock.patch.object(vdb, 'client', return_value={}), mock.patch.object(vdb, 'doctor', return_value={'vortex': state}):
            with self.assertRaisesRegex(ValueError, 'legacy duplicate'):
                vdb.deployment_context(self.root, 'requested')
            self.assertEqual(vdb.deployment_context(self.root, 'requested', 'verify')[1], state)


if __name__ == '__main__':
    unittest.main()
