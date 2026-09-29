"""Rebase two 21.5:9 GFX screens on the audited current game files.

Requires JPEXS Free Flash Decompiler 26.3 and the exact source assets pinned below.
This builds an isolated replacement package; it never edits the Vortex source.
"""

import argparse
import hashlib
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


INPUT_HASHES = {
    '04_200_chrmake_basechrselect': (
        '11e383b4972fd06301ff97a3623608697f94d0071160d54af3fd0ef35d9062ef',
        '9eecb05e4c7f0b9f8e67f740abc1d921b096b4f9071ea98e6b52151116c28627',
    ),
    '02_120_worldmap': (
        '75ad2435032b59c7db1c25d3f16d111ad6623ca93fed0623ab824cd08af50446',
        'c4eb5f1ceee7ab7de4300975481205016c522d3e4fe9d6f56490f60d675a9884',
    ),
}

# The sprite IDs differ in the class selector because the native game added images.
# Use a checked sprite identity for each matrix and retain all native definitions.
MATRICES = {
    '04_200_chrmake_basechrselect': [
        ((142, 0), (145, 0)),
        ((142, 1), (145, 1)),
    ],
    '02_120_worldmap': [
        ((None, 191), (None, 191)),
        ((210, 0), (210, 0)),
        *[((241, i), (241, i)) for i in (0, 5, 6, 7, 8, 9, 11)],
        *[((None, i), (None, i)) for i in (248, 252, 254, 258)],
    ],
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix(root, location):
    sprite_id, index = location
    tags = list(root.find('tags'))
    if sprite_id is None:
        tag = tags[index]
    else:
        matching = [tag for tag in tags if tag.get('type') == 'DefineSpriteTag' and tag.get('spriteId') == str(sprite_id)]
        if len(matching) != 1:
            raise ValueError(f'Expected one sprite {sprite_id}, found {len(matching)}')
        tag = list(matching[0].find('subTags'))[index]
    if tag.get('type') != 'PlaceObject2Tag':
        raise ValueError(f'Expected placement at {location}: {tag.attrib}')
    result = tag.find('matrix')
    if result is None:
        raise ValueError(f'Missing matrix at {location}')
    return result


def run_ffdec(jar, command, source, target):
    subprocess.run(['java', '-jar', str(jar), command, str(source), str(target)], check=True)
    if not target.is_file():
        raise RuntimeError(f'FFDec did not produce {target}')


def semantic_tree(element):
    # FFDec recalculates storage bit widths and ABC file offsets on XML import.
    # These fields do not affect decoded matrices or bytecode contents.
    attributes = tuple(sorted((key, value) for key, value in element.attrib.items()
                              if key not in {'fileOffset', 'nRotateBits', 'nScaleBits', 'nTranslateBits'}))
    return (element.tag, attributes, (element.text or '').strip(),
            tuple(semantic_tree(child) for child in element))


def build(args):
    source_files = sorted(args.ultrawide.rglob('*.gfx'))
    if len(source_files) != 50:
        raise ValueError(f'Expected 50 original GFX files, found {len(source_files)}')
    if args.output.exists():
        raise FileExistsError(f'Output already exists: {args.output}')
    if not args.ffdec.is_file():
        raise FileNotFoundError(args.ffdec)

    with tempfile.TemporaryDirectory(prefix='ultrawide-compat-', dir=args.scratch) as temporary:
        work = Path(temporary)
        replacements = {}
        for stem, (native_hash, old_hash) in INPUT_HASHES.items():
            native = args.native / f'{stem}.swf'
            old = args.ultrawide / 'menu' / f'{stem}.gfx'
            if sha256(native) != native_hash or sha256(old) != old_hash:
                raise ValueError(f'Input hash changed: {stem}')
            native_xml, old_xml = work / f'{stem}-native.xml', work / f'{stem}-old.xml'
            run_ffdec(args.ffdec, '-swf2xml', native, native_xml)
            run_ffdec(args.ffdec, '-swf2xml', old, old_xml)
            native_tree, old_tree = ET.parse(native_xml), ET.parse(old_xml)
            native_root, old_root = native_tree.getroot(), old_tree.getroot()

            if stem.startswith('04_200'):
                images = {tag.get('exportName') for tag in native_root.find('tags') if tag.get('type') == 'DefineExternalImage2'}
                if not {'MENU_Ch_11', 'MENU_Ch_12'} <= images:
                    raise ValueError('Current character portraits are missing')
            else:
                map_sprite = [tag for tag in native_root.find('tags') if tag.get('spriteId') == '171']
                if len(map_sprite) != 1 or map_sprite[0].get('frameCount') != '348':
                    raise ValueError('Current world map sprite is missing its 348-frame state')

            changed = 0
            for native_location, old_location in MATRICES[stem]:
                current, ultrawide = matrix(native_root, native_location), matrix(old_root, old_location)
                if current.attrib == ultrawide.attrib:
                    raise ValueError(f'Expected a layout difference at {stem} {native_location}')
                current.attrib.clear()
                current.attrib.update(ultrawide.attrib)
                changed += 1
            native_tree.write(native_xml, encoding='utf-8', xml_declaration=True)
            replacement = work / f'{stem}.gfx'
            run_ffdec(args.ffdec, '-xml2swf', native_xml, replacement)
            if replacement.read_bytes()[:3] != b'GFX':
                raise ValueError(f'Rebuilt asset is not GFX: {stem}')
            rebuilt_xml = work / f'{stem}-rebuilt.xml'
            run_ffdec(args.ffdec, '-swf2xml', replacement, rebuilt_xml)
            if semantic_tree(native_root) != semantic_tree(ET.parse(rebuilt_xml).getroot()):
                raise ValueError(f'Rebuilt {stem} differs beyond intended placements')
            replacements[stem] = replacement
            print(f'{stem}: {changed} ultrawide placement matrices on current game base')

        args.output.mkdir(parents=True)
        for source in source_files:
            target = args.output / source.relative_to(args.ultrawide)
            target.parent.mkdir(parents=True, exist_ok=True)
            replacement = replacements.get(source.stem)
            shutil.copyfile(replacement or source, target)
        print(f'Wrote {len(source_files)} files to {args.output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', type=Path, required=True, help='Audited extracted native .swf directory')
    parser.add_argument('--ultrawide', type=Path, required=True, help='Original ultrawide mod root')
    parser.add_argument('--ffdec', type=Path, required=True, help='FFDec 26.3 jar')
    parser.add_argument('--scratch', type=Path, required=True, help='Existing scratch directory')
    parser.add_argument('--output', type=Path, required=True, help='New isolated mod root')
    build(parser.parse_args())
