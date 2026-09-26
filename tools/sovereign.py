"""Repository-local Elden Ring inspection and candidate preparation. Python 3.11+."""
from __future__ import annotations
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import asset_workflow as assets

ROOT = Path(__file__).resolve().parents[1]
SCOPES = ('all', 'params', 'hks', 'events', 'maps', 'text', 'animations', 'sfx', 'models', 'talk', 'textures')


def runtime_base(root, manifest=None):
    if (Path(root) / 'asset-catalog.json').is_file():
        return assets.runtime_root(root)
    return Path(root)


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def contained(root, relative):
    root = Path(root).resolve()
    value = Path(relative)
    if value.is_absolute() or '..' in value.parts:
        raise ValueError(f'Expected a relative path: {relative}')
    target = (root / value).resolve()
    if not target.is_relative_to(root):
        raise ValueError(f'Path escapes {root}: {relative}')
    return target


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')


def config(args):
    path = Path(args.config) if args.config else ROOT / 'tools/eldenring-paths.local.json'
    if not path.is_file():
        raise ValueError('Copy tools/eldenring-paths.example.json to eldenring-paths.local.json and set local paths.')
    result = read_json(path)
    if result.get('schemaVersion') != 1:
        raise ValueError('Unsupported path configuration schema.')
    for group in ('roots', 'tools'):
        for key, value in result[group].items():
            if not Path(value).is_absolute():
                raise ValueError(f'{group}.{key} must be absolute.')
    return result


def runtime_files(root, manifest):
    """Explicit runtime patterns; reject symlink escapes and case-colliding paths."""
    catalog_path = Path(root) / 'asset-catalog.json'
    if catalog_path.is_file():
        data = assets.catalog(root)
        base = assets.safe_path(root, data['runtimeRoot'])
        expected = [name for group in data['groups'] if group['package'] == 'main' for name in group['files']]
        missing = [name for name in expected if not assets.safe_path(base, name).is_file()]
        if missing:
            raise ValueError('Missing catalogued runtime files: ' + ', '.join(missing))
        return sorted(expected)
    root = Path(root).resolve()
    found = {}
    for pattern in manifest['runtimePatterns']:
        contained(root, pattern)
        for path in root.glob(pattern):
            if not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            contained(root, relative)
            if any(part.lower() in ('src', 'modified', 'modifiedtodo', '.git', '.smithbox', '.codex-temp') for part in Path(relative).parts):
                raise ValueError(f'Authoring material matched a runtime pattern: {relative}')
            key = relative.lower()
            if key in found and found[key] != relative:
                raise ValueError(f'Case-colliding runtime paths: {relative}, {found[key]}')
            found[key] = relative
    return sorted(found.values())


def status_rows(root, settings, scope='all'):
    if (Path(root) / 'asset-catalog.json').is_file():
        return assets.status(root, settings, scope)
    root = Path(root)
    rows = []
    seen = set()
    for mapping in settings['mappings']:
        if scope not in ('all', mapping['scope']):
            continue
        contained(root, mapping['pattern'])
        prefix = Path(mapping['prefix'])
        editor_base = contained(settings['roots'][mapping['editorRoot']], mapping['editorPrefix'])
        pattern_parts = Path(mapping['pattern']).parts[len(prefix.parts):]
        editor_pattern = str(Path(*pattern_parts))
        relative_paths = {p.relative_to(root).as_posix() for p in root.glob(mapping['pattern']) if p.is_file()}
        if editor_base.is_dir():
            for p in editor_base.glob(editor_pattern):
                if p.is_file():
                    relative_paths.add((prefix / p.relative_to(editor_base)).as_posix())
        # Include managed live/staged-only files: they can otherwise survive old propagation.
        for target in ('live', 'vortex'):
            destination = Path(settings['roots'][target])
            if destination.is_dir():
                relative_paths.update(p.relative_to(destination).as_posix() for p in destination.glob(mapping['pattern']) if p.is_file())
        for relative in sorted(relative_paths):
            if relative in seen:
                continue
            seen.add(relative)
            tail = Path(relative).relative_to(prefix)
            paths = {'repo': contained(root, relative), 'editor': contained(editor_base, tail)}
            paths.update({key: contained(settings['roots'][key], relative) for key in ('live', 'vortex')})
            hashes = {key: digest(path) if path.is_file() else None for key, path in paths.items()}
            state = 'Match' if None not in hashes.values() and len(set(hashes.values())) == 1 else 'Review'
            rows.append({'scope': mapping['scope'], 'file': relative, 'state': state, 'hashes': hashes,
                         'paths': {key: str(path) for key, path in paths.items()}})
    return rows


def source_completeness_issues(root):
    issues = assets.source_inventory_issues(root)
    import recovered_sources
    issues.extend(recovered_sources.issues(root))
    commands = (Path(root) / 'docs/WORKFLOW-COMMANDS.md').read_text(encoding='utf-8')
    for recipe in assets.catalog(root).get('sourceRecipes', []):
        if recipe['source'] not in commands:
            issues.append(f"Recipe is not documented in WORKFLOW-COMMANDS.md: {recipe['source']}")
    return issues


def emit(value, as_json=False):
    if as_json:
        print(json.dumps(value, indent=2))
    elif isinstance(value, list):
        for row in value:
            print(' | '.join(f'{key}: {val}' for key, val in row.items()) if isinstance(row, dict) else row)
    else:
        print(value)


@contextmanager
def operation(name):
    scratch = contained(ROOT, '.codex-temp')
    locks = contained(scratch, 'locks')
    locks.mkdir(parents=True, exist_ok=True)
    lock = locks / name
    try:
        lock.mkdir()
    except FileExistsError:
        raise ValueError(f'Operation already locked: {lock}. Inspect the owner before removing a stale lock.')
    try:
        write_json(lock / 'owner.json', {'pid': os.getpid(), 'started': time.time()})
        yield
    finally:
        (lock / 'owner.json').unlink(missing_ok=True)
        lock.rmdir()


def new_run(name):
    run = contained(ROOT, f'.codex-temp/{name}/{time.time_ns()}')
    run.mkdir(parents=True)
    return run


def run_process(arguments, cwd, env=None, timeout=90):
    result = subprocess.run([str(x) for x in arguments], cwd=cwd, env=env, capture_output=True,
                            timeout=timeout, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    if result.returncode:
        raise ValueError(f'Command failed ({result.returncode}): {arguments[0]}\n' +
                         (result.stdout + result.stderr).decode('utf-8', errors='replace')[-4000:])
    return result


def build_inspector(settings):
    library = Path(settings['tools']['smithbox'])
    for name in ('Andre.SoulsFormats.dll', 'oo2core_9_win64.dll'):
        if not (library / name).is_file():
            raise ValueError(f'Missing inspection dependency: {library / name}')
    build = contained(ROOT, '.codex-temp/inspection-build')
    env = os.environ.copy()
    env.update(DOTNET_CLI_HOME=str(contained(ROOT, '.codex-temp/dotnet-home')),
               DOTNET_CLI_TELEMETRY_OPTOUT='1', DOTNET_GENERATE_ASPNET_CERTIFICATE='false')
    run_process(['dotnet', 'build', ROOT / 'tools/inspection/Inspect.csproj',
                 '-p:SmithboxRoot=' + str(library), '-p:BaseIntermediateOutputPath=' + str(build / 'obj') + '/',
                 '-o', build / 'bin', '-v:q'], ROOT, env)
    shutil.copy2(library / 'oo2core_9_win64.dll', build / 'bin/oo2core_9_win64.dll')
    env['SOVEREIGN_SMITHBOX'] = str(library)
    env['PATH'] = str(library) + os.pathsep + env.get('PATH', '')
    return build / 'bin', env


def event_data(binary, helper, env):
    result = run_process(['dotnet', helper / 'Inspect.dll', 'event-json', binary], helper, env)
    return json.loads(result.stdout)


def compare_events(before, after):
    # Keep event order and duplicate IDs visible; never collapse them into a dictionary.
    original = before['Events']
    current = after['Events']
    changed = []
    for index in range(max(len(original), len(current))):
        old = original[index] if index < len(original) else None
        new = current[index] if index < len(current) else None
        if old != new:
            changed.append({'index': index, 'beforeId': old['ID'] if old else None,
                            'afterId': new['ID'] if new else None})
    metadata = [key for key in set(before) | set(after) if key != 'Events' and before.get(key) != after.get(key)]
    return {'equal': before == after, 'changedEvents': changed, 'changedMetadata': sorted(metadata)}


def build_events(args):
    settings = config(args)
    runtime = runtime_base(ROOT)
    source_root = ROOT / 'event/src'
    if (ROOT / 'asset-catalog.json').is_file():
        source_root = assets.safe_path(ROOT, next(group['repo'] for group in assets.catalog(ROOT)['sources']
                                                 if group['id'] == 'event-sources'))
    executable = Path(settings['tools']['darkscript'])
    if not executable.is_file():
        raise ValueError('Configured DarkScript executable is missing.')
    with operation('events'):
        run = new_run('event-builds')
        source = run / 'input'
        output = run / 'compiled'
        source.mkdir()
        output.mkdir()
        # Include local common_func sources/binaries for typed initialization lookup.
        inputs = [p for p in source_root.iterdir() if p.is_file() and p.name.endswith(('.emevd.dcx', '.emevd.dcx.js'))]
        originals = {str(p): digest(p) for p in inputs}
        for path in inputs:
            contained(ROOT, path.relative_to(ROOT))
            shutil.copy2(path, source / path.name)
        expected = sorted(p.name[:-3] for p in inputs if p.name.endswith('.js'))
        if not expected:
            raise ValueError('No event sources found.')
        result = run_process([executable, '/cmd', '-compile', '-game', 'er', '-indir', source, '-outdir', output], executable.parent)
        (run / 'compiler.log').write_bytes(result.stdout + b'\n' + result.stderr)
        if sorted(p.name for p in output.iterdir() if p.is_file()) != expected:
            raise ValueError(f'Compiler output does not match expected files. Inspect {run}')
        helper, env = build_inspector(settings)
        results = []
        shipped = {p.name for p in (runtime / 'event').glob('*.dcx')}
        for name in expected:
            baseline = runtime / 'event' / name if name in shipped else source / name
            if not baseline.is_file():
                results.append({'file': name, 'runtimeCandidate': name in shipped, 'baselineHash': None,
                                'outputHash': digest(output / name), 'equal': None,
                                'reason': 'No compiled comparison baseline; round trip is unqualified'})
                continue
            baseline_hash = digest(baseline)
            before = event_data(baseline, helper, env)
            after = event_data(output / name, helper, env)
            if digest(baseline) != baseline_hash:
                raise ValueError(f'Baseline changed during inspection: {baseline}')
            row = {'file': name, 'runtimeCandidate': name in shipped, 'baselineHash': baseline_hash,
                   'outputHash': digest(output / name), **compare_events(before, after)}
            results.append(row)
            write_json(run / (name + '.before.json'), before)
            write_json(run / (name + '.after.json'), after)
        if any(not Path(path).is_file() or digest(path) != value for path, value in originals.items()):
            raise ValueError('Event source changed during the build. Candidate must not be accepted.')
        write_json(run / 'receipt.json', {'kind': 'local-event-candidate', 'compilerHash': digest(executable),
                   'readerLibraryHash': digest(Path(settings['tools']['smithbox']) / 'Andre.SoulsFormats.dll'),
                   'readerSourceHash': digest(ROOT / 'tools/inspection/Program.cs'),
                   'sources': originals, 'outputs': results, 'gameplayVerified': False})
        print(f'Candidate: {run}')
        for row in results:
            verdict = 'Equivalent' if row['equal'] else ('No baseline' if row['equal'] is None else 'Review changes')
            print(f"{row['file']}: {verdict}; runtime={row['runtimeCandidate']}")
        if args.require_equivalent and any(row['equal'] is False or (row['runtimeCandidate'] and row['equal'] is None) for row in results):
            raise ValueError('Unchanged-source qualification failed: review the recorded differences.')


def nexus_issues(root, manifest, descriptions_only=False):
    issues = []
    directory = contained(root, manifest['nexus']['descriptionDirectory'])
    texts = {}
    for name in ('nexus-full-desc.txt', 'nexus-short-desc.txt', 'nexus-file-desc.txt'):
        path = directory / name
        text = path.read_text(encoding='utf-8-sig') if path.is_file() else ''
        texts[name] = text.strip()
        if not text.strip():
            issues.append(f'{name}: missing or empty')
        if any(ord(c) > 127 for c in text):
            issues.append(f'{name}: non-ASCII characters')
        if '```' in text or re.search(r'\[code=', text, re.I):
            issues.append(f'{name}: use plain Nexus BBCode [code]')
    short = texts['nexus-short-desc.txt']; pitch = texts['nexus-file-desc.txt']
    if len(short) > 350:
        issues.append('Short description exceeds 350 characters')
    if len(pitch) > 255:
        issues.append('File description exceeds 255 characters')
    normalized = [re.sub(r'[^a-z0-9]+', ' ', text.lower()).strip() for text in (short, pitch)]
    if pitch and short and (len(pitch) >= len(short) or normalized[0] == normalized[1]):
        issues.append('File pitch must be distinct and shorter than the short description')
    # Structural check only; images, links, and rendering still require visual review.
    stack = []
    paired = {'b', 'i', 'u', 's', 'size', 'color', 'center', 'heading', 'url', 'img', 'code', 'list', 'quote', 'spoiler', '*'}
    for match in re.finditer(r'\[(/?)([a-z*]+)(?:[^\]]*)\]', texts['nexus-full-desc.txt'], re.I):
        closing, name = match.group(1), match.group(2).lower()
        if name not in paired:
            continue
        if closing:
            if not stack or stack.pop() != name:
                issues.append(f'Full description: mismatched closing tag {match.group(0)}'); break
        else:
            stack.append(name)
    if stack:
        issues.append('Full description: unclosed tags ' + ', '.join(stack))
    if descriptions_only:
        return issues
    if not manifest.get('version'):
        issues.append('Release version is not selected')
    else:
        import release_workflow
        try:
            release_workflow.check(root, manifest)
        except (ValueError, OSError) as error:
            issues.append(str(error))
    try:
        validate_nexus_metadata(manifest)
    except ValueError as error:
        issues.append(str(error))
    return issues


def validate_nexus_metadata(manifest):
    nexus = manifest['nexus']
    for key in ('gameScopedModId', 'modId', 'groupId'):
        if not isinstance(nexus.get(key), str) or not re.fullmatch(r'[1-9][0-9]*', nexus[key]):
            raise ValueError(f'Nexus metadata: {key} must be a positive decimal ID')
    expected = f"https://www.nexusmods.com/games/eldenring/mods/{nexus['gameScopedModId']}"
    if 'textures' in nexus:
        texture_group = nexus['textures'].get('groupId')
        if (not isinstance(texture_group, str) or not re.fullmatch(r'[1-9][0-9]*', texture_group)
                or texture_group == nexus['groupId']):
            raise ValueError('Nexus metadata: textures must have a distinct positive decimal groupId')
    if manifest.get('gameDomain') != 'eldenring' or nexus.get('url') != expected:
        raise ValueError('Nexus metadata: URL must match the Elden Ring page ID')


def nexus_get(path):
    """Read through the shared fixed-host transport, retaining this adapter's route policy."""
    if not re.fullmatch(r'/(?:games/eldenring/mods/[1-9][0-9]*|mods/[1-9][0-9]*/files|mod-files/[1-9][0-9]*/versions)', path):
        raise ValueError('Unsupported Nexus read path')
    import nexus_automation
    result = nexus_automation.read(ROOT, path)
    if not isinstance(result, dict):
        raise ValueError('Unexpected Nexus response schema; remote state remains Verify')
    return result


def nexus_status(manifest, get=nexus_get):
    validate_nexus_metadata(manifest)
    nexus = manifest['nexus']
    mod = get(f"/games/eldenring/mods/{nexus['gameScopedModId']}")
    if str(mod.get('id')) != nexus['modId'] or str(mod.get('game_scoped_id')) != nexus['gameScopedModId']:
        raise ValueError('Nexus page/unique mod IDs disagree; remote state remains Verify')
    files = get(f"/mods/{nexus['modId']}/files").get('mod_files')
    if not isinstance(files, list) or any(not isinstance(row, dict) for row in files):
        raise ValueError('Unexpected Nexus mod_files schema; remote state remains Verify')
    groups = [row for row in files if str(row.get('id')) == nexus['groupId']]
    if len(groups) != 1:
        raise ValueError('Configured Nexus file group was not found uniquely on this mod')
    versions = get(f"/mod-files/{nexus['groupId']}/versions").get('versions')
    if not isinstance(versions, list):
        raise ValueError('Unexpected Nexus versions schema; remote state remains Verify')
    for row in versions:
        if (not isinstance(row, dict) or not isinstance(row.get('file'), dict)
                or str(row['file'].get('id')) != nexus['groupId']
                or any(not isinstance(row.get(key), str) or not row[key]
                       for key in ('id', 'game_scoped_id', 'name', 'version', 'category', 'uploaded_at'))
                or not isinstance(row.get('is_primary', False), bool)):
            raise ValueError('Unexpected Nexus version identity/schema; remote state remains Verify')
    active = [row for row in versions if row['category'] in ('main', 'update', 'optional', 'miscellaneous')]
    primary = [row for row in active if row.get('is_primary', False)]
    candidates = primary or active
    # An archived upload can be newer than the active release. Never select by date alone.
    current = candidates[0] if len(candidates) == 1 else None
    keys = ('id', 'game_scoped_id', 'name', 'version', 'category', 'uploaded_at', 'is_primary')
    return {'observedAt': datetime.now(timezone.utc).isoformat(), 'url': nexus['url'],
            'modId': nexus['modId'], 'groupId': nexus['groupId'], 'groupName': groups[0].get('name'),
            'identityVerified': True, 'versionsCount': len(versions),
            'current': {key: current.get(key) for key in keys} if current else None,
            'activeVersions': [{key: row.get(key) for key in keys} for row in active],
            'releaseComparison': 'Verify' if current is None or not manifest.get('version') else
                                 ('Same version label; archive contents unverified' if current['version'] == manifest['version']
                                  else 'Different version labels; review before updating'),
            'descriptionStatus': 'Verify in browser; these API responses do not include page/file descriptions'}


def make_package(root, manifest, run, version):
    if not re.fullmatch(r'[0-9]+(?:\.[0-9]+){1,3}(?:-[A-Za-z0-9.-]+)?', version):
        raise ValueError('Use a numeric release version, optionally with a prerelease suffix.')
    files = runtime_files(root, manifest)
    root = runtime_base(root, manifest)
    if 'regulation.bin' not in files:
        raise ValueError('No regulation.bin in candidate.')
    expected = {name: digest(contained(root, name)) for name in files}
    archive = Path(run) / f'Sovereign-{version}-DRAFT.zip'
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as zipped:
        for name in files:
            data = contained(root, name).read_bytes()
            if hashlib.sha256(data).hexdigest() != expected[name]:
                raise ValueError(f'File changed during packaging: {name}')
            zipped.writestr('mod/' + name, data)
        zipped.writestr('DRAFT-NOT-FOR-RELEASE.txt', 'Unverified candidate. Runtime dependency and gameplay acceptance remain required.\n')
    with zipfile.ZipFile(archive) as zipped:
        wanted = {'mod/' + name for name in files} | {'DRAFT-NOT-FOR-RELEASE.txt'}
        if len(zipped.namelist()) != len(wanted) or set(zipped.namelist()) != wanted or zipped.testzip():
            raise ValueError('Archive validation failed.')
        for name, checksum in expected.items():
            if hashlib.sha256(zipped.read('mod/' + name)).hexdigest() != checksum:
                raise ValueError(f'Archive content mismatch: {name}')
    if any(digest(contained(root, name)) != checksum for name, checksum in expected.items()):
        raise ValueError('Source changed before package verification finished.')
    receipt = {'kind': 'draft-package', 'version': version, 'archive': archive.name,
               'sha256': digest(archive), 'files': expected, 'dependencies': manifest['dependencies'], 'gameplayVerified': False}
    write_json(Path(run) / 'receipt.json', receipt)
    return archive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', help='Absolute local path configuration override')
    sub = parser.add_subparsers(dest='command', required=True)
    status = sub.add_parser('status', help='Read-only hash comparison; Match is not a gameplay verdict')
    status.add_argument('--scope', choices=SCOPES, default='all'); status.add_argument('--json', action='store_true')
    status.add_argument('--sources', action='store_true', help='Also compare catalogued editor/source trees')
    status.add_argument('--verbose', action='store_true', help='Also list matching files (JSON always includes all files)')
    plan = sub.add_parser('propagation-plan', help='Preview repo-to-target differences; never copies or deletes')
    plan.add_argument('--scope', choices=SCOPES, required=True); plan.add_argument('--json', action='store_true')
    sub.add_parser('check', help='Validate local preparation and runtime manifest')
    sub.add_parser('version-check', help='Check the release target against changelog.txt; no writes')
    sub.add_parser('doctor', help='Check catalogued files and configured tools without writing')
    sub.add_parser('path-check', help='Check workspace paths, selected stages and Windows shortcuts; no writes')
    handoff = sub.add_parser('accept-plan', help='Prepare a hash-checked repo/editor handoff receipt; never deploy')
    handoff.add_argument('--scope', required=True)
    handoff.add_argument('--from', dest='source', choices=('repo', 'editor'), required=True)
    handoff.add_argument('--qualification', help='Current qualified format receipt for coordinated handoff')
    handoff.add_argument('--resolve-conflicts', action='store_true',
                         help='Explicitly choose the reviewed source after reconciling a sync conflict')
    baseline = sub.add_parser('sync-baseline', help='Record matching repo/editor hashes only; copy nothing')
    baseline.add_argument('--scope', default='all')
    for name in ('accept', 'restore'):
        command = sub.add_parser(name, help='Apply or restore a reviewed repo/editor handoff receipt')
        command.add_argument('--receipt', required=True)
    nexus = sub.add_parser('nexus-check', help='Local copy/metadata checks; no network or publishing')
    nexus.add_argument('--descriptions-only', action='store_true',
                       help='Check the three description files without requiring release version or API metadata')
    sub.add_parser('nexus-status', help='Read-only Nexus v3 identity and active file version check; environment key required')
    sub.add_parser('tests', help='List manual tests not marked Passed')
    logs = sub.add_parser('logs', help='Read the latest loader log tails; does not launch the game')
    logs.add_argument('--lines', type=int, default=60)
    events = sub.add_parser('build-events', help='Compile local candidates and compare decoded event data')
    events.add_argument('--require-equivalent', action='store_true')
    package = sub.add_parser('package', help='Build a verified draft archive; no deploy/upload')
    package.add_argument('--draft', action='store_true', required=True)
    package.add_argument('--version', required=True)
    args = parser.parse_args()
    manifest = read_json(ROOT / 'mod.json')
    if args.command in ('status', 'propagation-plan'):
        if getattr(args, 'sources', False) and (ROOT / 'asset-catalog.json').is_file():
            rows = assets.status(ROOT, config(args), args.scope, include_sources=True)
        else:
            rows = status_rows(ROOT, config(args), args.scope)
        if args.command == 'propagation-plan':
            rows = [dict(row, action='Review baseline before copying; no deletions proposed') for row in rows if row['state'] == 'Review']
        if args.json:
            emit(rows, True)
        else:
            for row in rows:
                if args.command == 'status' and not args.verbose and row['state'] == 'Match':
                    continue
                differences = [f'missing {key}' if value is None else f'differs {key}'
                               for key, value in row['hashes'].items()
                               if value != row['hashes']['repo'] or value is None]
                comparisons = row.get('comparisons', {})
                pairs = ', '.join(f'{name}: {value}' for name, value in comparisons.items())
                details = ', '.join(part for part in (', '.join(differences), pairs) if part)
                print(f"{row['state']:6} {row['file']}" + (f' ({details})' if details else ''))
            matching = sum(row['state'] == 'Match' for row in rows)
            print(f'{len(rows)} files inspected: {matching} match, {len(rows) - matching} need review. No files changed.')
            if args.command == 'status' and not args.verbose:
                print('Use --verbose for matching files or --json for full paths and hashes.')
    elif args.command == 'check':
        import release_workflow
        release_workflow.check(ROOT, manifest)
        if manifest.get('schemaVersion') != 1 or manifest.get('gameDomain') != 'eldenring':
            raise ValueError('Unexpected manifest schema/game.')
        files = runtime_files(ROOT, manifest)
        if (ROOT / 'asset-catalog.json').is_file():
            issues = source_completeness_issues(ROOT)
            if issues:
                raise ValueError('Source completeness check failed: ' + '; '.join(issues))
            findings = assets.inventory_review(ROOT, config(args))
            unknown = [row for row in findings if row['location'].startswith('repo') and row['state'] == 'Uncatalogued']
            if unknown:
                raise ValueError('Uncatalogued runtime files: ' + ', '.join(row['file'] for row in unknown))
        if 'regulation.bin' not in files:
            raise ValueError('Runtime manifest does not include regulation.bin.')
        for required in ('AGENTS.md', 'docs/WORKFLOW.md', 'docs/MECHANICS.md', 'TEST-MATRIX.md'):
            if not (ROOT / required).is_file():
                raise ValueError(f'Missing preparation document: {required}')
        print(f'Preparation checks passed; {len(files)} runtime candidate files. Release readiness is not implied.')
    elif args.command == 'version-check':
        import release_workflow
        emit(release_workflow.check(ROOT, manifest), True)
    elif args.command == 'path-check':
        import workspace_paths
        report = workspace_paths.check(ROOT, config(args))
        emit(report, True)
        if report['findings']:
            raise ValueError('Workspace path check failed; inspect the findings above')
    elif args.command == 'doctor':
        settings = config(args)
        rows = assets.status(ROOT, settings)
        emit({'runtimeRoot': str(runtime_base(ROOT)), 'files': len(rows),
              'review': [{'file': row['file'], 'state': row['state']} for row in rows if row['state'] != 'Match'],
              'tools': {name: {'path': path, 'exists': Path(path).exists()} for name, path in settings['tools'].items()},
              'inventoryFindings': assets.inventory_review(ROOT, settings),
              'externalOwned': assets.catalog(ROOT)['externalFiles'], 'releaseReady': manifest['releaseReady']}, True)
    elif args.command == 'accept-plan':
        print(assets.prepare_handoff(ROOT, config(args), args.scope, args.source, args.qualification,
                                    args.resolve_conflicts))
    elif args.command == 'sync-baseline':
        emit(assets.record_sync_baseline(ROOT, config(args), args.scope), True)
    elif args.command in ('accept', 'restore'):
        function = assets.apply_handoff if args.command == 'accept' else assets.restore_handoff
        result = function(ROOT, config(args), args.receipt)
        print(f"Handoff {result['status']}: {len(result['entries'])} files. No Vortex/live writes.")
    elif args.command == 'nexus-check':
        issues = nexus_issues(ROOT, manifest, args.descriptions_only)
        emit(issues or 'Local Nexus structure passes; remote state and mechanics still need verification.')
        if issues:
            return 2
    elif args.command == 'nexus-status':
        result = nexus_status(manifest)
        emit(result, True)
        if result['current'] is None:
            return 2
    elif args.command == 'tests':
        for line in (ROOT / 'TEST-MATRIX.md').read_text(encoding='utf-8').splitlines():
            if re.match(r'^\| ER-', line) and line.split('|')[-2].strip() != 'Passed':
                print(line)
    elif args.command == 'logs':
        if not 1 <= args.lines <= 1000:
            raise ValueError('--lines must be between 1 and 1000.')
        game = Path(config(args)['roots']['live']).parent
        paths = list((game / 'modengine2/logs').glob('*.log'))
        selected = [max(paths, key=lambda p: p.stat().st_mtime)] if paths else []
        if (game / 'mod_loader_log.txt').is_file():
            selected.append(game / 'mod_loader_log.txt')
        for path in selected:
            print(path)
            print('\n'.join(path.read_text(encoding='utf-8', errors='replace').splitlines()[-args.lines:]))
        if not selected:
            print('No loader logs found in the configured game directory.')
    elif args.command == 'build-events':
        build_events(args)
    elif args.command == 'package':
        import nexus_workflow
        with operation('package'):
            archive = nexus_workflow.build_vortex_package(nexus_workflow.vortex_root(args.config), manifest,
                                                          new_run('vortex-packages'), args.version)
            print(f'Draft archive: {archive}\nDependency policy and gameplay acceptance remain unresolved. No deployment or upload.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)
