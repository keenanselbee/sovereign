"""Cross-source contracts for the tome manifest and generated event."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import profane_tomes as tomes


class ProfaneTomeTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(tomes.MANIFEST.read_text(encoding='utf-8'))

    def test_items_and_stock_bits_do_not_alias(self):
        tomes.validate_flags(self.data)
        items, flags = [], []
        for book in self.data['books']:
            self.assertEqual(len(book['variants']), 8)
            items.extend([book['receiptGoods'], *book['variants']])
            flags.extend([book['collectedFlag'], book['availableFlag']])
            # Reserve ten bits even though a one-copy shop needs fewer.
            flags.extend(range(book['stockFlag'], book['stockFlag'] + 10))
        flags.append(self.data['hatFlag'])
        self.assertEqual(len(items), len(set(items)))
        self.assertEqual(len(flags), len(set(flags)))

    def test_invalid_temporary_and_foreign_flags_are_rejected(self):
        for flag in [1055421200, 1055423200, 1055426200, 1055422200, 1055425200, 1055434200]:
            with self.subTest(flag=flag):
                self.data['books'][0]['collectedFlag'] = flag
                with self.assertRaisesRegex(ValueError, 'valid saved'):
                    tomes.render_event(self.data)
                with self.assertRaisesRegex(ValueError, 'valid saved'):
                    tomes.candidates(self.data, {}, {})

    def test_stock_alignment_and_occupied_bits_are_checked(self):
        self.data['books'][0]['stockFlag'] += 1
        with self.assertRaisesRegex(ValueError, 'multiple of ten'):
            tomes.validate_flags(self.data)
        self.data['books'][0]['stockFlag'] -= 1
        self.data['hatFlag'] = self.data['books'][0]['stockFlag'] + 9
        with self.assertRaisesRegex(ValueError, 'Overlapping'):
            tomes.validate_flags(self.data)

    def test_existing_farums_remain_exclusive_and_kale_price_is_500(self):
        books = self.data['books']
        self.assertEqual(books[0]['shops'], [{'row': 100521, 'price': 500}])
        for index, goods, lot in [(5, 8870, 13000830), (7, 8871, 13000120)]:
            self.assertEqual(books[index]['receiptGoods'], goods)
            self.assertEqual(books[index]['mapLot'], lot)
            self.assertEqual(books[index]['shops'], [])

    def test_saved_controller_matches_manifest_and_regeneration_is_idempotent(self):
        source = (tomes.ROOT / 'src/events/common.emevd.dcx.js').read_text(encoding='utf-8')
        self.assertIn(tomes.render_event(self.data), source)
        self.assertEqual(tomes.event_candidate(source, self.data), source)
        self.assertEqual(source.count('$InitializeEvent(0, 5750140);'), 1)


if __name__ == '__main__':
    unittest.main()
