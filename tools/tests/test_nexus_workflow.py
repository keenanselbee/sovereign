import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import nexus_workflow as workflow
import nexus_publish as publisher


class NexusWorkflowTests(unittest.TestCase):
    def test_chrome_launch_uses_regular_browser_flags_and_dedicated_profile(self):
        args = workflow.chrome_arguments('chrome.exe', r'C:\repo\.codex-temp\profile', 43210)
        self.assertIn('--remote-debugging-address=127.0.0.1', args)
        self.assertIn('--remote-debugging-port=43210', args)
        self.assertIn(r'--user-data-dir=C:\repo\.codex-temp\profile', args)
        for flag in ('--no-sandbox', '--enable-automation', '--headless', '--disable-blink-features=AutomationControlled'):
            self.assertNotIn(flag, args)

    def setUp(self):
        scratch = workflow.ROOT / '.codex-temp/tests'
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = {'package': {'source': 'vortex', 'excludeDirectories': ['src', '.smithbox']},
                         'version': None, 'releaseReady': False, 'dependencies': [{'verified': False}]}

    def write(self, name, data=b'fixture'):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def test_vortex_inventory_keeps_extras_dll_and_zero_byte_files(self):
        self.write('source/mod/regulation.bin')
        self.write('source/mod/chr/vortex-only.dcx')
        self.write('source/mods/required.dll')
        self.write('source/mod/menu/empty.gfx', b'')
        self.write('source/mod/event/src/custom.js')
        self.write('source/mod/.smithbox/row-names.json')
        source = self.root / 'source'
        run = self.root / 'output'
        run.mkdir()
        archive = workflow.build_vortex_package(source, self.manifest, run, '0.0.0-test')
        with zipfile.ZipFile(archive) as zipped:
            self.assertEqual(set(zipped.namelist()), {'mod/regulation.bin', 'mod/chr/vortex-only.dcx',
                                                    'mods/required.dll', 'mod/menu/empty.gfx'})
            self.assertEqual(zipped.read('mod/menu/empty.gfx'), b'')
        receipt = workflow.core.read_json(run / 'receipt.json')
        self.assertTrue(receipt['draft'])
        self.assertEqual(len(receipt['excluded']), 2)
        self.assertEqual(receipt['sha256'], workflow.core.digest(archive))

    def test_package_rejects_drift_and_release_without_gates(self):
        self.write('source/mod/regulation.bin')
        run = self.root / 'output'
        run.mkdir()
        with self.assertRaisesRegex(ValueError, 'gates'):
            workflow.build_vortex_package(self.root / 'source', self.manifest, run, '1.0', draft=False)
        original = workflow.inventory
        calls = 0
        def changed(*args):
            nonlocal calls
            calls += 1
            if calls == 2:
                self.write('source/mod/new.dcx')
            return original(*args)
        with mock.patch.object(workflow, 'inventory', side_effect=changed):
            with self.assertRaisesRegex(ValueError, 'changed during packaging'):
                workflow.build_vortex_package(self.root / 'source', self.manifest, run, '0.0-test')
        self.assertFalse((run / 'receipt.json').exists())

    def test_unexpected_root_and_secret_files_are_not_silently_uploaded(self):
        self.write('mod/regulation.bin')
        for name in ('unexpected.txt', 'mod/.env', 'mod/API.txt'):
            path = self.write(name)
            with self.subTest(name=name), self.assertRaises(ValueError):
                workflow.inventory(self.root, self.manifest)
            path.unlink()

    def test_multipart_integer_size_etags_and_finalise_order(self):
        archive = self.write('candidate.zip', b'abcdefgh')
        calls, parts = [], []
        def api(method, path, body=None):
            calls.append((method, path, body))
            if path == '/uploads/multipart':
                self.assertIs(type(body['size_bytes']), int)
                return {'id': 'fixture-upload', 'part_size_bytes': 3,
                        'part_presigned_urls': ['https://s3.test/1', 'https://s3.test/2', 'https://s3.test/3'],
                        'complete_presigned_url': 'https://s3.test/complete'}
            return {'state': 'available'}
        def storage(method, url, data, content_type):
            if method == 'PUT':
                parts.append(data)
                return '"fixture-etag"', b''
            self.assertIn(b'<PartNumber>3</PartNumber>', data)
            return None, b'<CompleteMultipartUploadResult/>'
        self.assertEqual(publisher.upload_parts(archive, api, storage), 'fixture-upload')
        self.assertEqual(parts, [b'abc', b'def', b'gh'])
        self.assertEqual([row[1] for row in calls], ['/uploads/multipart', '/uploads/fixture-upload/finalise', '/uploads/fixture-upload'])

    def test_partial_upload_is_journaled_and_cannot_be_repeated(self):
        archive = self.write('candidate.zip')
        plan = {'archive': str(archive), 'archiveSha256': workflow.core.digest(archive), 'sourceHashes': {},
                'groupId': '893965', 'modId': '18610093293769', 'version': '0.2', 'name': 'Sovereign',
                'description': 'Pitch', 'changelog': 'Completed change', 'baseline': {'id': 'old'}}
        def api(method, path, body=None):
            if method == 'GET':
                return {'versions': [{'id': 'old', 'version': '0.1', 'category': 'main'}]}
            if path.endswith('/changelogs'):
                raise ValueError('Temporary error')
            return {'version': {'id': 'new'}}
        with self.assertRaisesRegex(ValueError, 'Temporary error'):
            publisher.publish(plan, api, lambda _: 'upload-id')
        state = workflow.core.read_json(archive.parent / 'upload-journal.json')
        self.assertEqual(state['versionId'], 'new')
        self.assertEqual(state['status'], 'changelog-post-started')
        with self.assertRaisesRegex(ValueError, 'journal already exists'):
            publisher.publish(plan, api, lambda _: self.fail('must not upload again'))

    def test_changelog_must_match_both_release_versions(self):
        self.write('nexus-changelog.txt', b'TargetVersion=0.2\nBaselineVersion=0.1\nCompleted change\n')
        self.assertEqual(publisher.reviewed_changelog(self.root, '0.2', '0.1'), 'Completed change')
        with self.assertRaises(ValueError):
            publisher.reviewed_changelog(self.root, '0.3', '0.1')

    def test_publish_success_records_immutable_id_and_exact_payload(self):
        archive = self.write('candidate.zip')
        plan = {'archive': str(archive), 'archiveSha256': workflow.core.digest(archive), 'sourceHashes': {},
                'groupId': '893965', 'modId': '18610093293769', 'version': '0.2', 'name': 'Sovereign',
                'description': 'Pitch', 'changelog': 'Completed change', 'baseline': {'id': 'old'}}
        created = False
        def api(method, path, body=None):
            nonlocal created
            if method == 'GET':
                return {'versions': [{'id': 'new' if created else 'old', 'version': '0.2' if created else '0.1',
                                      'category': 'main', 'game_scoped_id': '123'}]}
            if path.endswith('/versions'):
                self.assertEqual(body['previous_version_id'], 'old')
                self.assertEqual(body['description'], 'Pitch')
                self.assertTrue(body['archive_existing_file'])
                created = True
                return {'version': {'id': 'new'}}
            self.assertEqual(body, {'version': '0.2', 'changelog': 'Completed change'})
            return {}
        result = publisher.publish(plan, api, lambda _: 'upload-id')
        self.assertEqual(result['status'], 'version-read-verified')
        self.assertEqual(result['remoteVersion']['game_scoped_id'], '123')

    def test_remote_drift_blocks_version_creation_after_upload(self):
        archive = self.write('candidate.zip')
        plan = {'archive': str(archive), 'archiveSha256': workflow.core.digest(archive), 'sourceHashes': {},
                'groupId': '893965', 'version': '0.2', 'baseline': {'id': 'old'}}
        def api(method, path, body=None):
            self.assertEqual(method, 'GET')
            return {'versions': [{'id': 'changed', 'version': '0.3', 'category': 'main'}]}
        with self.assertRaisesRegex(ValueError, 'Remote release changed'):
            publisher.publish(plan, api, lambda _: 'upload-id')

    def test_current_file_requires_immutable_id_and_matching_vortex_payload(self):
        archive = self.write('.codex-temp/vortex-packages/fixture/release.zip')
        fingerprint = workflow.core.digest(archive)
        files = {'mod/regulation.bin': {'size': 7, 'sha256': 'fixture'}}
        plan = {'groupId': '893965', 'modId': '18610093293769', 'version': '0.2', 'archiveSha256': fingerprint}
        receipt = {'kind': 'vortex-package', 'draft': False, 'version': '0.2', 'files': files,
                   'archive': archive.name, 'sha256': fingerprint}
        workflow.core.write_json(archive.parent / 'receipt.json', receipt)
        workflow.core.write_json(archive.parent / 'upload-journal.json', {'versionId': 'new', 'plan': plan})
        remote = {'groupId': '893965', 'modId': '18610093293769', 'current': {'id': 'new', 'version': '0.2'}}
        with mock.patch.object(workflow, 'ROOT', self.root):
            self.assertTrue(workflow.published_payload_matches({'files': files}, remote))
            self.assertFalse(workflow.published_payload_matches({'files': {}}, remote))
            remote['current']['id'] = 'unrelated-same-label'
            self.assertFalse(workflow.published_payload_matches({'files': files}, remote))


if __name__ == '__main__':
    unittest.main()
