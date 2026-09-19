import copy
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import format_workflow as formats


class FormatTests(unittest.TestCase):
    def setUp(self):
        self.baseline = {'Files': [{'Name': r'N:\msg\Test.fmg', 'ID': 1, 'Flags': 2,
            'Payload': {'Entries': [{'ID': i, 'Text': text} for i, text in enumerate(
                [None, '', ' ', '%null%', '\u96ea\nline'])], 'Version': 2}}], 'Version': 'binder'}

    def test_exact_text_values_and_unedited_metadata_preserved(self):
        old = copy.deepcopy(self.baseline)
        patch = [{'file': 'Test.fmg', 'id': 3, 'before': '%null%', 'after': None}]
        result = formats.expected_text(self.baseline, patch)
        self.assertEqual(self.baseline, old)
        old['Files'][0]['Payload']['Entries'][3]['Text'] = None
        self.assertEqual(result, old)
        self.assertNotEqual(result['Files'][0]['Payload']['Entries'][1]['Text'], None)

    def test_wrong_old_value_duplicate_ids_and_implicit_null_rejected(self):
        for patch in ([{'file': 'Test.fmg', 'id': 0, 'before': '', 'after': 'x'}],
                      [{'file': 'Test.fmg', 'id': 0, 'after': 'x'}],
                      [{'file': 'Test.fmg', 'id': 0, 'before': None, 'after': 123}]):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                formats.expected_text(self.baseline, patch)
        self.baseline['Files'][0]['Payload']['Entries'].append({'ID': 3, 'Text': '%null%'})
        with self.assertRaisesRegex(ValueError, 'differs'):
            formats.expected_text(self.baseline, [{'file': 'Test.fmg', 'id': 3, 'before': '%null%', 'after': ''}])

    def test_added_text_requires_absence_and_does_not_replace_existing_null(self):
        change = {'file': 'Test.fmg', 'id': 8, 'before': None, 'beforeMissing': True, 'after': 'New hint'}
        result = formats.expected_text(self.baseline, [change])
        self.assertEqual(result['Files'][0]['Payload']['Entries'][-1], {'ID': 8, 'Text': 'New hint'})
        self.assertEqual(result['Files'][0]['Payload']['Entries'][:-1], self.baseline['Files'][0]['Payload']['Entries'])
        with self.assertRaisesRegex(ValueError, 'absent'):
            formats.expected_text(self.baseline, [{**change, 'id': 0}])
        with self.assertRaisesRegex(ValueError, 'differs'):
            formats.expected_text(self.baseline, [{**change, 'beforeMissing': False}])

    def test_dialogue_original_and_baseline_are_pinned_and_contained(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 't1.py'
            source.write_text('DSL source')
            (root / 'original.esd').write_bytes(b'original ESD')
            (root / 'baseline.txt').write_text('original DSL')
            data = {'member': 't1.esd', 'groups': [1], 'original': 'original.esd', 'baseline': 'baseline.txt',
                    'originalHash': formats.assets.checksum(root / 'original.esd'),
                    'baselineHash': formats.assets.checksum(root / 'baseline.txt')}
            manifest = source.with_suffix('.preserve.json')
            formats.assets.save(manifest, data)
            self.assertEqual(formats.dialogue_preservation(source)[0], manifest)
            (root / 'original.esd').write_bytes(b'later edit')
            with self.assertRaisesRegex(ValueError, 'changed'):
                formats.dialogue_preservation(source)
            data['original'] = '../outside.esd'
            formats.assets.save(manifest, data)
            with self.assertRaisesRegex(ValueError, 'direct companion'):
                formats.dialogue_preservation(source)

    def test_dialogue_reports_header_changes_without_hiding_them(self):
        before = {'Files': [{'Name': 't1.esd', 'ID': 1, 'Payload': {
            'Unk70': 7, 'StateGroups': {'1': {'0': {'EntryCommands': [1, 2]}}}}}], 'Version': 'x'}
        after = copy.deepcopy(before)
        after['Files'][0]['Payload']['Unk70'] = 9
        result = formats.compare_dialogue(before, after)
        self.assertFalse(result['equal'])
        self.assertEqual(result['members'][0]['metadataFields'], ['Unk70'])
        self.assertEqual(result['members'][0]['changedStateGroups'], [])
        after['Files'][0]['Payload']['StateGroups']['1']['0']['EntryCommands'].reverse()
        self.assertEqual(formats.compare_dialogue(before, after)['members'][0]['changedStateGroups'], ['1'])

    def test_dialogue_member_order_and_binder_metadata_are_checked(self):
        before = {'Files': [{'Name': 't1.esd', 'ID': 1, 'Payload': {'StateGroups': {}}}], 'Version': 'x'}
        after = copy.deepcopy(before)
        after['Files'][0]['ID'] = 2
        after['Version'] = 'y'
        result = formats.compare_dialogue(before, after)
        self.assertEqual(result['binderMetadataFields'], ['Version'])
        self.assertTrue(result['members'][0]['memberIdentityChanged'])

    def test_dialogue_command_selects_matching_header_and_one_explicit_source(self):
        command = formats.dialogue_command(Path('esdtool.exe'), Path('input/m00.talkesdbnd.dcx'),
                                           Path('source/t000001000.py'), Path('output/m00.talkesdbnd.dcx'))
        self.assertEqual(command, [Path('esdtool.exe'), '-er', '-noannotate', '-i', Path('input/m00.talkesdbnd.dcx'),
                                  '-f', 't000001000', '-i', Path('source/t000001000.py'), '-writebndfile',
                                  Path('output/m00.talkesdbnd.dcx')])


if __name__ == '__main__':
    unittest.main()
