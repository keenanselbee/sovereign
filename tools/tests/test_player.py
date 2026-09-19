from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import player_workflow as player
import asset_workflow as assets


class PlayerTests(unittest.TestCase):
    def setUp(self):
        scratch = player.core.ROOT / '.codex-temp/tests'
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def test_xml_comparison_preserves_values_order_and_reference_sharing(self):
        a = self.root / 'a.xml'; b = self.root / 'b.xml'
        a.write_text('<root><object id="a" kind="X"><ref>object2</ref><ref>object2</ref></object></root>')
        b.write_text('<root>\n <object kind="X" id="a">\n<ref>object2</ref><ref>object2</ref>\n</object>\n</root>')
        self.assertEqual(player.xml_fingerprint(a), player.xml_fingerprint(b))
        b.write_text('<root><object id="a" kind="X"><ref>object2</ref><ref>object3</ref></object></root>')
        self.assertNotEqual(player.xml_fingerprint(a), player.xml_fingerprint(b))

    def test_packing_metadata_rejects_output_redirect_and_escaping_member(self):
        path = self.root / '_witchy-bnd4.xml'
        for xml in ('<bnd4><filename>../elsewhere</filename></bnd4>',
                    '<bnd4><filename>c0000.behbnd.dcx</filename><files><file><path>../x.hkx</path></file></files></bnd4>'):
            path.write_text(xml)
            with self.assertRaises(ValueError):
                player.packing_metadata(self.root, path.name, 'c0000.behbnd.dcx')

    def test_cached_native_qualification_allows_hks_only_changes(self):
        data = {'schemaVersion': 1, 'runtimeRoot': 'mod', 'groups': [], 'sources': []}
        assets.save(self.root / 'asset-catalog.json', data)
        settings = {'roots': {'animations': str(self.root / 'editor')}}
        proof = {'kind': 'player-roundtrip', 'status': 'qualified', 'sourceRole': 'repo',
                 'catalogHash': assets.fingerprint(data), 'settingsHash': assets.fingerprint(settings),
                 'files': {'script.hks': 'old', 'graph.hkx': 'graph', 'names.txt': 'names'},
                 'tools': {'native': 'tool'}}
        path = self.root / '.codex-temp/player-qualifications/prior/receipt.json'
        path.parent.mkdir(parents=True)
        assets.save(path, proof)
        current = {**proof['files'], 'script.hks': 'new'}
        self.assertEqual(player.cached_qualification(self.root, settings, 'repo', current,
                         proof['tools'], {'script.hks'})[0], path)
        for inputs, tools, role in [({**current, 'graph.hkx': 'changed'}, proof['tools'], 'repo'),
                                   ({**current, 'names.txt': 'changed'}, proof['tools'], 'repo'),
                                   ({**current, 'new.tae': 'new'}, proof['tools'], 'repo'),
                                   (current, {'native': 'updated'}, 'repo'),
                                   (current, proof['tools'], 'editor')]:
            self.assertIsNone(player.cached_qualification(self.root, settings, role, inputs, tools, {'script.hks'}))


if __name__ == '__main__':
    unittest.main()
