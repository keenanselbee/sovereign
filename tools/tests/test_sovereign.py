import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import zipfile

SPEC = importlib.util.spec_from_file_location('sovereign', Path(__file__).resolve().parents[1] / 'sovereign.py')
workflow = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workflow)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        scratch = workflow.ROOT / '.codex-temp/tests'
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def write(self, relative, content=b'fixture'):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def manifest(self):
        return {'runtimePatterns': ['regulation.bin', 'event/*.dcx'], 'dependencies': []}

    def test_containment_rejects_parent_and_absolute_paths(self):
        for relative in ('../outside', 'event/../../outside', str(self.root / 'absolute')):
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                workflow.contained(self.root, relative)
        self.assertEqual(workflow.contained(self.root, 'event/common.dcx'), self.root / 'event/common.dcx')

    def test_status_reports_drift_and_destination_only_files_without_writing(self):
        for destination in ('repo', 'editor', 'live', 'vortex'):
            self.write(f'{destination}/event/common.dcx')
        self.write('editor/event/common.dcx', b'manual edit')
        self.write('live/event/orphan.dcx', b'old output')
        settings = {'roots': {key: str(self.root / key) for key in ('editor', 'live', 'vortex')},
                    'mappings': [{'scope': 'events', 'pattern': 'event/*.dcx', 'prefix': 'event',
                                  'editorRoot': 'editor', 'editorPrefix': 'event'}]}
        before = {str(p): workflow.digest(p) for p in self.root.rglob('*') if p.is_file()}
        rows = workflow.status_rows(self.root / 'repo', settings, 'events')
        common, orphan = rows
        self.assertEqual(common['state'], 'Review')
        self.assertNotEqual(common['hashes']['editor'], common['hashes']['repo'])
        self.assertIsNone(orphan['hashes']['repo'])
        self.assertIsNotNone(orphan['hashes']['live'])
        self.assertEqual(before, {str(p): workflow.digest(p) for p in self.root.rglob('*') if p.is_file()})

    def test_status_all_equal_is_match(self):
        settings = {'roots': {}, 'mappings': [{'scope': 'params', 'pattern': 'regulation.bin', 'prefix': '',
                                               'editorRoot': 'editor', 'editorPrefix': ''}]}
        for key in ('repo', 'editor', 'live', 'vortex'):
            self.write(f'{key}/regulation.bin')
            settings['roots'][key] = str(self.root / key)
        self.assertEqual(workflow.status_rows(self.root / 'repo', settings)[0]['state'], 'Match')

    def test_status_default_is_compact_and_verbose_preserves_matching_files(self):
        self.write('mod.json', b'{}')
        rows = [{'file': 'same.bin', 'state': 'Match', 'hashes': {'repo': 'same', 'editor': 'same'}},
                {'file': 'changed.bin', 'state': 'Review', 'hashes': {'repo': 'old', 'editor': 'new'}}]
        for extra in ([], ['--verbose']):
            with mock.patch.object(workflow, 'ROOT', self.root), \
                    mock.patch.object(workflow, 'config', return_value={}), \
                    mock.patch.object(workflow, 'status_rows', return_value=rows), \
                    mock.patch('sys.argv', ['sovereign.py', 'status', *extra]), \
                    mock.patch('sys.stdout', new_callable=io.StringIO) as output:
                workflow.main()
            self.assertIn('changed.bin', output.getvalue())
            self.assertIn('2 files inspected: 1 match, 1 need review', output.getvalue())
            self.assertEqual('same.bin' in output.getvalue(), bool(extra))

    def test_package_has_only_runtime_payload_and_verified_receipt(self):
        self.write('regulation.bin')
        self.write('event/common.dcx')
        self.write('event/src/common.dcx', b'source binary')
        self.write('event/src/common.dcx.js', b'source script')
        self.write('.smithbox/private.json')
        run = self.root / 'output'
        run.mkdir()
        archive = workflow.make_package(self.root, self.manifest(), run, '0.0.0-test')
        with zipfile.ZipFile(archive) as zipped:
            self.assertEqual(set(zipped.namelist()), {'mod/regulation.bin', 'mod/event/common.dcx', 'DRAFT-NOT-FOR-RELEASE.txt'})
        receipt = workflow.read_json(run / 'receipt.json')
        self.assertEqual(receipt['sha256'], workflow.digest(archive))
        self.assertFalse(receipt['gameplayVerified'])
        with self.assertRaises(FileExistsError):
            workflow.make_package(self.root, self.manifest(), run, '0.0.0-test')

    def test_package_rejects_source_directory_and_version_path_injection(self):
        self.write('regulation.bin')
        self.write('event/src/common.dcx')
        manifest = self.manifest()
        manifest['runtimePatterns'] = ['regulation.bin', 'event/**/*.dcx']
        with self.assertRaisesRegex(ValueError, 'Authoring'):
            workflow.runtime_files(self.root, manifest)
        with self.assertRaises(ValueError):
            workflow.make_package(self.root, self.manifest(), self.root, '../outside')

    def test_package_fails_when_source_changes_during_read(self):
        self.write('regulation.bin')
        original = Path.read_bytes
        def changed_read(path):
            data = original(path)
            return b'changed' if path.name == 'regulation.bin' else data
        with mock.patch.object(Path, 'read_bytes', changed_read):
            with self.assertRaisesRegex(ValueError, 'changed during packaging'):
                workflow.make_package(self.root, self.manifest(), self.root, '0.0.0-test')
        self.assertFalse((self.root / 'receipt.json').exists())

    def test_event_comparison_preserves_bindings_duplicate_ids_and_metadata(self):
        before = {'Events': [{'ID': 1, 'Parameters': [0], 'Instructions': []},
                             {'ID': 1, 'Parameters': [1], 'Instructions': []}], 'Format': 1}
        self.assertTrue(workflow.compare_events(before, copy.deepcopy(before))['equal'])
        after = copy.deepcopy(before)
        after['Events'][1]['Parameters'] = [2]
        after['Format'] = 2
        result = workflow.compare_events(before, after)
        self.assertFalse(result['equal'])
        self.assertEqual(result['changedEvents'], [{'index': 1, 'beforeId': 1, 'afterId': 1}])
        self.assertEqual(result['changedMetadata'], ['Format'])
        self.assertFalse(workflow.compare_events(before, dict(before, Events=list(reversed(before['Events']))))['equal'])

    def test_nexus_checks_missing_metadata_length_and_bbcode(self):
        manifest = {'version': None, 'nexus': {'descriptionDirectory': 'nexus', 'url': None, 'groupId': None}}
        self.write('nexus/nexus-full-desc.txt', b'[b]Broken[/i]')
        self.write('nexus/nexus-short-desc.txt', b'x' * 351)
        self.write('nexus/nexus-file-desc.txt', 'Non-ASCII \u2014'.encode())
        issues = workflow.nexus_issues(self.root, manifest)
        self.assertTrue(any('mismatched' in issue for issue in issues))
        self.assertTrue(any('350' in issue for issue in issues))
        self.assertTrue(any('non-ASCII' in issue for issue in issues))
        self.assertTrue(any('metadata' in issue for issue in issues))

    def nexus_fixture(self):
        manifest = {'gameDomain': 'eldenring', 'version': None, 'nexus': {
            'url': 'https://www.nexusmods.com/games/eldenring/mods/201',
            'gameScopedModId': '201', 'modId': '18610093293769', 'groupId': '893965'}}
        active = {'id': '18610093305851', 'game_scoped_id': '12283', 'name': 'Sovereign',
                  'version': '0.1', 'category': 'main', 'uploaded_at': '2023-01-08T03:51:21Z',
                  'file': {'id': '893965'}, 'is_primary': False}
        responses = {
            '/games/eldenring/mods/201': {'id': '18610093293769', 'game_scoped_id': '201'},
            '/mods/18610093293769/files': {'mod_files': [{'id': '893965', 'name': 'Sacred Tweaks'}]},
            '/mod-files/893965/versions': {'versions': [
                dict(active, id='18610093306013', version='7.8-1.07.1', category='archived',
                     uploaded_at='2023-01-14T21:16:20Z'), active]}}
        return manifest, responses

    def test_description_review_does_not_require_release_metadata(self):
        manifest = {'version': None, 'nexus': {'descriptionDirectory': 'nexus'}}
        self.write('nexus/nexus-full-desc.txt', b'[b]Sovereign[/b]')
        self.write('nexus/nexus-short-desc.txt', b'A harsher journey through the Lands Between.')
        self.write('nexus/nexus-file-desc.txt', b'Claim forbidden power.')
        self.assertEqual(workflow.nexus_issues(self.root, manifest, descriptions_only=True), [])
        self.assertIn('Release version is not selected', workflow.nexus_issues(self.root, manifest))
        self.write('nexus/nexus-file-desc.txt', b'')
        self.assertIn('nexus-file-desc.txt: missing or empty',
                      workflow.nexus_issues(self.root, manifest, descriptions_only=True))

    def test_file_pitch_limit_and_punctuation_only_copy(self):
        manifest = {'nexus': {'descriptionDirectory': 'nexus'}}
        self.write('nexus/nexus-full-desc.txt', b'[b]Sovereign[/b]')
        self.write('nexus/nexus-short-desc.txt', b'x' * 300)
        self.write('nexus/nexus-file-desc.txt', b'y' * 256)
        self.assertIn('File description exceeds 255 characters',
                      workflow.nexus_issues(self.root, manifest, descriptions_only=True))
        self.write('nexus/nexus-short-desc.txt', b'Claim forbidden power!!!')
        self.write('nexus/nexus-file-desc.txt', b'CLAIM forbidden power')
        self.assertIn('File pitch must be distinct and shorter than the short description',
                      workflow.nexus_issues(self.root, manifest, descriptions_only=True))

    def test_nexus_active_release_ignores_newer_archived_upload(self):
        manifest, responses = self.nexus_fixture()
        result = workflow.nexus_status(manifest, responses.__getitem__)
        self.assertEqual(result['current']['version'], '0.1')
        self.assertEqual(result['current']['game_scoped_id'], '12283')
        self.assertEqual(result['releaseComparison'], 'Verify')
        manifest['version'] = '0.1'
        self.assertIn('contents unverified', workflow.nexus_status(manifest, responses.__getitem__)['releaseComparison'])

    def test_nexus_rejects_wrong_mod_group_and_response_schema(self):
        for target, replacement in [
            ('/games/eldenring/mods/201', {'id': '123', 'game_scoped_id': '201'}),
            ('/mods/18610093293769/files', {'mod_files': [{'id': '123'}]}),
            ('/mod-files/893965/versions', {'versions': [{}]}),
            ('/mod-files/893965/versions', {'versions': None})]:
            manifest, responses = self.nexus_fixture()
            responses[target] = replacement
            with self.subTest(target=target), self.assertRaises(ValueError):
                workflow.nexus_status(manifest, responses.__getitem__)

    def test_nexus_ambiguous_active_versions_remain_unresolved(self):
        manifest, responses = self.nexus_fixture()
        versions = responses['/mod-files/893965/versions']['versions']
        versions.append(dict(versions[1], id='12345', category='optional', version='0.2'))
        result = workflow.nexus_status(manifest, responses.__getitem__)
        self.assertIsNone(result['current'])
        self.assertEqual(result['releaseComparison'], 'Verify')
        versions[-1]['is_primary'] = True
        self.assertEqual(workflow.nexus_status(manifest, responses.__getitem__)['current']['version'], '0.2')

    def test_nexus_metadata_cannot_inject_paths_or_change_host(self):
        manifest, _ = self.nexus_fixture()
        for key, value in [('groupId', '../123'), ('modId', 'qdbCxL2mS'),
                           ('url', 'https://example.com/games/eldenring/mods/201')]:
            altered = copy.deepcopy(manifest)
            altered['nexus'][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                workflow.validate_nexus_metadata(altered)

    def test_nexus_get_keeps_route_and_result_guards_with_shared_transport(self):
        import nexus_automation
        with mock.patch.object(nexus_automation, 'read', return_value={'mod_files': []}) as read:
            self.assertEqual(workflow.nexus_get('/mods/123/files'), {'mod_files': []})
            read.assert_called_once_with(workflow.ROOT, '/mods/123/files')
            read.reset_mock()
            with self.assertRaisesRegex(ValueError, 'Unsupported Nexus read path'):
                workflow.nexus_get('/mods/123/changelogs')
            read.assert_not_called()
        with mock.patch.object(nexus_automation, 'read', return_value=[]):
            with self.assertRaisesRegex(ValueError, 'Unexpected Nexus response'):
                workflow.nexus_get('/mods/123/files')
        with mock.patch.dict(nexus_automation.os.environ, {'NEXUS_API_KEY': ''}), mock.patch.object(nexus_automation.subprocess, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'NEXUS_API_KEY'):
                nexus_automation.read(workflow.ROOT, '/mods/123/files')
            run.assert_not_called()
        with mock.patch.dict(nexus_automation.os.environ, {'NEXUS_API_KEY': 'fixture-secret'}), mock.patch.object(nexus_automation, 'tool_root', return_value=workflow.ROOT), mock.patch.object(nexus_automation.subprocess, 'run', side_effect=nexus_automation.subprocess.CalledProcessError(1, ['node'], stderr='fixture-secret')):
            with self.assertRaisesRegex(ValueError, 'Nexus read failed') as caught:
                nexus_automation.read(workflow.ROOT, '/mods/123/files')
            self.assertNotIn('fixture-secret', str(caught.exception))


if __name__ == '__main__':
    unittest.main()
