from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import asset_workflow as assets
import propagate_workflow as propagate


class PropagateTests(unittest.TestCase):
    def test_plan_defaults_to_checked_regular_version(self):
        assets.save(self.root / 'mod.json', {'version': '1.0.1', 'releaseReady': False})
        (self.root / 'changelog.txt').write_text('Version 1.0.1\nUse regular versions.\n')
        (self.root / 'tools').mkdir()
        assets.save(self.root / 'tools/eldenring-paths.local.json', self.settings)
        planned_path = self.root / 'receipt.json'
        assets.save(planned_path, {})
        with mock.patch.object(propagate.core, 'ROOT', self.root), \
                mock.patch.object(sys, 'argv', ['propagate_workflow.py', 'plan', '--scope', 'params', '--from', 'repo']), \
                mock.patch.object(propagate, 'prepare', return_value=planned_path) as prepare, \
                mock.patch('builtins.print'):
            self.assertEqual(propagate.main(), 0)
        self.assertEqual(prepare.call_args.args[5], '1.0.1')

    def setUp(self):
        scratch = propagate.core.ROOT / '.codex-temp/tests'
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.data = {'schemaVersion': 1, 'runtimeRoot': 'mod', 'groups': [
            {'id': 'params', 'scope': 'params', 'package': 'main', 'files': ['regulation.bin'],
             'editor': {'root': 'editor', 'stripPrefix': '', 'base': ''}}], 'sources': []}
        assets.save(self.root / 'asset-catalog.json', self.data)
        self.settings = {'roots': {k: str(self.root / k) for k in ('editor', 'live', 'vortex', 'vortexTextures')}}
        for name in ('mod', 'editor'):
            (self.root / name).mkdir()
            (self.root / name / 'regulation.bin').write_bytes(b'accepted')

    def test_item_file_handoff_preserves_menu_and_validates_exact_guards(self):
        self.data['groups'][0].update(id='text', scope='text', recipe='fmg',
                                     files=['item.dcx', 'menu.dcx'])
        assets.save(self.root / 'asset-catalog.json', self.data)
        for name in ('item.dcx', 'menu.dcx'):
            (self.root / 'mod' / name).write_bytes(b'accepted')
            (self.root / 'editor' / name).write_bytes(b'editor change')
        with mock.patch.object(propagate.vdb, 'project'):
            path = propagate.prepare(self.root, self.settings, 'file:item.dcx', 'editor', 'main', '0.0.0-test')
        document = assets.read(path)
        self.assertEqual(len(document['guards']), 2)
        handoff = document['handoff']
        assets.apply_handoff(self.root, self.settings, handoff)
        self.assertEqual((self.root / 'mod/item.dcx').read_bytes(), b'editor change')
        self.assertEqual((self.root / 'mod/menu.dcx').read_bytes(), b'accepted')
        assets.restore_handoff(self.root, self.settings, handoff)
        self.assertEqual((self.root / 'mod/item.dcx').read_bytes(), b'accepted')
        self.assertEqual((self.root / 'editor/menu.dcx').read_bytes(), b'editor change')

    def test_single_file_scope_cannot_bypass_non_fmg_qualification(self):
        self.data['groups'][0].update(scope='hks', recipe='hks')
        assets.save(self.root / 'asset-catalog.json', self.data)
        with self.assertRaisesRegex(ValueError, 'catalog-owned FMG'):
            propagate.prepare(self.root, self.settings, 'file:regulation.bin', 'editor', 'main', '0.0.0-test')
        with self.assertRaisesRegex(ValueError, 'catalog-owned FMG'):
            assets.prepare_handoff(self.root, self.settings, 'file:regulation.bin', 'editor')

    def test_no_change_plan_still_guards_against_later_source_edits(self):
        with mock.patch.object(propagate.vdb, 'project'):
            path = propagate.prepare(self.root, self.settings, 'params', 'editor', 'main', '0.0.0-test')
        self.assertIsNone(assets.read(path)['handoff'])
        (self.root / 'mod/regulation.bin').write_bytes(b'later')
        with mock.patch.object(propagate.vdb, 'prepare') as stage:
            with self.assertRaisesRegex(ValueError, 'changed since'):
                propagate.apply(self.root, self.settings, path)
            stage.assert_not_called()

    def test_scoped_prepare_failure_retains_completed_source_handoff(self):
        (self.root / 'editor/regulation.bin').write_bytes(b'reviewed edit')
        with mock.patch.object(propagate.vdb, 'project'):
            path = propagate.prepare(self.root, self.settings, 'params', 'editor', 'main', '0.0.0-test')
        with mock.patch.object(propagate.vdb, 'prepare', side_effect=ValueError('stage missing')):
            with self.assertRaisesRegex(ValueError, 'stage missing'):
                propagate.apply(self.root, self.settings, path)
        doc = assets.read(path)
        self.assertEqual(doc['status'], 'source-accepted')
        self.assertEqual(assets.read(doc['handoff'])['status'], 'complete')
        self.assertEqual((self.root / 'mod/regulation.bin').read_bytes(), b'reviewed edit')
        assets.restore_handoff(self.root, self.settings, doc['handoff'])
        self.assertEqual((self.root / 'mod/regulation.bin').read_bytes(), b'accepted')

    def test_new_source_membership_invalidates_even_an_unchanged_plan(self):
        self.data['sources'] = [{'id': 'rows', 'scope': 'params', 'repo': 'src/rows',
            'editorRoot': 'editor', 'editor': 'rows', 'mode': 'overlay', 'patterns': ['*.json']}]
        assets.save(self.root / 'asset-catalog.json', self.data)
        with mock.patch.object(propagate.vdb, 'project'):
            path = propagate.prepare(self.root, self.settings, 'params', 'editor', 'main', '0.0.0-test')
        (self.root / 'src/rows').mkdir(parents=True)
        (self.root / 'src/rows/new.json').write_text('{}')
        with mock.patch.object(propagate.vdb, 'prepare') as stage:
            with self.assertRaisesRegex(ValueError, 'changed since'):
                propagate.apply(self.root, self.settings, path)
            stage.assert_not_called()

    def failed_preparation(self):
        (self.root / 'editor/regulation.bin').write_bytes(b'reviewed edit')
        with mock.patch.object(propagate.vdb, 'project'):
            path = propagate.prepare(self.root, self.settings, 'params', 'editor', 'main', '1.0.0-test')
        with mock.patch.object(propagate.vdb, 'prepare', side_effect=ValueError('disk unavailable')):
            with self.assertRaisesRegex(ValueError, 'disk unavailable'):
                propagate.apply(self.root, self.settings, path)
        return path

    def test_preparation_retry_does_not_repeat_source_acceptance(self):
        path = self.failed_preparation()
        stage = self.root / '.vdb/prepared/recovered/receipt.json'
        stage.parent.mkdir(parents=True)
        assets.save(stage, {'status': 'prepared', 'files': {'mod/regulation.bin': {
            'sha256': assets.checksum(self.root / 'mod/regulation.bin')}}})
        with mock.patch.object(propagate.vdb, 'prepare', return_value=stage), \
                mock.patch.object(assets, 'apply_handoff') as accept:
            result = propagate.apply(self.root, self.settings, path)
        self.assertEqual(result['status'], 'prepared')
        accept.assert_not_called()
        assets.restore_handoff(self.root, self.settings, result['handoff'])
        self.assertEqual((self.root / 'mod/regulation.bin').read_bytes(), b'accepted')

    def test_preparation_retry_rejects_later_edits_and_missing_recovery_guards(self):
        path = self.failed_preparation()
        (self.root / 'mod/regulation.bin').write_bytes(b'later manual edit')
        with mock.patch.object(propagate.vdb, 'prepare') as prepare:
            with self.assertRaisesRegex(ValueError, 'changed since'):
                propagate.apply(self.root, self.settings, path)
            prepare.assert_not_called()
        (self.root / 'mod/regulation.bin').write_bytes(b'reviewed edit')
        doc = assets.read(path); del doc['acceptedGuards']; assets.save(path, doc)
        with self.assertRaisesRegex(ValueError, 'changed since'):
            propagate.apply(self.root, self.settings, path)

    def test_resume_continues_preparation_then_waits_without_reaccepting(self):
        path = self.failed_preparation()
        stage = self.root / '.vdb/prepared/recovered/receipt.json'
        stage.parent.mkdir(parents=True)
        assets.save(stage, {'status': 'prepared', 'buildId': 'a' * 24, 'files': {
            'mod/regulation.bin': {'sha256': assets.checksum(self.root / 'mod/regulation.bin')}}})
        def submit(*unused):
            doc = assets.read(stage); doc['status'] = 'queued'; assets.save(stage, doc)
        with mock.patch.object(propagate.vdb, 'prepare', return_value=stage) as prepare, \
                mock.patch.object(propagate.vdb, 'load_prepared', side_effect=lambda *a: (stage, assets.read(stage))), \
                mock.patch.object(propagate.vdb, 'deployment_context'), \
                mock.patch.object(propagate.vdb, 'stage', side_effect=submit) as stage_submit, \
                mock.patch.object(propagate.vdb, 'wait'), \
                mock.patch.object(assets, 'apply_handoff') as accept:
            self.assertEqual(propagate.advance(self.root, self.settings, path, 'profile')['status'], 'staging')
        accept.assert_not_called()
        prepare.assert_called_once()
        stage_submit.assert_called_once()

    def test_unchanged_development_payload_reuses_selected_stage_without_preparing(self):
        with mock.patch.object(propagate.vdb, 'project'):
            path = propagate.prepare(self.root, self.settings, 'params', 'editor', 'main', '1.0.0-dev.new')
        stage = self.root / '.vdb/prepared/existing/receipt.json'
        stage.parent.mkdir(parents=True)
        data = {'status': 'completed', 'files': {'mod/regulation.bin': {
            'sha256': assets.checksum(self.root / 'mod/regulation.bin')}}}
        assets.save(stage, data)
        assets.save(self.root / '.vdb/selected.json', {'main': {'receipt': str(stage)}})
        with mock.patch.object(propagate.vdb, 'selected_source', return_value=self.root / 'stage'), \
                mock.patch.object(propagate.vdb, 'load_prepared', return_value=(stage, data)), \
                mock.patch.object(propagate.vdb, 'prepare') as prepare:
            result = propagate.apply(self.root, self.settings, path)
        self.assertTrue(result['reusedBuild'])
        self.assertEqual(result['stageReceipt'], str(stage))
        prepare.assert_not_called()

    def test_reuse_rejects_changed_payload_and_preserves_explicit_release_identity(self):
        stage = self.root / '.vdb/prepared/existing/receipt.json'
        stage.parent.mkdir(parents=True)
        assets.save(self.root / '.vdb/selected.json', {'main': {'receipt': str(stage)}})
        with mock.patch.object(propagate.vdb, 'selected_source', return_value=self.root / 'stage'), \
                mock.patch.object(propagate.vdb, 'load_prepared', return_value=(stage, {'files': {
                    'mod/regulation.bin': {'sha256': 'old'}}})):
            self.assertIsNone(propagate.unchanged_stage(self.root, self.settings,
                {'version': '1.0.0-dev.new', 'packageId': 'main'}, {'mod/regulation.bin': 'new'}))
        with mock.patch.object(propagate.vdb, 'selected_source') as selected:
            self.assertIsNone(propagate.unchanged_stage(self.root, self.settings,
                {'version': '1.0.0', 'packageId': 'main'}, {'mod/regulation.bin': 'old'}))
            selected.assert_not_called()

    def test_reuse_does_not_hide_new_catalog_membership_outside_the_scope(self):
        self.data['groups'].append({'id': 'maps', 'scope': 'maps', 'package': 'main', 'files': ['map/new.dcx']})
        assets.save(self.root / 'asset-catalog.json', self.data)
        stage = self.root / '.vdb/prepared/existing/receipt.json'
        stage.parent.mkdir(parents=True)
        assets.save(self.root / '.vdb/selected.json', {'main': {'receipt': str(stage)}})
        with mock.patch.object(propagate.vdb, 'selected_source', return_value=self.root / 'stage'), \
                mock.patch.object(propagate.vdb, 'load_prepared', return_value=(stage, {'files': {
                    'mod/regulation.bin': {'sha256': 'same'}}})):
            self.assertIsNone(propagate.unchanged_stage(self.root, self.settings,
                {'version': '1.0.0-dev.new', 'packageId': 'main'}, {'mod/regulation.bin': 'same'}))

    def test_qualification_is_rechecked_when_no_source_copy_is_needed(self):
        self.data['groups'][0]['scope'] = 'animations'
        assets.save(self.root / 'asset-catalog.json', self.data)
        with mock.patch.object(propagate.vdb, 'project'), mock.patch.object(assets, 'validate_player_qualification'):
            path = propagate.prepare(self.root, self.settings, 'animations', 'editor', 'main', '0.0.0-test', 'proof')
        with mock.patch.object(assets, 'validate_player_qualification', side_effect=ValueError('Tool changed')), \
                mock.patch.object(propagate.vdb, 'prepare') as stage:
            with self.assertRaisesRegex(ValueError, 'Tool changed'):
                propagate.apply(self.root, self.settings, path)
            stage.assert_not_called()

    def prepared_propagation(self, stage_status='queued'):
        directory = self.root / '.sovereign/propagation/fixture'
        directory.mkdir(parents=True)
        stage = self.root / '.vdb/prepared/fixture/receipt.json'
        stage.parent.mkdir(parents=True)
        assets.save(stage, {'status': stage_status, 'buildId': 'a' * 24})
        path = directory / 'receipt.json'
        assets.save(path, {'status': 'prepared', 'stageReceipt': str(stage), 'packageId': 'main'})
        return path, stage

    def test_pending_stage_and_deploy_resume_same_requests_then_select_once(self):
        path, stage = self.prepared_propagation()
        operation_paths = []
        def deploy(root, settings, stage_path, operation, profile, operation_id):
            target = root / '.vdb/operations' / operation_id / 'receipt.json'
            target.parent.mkdir(parents=True)
            assets.save(target, {'status': 'queued', 'operation': 'deploy', 'profileId': profile,
                'packageId': 'main', 'buildId': 'a' * 24, 'stageReceipt': str(stage), 'requests': []})
            operation_paths.append(target)
        with mock.patch.object(propagate.vdb, 'deployment_context'), \
                mock.patch.object(propagate.vdb, 'load_prepared', side_effect=lambda *a: (stage, assets.read(stage))), \
                mock.patch.object(propagate.vdb, 'staged_source'), mock.patch.object(propagate.vdb, 'stage') as submit_stage, \
                mock.patch.object(propagate.vdb, 'wait') as wait_stage, \
                mock.patch.object(propagate.vdb, 'operate', side_effect=deploy) as submit_deploy, \
                mock.patch.object(propagate.vdb, 'wait_operation') as wait_deploy, \
                mock.patch.object(propagate.vdb, 'select') as select:
            self.assertEqual(propagate.advance(self.root, self.settings, path, 'profile')['status'], 'staging')
            submit_stage.assert_not_called()
            submit_deploy.assert_not_called()
            wait_stage.assert_called_once()
            assets.save(stage, {'status': 'completed', 'buildId': 'a' * 24})
            self.assertEqual(propagate.advance(self.root, self.settings, path, 'profile')['status'], 'deploying')
            self.assertEqual(submit_deploy.call_count, 1)
            select.assert_not_called()
            operation = assets.read(operation_paths[0])
            operation.update(status='completed', requests=[{'result': {'operation': 'deploy', 'result': {
                'verification': {'deployed': 'verified', 'enabled': True, 'differences': []}}}}])
            assets.save(operation_paths[0], operation)
            self.assertEqual(propagate.advance(self.root, self.settings, path, 'profile')['status'], 'complete')
            self.assertEqual(submit_deploy.call_count, 1)
            select.assert_called_once()
            propagate.advance(self.root, self.settings, path, 'profile')
            select.assert_called_once()

    def test_completed_deployment_with_wrong_live_bytes_never_selects(self):
        path, stage = self.prepared_propagation('completed')
        operation_path = self.root / '.vdb/operations/fixture/receipt.json'
        operation_path.parent.mkdir(parents=True)
        assets.save(operation_path, {'status': 'completed', 'operation': 'deploy', 'profileId': 'profile',
            'packageId': 'main', 'buildId': 'a' * 24, 'stageReceipt': str(stage), 'requests': [
                {'result': {'operation': 'deploy', 'result': {'verification': {
                    'deployed': 'differences', 'enabled': True, 'differences': [{'path': 'mod/regulation.bin'}]}}}}]})
        doc = assets.read(path)
        doc.update(status='deploying', deploymentReceipt=str(operation_path), profileId='profile')
        assets.save(path, doc)
        with mock.patch.object(propagate.vdb, 'deployment_context'), \
                mock.patch.object(propagate.vdb, 'load_prepared', return_value=(stage, assets.read(stage))), \
                mock.patch.object(propagate.vdb, 'staged_source'), mock.patch.object(propagate.vdb, 'select') as select:
            with self.assertRaisesRegex(ValueError, 'without matching live bytes'):
                propagate.advance(self.root, self.settings, path, 'profile')
            select.assert_not_called()

    def test_unrecorded_deployment_is_not_automatically_resubmitted(self):
        path, stage = self.prepared_propagation('completed')
        doc = assets.read(path)
        doc.update(status='deploying', deploymentReceipt=str(self.root / '.vdb/operations/missing/receipt.json'))
        assets.save(path, doc)
        with mock.patch.object(propagate.vdb, 'deployment_context'), \
                mock.patch.object(propagate.vdb, 'load_prepared', return_value=(stage, assets.read(stage))), \
                mock.patch.object(propagate.vdb, 'staged_source'), mock.patch.object(propagate.vdb, 'operate') as submit:
            with self.assertRaisesRegex(ValueError, 'submission interrupted'):
                propagate.advance(self.root, self.settings, path, 'profile')
            submit.assert_not_called()

    def test_stale_heartbeat_does_not_prevent_observing_a_queued_request(self):
        path, stage = self.prepared_propagation()
        with mock.patch.object(propagate.vdb, 'deployment_context', side_effect=ValueError('stale')) as preflight, \
                mock.patch.object(propagate.vdb, 'load_prepared', return_value=(stage, assets.read(stage))), \
                mock.patch.object(propagate.vdb, 'wait') as observe:
            self.assertEqual(propagate.advance(self.root, self.settings, path, 'profile')['status'], 'staging')
            observe.assert_called_once()
            preflight.assert_not_called()


if __name__ == '__main__':
    unittest.main()
