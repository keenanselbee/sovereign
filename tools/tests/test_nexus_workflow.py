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
        shared = workflow.automation.tool_root(workflow.ROOT)
        script = "import { chromeArguments } from " + json.dumps((shared / 'src/browser/session.mjs').as_uri()) + "; console.log(JSON.stringify(chromeArguments('C:/repo/.codex-temp/profile', 43210)))"
        args = json.loads(workflow.subprocess.run(['node', '--input-type=module', '-e', script], check=True, capture_output=True, text=True).stdout)
        self.assertIn('--remote-debugging-address=127.0.0.1', args)
        self.assertIn('--remote-debugging-port=43210', args)
        self.assertIn('--user-data-dir=C:/repo/.codex-temp/profile', args)
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

    def test_zip_creation_checks_recovered_sources_before_writing(self):
        import recovered_sources
        self.write('source/mod/regulation.bin')
        run = self.root / 'output'
        run.mkdir()
        with mock.patch.object(recovered_sources, 'require_fresh', side_effect=ValueError('stale sources')):
            with self.assertRaisesRegex(ValueError, 'stale sources'):
                workflow.write_vortex_package(self.root / 'source', self.manifest, run, '0.0.0-test')
        self.assertEqual(list(run.iterdir()), [])

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

    def test_existing_upload_journal_blocks_adapter_before_any_shared_call(self):
        archive = self.write('candidate.zip')
        self.write('upload-journal.json', b'{"versionId":"31"}')
        with mock.patch.object(workflow.automation, 'invoke') as invoke:
            with self.assertRaisesRegex(ValueError, 'journal already exists'):
                publisher.publish({'archive': str(archive)})
            invoke.assert_not_called()

    def test_changelog_must_match_both_release_versions(self):
        self.write('nexus-changelog.txt', b'TargetVersion=0.2\nBaselineVersion=0.1\nCompleted change\n')
        self.assertEqual(publisher.reviewed_changelog(self.root, '0.2', '0.1'), 'Completed change')
        with self.assertRaises(ValueError):
            publisher.reviewed_changelog(self.root, '0.3', '0.1')

    def test_publish_plan_keeps_every_active_id_and_adapter_forwards_it(self):
        archive = self.write('.codex-temp/vortex-packages/fixture/release.zip')
        directory = self.root / 'nexus'
        manifest = {
            'id': 'Sovereign', 'displayName': 'Sovereign', 'version': '0.2', 'releaseReady': True,
            'dependencies': [{'verified': True}], 'package': {'excludeDirectories': ['src']},
            'nexus': {'url': 'https://www.nexusmods.com/games/eldenring/mods/201',
                      'descriptionDirectory': 'nexus', 'groupId': '20', 'modId': '10'}
        }
        self.write('mod.json', json.dumps(manifest).encode())
        self.write('changelog.txt', b'Version 1.0.0\nCompleted change\n')
        for name, text in {
            'nexus-short-desc.txt': 'Short', 'nexus-full-desc.txt': '[b]Full[/b]',
            'nexus-file-desc.txt': 'Pitch',
            'nexus-changelog.txt': 'TargetVersion=0.2\nBaselineVersion=0.1\nCompleted change\n'
        }.items():
            self.write(f'nexus/{name}', text.encode())
        remote = {
            'current': {'id': '30', 'version': '0.1'},
            'activeVersions': [
                {'id': '30', 'version': '0.1', 'category': 'main', 'is_primary': True},
                {'id': '29', 'version': '0.0.9', 'category': 'optional', 'is_primary': False}
            ]
        }
        receipt = {'sha256': workflow.core.digest(archive), 'source': str(self.root / 'vortex'), 'files': {}}
        with mock.patch.object(workflow.core, 'ROOT', self.root), \
                mock.patch.object(publisher, 'verified_archive', return_value=(archive, receipt)), \
                mock.patch.object(publisher.core, 'nexus_issues', return_value=[]), \
                mock.patch.object(publisher.core, 'nexus_status', return_value=remote), \
                mock.patch.object(publisher, 'api', return_value={'versions': []}):
            plan = publisher.publish_plan(archive, manifest)
        self.assertEqual(plan['baseline'], remote['current'])
        self.assertEqual(plan['expectedActiveIds'], ['29', '30'])

        def invoke(_repo, _command, request_path):
            request = workflow.core.read_json(request_path)
            self.assertEqual(request['baselineVersionId'], '30')
            self.assertEqual(request['expectedActiveIds'], ['29', '30'])
            return {'status': 'version-read-verified', 'versionId': '31'}

        with mock.patch.object(workflow.core, 'ROOT', self.root), \
                mock.patch.object(workflow.automation, 'invoke', side_effect=invoke):
            self.assertEqual(publisher.publish(plan)['versionId'], '31')

    def test_publish_plan_rejects_metadata_changed_during_remote_review(self):
        archive = self.write('.codex-temp/vortex-packages/fixture/release.zip')
        manifest = {
            'id': 'Sovereign', 'displayName': 'Sovereign', 'version': '0.2', 'releaseReady': True,
            'dependencies': [{'verified': True}], 'package': {'excludeDirectories': ['src']},
            'nexus': {'url': 'https://www.nexusmods.com/games/eldenring/mods/201',
                      'descriptionDirectory': 'nexus', 'groupId': '20', 'modId': '10'}
        }
        self.write('mod.json', json.dumps(manifest).encode())
        for name, text in {
            'nexus-short-desc.txt': 'Short', 'nexus-full-desc.txt': '[b]Full[/b]',
            'nexus-file-desc.txt': 'Pitch',
            'nexus-changelog.txt': 'TargetVersion=0.2\nBaselineVersion=0.1\nCompleted change\n'
        }.items():
            self.write(f'nexus/{name}', text.encode())
        remote = {'current': {'id': '30', 'version': '0.1'}, 'activeVersions': [{'id': '30'}]}
        receipt = {'sha256': workflow.core.digest(archive), 'source': str(self.root / 'vortex'), 'files': {}}

        for changed in ('mod.json', 'nexus/nexus-changelog.txt', 'changelog.txt'):
            with self.subTest(changed=changed):
                def remote_read(_manifest):
                    if changed == 'mod.json':
                        self.write(changed, json.dumps({**manifest, 'displayName': 'Changed'}).encode())
                    else:
                        self.write(changed, b'TargetVersion=0.2\nBaselineVersion=0.1\nRevised change\n')
                    return remote

                self.write('mod.json', json.dumps(manifest).encode())
                self.write('changelog.txt', b'Version 1.0.0\nCompleted change\n')
                self.write('nexus/nexus-changelog.txt', b'TargetVersion=0.2\nBaselineVersion=0.1\nCompleted change\n')
                with mock.patch.object(workflow.core, 'ROOT', self.root), \
                        mock.patch.object(publisher, 'verified_archive', return_value=(archive, receipt)), \
                        mock.patch.object(publisher.core, 'nexus_issues', return_value=[]), \
                        mock.patch.object(publisher.core, 'nexus_status', side_effect=remote_read), \
                        mock.patch.object(publisher, 'api', return_value={'versions': []}):
                    with self.assertRaisesRegex(ValueError, 'Release inputs changed during planning'):
                        publisher.publish_plan(archive, manifest)

    def test_shared_publish_adapter_preserves_payload_and_source_preconditions(self):
        archive = self.write('candidate.zip')
        self.write('mod.json', json.dumps({'id': 'Sovereign', 'nexus': {'url': 'https://www.nexusmods.com/games/eldenring/mods/201'}}).encode())
        plan = {'archive': str(archive), 'archiveSha256': workflow.core.digest(archive),
                'sourceHashes': {str(archive): workflow.core.digest(archive)}, 'sourceInventory': {'root': str(self.root), 'names': []},
                'groupId': '893965', 'modId': '18610093293769', 'version': '0.2', 'name': 'Sovereign',
                'description': 'Pitch', 'changelog': 'Completed change', 'baseline': {'id': '30', 'version': '0.1'}}
        def invoke(repo, command, request_path):
            self.assertEqual(repo, self.root)
            self.assertEqual(command, 'publish')
            request = workflow.core.read_json(request_path)
            self.assertTrue(request['apply'])
            self.assertEqual(request['file']['previous_version_id'], '30')
            self.assertEqual(request['file']['description'], 'Pitch')
            self.assertTrue(request['file']['show_requirements_pop_up'])
            self.assertTrue(request['file']['archive_existing_file'])
            self.assertEqual(request['sourceHashes'], plan['sourceHashes'])
            self.assertEqual(request['sourceInventory'], plan['sourceInventory'])
            self.assertIsNone(request['expectedActiveIds'])
            self.assertEqual(request['journalPath'], str(archive.parent / 'upload-journal.json'))
            return {'status': 'version-read-verified', 'versionId': '31'}
        with mock.patch.object(workflow.core, 'ROOT', self.root), mock.patch.object(workflow.automation, 'invoke', side_effect=invoke):
            self.assertEqual(publisher.publish(plan)['versionId'], '31')

    def test_shared_publish_failure_preserves_partial_journal(self):
        archive = self.write('candidate.zip')
        self.write('mod.json', json.dumps({'id': 'Sovereign', 'nexus': {'url': 'https://www.nexusmods.com/games/eldenring/mods/201'}}).encode())
        plan = {'archive': str(archive), 'archiveSha256': workflow.core.digest(archive), 'sourceHashes': {},
                'groupId': '893965', 'modId': '18610093293769', 'version': '0.2', 'name': 'Sovereign',
                'description': 'Pitch', 'changelog': 'Change', 'baseline': {'id': '30', 'version': '0.1'}}
        def failed(*args):
            self.write('upload-journal.json', b'{"versionId":"31","phase":"changelog-post-started"}')
            raise workflow.subprocess.CalledProcessError(1, ['node'])
        with mock.patch.object(workflow.core, 'ROOT', self.root), mock.patch.object(workflow.automation, 'invoke', side_effect=failed):
            with self.assertRaisesRegex(ValueError, 'Publish incomplete'):
                publisher.publish(plan)
        self.assertEqual(workflow.core.read_json(archive.parent / 'upload-journal.json')['versionId'], '31')

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

    def test_current_file_finds_durable_release_journals(self):
        archive = self.write('.vdb/releases/main/1.0.0/Sovereign-1.0.0.zip')
        fingerprint = workflow.core.digest(archive)
        files = {'mod/regulation.bin': {'size': 7, 'sha256': 'fixture'}}
        plan = {'groupId': '893965', 'modId': '18610093293769', 'version': '1.0.0', 'archiveSha256': fingerprint}
        workflow.core.write_json(archive.parent / 'receipt.json', {'kind': 'vortex-package', 'draft': False,
            'version': '1.0.0', 'files': files, 'archive': archive.name, 'sha256': fingerprint})
        workflow.core.write_json(archive.parent / 'upload-journal.json', {'versionId': 'new', 'plan': plan})
        remote = {'groupId': '893965', 'modId': '18610093293769', 'current': {'id': 'new', 'version': '1.0.0'}}
        with mock.patch.object(workflow, 'ROOT', self.root):
            self.assertTrue(workflow.published_payload_matches({'files': files}, remote))


if __name__ == '__main__':
    unittest.main()
