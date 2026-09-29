"""Render a bounded, on-demand nearest-clear-point tournament from native map data."""
import argparse
import json
import re
from pathlib import Path


def render(manifest, mode='ordinary'):
    clearances = {r['destinationId']: r['EntityID'] for r in manifest['clearanceRegions']}
    pairs = {(r['low'], r['high']): r['regionId'] for r in manifest['pairRegions']}
    eligibility = {r['destinationId']: r['EntityID'] for r in manifest.get('eligibilityRegions', [])}
    ids = sorted(clearances)
    count = len(ids)
    if not 1 <= count <= 18 or len(pairs) != count * (count - 1) // 2:
        raise ValueError('Expected complete pair mappings for at most 18 destinations')
    if mode == 'vortex' and set(eligibility) != set(ids):
        raise ValueError('Every Vortex destination needs its reach sphere')
    name = 'VORTEX' if mode == 'vortex' else 'NEAREST'
    lines = [f'// BEGIN HADEON {name} SELECTOR (generated from the map manifest)',
             '// One forward tournament per request; no waits or continuous region polling.',
             '// At most N-1 distance comparisons execute, despite N*(N-1)/2 authored pairs.']

    def guard(destination, statement):
        checks = [f'!InArea(10000, {clearances[destination]})']
        if mode in ('periodic', 'vortex'):
            checks.insert(0, f'!InArea(18002354, {clearances[destination]})')
        if mode == 'vortex':
            checks.insert(0, f'InArea(10000, {eligibility[destination]})')
        # Simple nested checks compile to conditional skips, without retaining
        # one AND group per point or checking distant points every frame.
        branch = [statement]
        for condition in reversed(checks):
            branch = [f'if ({condition}) {{'] + ['    ' + s for s in branch] + ['}']
        return branch

    for i, destination in enumerate(ids):
        lines.extend(guard(destination, f'Goto(L{i});'))
    if mode == 'vortex':
        lines.append('SetEventFlagID(1055425277, ON);')
    lines.append(f'Goto(L{19 if mode == "periodic" else count});')
    for i, destination in enumerate(ids):
        lines.append(f'L{i}:')
        for j in range(i + 1, count):
            rival = ids[j]
            lines.extend(guard(rival, f'GotoIf(L{j}, !InArea(10000, {pairs[(destination, rival)]}));'))
        if mode in ('periodic', 'vortex'):
            lines.append('SpawnOneshotSFX(TargetEntityType.Character, 18002354, 220, 440621);')
        lines.append(f'WarpCharacterAndCopyFloor(18002354, TargetEntityType.Area, {destination}, -1, {destination});')
        if mode == 'vortex':
            lines.append('RotateCharacter(18002354, 10000, -1, false);')
        lines.append(f'SpawnOneshotSFX(TargetEntityType.Area, {destination}, -1, 440481);')
        if mode == 'vortex':
            lines.extend(['SetEventFlagID(1055425259, ON);', 'SetEventFlagID(1055425278, ON);'])
        lines.append(f'Goto(L{count});')
    lines.extend([f'L{count}:', 'NoOp();', f'// END HADEON {name} SELECTOR'])
    return '\n'.join(lines) + '\n'


def update_events(source, manifest):
    for event_id, mode in [(5750304, 'ordinary'), (5750311, 'ordinary'),
                           (5750430, 'periodic'), (5750432, 'vortex')]:
        start = source.index(f'$Event({event_id},')
        end = source.index('\n});', start)
        body = source[start:end]
        name = 'VORTEX' if mode == 'vortex' else 'NEAREST'
        pattern = rf'(?m)^( *)// BEGIN HADEON {name} SELECTOR[^\n]*\n[\s\S]*?^ *// END HADEON {name} SELECTOR'
        matches = list(re.finditer(pattern, body))
        if len(matches) != 1:
            raise ValueError(f'Event {event_id} must contain exactly one shared selector')
        margin = matches[0][1]
        replacement = '\n'.join(margin + line for line in render(manifest, mode).rstrip().splitlines())
        body = re.sub(pattern, lambda _: replacement, body)
        # Retire the eight retained AND groups used by the historical Vortex block.
        if mode == 'vortex':
            body = re.sub(r'(?m)^ *vortexPoint\d+ = [^\n]+\n', '', body)
        source = source[:start] + body + source[end:]
    return source


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('output', type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--periodic', action='store_true')
    mode.add_argument('--vortex', action='store_true')
    parser.add_argument('--events', type=Path, help='Render all selector blocks in this event source to output')
    args = parser.parse_args()
    mode = 'vortex' if args.vortex else 'periodic' if args.periodic else 'ordinary'
    manifest = json.loads(args.manifest.read_text(encoding='utf-8-sig'))
    result = update_events(args.events.read_text(encoding='utf-8-sig'), manifest) if args.events else render(manifest, mode)
    args.output.write_text(result, encoding='utf-8')
