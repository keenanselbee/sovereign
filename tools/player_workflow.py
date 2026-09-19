"""Rebuild the coordinated player binders in scratch and verify authoring consistency."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import xml.etree.ElementTree as ET

import asset_workflow as assets
import format_workflow as formats
import sovereign as core


def xml_fingerprint(path):
    digest = hashlib.sha256()
    def visit(node):
        digest.update(json.dumps([node.tag, sorted(node.attrib.items()), (node.text or '').strip()]).encode())
        for child in node:
            visit(child)
        digest.update(b'/end')
    visit(ET.parse(path).getroot())
    return digest.hexdigest()


def packing_metadata(folder, name, expected):
    doc = ET.parse(folder / name).getroot()
    if doc.findtext('filename') != expected or doc.findtext('sourcePath') not in (None, ''):
        raise ValueError('Player packing metadata redirects the expected scratch output')
    for member in doc.findall('./files/file'):
        relative = member.findtext('path')
        if not relative or not assets.safe_path(folder, relative).is_file():
            raise ValueError('Missing or escaping player binder member')


def cached_qualification(root, settings, role, inputs, fingerprints, hks_paths):
    """HKS is guarded but not compiled by the native binder/graph qualification."""
    base = root / '.codex-temp/player-qualifications'
    for path in sorted(base.glob('*/receipt.json'), key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            proof = assets.read(path)
            if (proof.get('kind') != 'player-roundtrip' or proof.get('status') != 'qualified'
                    or proof.get('sourceRole') != role
                    or proof.get('catalogHash') != assets.fingerprint(assets.catalog(root))
                    or proof.get('settingsHash') != assets.fingerprint(settings)
                    or proof.get('tools') != fingerprints or set(proof.get('files', {})) != set(inputs)
                    or any(proof['files'][p] != h for p, h in inputs.items() if p not in hks_paths)):
                continue
            return path, proof
        except (ValueError, OSError, KeyError, TypeError):
            continue
    return None


def qualify(root, settings, role):
    if role not in ('repo', 'editor'):
        raise ValueError('Choose repo or editor player source')
    data = assets.catalog(root)
    editor_root = Path(settings['roots']['animations'])
    # A saved project may override packed timelines. Never archive a new one implicitly.
    projects = list(editor_root.glob('c0000*.dsaproj'))
    if projects:
        raise ValueError('Reconcile the active DSAnimStudio project before qualification: ' + ', '.join(map(str, projects)))
    rows = [r for r in assets.locations(root, settings, data, True) if r['scope'] in ('hks', 'animations')]
    paths = {str(r['paths'].get(role, r['paths']['repo'])) for r in rows}
    inputs = {p: assets.checksum(p) for p in paths}
    if None in inputs.values():
        raise ValueError('Missing coordinated player source; do not substitute an old packed baseline')
    witchy, witchy_hashes = formats.witchy(settings)
    hk = Path(settings['tools']['hklib'])
    tools = [witchy, witchy.parent / 'appsettings.json', hk, *sorted(hk.parent.glob('*.dll')),
             root / 'tools/player_workflow.py', root / 'tools/inspection/Program.cs',
             root / 'tools/inspection/Inspect.csproj', root / 'tools/format_workflow.py',
             root / 'tools/asset_workflow.py', root / 'tools/sovereign.py',
             Path(settings['tools']['smithbox']) / 'Andre.SoulsFormats.dll']
    fingerprints = {str(p): assets.checksum(p) for p in tools}
    if None in fingerprints.values():
        raise ValueError('Missing player-format dependency')
    hks_paths = {str(r['paths'].get(role, r['paths']['repo'])) for r in rows if r['scope'] == 'hks'}
    cached = cached_qualification(root, settings, role, inputs, fingerprints, hks_paths)
    if cached:
        previous, proof = cached
        proof = {**proof, 'files': inputs, 'reusedQualification': str(previous)}
        run = core.new_run('player-qualifications')
        assets.save(run / 'receipt.json', proof)
        # Recheck all current inputs, membership, tools and saved-project state.
        assets.validate_player_qualification(root, settings, role, run / 'receipt.json')
        print('Player assets/tools unchanged; reusing native qualification with current HKS guards.', flush=True)
        return run / 'receipt.json'
    run = core.new_run('player-qualifications')
    helper, env = core.build_inspector(settings)
    reports = []
    for identifier, filename, metadata in [('animation-sources', 'c0000.anibnd.dcx', '_witchy-anibnd4.xml'),
                                            ('behavior-sources', 'c0000.behbnd.dcx', '_witchy-bnd4.xml')]:
        group = next(s for s in data['sources'] if s['id'] == identifier)
        source = assets.safe_path(root, group['repo']) if role == 'repo' else assets.safe_path(settings['roots'][group['editorRoot']], group['editor'])
        before_tree = formats.tree(source)
        folder = run / identifier / source.name
        folder.parent.mkdir()
        shutil.copytree(source, folder)
        if formats.tree(folder) != before_tree:
            raise ValueError('Player authoring folder changed while copying')
        packing_metadata(folder, metadata, filename)
        baseline = assets.safe_path(assets.runtime_root(root), 'chr/' + filename) if role == 'repo' else editor_root / filename
        before = formats.inspect(baseline, helper, env)
        if identifier == 'behavior-sources':
            original_xml = folder / 'Behaviors/c0000.xml'
            original_hkx = folder / 'Behaviors/c0000.hkx'
            graph = run / 'graph'
            graph.mkdir()
            shutil.copy2(original_xml, graph / 'supplied.xml')
            shutil.copy2(original_hkx, graph / 'original.hkx')
            for path in (graph / 'supplied.xml', graph / 'original.hkx'):
                result = core.run_process([hk, path], graph, timeout=240)
                (graph / (path.name + '.log')).write_bytes(result.stdout + result.stderr)
            expected = xml_fingerprint(original_xml)
            if xml_fingerprint(graph / 'original.xml') != expected:
                raise ValueError('Behavior XML does not describe the selected HKX')
            shutil.copy2(graph / 'supplied.hkx', graph / 'rebuilt.hkx')
            result = core.run_process([hk, graph / 'rebuilt.hkx'], graph, timeout=240)
            (graph / 'roundtrip.log').write_bytes(result.stdout + result.stderr)
            if xml_fingerprint(graph / 'rebuilt.xml') != expected:
                raise ValueError('HKLib changed decoded graph values during roundtrip')
            if assets.checksum(graph / 'supplied.hkx') != assets.checksum(original_hkx):
                raise ValueError('Behavior HKX encoding changed; explicit preservation review is required')
            shutil.copy2(graph / 'supplied.hkx', original_hkx)
        result = core.run_process([witchy, '--silent', *(['--bnd'] if identifier == 'behavior-sources' else []),
                                   '--repack', folder], witchy.parent, timeout=240)
        (folder.parent / 'build.log').write_bytes(result.stdout + result.stderr)
        candidate = folder.parent / filename
        if not candidate.is_file():
            raise ValueError('Player rebuild did not create the expected scratch binder')
        after = formats.inspect(candidate, helper, env)
        if before != after:
            assets.save(folder.parent / 'before.json', before)
            assets.save(folder.parent / 'after.json', after)
            raise ValueError('Packed player output differs from its loose sources: ' + filename)
        if formats.tree(source) != before_tree:
            raise ValueError('Player source changed while building')
        reports.append({'file': filename, 'source': str(source), 'baselineHash': assets.checksum(baseline),
                        'candidate': str(candidate), 'candidateHash': assets.checksum(candidate),
                        'members': len(after['Files']), 'decodedBinderEqual': True})
    motion = assets.safe_path(assets.runtime_root(root), 'chr/c0000_a0x.anibnd.dcx') if role == 'repo' else editor_root / 'c0000_a0x.anibnd.dcx'
    members = formats.inspect(motion, helper, env)['Files']
    ultimate = [m for m in members if m['Name'].replace('\\', '/').endswith('/a984_032400.hkx')]
    if len(ultimate) != 1:
        raise ValueError('Selected motion binder lost the preserved ultimate motion')
    if list(editor_root.glob('c0000*.dsaproj')) or any(assets.checksum(p) != h for p, h in inputs.items()):
        raise ValueError('Player source/project state changed during qualification')
    if any(assets.checksum(p) != h for p, h in fingerprints.items()):
        raise ValueError('Player tool changed during qualification')
    proof = {'kind': 'player-roundtrip', 'status': 'qualified', 'sourceRole': role,
             'catalogHash': assets.fingerprint(data), 'settingsHash': assets.fingerprint(settings),
             'files': inputs, 'tools': fingerprints, 'reports': reports, 'ultimateMember': ultimate[0],
             'editorProject': 'No c0000*.dsaproj present', 'gameplayVerified': False,
             'note': 'Proves source/packed consistency and graph roundtrip, not HKS runtime compilation, clip semantics or playtesting.'}
    assets.save(run / 'receipt.json', proof)
    return run / 'receipt.json'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--from', dest='source', choices=('repo', 'editor'), required=True)
    args = parser.parse_args()
    settings = assets.read(core.ROOT / 'tools/eldenring-paths.local.json')
    print(qualify(core.ROOT, settings, args.source))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, StopIteration, ET.ParseError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)
