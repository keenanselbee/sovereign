"""Verify native readback changes only the four private attack routes."""

import copy
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def field(obj, name):
    prefix = './' if obj.tag == 'record' else './record/'
    return obj.find(f'{prefix}field[@name="{name}"]')


def clean(element):
    if element.text is not None and not element.text.strip():
        element.text = None
    if element.tail is not None and not element.tail.strip():
        element.tail = None
    for child in element:
        clean(child)


def main(original, readback, hks_path, event_names_path, state_names_path,
         receipt_path=None):
    old = ET.parse(original).getroot()
    new = ET.parse(readback).getroot()
    old_objects = old.findall('object')
    new_objects = new.findall('object')
    private_names = {
        name for anim in range(3030, 3034)
        for name in (f'Attack{anim}', f'Attack{anim}_CMSG', f'a000_003028_Hadeon{anim}')
    }
    def name(obj):
        node = field(obj, 'name')
        item = node.find('string') if node is not None else None
        return item.get('value') if item is not None else None
    additions = [obj for obj in new_objects if name(obj) in private_names]
    if len(additions) != 12 or {name(obj) for obj in additions} != private_names:
        raise ValueError('Readback is missing a private state, selector or clip')
    filtered = [obj for obj in new_objects if obj not in additions]
    if len(filtered) != len(old_objects):
        raise ValueError('Unrelated graph object count changed')
    id_map = {before.get('id'): after.get('id') for before, after in zip(old_objects, filtered)}
    reverse = {after: before for before, after in id_map.items()}
    if len(reverse) != len(id_map):
        raise ValueError('Graph object mapping is ambiguous')
    named_additions = {name(obj): obj for obj in additions}
    original_objects = {obj.get('id'): obj for obj in old_objects}
    names = [item.get('value') for item in field(original_objects['object8'], 'eventNames').find('array').findall('string')]
    infos = field(original_objects['object4'], 'eventInfos').find('array').findall('record')
    if len(names) != len(infos) or len(names) != 1366:
        raise ValueError('Native event names and eventInfos are misaligned')
    hks = Path(hks_path).read_bytes().decode('latin-1')
    event_registry = Path(event_names_path).read_bytes().decode('latin-1')
    state_registry = Path(state_names_path).read_bytes().decode('latin-1')
    machine = filtered[old_objects.index(next(obj for obj in old_objects if obj.get('id') == 'object314'))]
    state_array = field(machine, 'states').find('array')
    transition_object = filtered[old_objects.index(next(obj for obj in old_objects if obj.get('id') == 'object378'))]
    transition_array = field(transition_object, 'transitions').find('array')
    for index, anim in enumerate(range(3030, 3034)):
        state = named_additions[f'Attack{anim}']
        selector = named_additions[f'Attack{anim}_CMSG']
        clip = named_additions[f'a000_003028_Hadeon{anim}']
        if field(state, 'stateId').find('integer').get('value') != str(57 + index):
            raise ValueError(f'{anim}: wrong state ID')
        if field(state, 'generator').find('pointer').get('id') != selector.get('id'):
            raise ValueError(f'{anim}: state misses selector')
        if field(selector, 'animId').find('integer').get('value') != str(anim):
            raise ValueError(f'{anim}: selector TAE ID changed')
        if field(selector, 'userData').find('integer').get('value') != str(18546718 + index):
            raise ValueError(f'{anim}: selector userData collision')
        if field(selector, 'generators').find('array').find('pointer').get('id') != clip.get('id'):
            raise ValueError(f'{anim}: selector misses clip')
        if field(clip, 'animationName').find('string').get('value') != f'a000_{anim:06d}':
            raise ValueError(f'{anim}: private TAE timeline is not selected')
        if field(clip, 'animationInternalId').find('integer').get('value') != field(original_objects['object717'], 'animationInternalId').find('integer').get('value'):
            raise ValueError(f'{anim}: native clip binding changed')
        if state_array[-4 + index].get('id') != state.get('id'):
            raise ValueError(f'{anim}: attack machine misses private state')
        transition = transition_array[-4 + index]
        if field(transition, 'eventId').find('integer').get('value') != str(198 + 2 * index) \
                or field(transition, 'toStateId').find('integer').get('value') != str(57 + index):
            raise ValueError(f'{anim}: attack event transition changed')
        slot = 198 + 2 * index
        if names[slot:slot + 2] != [f'W_Attack{anim}', f'W_Event{anim}']:
            raise ValueError(f'{anim}: native event names missing')
        if any(field(info, 'flags').find('integer').get('value') != '0' for info in infos[slot:slot + 2]):
            raise ValueError(f'{anim}: native eventInfo changed')
        if not re.search(rf'function Attack{anim}_onActivate\(\)\s*CallActionState\({anim}\)', hks):
            raise ValueError(f'{anim}: native HKS activate callback missing')
        if not re.search(rf'function Attack{anim}_onUpdate\(\)\s*if AttackCommonFunction\({anim},', hks):
            raise ValueError(f'{anim}: native HKS update callback missing')
        for registry, expected in ((event_registry, f'W_Attack{anim}'),
                                   (event_registry, f'W_Event{anim}'),
                                   (state_registry, f'Attack{anim}')):
            if not re.search(rf'(?m)^\s*\d+\s*=\s*"{expected}"\s*$', registry):
                raise ValueError(f'{anim}: native name registry lacks {expected}')
    for before, after in zip(old_objects, filtered):
        a, b = copy.deepcopy(before), copy.deepcopy(after)
        if a.get('typeid') != b.get('typeid'):
            raise ValueError(f'{a.get("id")}: graph type changed')
        b.set('id', a.get('id'))
        for pointer in b.iter('pointer'):
            ptr = pointer.get('id')
            if ptr in reverse:
                pointer.set('id', reverse[ptr])
        if a.get('id') == 'object314':
            array = field(b, 'states').find('array')
            if len(array) != 34:
                raise ValueError('Attack state count changed')
            for item in list(array)[30:]:
                array.remove(item)
            array.set('count', '30')
        elif a.get('id') == 'object378':
            array = field(b, 'transitions').find('array')
            if len(array) != len(field(a, 'transitions').find('array')) + 4:
                raise ValueError('Attack transition count changed')
            for item in list(array)[-4:]:
                array.remove(item)
            array.set('count', field(a, 'transitions').find('array').get('count'))
        clean(a)
        clean(b)
        if ET.tostring(a) != ET.tostring(b):
            raise ValueError(f'{a.get("id")}: unrelated graph content changed')
    if receipt_path is not None:
        output = Path(receipt_path)
        if output.exists():
            raise FileExistsError(output)
        inputs = (original, readback, hks_path, event_names_path, state_names_path)
        receipt = {
            'inputSha256': {
                str(path): hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()
                for path in inputs
            },
            'preservedOriginalObjects': len(old_objects),
            'privateRouteObjects': len(additions),
            'eventNames': len(names),
            'eventInfos': len(infos),
            'nativeAttackEventSlots': [198, 200, 202, 204],
            'routes': list(range(3030, 3034)),
            'nativeHksAndNameRegistriesVerified': True,
            'gameTested': False,
        }
        output.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(f'Verified {len(old_objects)} original graph objects, 12 private route objects, native eventInfos/HKS/name dispatch')


if __name__ == '__main__':
    if len(sys.argv) not in (6, 7):
        raise SystemExit('verify-graph.py original.xml candidate-readback.xml c9997.hks eventnameid.txt statenameid.txt [receipt.json]')
    main(*sys.argv[1:])
