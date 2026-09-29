"""Add private Hadeon routes for the native c2500 Attack3028 graph."""

import copy
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def field(obj, name):
    prefix = './' if obj.tag == 'record' else './record/'
    value = obj.find(f'{prefix}field[@name="{name}"]')
    if value is None:
        raise ValueError(f'{obj.get("id")}: missing {name}')
    return value


def value(obj, name, kind):
    return field(obj, name).find(kind)


def main(source, output):
    root = ET.parse(source).getroot()
    objects = {obj.get('id'): obj for obj in root.findall('object')}
    if len(objects) != len(root.findall('object')):
        raise ValueError('Duplicate graph object ID')
    graph_data = objects['object8']
    graph_events = objects['object4']
    attack_machine = objects['object314']
    transitions = objects['object378']
    state = objects['object377']
    selector = objects['object464']
    clip = objects['object717']
    event_names = field(graph_data, 'eventNames').find('array')
    event_infos = field(graph_events, 'eventInfos').find('array')
    state_list = field(attack_machine, 'states').find('array')
    transition_list = field(transitions, 'transitions').find('array')
    names = [item.get('value') for item in event_names.findall('string')]
    if names[194:196] != ['W_Attack3028', 'W_Event3028']:
        raise ValueError('Attack3028 event names changed')
    if len(names) != len(event_infos.findall('record')) or len(names) != 1366:
        raise ValueError('Native event names and eventInfos are not aligned')
    for index, anim_id in enumerate(range(3030, 3034)):
        slot = 198 + 2 * index
        if names[slot:slot + 2] != [f'W_Attack{anim_id}', f'W_Event{anim_id}']:
            raise ValueError(f'Native event slots for {anim_id} changed')
        if any(value(item, 'flags', 'integer').get('value') != '0'
               for item in event_infos.findall('record')[slot:slot + 2]):
            raise ValueError(f'Native eventInfos for {anim_id} changed')
    if value(state, 'name', 'string').get('value') != 'Attack3028':
        raise ValueError('Attack3028 state changed')
    if value(state, 'stateId', 'integer').get('value') != '32':
        raise ValueError('Attack3028 state ID changed')
    if value(selector, 'animId', 'integer').get('value') != '3028':
        raise ValueError('Attack3028 selector changed')
    if value(clip, 'animationName', 'string').get('value') != 'a000_003028':
        raise ValueError('Attack3028 motion changed')
    existing_states = {
        int(value(objects[p.get('id')], 'stateId', 'integer').get('value'))
        for p in state_list.findall('pointer')
    }
    if any(s in existing_states for s in range(57, 61)):
        raise ValueError('Private state ID collision')
    names_in_graph = {
        value(obj, 'name', 'string').get('value')
        for obj in objects.values() if obj.find('./record/field[@name="name"]') is not None
        and value(obj, 'name', 'string') is not None
    }
    if any(f'Attack{anim_id}' in names_in_graph or f'Attack{anim_id}_CMSG' in names_in_graph
           for anim_id in range(3030, 3034)):
        raise ValueError('Private graph route name collision')
    existing_user_data = {
        value(obj, 'userData', 'integer').get('value')
        for obj in objects.values() if obj.find('./record/field[@name="userData"]') is not None
        and value(obj, 'userData', 'integer') is not None
    }
    if any(str(user_data) in existing_user_data for user_data in range(18546718, 18546722)):
        raise ValueError('Private selector userData collision')
    template_transitions = [
        item for item in transition_list.findall('record')
        if value(item, 'eventId', 'integer').get('value') == '194'
        and value(item, 'toStateId', 'integer').get('value') == '32'
    ]
    if len(template_transitions) != 1:
        raise ValueError('Attack3028 transition changed')
    next_object = max(int(name[6:]) for name in objects) + 1
    for index, anim_id in enumerate(range(3030, 3034)):
        event_id = 198 + 2 * index

        state_copy, selector_copy, clip_copy = (
            copy.deepcopy(item) for item in (state, selector, clip)
        )
        state_id, selector_id, clip_id = (
            f'object{next_object + offset}' for offset in range(3)
        )
        next_object += 3
        state_copy.set('id', state_id)
        selector_copy.set('id', selector_id)
        clip_copy.set('id', clip_id)
        value(state_copy, 'name', 'string').set('value', f'Attack{anim_id}')
        value(state_copy, 'stateId', 'integer').set('value', str(57 + index))
        value(state_copy, 'generator', 'pointer').set('id', selector_id)
        value(selector_copy, 'name', 'string').set('value', f'Attack{anim_id}_CMSG')
        value(selector_copy, 'animId', 'integer').set('value', str(anim_id))
        value(selector_copy, 'userData', 'integer').set('value', str(18546718 + index))
        value(selector_copy, 'generators', 'array').find('pointer').set('id', clip_id)
        value(clip_copy, 'name', 'string').set('value', f'a000_003028_Hadeon{anim_id}')
        value(clip_copy, 'animationName', 'string').set('value', f'a000_{anim_id:06d}')
        # The private clip name selects its TAE timeline. Its internal ID still
        # references native 3028 motion, imported by that timeline.
        root.extend((state_copy, selector_copy, clip_copy))
        ET.SubElement(state_list, 'pointer', id=state_id)
        transition = copy.deepcopy(template_transitions[0])
        value(transition, 'eventId', 'integer').set('value', str(event_id))
        value(transition, 'toStateId', 'integer').set('value', str(57 + index))
        transition_list.append(transition)

    for array in (state_list, transition_list):
        array.set('count', str(len(array)))
    if Path(output).exists():
        raise FileExistsError(output)
    ET.indent(root, space='  ')
    ET.ElementTree(root).write(output, encoding='utf-8', xml_declaration=True)
    print(f'Private graph routes 3030-3033 written to {output}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('build-graph.py source.xml output.xml')
    main(*sys.argv[1:])
