import shutil
from pathlib import Path
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import asset_workflow as assets
import finish_workflow as finish
import vdb_workflow as vdb
import test_vdb


class FinishTests(unittest.TestCase):
    write = test_vdb.VdbTests.write

    def setUp(self):
        test_vdb.VdbTests.setUp(self)
        self.stage = vdb.prepare(self.root, self.settings, 'main', '1.0.1', 'repo')
        self.path = self.root / '.vdb/finalizations/test/receipt.json'
        self.build = {'packageId': 'main', 'buildId': 'a' * 24, 'version': '1.0.1'}
        self.request = '12345678-1234-1234-1234-123456789012'
        self.calls = []
        self.outcome = {'id': self.request, 'operation': 'finish', 'projectId': 'sovereign',
                        'status': 'pending', 'result': {}}
        self.selected = {'version': '0.1.2'}
        for owner, name, value in ((finish, 'compatible_client', self.selected),):
            patch = mock.patch.object(owner, name, return_value=value)
            patch.start(); self.addCleanup(patch.stop)
        patch = mock.patch.object(vdb, 'invoke', side_effect=self.invoke)
        patch.start(); self.addCleanup(patch.stop)

    def invoke(self, selected, arguments):
        self.calls.append(arguments)
        if arguments[0] == 'register':
            return {'exitCode': 0, 'result': {}}
        if arguments[0] == 'finish-batch':
            return {'exitCode': 0, 'result': {'id': self.request, 'status': 'queued', 'builds': [self.build]}}
        self.assertEqual(arguments[0], 'wait')
        return {'exitCode': 2 if self.outcome['status'] == 'pending' else 0, 'result': self.outcome}

    def acknowledge_stage(self, completed=False):
        target = self.root / ('vdb-sovereign-main-' + self.build['buildId'])
        shutil.copytree(self.stage.parent / 'payload', target)
        self.outcome = {**self.outcome, 'status': 'completed' if completed else 'pending', 'result': {
            'builds': [{**self.build, 'staging': 'completed'}], 'verification': [],
            'profiles': [{'profileId': 'disabled', 'status': 'completed', 'builds': [{'status': 'updated-disabled'}]}]}}

    def test_offline_all_profile_request_resumes_without_resubmission(self):
        result = finish.submit(self.root, self.settings, [self.stage], self.path)
        self.assertEqual(result['profileScope'], 'all')
        command = next(c for c in self.calls if c[0] == 'finish-batch')
        self.assertNotIn('--profile', command)
        self.assertNotIn('--stage-only', command)
        finish.refresh(self.root, self.settings, self.path)
        self.assertEqual(assets.read(self.stage)['status'], 'prepared')
        self.acknowledge_stage()
        finish.refresh(self.root, self.settings, self.path)
        vdb.staged_source(self.root, self.settings, self.stage)
        self.assertFalse((self.root / '.vdb/selected.json').exists())
        self.outcome['status'] = 'completed'
        finish.refresh(self.root, self.settings, self.path)
        self.assertEqual(sum(c[0] == 'finish-batch' for c in self.calls), 1)
        with self.assertRaisesRegex(ValueError, 'resume existing'):
            finish.submit(self.root, self.settings, [self.stage], self.path)

    def test_stage_only_omits_profile_and_does_not_select_packaging_source(self):
        propagation = self.root / 'propagation.json'
        doc = {'status': 'prepared', 'stageReceipt': str(self.stage), 'finishReceipt': str(self.path)}
        assets.save(propagation, doc)
        self.acknowledge_stage(completed=True)
        result = finish.advance(self.root, self.settings, propagation, doc, None, 0, True)
        self.assertEqual(result['status'], 'complete')
        command = next(c for c in self.calls if c[0] == 'finish-batch')
        self.assertIn('--stage-only', command)
        self.assertNotIn('--profile', command)
        self.assertFalse((self.root / '.vdb/selected.json').exists())

    def test_explicit_profile_is_bound_and_disabled_completion_selects_verified_stage(self):
        propagation = self.root / 'propagation.json'
        doc = {'status': 'prepared', 'stageReceipt': str(self.stage), 'finishReceipt': str(self.path)}
        assets.save(propagation, doc)
        finish.advance(self.root, self.settings, propagation, doc, 'p1', 0)
        self.assertIn('p1', next(c for c in self.calls if c[0] == 'finish-batch'))
        doc = assets.read(propagation)
        with self.assertRaisesRegex(ValueError, 'different profile'):
            finish.advance(self.root, self.settings, propagation, doc, 'p2', 0)
        self.acknowledge_stage(completed=True)
        result = finish.advance(self.root, self.settings, propagation, doc, 'p1', 0)
        self.assertEqual(result['status'], 'complete')
        self.assertEqual(assets.read(self.root / '.vdb/selected.json')['main']['buildId'], self.build['buildId'])

    def test_global_completion_is_not_package_stage_proof(self):
        finish.submit(self.root, self.settings, [self.stage], self.path)
        self.outcome = {**self.outcome, 'status': 'completed', 'result': {'staging': 'completed', 'builds': []}}
        finish.refresh(self.root, self.settings, self.path)
        with self.assertRaisesRegex(ValueError, 'completed stage'):
            vdb.staged_source(self.root, self.settings, self.stage)

    def test_refresh_recovers_submission_saved_before_stage_receipt_binding(self):
        finish.submit(self.root, self.settings, [self.stage], self.path)
        doc = assets.read(self.stage)
        for key in ('buildId', 'requestId', 'client', 'finishReceipt'):
            doc.pop(key, None)
        assets.save(self.stage, doc)
        self.acknowledge_stage(completed=True)
        finish.refresh(self.root, self.settings, self.path)
        doc = assets.read(self.stage)
        self.assertEqual(doc['requestId'], self.request)
        self.assertEqual(doc['client'], self.selected)
        vdb.staged_source(self.root, self.settings, self.stage)
        self.assertEqual(sum(c[0] == 'finish-batch' for c in self.calls), 1)

    def test_uncertain_submission_and_changed_reserved_payload_never_resubmit(self):
        finish.submit(self.root, self.settings, [self.stage], self.path)
        receipt = assets.read(self.path)
        receipt['status'] = 'submitting'
        assets.save(self.path, receipt)
        finish.refresh(self.root, self.settings, self.path)
        self.assertEqual(sum(c[0] == 'finish-batch' for c in self.calls), 1)
        self.write('mod/regulation.bin', b'new payload')
        changed = vdb.prepare(self.root, self.settings, 'main', '1.0.1', 'repo')
        with self.assertRaisesRegex(ValueError, 'different contents'):
            finish.submit(self.root, self.settings, [changed], self.root / '.vdb/finalizations/changed/receipt.json')
        self.assertEqual(sum(c[0] == 'finish-batch' for c in self.calls), 1)


class CompatibilityTests(unittest.TestCase):
    def test_closed_vortex_is_allowed_but_fresh_old_consumer_is_rejected(self):
        for stale in (True, False):
            response = {'exitCode': 0, 'result': {'clientVersion': '0.1.2', 'capabilities': [finish.CAPABILITY],
                        'vortex': {'stale': stale, 'capabilities': []}}}
            with mock.patch.object(vdb, 'client', return_value={'version': '0.1.2'}), \
                    mock.patch.object(vdb, 'invoke', return_value=response):
                if stale:
                    self.assertEqual(finish.compatible_client(Path('.'))['version'], '0.1.2')
                else:
                    with self.assertRaisesRegex(ValueError, 'too old'):
                        finish.compatible_client(Path('.'))


if __name__ == '__main__':
    unittest.main()
