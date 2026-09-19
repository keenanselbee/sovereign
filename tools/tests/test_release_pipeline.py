import hashlib
import json
from pathlib import Path
import shutil
import sys
import unittest
from unittest import mock
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import asset_workflow as assets
import nexus_workflow as workflow
import nexus_publish as publisher
import release_pipeline as pipeline
import vdb_workflow as vdb
import test_vdb


class PipelineTests(unittest.TestCase):
    write = test_vdb.VdbTests.write

    def setUp(self):
        test_vdb.VdbTests.setUp(self)
        for owner in (workflow, publisher.core):
            patch = mock.patch.object(owner, 'ROOT', self.root)
            patch.start()
            self.addCleanup(patch.stop)
        patch = mock.patch.object(publisher.core, 'config', return_value=self.settings)
        patch.start()
        self.addCleanup(patch.stop)
        self.manifest = assets.read(self.root / 'mod.json')
        self.manifest.update(version='1.0.0', releaseReady=True, dependencies=[{'verified': True}])
        assets.save(self.root / 'mod.json', self.manifest)
        self.write('changelog.txt', b'Version 1.0.0\nCompleted change.\n')
        for name, text in {'nexus-short-desc.txt': 'Short', 'nexus-full-desc.txt': '[b]Full[/b]',
                           'nexus-file-desc.txt': 'Main pitch', 'nexus-textures-file-desc.txt': 'Textures pitch',
                           'nexus-changelog.txt': 'TargetVersion=1.0.0\nBaselineVersion=0.1.0\nCompleted change.'}.items():
            self.write('_/nexus-page/' + name, text.encode())
        self.archives = {}
        self.stage_paths = {}
        self.remote = {}
        for package_id, build_id in (('main', 'a' * 24), ('textures', 'b' * 24)):
            path = vdb.prepare(self.root, self.settings, package_id, '1.0.0', 'vortex')
            doc = assets.read(path)
            doc.update(status='completed', buildId=build_id, requestId='stage-' + package_id, client={})
            doc['requests'] = [{'result': {'status': 'completed', 'operation': 'stage', 'projectId': 'sovereign',
                'packageId': package_id, 'result': {'buildId': build_id}}}]
            assets.save(path, doc)
            target = self.root / ('vdb-sovereign-' + package_id + '-' + build_id)
            shutil.copytree(path.parent / 'payload', target)
            vdb.select(self.root, self.settings, path)
            run = self.root / ('output-' + package_id)
            run.mkdir()
            self.archives[package_id] = workflow.build_vortex_package(target, self.manifest, run, '1.0.0', False, self.settings, package_id)
            self.stage_paths[package_id] = path
            group = self.manifest['nexus']['groupId'] if package_id == 'main' else self.manifest['nexus']['textures']['groupId']
            self.remote[group] = [{'id': '10' if package_id == 'main' else '20', 'version': '0.1.0',
                'file': {'id': group}, 'category': 'main', 'is_primary': package_id == 'main', 'game_scoped_id': '123'}]
        self.uploads = []
        self.bridge_calls = []
        self.pending = False
        for owner, name, effect in ((publisher, 'api', self.api), (publisher.core, 'nexus_status', self.status),
                                   (workflow.automation, 'invoke', self.upload), (vdb, 'invoke', self.bridge)):
            patch = mock.patch.object(owner, name, side_effect=effect)
            patch.start()
            self.addCleanup(patch.stop)
        for owner, name, value in ((publisher.core, 'nexus_issues', []), (vdb, 'client', {}), (vdb, 'doctor', {})):
            patch = mock.patch.object(owner, name, return_value=value)
            patch.start()
            self.addCleanup(patch.stop)

    def api(self, method, route, body=None):
        self.assertEqual(method, 'GET')
        return {'versions': self.remote[route.split('/')[2]]}

    def status(self, manifest):
        rows = self.remote[manifest['nexus']['groupId']]
        return {'current': rows[-1], 'activeVersions': rows}

    def upload(self, root, command, path):
        self.assertEqual(command, 'publish')
        request = assets.read(path)
        package_id = 'main' if request['groupId'] == self.manifest['nexus']['groupId'] else 'textures'
        self.uploads.append(package_id)
        self.assertEqual(request['file']['primary_mod_manager_download'], package_id == 'main')
        self.assertEqual(request['file']['update_mod_version'], package_id == 'main')
        self.assertEqual(bool(request['changelog']), package_id == 'main')
        archive = Path(request['archivePath'])
        version_id = '31' if package_id == 'main' else '32'
        self.remote[request['groupId']] = [{'id': version_id, 'version': '1.0.0', 'category': 'main',
            'file': {'id': request['groupId']}, 'is_primary': package_id == 'main', 'game_scoped_id': '500' + version_id}]
        journal = {'schemaVersion': 1, 'phase': 'verified', 'status': 'version-read-verified', 'plan': request,
                   'versionId': version_id, 'changelogStatus': 'posted' if request['changelog'] else 'not-requested',
                   'archive': {'sha256': assets.checksum(archive), 'md5': hashlib.md5(archive.read_bytes()).hexdigest(),
                               'sizeBytes': archive.stat().st_size}}
        assets.save(Path(request['journalPath']), journal)
        return journal

    def bridge(self, client, args):
        self.bridge_calls.append(args)
        if args[0] == 'register':
            return {'exitCode': 0, 'result': {}}
        if args[0] == 'promote':
            package_id = args[args.index('--package') + 1]
            receipt = assets.read(args[args.index('--receipt') + 1])
            self.assertEqual(receipt['groupId'], self.manifest['nexus']['groupId'] if package_id == 'main' else self.manifest['nexus']['textures']['groupId'])
            return {'exitCode': 0, 'result': {'status': 'queued', 'id': 'promotion-' + package_id}}
        self.assertEqual(args[0], 'wait')
        request_id = args[args.index('--request') + 1]
        return {'exitCode': 2 if self.pending else 0, 'result': {'status': 'pending' if self.pending else 'completed',
            'id': request_id, 'operation': 'promote', 'projectId': 'sovereign', 'packageId': request_id.removeprefix('promotion-'),
            'result': {'publication': 'verified'}}}

    def test_texture_archive_and_joint_release_order_and_exact_retry(self):
        with zipfile.ZipFile(self.archives['textures']) as archive:
            self.assertEqual(sorted(archive.namelist()), ['mod/menu/hi/data', 'mod/menu/hi/header'])
        result = pipeline.release_batch(self.archives, self.settings)
        self.assertEqual(result['order'], ['textures', 'main'])
        self.assertFalse(self.uploads)
        self.assertFalse(self.bridge_calls)
        result = pipeline.release_batch(self.archives, self.settings, apply=True)
        self.assertEqual(result['status'], 'completed')
        self.assertEqual(self.uploads, ['textures', 'main'])
        before = len(self.bridge_calls)
        pipeline.release_batch(self.archives, self.settings, apply=True, resume=True)
        self.assertEqual(self.uploads, ['textures', 'main'])
        self.assertEqual(len(self.bridge_calls), before)

    def test_all_packages_preflight_before_any_upload(self):
        self.archives['main'].write_bytes(b'corrupt')
        with self.assertRaises(ValueError):
            pipeline.release_batch(self.archives, self.settings, apply=True)
        self.assertFalse(self.uploads)

    def test_texture_failure_blocks_main_and_uncertain_post_cannot_resume(self):
        def uncertain(root, command, path):
            request = assets.read(path)
            assets.save(Path(request['journalPath']), {'schemaVersion': 1, 'phase': 'version-post-started', 'plan': request})
            raise ValueError('uncertain texture upload')
        with mock.patch.object(workflow.automation, 'invoke', side_effect=uncertain):
            with self.assertRaisesRegex(ValueError, 'uncertain texture'):
                pipeline.release_batch(self.archives, self.settings, apply=True)
        with self.assertRaisesRegex(ValueError, 'exact package set'):
            pipeline.release_batch({'main': self.archives['main']}, self.settings, apply=True)
        with self.assertRaisesRegex(ValueError, 'uncertain'):
            pipeline.release_batch(self.archives, self.settings, apply=True, resume=True)
        self.assertFalse(self.uploads)

    def test_pending_promotion_reuses_request_without_upload_or_submission(self):
        self.pending = True
        result = pipeline.release_batch(self.archives, self.settings, apply=True)
        self.assertEqual(result['status'], 'pending-promotion')
        submissions = len([c for c in self.bridge_calls if c[0] == 'promote'])
        self.pending = False
        result = pipeline.release_batch(self.archives, self.settings, apply=True, resume=True)
        self.assertEqual(result['status'], 'completed')
        self.assertEqual(len([c for c in self.bridge_calls if c[0] == 'promote']), submissions)
        self.assertEqual(len(self.uploads), 2)

    def test_missing_file_id_stays_pending_and_identity_mismatch_blocks_promotion(self):
        plan = publisher.publish_plan(self.archives['main'], self.manifest)
        publisher.publish(plan)
        row = self.remote[self.manifest['nexus']['groupId']][0]
        del row['game_scoped_id']
        self.assertEqual(pipeline.promote(self.archives['main'], self.settings)['status'], 'pending-file-id')
        self.assertFalse(self.bridge_calls)
        row.update(game_scoped_id='5031', version='wrong')
        with self.assertRaisesRegex(ValueError, 'identity'):
            pipeline.promote(self.archives['main'], self.settings)
        self.assertFalse(self.bridge_calls)

    def test_promotion_only_retry_does_not_require_current_selection(self):
        pipeline.release_batch(self.archives, self.settings, apply=True)
        (self.root / '.vdb/selected.json').unlink()
        self.assertEqual(pipeline.promote(self.archives['main'], self.settings)['status'], 'completed')
        self.assertEqual(len(self.uploads), 2)

    def test_terminal_or_interrupted_promotion_never_resubmits(self):
        pipeline.release_batch(self.archives, self.settings, apply=True)
        path = self.archives['main'].parent / 'promotion.json'
        operation = assets.read(path)
        before = len(self.bridge_calls)
        for status in ('submitting', 'failed', 'expired', 'interrupted'):
            operation['status'] = status
            assets.save(path, operation)
            with self.assertRaisesRegex(ValueError, 'interrupted/terminal'):
                pipeline.promote(self.archives['main'], self.settings)
        self.assertEqual(len(self.bridge_calls), before)

    def snapshot(self):
        return {'stale': False, 'activeGameId': 'eldenring', 'activeProfileId': 'fixture', 'activeMods': [
            {'id': p, 'version': '1.0.0', 'vdbProjectId': 'sovereign', 'vdbPackageId': p,
             'vdbBuildId': ('a' if p == 'main' else 'b') * 24, 'source': 'nexus', 'vdbPublication': 'verified',
             'modId': 201, 'fileId': '50031' if p == 'main' else '50032'} for p in ('main', 'textures')]}

    def test_readiness_requires_both_exact_enabled_promoted_builds(self):
        snapshot = self.snapshot()
        self.assertFalse(pipeline.collection_readiness(self.settings, snapshot)['ready'])
        pipeline.release_batch(self.archives, self.settings, apply=True)
        before = list(self.bridge_calls)
        self.assertTrue(pipeline.collection_readiness(self.settings, snapshot)['ready'])
        self.assertEqual(self.bridge_calls, before)
        snapshot['activeMods'][0]['fileId'] = '999'
        self.assertFalse(pipeline.collection_readiness(self.settings, snapshot)['ready'])
        snapshot = self.snapshot()
        snapshot['activeMods'].pop()
        self.assertEqual(pipeline.collection_readiness(self.settings, snapshot)['missingPackages'], ['textures'])
        snapshot['stale'] = True
        self.assertEqual(pipeline.collection_readiness(self.settings, snapshot)['status'], 'unavailable')

    def test_safe_upload_resume_uses_original_request(self):
        plan = publisher.publish_plan(self.archives['main'], self.manifest)
        publisher.publish(plan)
        path = self.archives['main'].parent / 'upload-journal.json'
        journal = assets.read(path)
        journal.update(phase='version-created', status='in-progress', changelogStatus='pending')
        assets.save(path, journal)
        with mock.patch.object(workflow.automation, 'invoke', return_value={}) as invoke:
            pipeline.resume_upload(self.archives['main'], self.settings)
        request = assets.read(invoke.call_args.args[2])
        self.assertTrue(request['resume'])
        self.assertEqual(request['archivePath'], journal['plan']['archivePath'])
        self.assertEqual(request['sourceHashes'], journal['plan']['sourceHashes'])


if __name__ == '__main__':
    unittest.main()
