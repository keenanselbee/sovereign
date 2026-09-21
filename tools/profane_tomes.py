"""Generate reviewed tome candidates; never accept, deploy, or edit an editor workspace."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'src/tomes/profane-tomes.json'
BEGIN = '// BEGIN GENERATED PROFANE TOMES'
END = '// END GENERATED PROFANE TOMES'


def validate_flags(data):
    """Tomes require saved state within Sovereign's registered flag namespace."""
    occupied = set()
    allocations = [(data['hatFlag'], 1)]
    for book in data['books']:
        if book['stockFlag'] % 10:
            raise ValueError('Tome stock flags must start at a multiple of ten')
        allocations.extend([(book['collectedFlag'], 1), (book['availableFlag'], 1),
                            (book['stockFlag'], 10)])
    for start, width in allocations:
        for flag in range(start, start + width):
            if not 1055420000 <= flag <= 1055429999 or (flag // 1000) % 10 not in (0, 4, 7, 8, 9):
                raise ValueError(f'Tome flag must use a valid saved Sovereign block: {flag}')
            if flag in occupied:
                raise ValueError(f'Overlapping tome flag allocation: {flag}')
            occupied.add(flag)


def owned(ids, kind='Goods', storage=False):
    fn = 'PlayerHasItemIncludingBBox' if storage else 'PlayerHasItem'
    return ' || '.join(f'{fn}(ItemType.{kind}, {i})' for i in ids)


def render_event(data):
    validate_flags(data)
    books = data['books']
    lines = [BEGIN, '// Authored text and allocations: src/tomes/profane-tomes.json.',
             '// One host controller serializes discovery numbers. Grant before removing receipts.',
             f"$Event({data['eventId']}, Restart, function() {{",
             '    EndIf(!PlayerIsInOwnWorld());']
    for book in books:
        ids = [book['receiptGoods'], *book['variants']]
        lines += [f"    // {book['title']}", f"    if ({owned(ids)}) {{",
                  f"        SetEventFlagID({book['collectedFlag']}, ON);",
                  f"        SetEventFlagID({book['availableFlag']}, OFF);", '    } else {',
                  f"        SetEventFlagID({book['availableFlag']}, OFF);",
                  f"        if (!EventFlag({book['collectedFlag']})) {{",
                  f"            SetEventFlagID({book['availableFlag']}, ON);", '        }', '    }']
        lines += [f"    if (PlayerHasItem(ItemType.Goods, {book['receiptGoods']})) {{",
                  f"        if (!({owned(book['variants'])})) {{"]
        for n, variant in enumerate(book['variants']):
            occupied = owned([b['variants'][n] for b in books])
            lines += [f"            if (!({occupied})) {{",
                      f'                AwardItemLot({variant * 10});',
                      f'                WaitFor(PlayerHasItem(ItemType.Goods, {variant}));',
                      f"                RemoveItemFromPlayer(ItemType.Goods, {book['receiptGoods']}, 1);",
                      '                RestartEvent();', '            }',
                      '            WaitFor(PlayerIsInOwnWorld());']
        lines += ['        }', f"        if ({owned(book['variants'])}) {{",
                  f"            RemoveItemFromPlayer(ItemType.Goods, {book['receiptGoods']}, 1);",
                  '        }', '    }', '    WaitFor(PlayerIsInOwnWorld());']
    elder = books[5]
    final = books[7]
    lines += [f"    if ({owned([elder['receiptGoods'], *elder['variants']])}) {{",
              '        SetEventFlagID(1055420240, ON);', '    }',
              f"    if ({owned([final['receiptGoods'], *final['variants']])}) {{",
              '        SetEventFlagID(1055420245, ON);',
              '    }',
              '    if (PlayerHasItemIncludingBBox(ItemType.Armor, 110000)) {',
              f"        SetEventFlagID({data['hatFlag']}, ON);", '    }',
              '    if (PlayerHasItemIncludingBBox(ItemType.Weapon, 34200000)) {',
              '        SetEventFlagID(1055420220, ON);', '    }',
              '    WaitFixedTimeSeconds(0.25);', '    RestartEvent();', '});', END]
    # Reuse one explicit OR group. Large auto-generated expressions otherwise exhaust
    # DarkScript's finite temporary groups, even across conditional waits.
    checked = []
    for line in lines:
        if 'if (' in line and ' || ' in line:
            indent = line[:len(line) - len(line.lstrip())]
            expression = line.strip()[4:-3]
            negative = expression.startswith('!(')
            if negative:
                expression = expression[2:-1]
            checked.append(indent + 'WaitFor(PlayerIsInOwnWorld());')
            for part in expression.split(' || '):
                checked.append(indent + 'tomeCheck |= ' + part + ';')
            checked.append(indent + ('if (!tomeCheck) {' if negative else 'if (tomeCheck) {'))
        else:
            checked.append(line)
    return '\n'.join(checked)


def event_candidate(source, data):
    if BEGIN in source:
        a, b = source.index(BEGIN), source.index(END) + len(END)
        source = source[:a] + render_event(data) + source[b:]
    else:
        source = source.rstrip() + '\n\n' + render_event(data) + '\n'
        anchor = '    $InitializeEvent(0, 5750000);'
        assert source.count(anchor) == 1
        source = source.replace(anchor, anchor + f"\n    $InitializeEvent(0, {data['eventId']});", 1)
        for subject, event_id, flag in [(5, 5750035, 1055420240), (7, 5750036, 1055420245)]:
            start = source.index(f'$Event({event_id},')
            end = source.index('\n});', start)
            segment = source[start:end]
            book = data['books'][subject]
            wait = f'    WaitFor(EventFlag({flag}));'
            assert segment.count(wait) == 1
            # Retained books are the source of recipe knowledge, including in NG+.
            segment = segment.replace(wait, f"    WaitFor({owned([book['receiptGoods'], *book['variants']])});")
            segment = segment.replace('PlayerHasItem(ItemType.Weapon,', 'PlayerHasItemIncludingBBox(ItemType.Weapon,')
            # Already-crafted equipment must not leave a stale recipe available on load/NG+.
            segment = segment.replace('        EndEvent();', f'        SetEventFlagID({flag + 1}, OFF);\n        EndEvent();', 1)
            segment = segment.replace('    WaitFor(', f'    SetEventFlagID({flag + 1}, OFF);\n    WaitFor(', 1)
            source = source[:start] + segment + source[end:]
    return source


def candidates(data, baseline, texts):
    validate_flags(data)
    tables = baseline['Tables']
    patch = []
    fmg = []

    def change(table, identity, edits, clone=None, name=None):
        rows = tables[table]
        if clone is not None:
            if str(identity) in rows:
                raise ValueError(f'Allocated row exists: {table}:{identity}')
            row = rows[str(clone)]
        else:
            row = rows[str(identity)]
        patch.append(dict(table=table, id=identity, clone=clone, name=name,
                          before={k: row['Cells'][k] for k in edits}, after=edits))

    def text(identity, title, caption):
        for file, value in [('GoodsName.fmg', title), ('GoodsInfo.fmg', 'Acquire forbidden knowledge'),
                            ('GoodsCaption.fmg', caption)]:
            entries = [r for r in texts[file] if r['ID'] == identity]
            if len(entries) > 1:
                raise ValueError('Duplicate existing FMG entry')
            fmg.append(dict(file=file, id=identity, before=entries[0]['Text'] if entries else None,
                            beforeMissing=not entries, after=value))

    for book in data['books']:
        identity = book['receiptGoods']
        base_edits = dict(isRemoveItem_forGameClear=0, showDialogCondType=0, showLogCondType=0)
        change('EquipParamGoods', identity, base_edits,
               clone=8870 if identity not in (8870, 8871) else None,
               name=f"[Sovereign] Profane Tome receipt - {book['title']}")
        text(identity, 'Profane Tome: ' + book['title'], book['caption'])
        for n, variant in enumerate(book['variants'], 1):
            title = f"Profane Tome [{n}]: {book['title']}"
            change('EquipParamGoods', variant,
                   dict(isRemoveItem_forGameClear=0, sortId=206100 + n * 10 + book['subject']),
                   clone=8870, name='[Sovereign] ' + title)
            text(variant, title, book['caption'])
            # Consecutive lot IDs form one award group. Leave a gap after every book.
            change('ItemLotParam_map', variant * 10,
                   dict(lotItemId01=variant, getItemFlagId=0, GameClearOffset=-1),
                   clone=13000830, name='[Sovereign] ' + title)
        for shop in book['shops']:
            change('ShopLineupParam', shop['row'],
                   dict(equipId=identity, value=shop['price'], nameMsgId=-1,
                        eventFlag_forStock=book['stockFlag'], eventFlag_forRelease=book['availableFlag']),
                   clone=100500, name=f"[Sovereign] {book['title']}")
        if book['mapLot'] and identity not in (8870, 8871):
            change('ItemLotParam_map', book['mapLot'],
                   dict(lotItemId01=identity, lotItemNum01=1, getItemFlagId=book['collectedFlag']),
                   name=f"[Sovereign] {book['title']} (Arteria Leaf replacement)")
    fire = data['books'][4]
    # A separate appended lot leaves every original Fire Monk equipment/material roll intact.
    change('ItemLotParam_enemy', data['fireMonkLot'],
           dict(lotItemId01=fire['receiptGoods'], lotItemCategory01=1, lotItemNum01=1,
                lotItemBasePoint01=50, lotItemBasePoint02=950,
                getItemFlagId=fire['collectedFlag'], enableLuck01=0),
           clone=524095715, name='[Sovereign] Fire Remembered - 5% once-only')
    change('ItemLotParam_enemy', 450542001, dict(getItemFlagId08=data['hatFlag']))
    return patch, fmg


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--texts', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to((ROOT / '.codex-temp').resolve()):
        raise ValueError('Candidates must be inside repository .codex-temp')
    output.mkdir(parents=True, exist_ok=False)
    data = json.loads(MANIFEST.read_text())
    baseline = json.loads(args.baseline.read_text(encoding='utf-8-sig'))
    runtime = ROOT / 'mod/regulation.bin'
    if hashlib.sha256(runtime.read_bytes()).hexdigest().lower() != baseline['Hash'].lower():
        raise ValueError('Regulation export is stale')
    patch, fmg = candidates(data, baseline, json.loads(args.texts.read_text(encoding='utf-8-sig')))
    for name, value in [('params.json', dict(sourceHash=baseline['Hash'], changes=patch)), ('text.json', fmg)]:
        (output / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    source = (ROOT / 'src/events/common.emevd.dcx.js').read_text(encoding='utf-8-sig')
    (output / 'common.emevd.dcx.js').write_text(event_candidate(source, data), encoding='utf-8')
    print(output)


if __name__ == '__main__':
    main()
