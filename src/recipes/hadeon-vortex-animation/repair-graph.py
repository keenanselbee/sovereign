"""Select the four private TAE timelines in the accepted c2500 graph."""

import copy
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def field(obj, name):
    result = obj.find(f'./record/field[@name="{name}"]')
    if result is None:
        raise ValueError(f'{obj.get("id")}: missing {name}')
    return result


def scalar(obj, name, kind):
    result = field(obj, name).find(kind)
    if result is None:
        raise ValueError(f'{obj.get("id")}: missing {name}/{kind}')
    return result


def main(source, output):
    root = ET.parse(source).getroot()
    objects = {obj.get('id'): obj for obj in root.findall('object')}
    if len(objects) != len(root.findall('object')):
        raise ValueError('Duplicate graph object ID')
    graph_data = next(obj for obj in objects.values()
                      if obj.find('./record/field[@name="animationNames"]') is not None)
    names = field(graph_data, 'animationNames').find('array')
    if names is None or len(names) != 278 or not names[74].get('value', '').endswith('a000_003028.hkx'):
        raise ValueError('Native 3028 motion index changed')
    by_name = {scalar(obj, 'name', 'string').get('value'): obj
               for obj in objects.values()
               if obj.find('./record/field[@name="name"]/string') is not None}
    for anim in range(3030, 3034):
        state = by_name[f'Attack{anim}']
        selector = objects[scalar(state, 'generator', 'pointer').get('id')]
        clip = objects[field(selector, 'generators').find('array/pointer').get('id')]
        if scalar(selector, 'name', 'string').get('value') != f'Attack{anim}_CMSG' \
                or scalar(selector, 'animId', 'integer').get('value') != str(anim) \
                or scalar(clip, 'name', 'string').get('value') != f'a000_003028_Hadeon{anim}' \
                or scalar(clip, 'animationName', 'string').get('value') != 'a000_003028' \
                or scalar(clip, 'animationInternalId', 'integer').get('value') != '74':
            raise ValueError(f'Private route {anim} is not the reviewed graph')
        scalar(clip, 'animationName', 'string').set('value', f'a000_{anim:06d}')
    if Path(output).exists():
        raise FileExistsError(output)
    ET.indent(root, space='  ')
    ET.ElementTree(root).write(output, encoding='utf-8', xml_declaration=True)
    print(f'Updated four private clip timeline names in {output}')


def verify(source, readback, receipt):
    before = ET.parse(source).getroot().findall('object')
    after = ET.parse(readback).getroot().findall('object')
    if len(before) != len(after) or len(before) != 2280:
        raise ValueError('Graph object count changed')
    mapping = {a.get('id'): b.get('id') for a, b in zip(before, after)}
    reverse = {b: a for a, b in mapping.items()}
    if len(reverse) != len(mapping):
        raise ValueError('Graph object mapping is ambiguous')
    changed = []
    for original, rebuilt in zip(before, after):
        a, b = copy.deepcopy(original), copy.deepcopy(rebuilt)
        if a.get('typeid') != b.get('typeid'):
            raise ValueError(f'{a.get("id")}: graph type changed')
        b.set('id', a.get('id'))
        for pointer in b.iter('pointer'):
            target = pointer.get('id')
            if target in reverse:
                pointer.set('id', reverse[target])
        name = scalar(a, 'name', 'string').get('value') if a.find('./record/field[@name="name"]/string') is not None else None
        if name and name.startswith('a000_003028_Hadeon'):
            anim = int(name.removeprefix('a000_003028_Hadeon'))
            if anim not in range(3030, 3034) or scalar(a, 'animationName', 'string').get('value') != 'a000_003028' \
                    or scalar(b, 'animationName', 'string').get('value') != f'a000_{anim:06d}':
                raise ValueError(f'{name}: unexpected timeline mapping')
            scalar(b, 'animationName', 'string').set('value', 'a000_003028')
            changed.append(anim)
        for obj in (a, b):
            for node in obj.iter():
                if node.text is not None and not node.text.strip():
                    node.text = None
                if node.tail is not None and not node.tail.strip():
                    node.tail = None
        if ET.tostring(a) != ET.tostring(b):
            raise ValueError(f'{a.get("id")}: unrelated graph content changed')
    if sorted(changed) != list(range(3030, 3034)):
        raise ValueError('Expected exactly four private clip changes')
    path = Path(receipt)
    if path.exists():
        raise FileExistsError(path)
    path.write_text(json.dumps({
        'sourceSha256': hashlib.sha256(Path(source).read_bytes()).hexdigest().upper(),
        'readbackSha256': hashlib.sha256(Path(readback).read_bytes()).hexdigest().upper(),
        'preservedGraphObjects': len(before),
        'changedClipTimelineIds': changed,
        'preservedAllOtherGraphFields': True,
        'gameTested': False,
    }, indent=2) + '\n', encoding='utf-8')
    print('Verified 2,280 graph objects; only four private clip timeline IDs changed')


if __name__ == '__main__':
    if len(sys.argv) == 5 and sys.argv[1] == '--verify':
        verify(*sys.argv[2:])
    elif len(sys.argv) == 3:
        main(*sys.argv[1:])
    else:
        raise SystemExit('repair-graph.py accepted-graph.xml candidate-graph.xml | --verify accepted-graph.xml readback.xml receipt.json')
