"""Catalogued assets and explicit, recoverable repo/editor handoffs. No deployment."""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import time
import uuid


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def checksum(path):
    if not Path(path).is_file():
        return None
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def safe_path(root, relative):
    root = Path(root).resolve()
    relative = Path(relative)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError(f'Expected a contained relative path: {relative}')
    target = root / relative
    for part in [target, *target.parents]:
        if part == root:
            break
        if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
            raise ValueError(f'Linked asset path is not supported: {part}')
    if not target.resolve().is_relative_to(root):
        raise ValueError(f'Path escapes managed root: {target}')
    return target


def catalog(root):
    result = read(Path(root) / 'asset-catalog.json')
    if result.get('schemaVersion') != 1:
        raise ValueError('Unsupported asset catalog schema')
    safe_path(root, result['runtimeRoot'])
    ids, paths = set(), set()
    for group in result['groups']:
        if group['id'] in ids or group['package'] not in ('main', 'textures'):
            raise ValueError('Duplicate asset group or unknown package')
        ids.add(group['id'])
        for name in group['files']:
            safe_path(root, name)
            key = name.casefold()
            if key in paths:
                raise ValueError(f'Duplicate/case-colliding catalog path: {name}')
            paths.add(key)
    return result


def runtime_root(root, package='main'):
    data = catalog(root)
    return safe_path(root, data.get('packageRoots', {}).get(package, data['runtimeRoot']))


def locations(root, settings, data, include_sources=False):
    for group in data['groups']:
        runtime = safe_path(root, data.get('packageRoots', {}).get(group['package'], data['runtimeRoot']))
        stage_key = 'vortex' if group['package'] == 'main' else 'vortexTextures'
        for name in group['files']:
            paths = {'repo': safe_path(runtime, name),
                     'vortex': safe_path(settings['roots'][stage_key], name),
                     'live': safe_path(settings['roots']['live'], name)}
            if editor := group.get('editor'):
                tail = Path(name).relative_to(editor['stripPrefix']) if editor['stripPrefix'] else Path(name)
                paths['editor'] = safe_path(settings['roots'][editor['root']], Path(editor['base']) / tail)
            yield {'scope': group['scope'], 'group': group['id'], 'file': name,
                   'kind': 'runtime', 'package': group['package'], 'paths': paths}
    if include_sources:
        for group in data['sources']:
            repo_dir = safe_path(root, group['repo'])
            editor_dir = safe_path(settings['roots'][group['editorRoot']], group['editor'])
            names = set()
            # Overlay sources intentionally track only the mod's subset of a full editor extraction.
            for base in ((repo_dir,) if group.get('mode') == 'overlay' else (repo_dir, editor_dir)):
                for pattern in group['patterns']:
                    safe_path(base, pattern)
                    names.update(p.relative_to(base).as_posix() for p in base.glob(pattern) if p.is_file())
            for name in sorted(names):
                yield {'scope': group['scope'], 'group': group['id'], 'file': group['repo'] + '/' + name,
                       'kind': 'source', 'paths': {'repo': safe_path(repo_dir, name),
                                                  'editor': safe_path(editor_dir, name)}}


def comparison_stages(root, settings):
    """Resolve verified selected stages once per audit; never hide selected-stage drift."""
    stages = {package: Path(settings['roots'][key]) for package, key in
              [('main', 'vortex'), ('textures', 'vortexTextures')]}
    if (Path(root) / '.vdb/selected.json').is_file():
        import vdb_workflow
        for package in stages:
            selected = vdb_workflow.selected_source(Path(root), settings, package)
            if selected is not None:
                stages[package] = selected / 'mod'
    return stages


def status(root, settings, scope='all', include_sources=False):
    data = catalog(root)
    stages = comparison_stages(root, settings)
    rows = []
    for row in locations(root, settings, data, include_sources):
        if scope not in ('all', row['scope'], row['group']):
            continue
        if row['kind'] == 'runtime':
            row['paths']['vortex'] = safe_path(stages[row['package']], row['file'])
        hashes = {key: checksum(path) for key, path in row['paths'].items()}
        state = 'Match' if None not in hashes.values() and len(set(hashes.values())) == 1 else 'Review'
        equivalence = next((item for item in data.get('equivalences', [])
                            if item['file'] == row['file'] and None not in hashes.values()
                            and set(hashes.values()) <= set(item['hashes'])), None)
        if state == 'Review' and equivalence:
            state = equivalence['state']
        rows.append({**row, 'paths': {key: str(path) for key, path in row['paths'].items()},
                     'hashes': hashes, 'state': state})
    return rows


def inventory_review(root, settings):
    data = catalog(root)
    stages = comparison_stages(root, settings)
    manifest = read(Path(root) / 'mod.json')
    owned = {name for group in data['groups'] for name in group['files']}
    external = {item['path']: item['owner'] for item in data.get('externalFiles', [])}
    locations_to_scan = {'repo': runtime_root(root), 'repo-textures': runtime_root(root, 'textures'),
                         'vortex': stages['main'],
                         'textures': stages['textures'],
                         'live': Path(settings['roots']['live'])}
    findings = []
    if runtime_root(root) != Path(root).resolve():
        # Old editor buffers or an obsolete script must not silently recreate a
        # second runtime tree after the migration.
        for pattern in [*manifest['runtimePatterns'], 'menu/hi/*']:
            for path in Path(root).glob(pattern):
                if path.is_file():
                    safe_path(root, path.relative_to(root))
                    findings.append({'location': 'repo-retired', 'file': path.relative_to(root).as_posix(),
                                     'state': 'Uncatalogued', 'owner': None})
    for role, base in locations_to_scan.items():
        actual = set()
        for pattern in [*manifest['runtimePatterns'], 'menu/hi/*']:
            for path in base.glob(pattern):
                if path.is_file():
                    safe_path(base, path.relative_to(base))
                    actual.add(path.relative_to(base).as_posix())
        expected = owned if role in ('repo', 'repo-textures', 'live') else {
            name for group in data['groups'] if group['package'] == ('textures' if role == 'textures' else 'main')
            for name in group['files']}
        for name in sorted(actual - expected):
            findings.append({'location': role, 'file': name,
                             'state': 'External-owned' if role == 'live' and name in external else 'Uncatalogued',
                             'owner': external.get(name) if role == 'live' else None})
    return findings


def save(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + '.writing')
    with temporary.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
    os.replace(temporary, path)


@contextmanager
def lock(root):
    directory = safe_path(root, '.sovereign')
    directory.mkdir(exist_ok=True)
    path = directory / 'accept.lock'
    with path.open('x', encoding='utf-8') as stream:
        json.dump({'pid': os.getpid(), 'started': time.time()}, stream)
    try:
        yield
    finally:
        path.unlink()


def validate_talk_qualification(root, settings, source, qualification):
    if source != 'repo' or not qualification:
        raise ValueError('Talk handoff requires repo sources and a current qualify-talk receipt')
    base = safe_path(root, '.codex-temp/talk-qualifications')
    path = Path(qualification).absolute()
    if not path.is_relative_to(base):
        raise ValueError('Expected a repo-local talk qualification receipt')
    path = safe_path(base, path.relative_to(base))
    proof = read(path)
    if proof.get('kind') != 'talk-roundtrip' or proof.get('status') != 'qualified':
        raise ValueError('Talk roundtrip did not qualify')
    data = catalog(root)
    wanted = {str(row['paths']['repo']) for row in locations(root, settings, data, True) if row['scope'] == 'talk'}
    if set(proof['files']) != wanted or any(checksum(p) != h for p, h in proof['files'].items()):
        raise ValueError('Talk inputs/membership changed since qualification')
    if any(checksum(p) != h for p, h in proof['tools'].items()):
        raise ValueError('Talk tools changed since qualification')
    if proof['catalogHash'] != fingerprint(data) or proof['settingsHash'] != fingerprint(settings):
        raise ValueError('Talk catalog/settings changed since qualification')
    return {'path': str(path), 'sha256': checksum(path)}


def validate_player_qualification(root, settings, source, qualification):
    if not qualification:
        raise ValueError('Player handoff requires a current player_workflow qualification receipt')
    base = safe_path(root, '.codex-temp/player-qualifications')
    path = Path(qualification).absolute()
    if not path.is_relative_to(base):
        raise ValueError('Expected a repo-local player qualification receipt')
    path = safe_path(base, path.relative_to(base))
    proof = read(path)
    data = catalog(root)
    if proof.get('kind') != 'player-roundtrip' or proof.get('status') != 'qualified' or proof.get('sourceRole') != source:
        raise ValueError('Player roundtrip/source role did not qualify')
    if proof['catalogHash'] != fingerprint(data) or proof['settingsHash'] != fingerprint(settings):
        raise ValueError('Player catalog/settings changed since qualification')
    wanted = {str(row['paths'].get(source, row['paths']['repo'])) for row in locations(root, settings, data, True)
              if row['scope'] in ('hks', 'animations')}
    if set(proof['files']) != wanted or any(checksum(p) != h for p, h in proof['files'].items()):
        raise ValueError('Player inputs/membership changed since qualification')
    if any(checksum(p) != h for p, h in proof['tools'].items()):
        raise ValueError('Player tools changed since qualification')
    if list(Path(settings['roots']['animations']).glob('c0000*.dsaproj')):
        raise ValueError('A DSAnimStudio project appeared; reconcile it before handoff')
    return {'path': str(path), 'sha256': checksum(path)}


def matches_scope(data, scope, row):
    if scope.startswith('file:'):
        name = scope[5:]
        owners = [group for group in data['groups'] if name in group['files']]
        if len(owners) != 1 or owners[0].get('recipe') != 'fmg':
            raise ValueError('Single-file scope requires a catalog-owned FMG binder')
        return row['kind'] == 'runtime' and row['file'] == name
    scopes = data.get('coordinatedScopes', {}).get(scope, [scope])
    return row['scope'] in scopes or row['group'] in scopes


def sync_state(root):
    path = safe_path(root, '.sovereign/editor-sync.json')
    state = read(path) if path.exists() else {'schemaVersion': 1, 'pairs': {}}
    if state.get('schemaVersion') != 1 or not isinstance(state.get('pairs'), dict):
        raise ValueError('Invalid editor sync baseline; inspect .sovereign/editor-sync.json')
    return state


def sync_pair(repo, editor):
    # Paths identify each pair, so changing a configured workspace cannot reuse its history.
    return fingerprint([str(Path(repo).resolve()).casefold(), str(Path(editor).resolve()).casefold()])


def check_sync_conflicts(root, settings, scope, source, require_known=False):
    state = sync_state(root)
    data = catalog(root)
    destination = 'editor' if source == 'repo' else 'repo'
    for row in locations(root, settings, data, True):
        if scope != 'all' and not matches_scope(data, scope, row):
            continue
        paths = row['paths']
        if 'editor' not in paths:
            continue
        src, dst = checksum(paths[source]), checksum(paths[destination])
        if src == dst:
            continue
        baseline = state['pairs'].get(sync_pair(paths['repo'], paths['editor']))
        if baseline is None:
            if require_known and dst is not None:
                raise ValueError(f'No shared sync baseline for {row["file"]}; review a scoped '
                                 'accept-plan/accept handoff before automatic propagation')
            continue
        if not re.fullmatch(r'[0-9a-f]{64}', baseline.get('sha256', '')):
            raise ValueError('Invalid content hash in editor sync baseline')
        if dst != baseline['sha256']:
            reason = 'selected source is stale' if src == baseline['sha256'] else 'both sides changed'
            raise ValueError(f'Sync conflict ({reason}): {row["file"]}. Reconcile the contents, '
                             'then use accept-plan --resolve-conflicts with the reviewed source. '
                             'No files were copied.')


def record_sync_guards(root, guards, source):
    state = sync_state(root)
    for row in guards:
        src, dst = Path(row['source']), Path(row['destination'])
        if checksum(src) != row['after'] or checksum(dst) != row['after']:
            raise ValueError('Cannot record a sync baseline for differing or missing files')
        repo, editor = (src, dst) if source == 'repo' else (dst, src)
        state['pairs'][sync_pair(repo, editor)] = {
            'repo': str(repo), 'editor': str(editor), 'sha256': row['after']}
    save(safe_path(root, '.sovereign/editor-sync.json'), state)


def record_sync_baseline(root, settings, scope='all'):
    # Explicitly record only observed equality; never infer a winner from dates/history.
    with lock(root):
        data = catalog(root)
        guards, skipped = [], []
        for row in locations(root, settings, data, True):
            if (scope != 'all' and not matches_scope(data, scope, row)) or 'editor' not in row['paths']:
                continue
            repo, editor = row['paths']['repo'], row['paths']['editor']
            value = checksum(repo)
            if value is not None and value == checksum(editor):
                guards.append({'source': str(repo), 'destination': str(editor), 'after': value})
            else:
                skipped.append(row['file'])
        record_sync_guards(root, guards, 'repo')
        return {'recorded': len(guards), 'skipped': skipped}


def prepare_handoff(root, settings, scope, source, qualification=None, resolve_conflicts=False):
    if scope == 'all' or source not in ('repo', 'editor'):
        raise ValueError('Choose a specific scope and --from repo or editor')
    data = catalog(root)
    if scope in {group['id'] for group in data['sources']}:
        raise ValueError('Choose the whole coordinated scope, not a source-only group')
    scopes = data.get('coordinatedScopes', {}).get(scope, [scope])
    player = any(s in ('animations', 'hks', 'player-names', 'player-scripts') for s in scopes)
    proof = validate_talk_qualification(root, settings, source, qualification) if 'talk' in scopes else None
    if 'events' in scopes:
        import event_workflow
        qualification = qualification or event_workflow.qualify(root, settings, source)
        proof = event_workflow.validate(root, settings, source, qualification)
    if player:
        if set(scopes) != {'hks', 'animations'}:
            raise ValueError('Player scope must include HKS, names, animations and graph sources together')
        proof = validate_player_qualification(root, settings, source, qualification)
    destination = 'editor' if source == 'repo' else 'repo'
    entries, guards, destinations = [], [], {}
    for row in locations(root, settings, data, True):
        if not matches_scope(data, scope, row):
            continue
        if source not in row['paths'] or destination not in row['paths']:
            continue
        src, dst = row['paths'][source], row['paths'][destination]
        after, before = checksum(src), checksum(dst)
        if after is None:
            raise ValueError(f'Missing {source} source: {src}; no deletion or replacement inferred')
        guards.append({'source': str(src), 'destination': str(dst), 'before': before, 'after': after})
        if str(dst) in destinations:
            if destinations[str(dst)] != after:
                raise ValueError(f'Conflicting source/runtime outputs for {dst}; rebuild and reconcile first')
            continue
        destinations[str(dst)] = after
        if after != before:
            entries.append({'group': row['group'], 'kind': row['kind'], 'source': str(src),
                            'destination': str(dst), 'before': before, 'after': after})
    if not entries:
        raise ValueError('No differing files with a configured handoff destination in this scope')
    if not resolve_conflicts:
        check_sync_conflicts(root, settings, scope, source)
    directory = safe_path(root, '.sovereign/handoffs/' + uuid.uuid4().hex)
    directory.mkdir(parents=True)
    document = {'schemaVersion': 1, 'status': 'planned', 'scope': scope, 'sourceRole': source,
                'root': str(Path(root).resolve()), 'catalogHash': fingerprint(data),
                'settingsHash': fingerprint(settings), 'entries': entries, 'guards': guards,
                'qualification': proof, 'resolveConflicts': resolve_conflicts,
                'note': 'Exact-byte source acceptance only; inspect semantics and build evidence before applying. No stage/live writes.'}
    save(directory / 'receipt.json', document)
    return directory / 'receipt.json'


def validate_receipt(root, settings, path, restoring=False):
    path = Path(path).absolute()
    base = safe_path(root, '.sovereign/handoffs')
    if not path.is_relative_to(base):
        raise ValueError('Handoff receipt must be in this repo\'s durable handoff directory')
    path = safe_path(base, path.relative_to(base))
    document = read(path)
    if (document['root'] != str(Path(root).resolve()) or document['settingsHash'] != fingerprint(settings)
            or document['catalogHash'] != fingerprint(catalog(root))):
        raise ValueError('Catalog, paths or repository changed since handoff planning')
    data = catalog(root)
    source = document['sourceRole']
    if source not in ('repo', 'editor') or document['schemaVersion'] != 1:
        raise ValueError('Invalid handoff schema or source role')
    if not isinstance(document.get('resolveConflicts', False), bool):
        raise ValueError('Conflict resolution must be an explicit boolean')
    destination = 'editor' if source == 'repo' else 'repo'
    scope = document['scope']
    if scope in {group['id'] for group in data['sources']}:
        raise ValueError('Source-only handoffs cannot bypass coordinated scope requirements')
    scopes = data.get('coordinatedScopes', {}).get(scope, [scope])
    if 'all' in scopes:
        raise ValueError('This scope requires its documented coordinated handoff recipe')
    if 'talk' in scopes and not restoring:
        proof = document.get('qualification') or {}
        if checksum(proof.get('path', '')) != proof.get('sha256') or validate_talk_qualification(root, settings, source, proof.get('path')) != proof:
            raise ValueError('Talk qualification changed since planning')
    if 'events' in scopes and not restoring:
        import event_workflow
        proof = document.get('qualification') or {}
        if event_workflow.validate(root, settings, source, proof.get('path')) != proof:
            raise ValueError('Event qualification changed since planning')
    if any(s in ('animations', 'hks', 'player-names', 'player-scripts') for s in scopes):
        if set(scopes) != {'hks', 'animations'}:
            raise ValueError('Incomplete coordinated player scope')
        if not restoring:
            proof = document.get('qualification') or {}
            if checksum(proof.get('path', '')) != proof.get('sha256') or validate_player_qualification(root, settings, source, proof.get('path')) != proof:
                raise ValueError('Player qualification changed since planning')
    allowed = {(str(row['paths'][source]), str(row['paths'][destination]), row['group'], row['kind'])
               for row in locations(root, settings, data, True)
               if matches_scope(data, scope, row)
               and source in row['paths'] and destination in row['paths']}
    pairs = {(src, dst) for src, dst, _, _ in allowed}
    seen = set()
    guard_rows = {(r['source'], r['destination'], r['before'], r['after']) for r in document['guards']}
    for row in document['entries']:
        if (row['source'], row['destination'], row['group'], row['kind']) not in allowed:
            raise ValueError('Handoff contains an unmanaged source/destination pair')
        if row['destination'] in seen:
            raise ValueError('Handoff repeats a destination')
        seen.add(row['destination'])
        if (row['source'], row['destination'], row['before'], row['after']) not in guard_rows:
            raise ValueError('Handoff entry differs from its input guard')
        for key in ('before', 'after'):
            if not (key == 'before' and row[key] is None) and not re.fullmatch(r'[0-9a-f]{64}', row[key] or ''):
                raise ValueError('Invalid handoff content hash')
        for key in ('backup', 'candidate'):
            if key in row:
                safe_path(path.parent, row[key])
    for row in document['guards']:
        if (row['source'], row['destination']) not in pairs:
            raise ValueError('Unmanaged handoff guard')
    if {(r['source'], r['destination']) for r in document['guards']} != pairs:
        raise ValueError('Handoff scope membership changed since planning')
    return path, document


def apply_handoff(root, settings, path):
    with lock(root):
        path, document = validate_receipt(root, settings, path)
        if document['status'] != 'planned':
            raise ValueError('Handoff is no longer planned; inspect its receipt before retrying')
        for row in document['guards']:
            if checksum(row['source']) != row['after'] or checksum(row['destination']) != row['before']:
                raise ValueError('Source/destination changed since plan: ' + row['destination'])
        if not document.get('resolveConflicts', False):
            check_sync_conflicts(root, settings, document['scope'], document['sourceRole'])
        # Finish independent backups and candidate copies before the first destination mutation.
        for i, row in enumerate(document['entries']):
            candidate = path.parent / f'{i:05d}-after.bin'
            shutil.copy2(row['source'], candidate)
            if checksum(candidate) != row['after']:
                raise ValueError('Source changed while preparing the handoff')
            row['candidate'] = candidate.name
            if row['before'] is not None:
                backup = path.parent / f'{i:05d}-before.bin'
                shutil.copy2(row['destination'], backup)
                if checksum(backup) != row['before']:
                    raise ValueError('Destination changed while backing up the handoff')
                row['backup'] = backup.name
        document['status'] = 'applying'
        save(path, document)
        try:
            for row in document['entries']:
                if checksum(row['source']) != row['after'] or checksum(row['destination']) != row['before']:
                    raise ValueError('Source/destination drift during acceptance: ' + row['destination'])
                dst = Path(row['destination'])
                dst.parent.mkdir(parents=True, exist_ok=True)
                temporary = dst.with_name(dst.name + '.sovereign-accepting')
                with temporary.open('xb') as stream, safe_path(path.parent, row['candidate']).open('rb') as source:
                    shutil.copyfileobj(source, stream)
                if checksum(temporary) != row['after']:
                    raise ValueError('Candidate copy verification failed')
                os.replace(temporary, dst)  # Never truncate an existing shared hardlink.
                row['applied'] = True
                save(path, document)
                if checksum(dst) != row['after']:
                    raise ValueError('Accepted file verification failed')
            if any(checksum(row['source']) != row['after'] or checksum(row['destination']) != row['after']
                   for row in document['guards']):
                raise ValueError('Source/companion changed before handoff verification finished')
            validate_receipt(root, settings, path)
            record_sync_guards(root, document['guards'], document['sourceRole'])
            document['status'] = 'complete'
        except Exception as error:
            document.update(status='interrupted', error=str(error))
            raise
        finally:
            save(path, document)
    return document


def restore_handoff(root, settings, path):
    with lock(root):
        path, document = validate_receipt(root, settings, path, restoring=True)
        if document['status'] not in ('complete', 'interrupted', 'applying'):
            raise ValueError('Only an applied/interrupted handoff can be restored')
        applied = [r for r in document['entries'] if checksum(r['destination']) == r['after']]
        for row in document['entries']:
            if checksum(row['destination']) not in (row['before'], row['after']):
                raise ValueError('Destination changed after handoff; restore refused')
            if row['before'] is not None and checksum(safe_path(path.parent, row['backup'])) != row['before']:
                raise ValueError('Recovery copy differs from receipt')
        for row in reversed(applied):
            dst = Path(row['destination'])
            if checksum(dst) != row['after']:
                raise ValueError('Destination drift during restore')
            if row['before'] is None:
                dst.unlink()
            else:
                temporary = dst.with_name(dst.name + '.sovereign-restoring')
                with temporary.open('xb') as stream, safe_path(path.parent, row['backup']).open('rb') as source:
                    shutil.copyfileobj(source, stream)
                if checksum(temporary) != row['before']:
                    raise ValueError('Recovery copy changed during restore')
                os.replace(temporary, dst)
            if checksum(dst) != row['before']:
                raise ValueError('Restore verification failed')
        document['status'] = 'restored'
        save(path, document)
    return document
