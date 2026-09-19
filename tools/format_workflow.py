"""Isolated Witchy BND and binary FMG candidates with independent preservation checks."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import shutil
import sys
import xml.etree.ElementTree as ET

import asset_workflow as assets
import sovereign as core


def tree(root):
    result = {}
    for path in Path(root).rglob('*'):
        assets.safe_path(root, path.relative_to(root))
        if path.is_file():
            result[path.relative_to(root).as_posix()] = assets.checksum(path)
    return result


def witchy(settings):
    executable = Path(settings['tools']['witchy'])
    config = executable.parent / 'appsettings.json'
    data = assets.read(config)
    if data.get('Recursive') is not False:
        raise ValueError('Witchy effective Recursive must be false; do not change global settings implicitly')
    return executable, {'executable': assets.checksum(executable), 'settings': assets.checksum(config)}


def inspect(binary, helper, env, text=False):
    response = core.run_process(['dotnet', helper / 'Inspect.dll', 'text-json' if text else 'binder-json', binary], helper, env)
    return json.loads(response.stdout)


def compare_dialogue(before, after):
    """Keep unknown header changes separate from decoded command/condition changes."""
    metadata = sorted(k for k in before.keys() | after.keys() if k != 'Files' and before.get(k) != after.get(k))
    changes = []
    for index in range(max(len(before['Files']), len(after['Files']))):
        old = before['Files'][index] if index < len(before['Files']) else None
        new = after['Files'][index] if index < len(after['Files']) else None
        if old == new:
            continue
        if old is None or new is None or ({k: v for k, v in old.items() if k != 'Payload'} !=
                                          {k: v for k, v in new.items() if k != 'Payload'}):
            changes.append({'index': index, 'memberIdentityChanged': True})
            continue
        a, b = old['Payload'], new['Payload']
        fields = sorted(k for k in a.keys() | b.keys() if k != 'StateGroups' and a.get(k) != b.get(k))
        groups = sorted(k for k in a['StateGroups'].keys() | b['StateGroups'].keys()
                        if a['StateGroups'].get(k) != b['StateGroups'].get(k))
        changes.append({'index': index, 'name': old['Name'], 'metadataFields': fields, 'changedStateGroups': groups})
    return {'equal': before == after, 'binderMetadataFields': metadata, 'members': changes}


def dialogue_command(executable, template, source, output):
    # ESDTool replaces its input lists at each -i and uses the last parsed ESD as
    # header template. One filtered member per invocation preserves the right header.
    return [executable, '-er', '-noannotate', '-i', template, '-f', source.stem,
            '-i', source, '-writebndfile', output]


def unpack(root, settings, relative, specialized=False):
    data = assets.catalog(root)
    group = next((g for g in data['groups'] if relative in g['files']), None)
    if not group or (group['recipe'] not in ('fmg', 'bnd', 'esd', 'binary')
                     and not (specialized and group['recipe'] == 'witchy-sfx')) or not relative.endswith('.dcx'):
        raise ValueError('This file requires its specialized recipe; basic BND unpack is not qualified for it')
    executable, tool_hashes = witchy(settings)
    binary = assets.safe_path(assets.runtime_root(root), relative)
    before = assets.checksum(binary)
    if before is None:
        raise ValueError('Missing catalogued runtime input')
    helper, env = core.build_inspector(settings)
    baseline = inspect(binary, helper, env, group['recipe'] == 'fmg')
    run = core.new_run('binder-work')
    original = run / 'original' / binary.name
    original.parent.mkdir()
    shutil.copy2(binary, original)
    work = run / 'unpacked'
    work.mkdir()
    copy_path = work / binary.name
    shutil.copy2(original, copy_path)
    result = core.run_process([executable, '--silent', '--bnd', '--unpack', copy_path], executable.parent)
    (run / 'unpack.log').write_bytes(result.stdout + result.stderr)
    metadata = list(work.rglob('_witchy-bnd4.xml'))
    if len(metadata) != 1:
        raise ValueError('Expected exactly one basic BND4 unpack; inspect ' + str(run))
    folder = metadata[0].parent
    if assets.checksum(binary) != before or assets.checksum(original) != before or witchy(settings)[1] != tool_hashes:
        raise ValueError('Input/tool settings changed during unpack')
    if group['recipe'] == 'fmg' and list(folder.glob('*.fmg.xml')):
        raise ValueError('Recursive FMG XML is not an accepted source')
    receipt = {'schemaVersion': 1, 'status': 'unpacked', 'runtimeFile': relative, 'recipe': group['recipe'],
               'sourceHash': before, 'tools': tool_hashes, 'unpacked': str(folder.relative_to(run)),
               'baseline': baseline, 'unpackedFiles': tree(folder),
               'readerLibraryHash': assets.checksum(Path(settings['tools']['smithbox']) / 'Andre.SoulsFormats.dll'),
               'readerSourceHash': assets.checksum(root / 'tools/inspection/Program.cs'), 'gameplayVerified': False}
    assets.save(run / 'receipt.json', receipt)
    return run / 'receipt.json'


def expected_text(baseline, patch):
    expected = copy.deepcopy(baseline)
    seen = set()
    for change in patch:
        name, identity = change['file'], change['id']
        if (name, identity) in seen or not {'before', 'after'} <= change.keys():
            raise ValueError('Duplicate patch or missing exact before/after text')
        if any(change[k] is not None and not isinstance(change[k], str) for k in ('before', 'after')):
            raise ValueError('FMG values must be text or explicit null')
        seen.add((name, identity))
        members = [f for f in expected['Files'] if f['Name'].replace('\\', '/').split('/')[-1] == name]
        if len(members) != 1:
            raise ValueError('FMG member must match uniquely: ' + name)
        entries = [e for e in members[0]['Payload']['Entries'] if e['ID'] == identity]
        if 'beforeMissing' in change and not isinstance(change['beforeMissing'], bool):
            raise ValueError('beforeMissing must be an explicit boolean')
        if change.get('beforeMissing'):
            if entries or change['before'] is not None:
                raise ValueError('New FMG entry must be absent, not an existing null entry')
            rows = members[0]['Payload']['Entries']
            index = next((i for i, row in enumerate(rows) if row['ID'] > identity), len(rows))
            rows.insert(index, {'ID': identity, 'Text': change['after']})
            continue
        if len(entries) != 1 or entries[0]['Text'] != change['before']:
            raise ValueError(f'Expected old FMG value differs: {name}:{identity}')
        entries[0]['Text'] = change['after']
    return expected


def rebuild(root, settings, receipt_path, patch_path=None, require_equivalent=False):
    run_root = assets.safe_path(root, '.codex-temp/binder-work')
    receipt_path = Path(receipt_path).absolute()
    if not receipt_path.is_relative_to(run_root):
        raise ValueError('Use an unpack receipt from .codex-temp/binder-work')
    receipt_path = assets.safe_path(run_root, receipt_path.relative_to(run_root))
    original_run = receipt_path.parent
    receipt = assets.read(receipt_path)
    executable, tool_hashes = witchy(settings)
    if (tool_hashes != receipt['tools'] or assets.checksum(Path(settings['tools']['smithbox']) / 'Andre.SoulsFormats.dll') != receipt['readerLibraryHash']
            or assets.checksum(root / 'tools/inspection/Program.cs') != receipt['readerSourceHash']):
        raise ValueError('Format tool/settings changed; requalify from a fresh unpack')
    original = original_run / 'original' / Path(receipt['runtimeFile']).name
    if assets.checksum(original) != receipt['sourceHash']:
        raise ValueError('Original qualification copy changed')
    if assets.checksum(assets.safe_path(assets.runtime_root(root), receipt['runtimeFile'])) != receipt['sourceHash']:
        raise ValueError('Runtime baseline changed since unpack')
    folder = assets.safe_path(original_run, receipt['unpacked'])
    inputs = tree(folder)
    patch = assets.read(patch_path) if patch_path else []
    if patch and (receipt['recipe'] != 'fmg' or require_equivalent):
        raise ValueError('Text patches require FMG mode and an intentional-change build')
    if receipt['recipe'] == 'fmg' and inputs != receipt['unpackedFiles']:
        raise ValueError('FMG input changed outside the exact-value patch route; unpack again')
    expected = expected_text(receipt['baseline'], patch) if receipt['recipe'] == 'fmg' else receipt['baseline']
    candidate_run = core.new_run('binder-candidates')
    candidate_folder = candidate_run / folder.name
    shutil.copytree(folder, candidate_folder)
    if tree(candidate_folder) != inputs:
        raise ValueError('Unpacked inputs changed while copying')
    # Metadata can name an output path. Require a direct original basename before invoking Witchy.
    metadata = ET.parse(candidate_folder / '_witchy-bnd4.xml').getroot()
    filename = metadata.findtext('filename')
    if filename != original.name:
        raise ValueError('Witchy metadata filename must match the original binder')
    if metadata.findtext('sourcePath') not in (None, ''):
        raise ValueError('Witchy metadata must not redirect output outside scratch')
    for member in metadata.findall('./files/file'):
        member_path = member.findtext('path')
        if not member_path or not assets.safe_path(candidate_folder, member_path).is_file():
            raise ValueError('Witchy member path is missing or outside scratch')
    helper, env = core.build_inspector(settings)
    if patch:
        assets.save(candidate_run / 'text-patch.json', patch)
        core.run_process(['dotnet', helper / 'Inspect.dll', 'edit-fmgs', candidate_folder,
                          candidate_run / 'text-patch.json'], helper, env)
    result = core.run_process([executable, '--silent', '--bnd', '--repack', candidate_folder], executable.parent)
    (candidate_run / 'repack.log').write_bytes(result.stdout + result.stderr)
    output = candidate_run / original.name
    if not output.is_file():
        raise ValueError('Witchy did not generate the expected scratch binder')
    after = inspect(output, helper, env, receipt['recipe'] == 'fmg')
    equal = after == expected
    assets.save(candidate_run / 'decoded.json', after)
    if (tree(folder) != inputs or witchy(settings)[1] != tool_hashes
            or assets.checksum(assets.safe_path(assets.runtime_root(root), receipt['runtimeFile'])) != receipt['sourceHash']):
        raise ValueError('Source/tool changed during build')
    assets.save(candidate_run / 'receipt.json', {'schemaVersion': 1, 'status': 'candidate',
        'runtimeFile': receipt['runtimeFile'], 'sourceHash': receipt['sourceHash'],
        'unpackReceipt': str(receipt_path), 'inputFiles': inputs, 'output': str(output),
        'outputHash': assets.checksum(output), 'tools': tool_hashes, 'expectedDecodedMatch': equal,
        'patch': patch, 'gameplayVerified': False})
    if not equal and (require_equivalent or receipt['recipe'] == 'fmg'):
        raise ValueError('Decoded preservation check failed; candidate rejected: ' + str(candidate_run))
    return {'candidate': str(candidate_run), 'expectedDecodedMatch': equal, 'gameplayVerified': False}


def dialogue_preservation(source):
    manifest = source.with_suffix('.preserve.json')
    if not manifest.is_file():
        return None, []
    data = assets.read(manifest)
    if data.get('member') != source.stem + '.esd' or not data.get('groups'):
        raise ValueError('Dialogue preservation must identify its member and owned groups')
    companions = []
    for key in ('original', 'baseline'):
        name = data[key]
        if Path(name).name != name:
            raise ValueError('Dialogue preservation requires direct companion filenames')
        path = assets.safe_path(source.parent, name)
        if assets.checksum(path) is None or assets.checksum(path) != data[key + 'Hash']:
            raise ValueError('Dialogue preservation companion changed: ' + name)
        companions.append(path)
    return manifest, companions


def build_dialogue(root, settings, relative, source_names, require_equivalent=False):
    data = assets.catalog(root)
    if not any(relative in g['files'] and g['recipe'] == 'esd' for g in data['groups']):
        raise ValueError('Expected a catalogued current mod dialogue template')
    template = assets.safe_path(assets.runtime_root(root), relative)
    permitted = [assets.safe_path(root, g['repo']) for g in data['sources'] if g['scope'] == 'talk']
    sources = [assets.safe_path(root, name) for name in source_names]
    if not sources or len({p.name for p in sources}) != len(sources) or any(
            p.suffix != '.py' or not any(p.is_relative_to(base) for base in permitted) for p in sources):
        raise ValueError('Select unique ESD DSL files from the catalogued dialogue sources')
    preservation = {p: dialogue_preservation(p) for p in sources}
    all_inputs = [template, *sources]
    for manifest, companions in preservation.values():
        if manifest:
            all_inputs.extend([manifest, *companions])
    if len({p.name for p in all_inputs}) != len(all_inputs):
        raise ValueError('Dialogue inputs have colliding basenames')
    hashes = {str(p): assets.checksum(p) for p in all_inputs}
    if None in hashes.values():
        raise ValueError('Missing dialogue input')
    executable = Path(settings['tools']['esdtool'])
    tool_hash = assets.checksum(executable)
    helper, env = core.build_inspector(settings)
    before = inspect(template, helper, env)
    run = core.new_run('dialogue-builds')
    inputs, output = run / 'input', run / 'output'
    inputs.mkdir(); output.mkdir()
    for path in all_inputs:
        shutil.copy2(path, inputs / path.name)
        if assets.checksum(inputs / path.name) != hashes[str(path)]:
            raise ValueError('Dialogue input changed while copying')
    candidate = inputs / template.name
    for index, path in enumerate(sources):
        step = output / str(index)
        step.mkdir()
        destination = step / template.name
        arguments = dialogue_command(executable, candidate, inputs / path.name, destination)
        result = core.run_process(arguments, executable.parent, timeout=240)
        (run / f'compiler-{index}.log').write_bytes(result.stdout + result.stderr)
        if not destination.is_file():
            raise ValueError(f'ESDTool skipped {path.name}; check source identity and template basename')
        manifest, companions = preservation[path]
        if manifest:
            baseline_folder = step / 'baseline'
            baseline_folder.mkdir()
            baseline_source = baseline_folder / path.name
            data = assets.read(inputs / manifest.name)
            shutil.copy2(inputs / data['baseline'], baseline_source)
            baseline_output = baseline_folder / template.name
            result = core.run_process(dialogue_command(executable, candidate, baseline_source, baseline_output),
                                      executable.parent, timeout=240)
            (run / f'baseline-compiler-{index}.log').write_bytes(result.stdout + result.stderr)
            preserved = step / 'preserved'
            preserved.mkdir()
            merged = preserved / template.name
            result = core.run_process(['dotnet', helper / 'Inspect.dll', 'merge-esd-groups', candidate,
                baseline_output, destination, inputs / manifest.name, merged], helper, env)
            (run / f'preservation-{index}.json').write_bytes(result.stdout)
            destination = merged
        candidate = destination
    after = inspect(candidate, helper, env)
    decoded = []
    for label, binary in [('before', template), ('after', candidate)]:
        result = core.run_process(['dotnet', helper / 'Inspect.dll', 'dialogue-json', binary], helper, env)
        document = json.loads(result.stdout)
        assets.save(run / (label + '-esd.json'), document)
        decoded.append(document)
    comparison = compare_dialogue(*decoded)
    allowed = {p.stem + '.esd' for p in sources}
    if {k: v for k, v in before.items() if k != 'Files'} != {k: v for k, v in after.items() if k != 'Files'}:
        raise ValueError('ESDTool changed binder header metadata')
    if len(before['Files']) != len(after['Files']):
        raise ValueError('ESDTool changed binder membership')
    changes = []
    for old, new in zip(before['Files'], after['Files']):
        if {k: v for k, v in old.items() if k != 'Payload'} != {k: v for k, v in new.items() if k != 'Payload'}:
            raise ValueError('ESDTool changed binder member identity/order/metadata')
        if old['Payload'] != new['Payload']:
            name = old['Name'].replace('\\', '/').split('/')[-1]
            if name not in allowed:
                raise ValueError('Unedited ESD member changed: ' + name)
            changes.append(name)
    if any(assets.checksum(name) != value for name, value in hashes.items()) or assets.checksum(executable) != tool_hash:
        raise ValueError('Dialogue inputs/tool changed during compilation')
    receipt = {'status': 'candidate', 'runtimeFile': relative, 'sources': hashes,
               'compilerHash': tool_hash, 'readerLibraryHash': assets.checksum(Path(settings['tools']['smithbox']) / 'Andre.SoulsFormats.dll'),
               'candidate': str(candidate), 'sha256': assets.checksum(candidate), 'changedMembers': changes,
               'decodedComparison': comparison,
               'readerSourceHash': assets.checksum(root / 'tools/inspection/Program.cs'),
               'unchangedMembersPreserved': True, 'gameplayVerified': False,
               'note': 'Changed ESD groups/states require decoded semantic review before acceptance.'}
    assets.save(run / 'receipt.json', receipt)
    if require_equivalent and changes:
        raise ValueError('Unchanged dialogue source altered member payloads; inspect ' + str(run))
    return receipt


def build_sfx(root, settings, require_equivalent=False, source_role='repo'):
    if source_role not in ('repo', 'editor'):
        raise ValueError('Choose repo or editor as the SFX source')
    data = assets.catalog(root)
    group = next(g for g in data['groups'] if g['recipe'] == 'witchy-sfx')
    source = next(g for g in data['sources'] if g['id'] == 'sfx-sources')
    overlays = assets.safe_path(root, source['repo'])
    overlay_hashes = tree(overlays)
    if '_witchy-ffxbnd.xml' not in overlay_hashes:
        raise ValueError('Accepted specialized SFX packing metadata is required in the source overlay')
    # Specialized SFX sources contain DDS textures; a basic BND unpack contains TPFs.
    # Use the catalogued complete editor extraction, never substitute a partial overlay.
    complete = assets.safe_path(settings['roots'][source['editorRoot']], source['editor'])
    complete_hashes = tree(complete)
    if source_role == 'editor' and set(overlay_hashes) - set(complete_hashes):
        raise ValueError('Editor extraction is missing an owned SFX source; reconcile before rebuilding')
    executable, tool_hashes = witchy(settings)
    binary = (assets.safe_path(assets.runtime_root(root), group['files'][0]) if source_role == 'repo'
              else assets.safe_path(settings['roots'][source['editorRoot']], Path(group['files'][0]).name))
    source_hash = assets.checksum(binary)
    fingerprints = {str(p): assets.checksum(p) for p in (
        executable, executable.parent / 'appsettings.json',
        Path(settings['tools']['smithbox']) / 'Andre.SoulsFormats.dll',
        root / 'tools/inspection/Program.cs', root / 'tools/format_workflow.py')}
    helper, env = core.build_inspector(settings)
    baseline = inspect(binary, helper, env)
    run = core.new_run('sfx-builds')
    folder = run / complete.name
    shutil.copytree(complete, folder)
    if tree(folder) != complete_hashes:
        raise ValueError('Full SFX extraction changed while copying')
    for name in (overlay_hashes if source_role == 'repo' else {}):
        target = assets.safe_path(folder, name)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(assets.safe_path(overlays, name), target)
        if assets.checksum(target) != overlay_hashes[name]:
            raise ValueError('SFX overlay changed while copying')
    metadata = ET.parse(folder / '_witchy-ffxbnd.xml').getroot()
    if metadata.findtext('filename') != Path(group['files'][0]).name or metadata.findtext('sourcePath') not in (None, ''):
        raise ValueError('SFX metadata must target the expected scratch filename')
    for key in ('effectDir', 'textureDir', 'modelDir', 'animDir', 'resDir'):
        assets.safe_path(folder, metadata.findtext(key) or '')
    original_copy = folder.parent / Path(group['files'][0]).name
    result = core.run_process([executable, '--silent', '--repack', folder], executable.parent, timeout=240)
    (run / 'sfx-build.log').write_bytes(result.stdout + result.stderr)
    if not original_copy.is_file():
        raise ValueError('Specialized SFX repack did not create expected output')
    after = inspect(original_copy, helper, env)
    equal = after == baseline
    if (tree(overlays) != overlay_hashes or tree(complete) != complete_hashes
            or assets.checksum(binary) != source_hash or witchy(settings)[1] != tool_hashes
            or any(assets.checksum(p) != h for p, h in fingerprints.items())):
        raise ValueError('SFX inputs/tools changed during build')
    assets.save(run / 'before.json', baseline)
    assets.save(run / 'after.json', after)
    assets.save(run / 'complete-source.json', {'root': str(complete), 'files': complete_hashes})
    result = {'status': 'candidate', 'kind': 'sfx-build', 'sourceRole': source_role,
              'candidate': str(original_copy), 'sha256': assets.checksum(original_copy),
              'receipt': str(run / 'receipt.json'), 'baselineFile': str(binary),
              'catalogHash': assets.fingerprint(data), 'settingsHash': assets.fingerprint(settings),
              'toolFiles': fingerprints,
              'sourceHash': source_hash, 'overlayFiles': overlay_hashes, 'tools': tool_hashes,
              'expectedDecodedMatch': equal, 'gameplayVerified': False}
    assets.save(run / 'receipt.json', result)
    if require_equivalent and not equal:
        raise ValueError('SFX preservation check failed; inspect ' + str(run))
    return result


def qualify_talk(root, settings):
    data = assets.catalog(root)
    files = {str(row['paths']['repo']): assets.checksum(row['paths']['repo'])
             for row in assets.locations(root, settings, data, True) if row['scope'] == 'talk'}
    if None in files.values():
        raise ValueError('Missing accepted talk input')
    reports = []
    helper, env = core.build_inspector(settings)
    for source in (s for s in data['sources'] if s['scope'] == 'talk'):
        directory = assets.safe_path(root, source['repo'])
        scripts = sorted(directory.glob('*.py'))
        relative = 'script/talk/' + source['id'].removeprefix('talk-source-') + '.talkesdbnd.dcx'
        binary = assets.safe_path(assets.runtime_root(root), relative)
        members = inspect(binary, helper, env)['Files']
        for script in scripts:
            name = script.stem + '.esd'
            matching = [m for m in members if m['Name'].replace('\\', '/').split('/')[-1] == name]
            if len(matching) != 1 or assets.checksum(directory / name) != matching[0]['Payload']['Sha256']:
                raise ValueError('Accept the exact runtime ESD companion before handoff: ' + str(directory / name))
        reports.append(build_dialogue(root, settings, relative, [p.relative_to(root).as_posix() for p in scripts], True))
    if any(assets.checksum(p) != h for p, h in files.items()):
        raise ValueError('Talk source changed during qualification')
    run = core.new_run('talk-qualifications')
    tools = [Path(settings['tools']['esdtool']), Path(settings['tools']['smithbox']) / 'Andre.SoulsFormats.dll',
             root / 'tools/inspection/Program.cs', root / 'tools/format_workflow.py']
    proof = {'kind': 'talk-roundtrip', 'status': 'qualified', 'files': files,
             'tools': {str(p): assets.checksum(p) for p in tools}, 'reports': reports,
             'catalogHash': assets.fingerprint(data), 'settingsHash': assets.fingerprint(settings),
             'note': 'Every owned DSL source rebuilt against its matching ESD header; companion ESDs match runtime.'}
    assets.save(run / 'receipt.json', proof)
    return run / 'receipt.json'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    command = sub.add_parser('unpack')
    command.add_argument('--file', required=True, help='Catalog runtime-relative path')
    command = sub.add_parser('build')
    command.add_argument('--receipt', required=True)
    command.add_argument('--patch', help='Exact-value binary FMG patch JSON')
    command.add_argument('--require-equivalent', action='store_true')
    command = sub.add_parser('build-dialogue')
    command.add_argument('--file', required=True)
    command.add_argument('--source', action='append', required=True)
    command.add_argument('--require-equivalent', action='store_true')
    command = sub.add_parser('build-sfx')
    command.add_argument('--require-equivalent', action='store_true')
    command.add_argument('--from', dest='source_role', choices=('repo', 'editor'), default='repo')
    sub.add_parser('qualify-talk')
    args = parser.parse_args()
    settings = assets.read(core.ROOT / 'tools/eldenring-paths.local.json')
    if args.command == 'unpack':
        print(unpack(core.ROOT, settings, args.file))
    elif args.command == 'build':
        print(json.dumps(rebuild(core.ROOT, settings, args.receipt, args.patch, args.require_equivalent), indent=2))
    elif args.command == 'build-dialogue':
        print(json.dumps(build_dialogue(core.ROOT, settings, args.file, args.source, args.require_equivalent), indent=2))
    elif args.command == 'qualify-talk':
        print(qualify_talk(core.ROOT, settings))
    else:
        result = build_sfx(core.ROOT, settings, args.require_equivalent, args.source_role)
        print(json.dumps({key: value for key, value in result.items() if key != 'overlayFiles'}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, ET.ParseError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)
