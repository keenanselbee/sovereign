"""Freshness and reviewed handoff of recovered archive members."""
import copy
import json
from pathlib import Path

import asset_workflow as assets


def outputs(archive):
    for entry in archive.get('outputs', []) + archive.get('members', []):
        yield entry
        yield from entry.get('textures', [])


def definition(root):
    data = assets.catalog(root)
    relative = data.get('recoveredSources', {}).get('manifest')
    if relative is None:
        return None, None
    path = assets.safe_path(root, relative)
    if not path.is_relative_to(Path(root) / 'src'):
        raise ValueError('Recovered source manifest must live under src')
    if not path.is_file():
        raise ValueError('Missing recovered source manifest: ' + relative)
    doc = assets.read(path)
    validate_definition(root, doc)
    return path, doc


def validate_definition(root, doc):
    if doc.get('schemaVersion') != 1 or not isinstance(doc.get('archives'), list):
        raise ValueError('Invalid recovered source manifest')
    data = assets.catalog(root)
    owned = {str(assets.safe_path(assets.runtime_root(root, g['package']), name))
             for g in data['groups'] for name in g['files']}
    seen_runtime, seen_sources = set(), set()
    for archive in doc['archives']:
        runtime = str(assets.safe_path(root, archive['runtime']))
        if runtime not in owned or runtime in seen_runtime:
            raise ValueError('Unmanaged or duplicate recovered archive: ' + archive['runtime'])
        seen_runtime.add(runtime)
        for entry in outputs(archive):
            path = assets.safe_path(root, entry['source'])
            if not path.is_relative_to(Path(root) / 'src') or str(path) in seen_sources:
                raise ValueError('Invalid or duplicate recovered source: ' + entry['source'])
            seen_sources.add(str(path))
            if not assets.re.fullmatch(r'[a-f0-9]{64}', entry.get('sha256', '')):
                raise ValueError('Invalid recovered source hash: ' + entry['source'])
        if not assets.re.fullmatch(r'[a-f0-9]{64}', archive.get('sha256', '')):
            raise ValueError('Invalid recovered archive hash: ' + archive['runtime'])


def issues(root, runtime_paths=None):
    try:
        _, doc = definition(root)
    except (ValueError, OSError, KeyError, TypeError) as error:
        return [str(error)]
    if doc is None:
        return []
    selected = None if runtime_paths is None else {str(Path(p).resolve()) for p in runtime_paths}
    findings = []
    for archive in doc['archives']:
        runtime = assets.safe_path(root, archive['runtime'])
        if selected is not None and str(runtime.resolve()) not in selected:
            continue
        if assets.checksum(runtime) != archive['sha256']:
            findings.append('Recovered sources need reviewed handoff: ' + archive['runtime'])
        for entry in outputs(archive):
            current = assets.checksum(assets.safe_path(root, entry['source']))
            if current is None:
                findings.append('Missing recovered source: ' + entry['source'])
            elif current != entry['sha256']:
                findings.append('Edited recovered source needs matching packed output: ' + entry['source'])
    return findings


def require_fresh(root, package):
    if not (Path(root) / 'asset-catalog.json').is_file():
        return
    selected = [assets.safe_path(assets.runtime_root(root, package), name)
                for group in assets.catalog(root)['groups'] if group['package'] == package
                for name in group['files']]
    findings = issues(root, selected)
    if findings:
        raise ValueError('Source freshness blocks packaging: ' + '; '.join(findings))


def export_archive(settings, binary, archive, directory):
    import sovereign as core
    directory.mkdir(parents=True)
    spec = directory / 'archive.json'
    assets.save(spec, archive)
    helper, env = core.build_inspector(settings)
    response = core.run_process(['dotnet', helper / 'Inspect.dll', 'tracked-members', binary,
                                 spec, directory / 'output'], helper, env)
    return json.loads(response.stdout), directory / 'output'


def plan(root, settings, scope, source, directory):
    manifest_path, original = definition(root)
    if original is None:
        return None
    rows = {str(row['paths']['repo']): row for row in assets.locations(root, settings, assets.catalog(root))
            if row['kind'] == 'runtime' and assets.matches_scope(assets.catalog(root), scope, row)}
    updated = copy.deepcopy(original)
    guards, entries, inputs = [], [], []
    selected = []
    for index, archive in enumerate(original['archives']):
        runtime = assets.safe_path(root, archive['runtime'])
        row = rows.get(str(runtime))
        if row is None:
            continue
        # Unmapped assets in a mixed scope remain repository-owned.
        binary = row['paths'].get(source, runtime)
        packed_hash = assets.checksum(binary)
        if packed_hash is None:
            raise ValueError('Missing recovered archive input: ' + str(binary))
        current = {e['source']: assets.checksum(assets.safe_path(root, e['source'])) for e in outputs(archive)}
        if None in current.values():
            raise ValueError('Missing recovered source; recover/reconcile it before handoff: ' + archive['runtime'])
        inputs.append({'path': str(binary), 'sha256': packed_hash})
        selected.append(archive['runtime'])
        if packed_hash == archive['sha256'] and all(current[e['source']] == e['sha256'] for e in outputs(archive)):
            for entry in outputs(archive):
                path = str(assets.safe_path(root, entry['source']))
                guards.append(dict(source=path, destination=path, before=entry['sha256'],
                                   after=entry['sha256'], recovered=True))
            continue
        response, exported = export_archive(settings, binary, archive, directory / f'recovered-{index}')
        replacement = response['archive']
        if replacement['runtime'] != archive['runtime'] or replacement['sha256'] != packed_hash:
            raise ValueError('Recovered archive export identity mismatch')
        old_entries = {e['source']: e for e in outputs(archive)}
        new_entries = {e['source']: e for e in outputs(replacement)}
        files = {e['source']: e for e in response['files']}
        if set(old_entries) != set(new_entries) or set(files) != set(old_entries):
            raise ValueError('Recovered member membership changed; review the manifest explicitly')
        for name, old in old_entries.items():
            expected = new_entries[name]['sha256']
            candidate = assets.safe_path(exported, files[name]['candidate'])
            if assets.checksum(candidate) != expected or files[name]['sha256'] != expected:
                raise ValueError('Recovered export payload mismatch: ' + name)
            before = current[name]
            if before not in (old['sha256'], expected):
                raise ValueError('Independent recovered source edit conflicts with packed output: ' + name)
            destination = str(assets.safe_path(root, name))
            guard = dict(source=str(candidate), destination=destination, before=before, after=expected, recovered=True)
            guards.append(guard)
            if before != expected:
                entries.append(dict(guard, group='recovered-sources', kind='snapshot'))
        if assets.checksum(binary) != packed_hash:
            raise ValueError('Recovered archive changed during export')
        updated['archives'][index] = replacement
    if not selected:
        return None
    directory.mkdir(parents=True, exist_ok=True)
    definition_path = directory / 'recovered-definition.json'
    assets.save(definition_path, original)
    before = assets.checksum(manifest_path)
    if updated != original:
        next_manifest = directory / 'recovered-manifest.json'
        assets.save(next_manifest, updated)
        guard = dict(source=str(next_manifest), destination=str(manifest_path), before=before,
                     after=assets.checksum(next_manifest), recovered=True)
        entries.append(dict(guard, group='recovered-sources', kind='snapshot'))
    else:
        guard = dict(source=str(manifest_path), destination=str(manifest_path), before=before, after=before, recovered=True)
    guards.append(guard)
    return dict(definition=definition_path.name, definitionHash=assets.checksum(definition_path),
                manifest=str(manifest_path), selected=selected, inputs=inputs, entries=entries, guards=guards)


def validate_plan(root, settings, path, document):
    """Validate managed destinations and pinned candidates; normal handoff guards own drift checks."""
    recovery = document.get('recoveredSources')
    configured = assets.catalog(root).get('recoveredSources')
    if not recovery:
        if configured and document.get('status') == 'planned':
            # Old plans must not bypass newly enabled source checks.
            relevant = [r['paths']['repo'] for r in assets.locations(root, settings, assets.catalog(root))
                        if r['kind'] == 'runtime' and assets.matches_scope(assets.catalog(root), document['scope'], r)]
            errors = issues(root, relevant)
            if errors:
                raise ValueError('; '.join(errors))
        return set(), set()
    pinned = assets.safe_path(path.parent, recovery['definition'])
    if assets.checksum(pinned) != recovery['definitionHash']:
        raise ValueError('Recovered definition changed since handoff planning')
    original = assets.read(pinned)
    validate_definition(root, original)
    manifest_path, _ = definition(root)
    if str(manifest_path) != recovery['manifest']:
        raise ValueError('Recovered manifest mapping changed')
    rows = {str(r['paths']['repo']): r for r in assets.locations(root, settings, assets.catalog(root))
            if r['kind'] == 'runtime' and assets.matches_scope(assets.catalog(root), document['scope'], r)}
    selected = [a for a in original['archives'] if str(assets.safe_path(root, a['runtime'])) in rows]
    if recovery['selected'] != [a['runtime'] for a in selected]:
        raise ValueError('Recovered handoff scope changed')
    expected_inputs = {str(rows[str(assets.safe_path(root, a['runtime']))]['paths'].get(
        document['sourceRole'], assets.safe_path(root, a['runtime']))) for a in selected}
    if {g['path'] for g in recovery['inputs']} != expected_inputs:
        raise ValueError('Recovered archive input mapping changed')
    destinations = {str(assets.safe_path(root, e['source'])) for a in selected for e in outputs(a)} | {str(manifest_path)}
    if {g['destination'] for g in recovery['guards']} != destinations or len(recovery['guards']) != len(destinations):
        raise ValueError('Recovered source guard membership changed')
    pairs, allowed = set(), set()
    for guard in recovery['guards']:
        src, dst = Path(guard['source']), Path(guard['destination'])
        if src != dst:
            assets.safe_path(path.parent, src.relative_to(path.parent))
        if not guard.get('recovered') or guard not in document['guards']:
            raise ValueError('Recovered guard missing from coordinated handoff')
        pairs.add((str(src), str(dst)))
        if guard['before'] != guard['after']:
            expected = dict(guard, group='recovered-sources', kind='snapshot')
            if not any(all(row.get(k) == v for k, v in expected.items()) for row in document['entries']):
                raise ValueError('Recovered update missing from handoff')
            allowed.add((str(src), str(dst), 'recovered-sources', 'snapshot'))
    return allowed, pairs


def check_inputs(document):
    for guard in document.get('recoveredSources', {}).get('inputs', []):
        if assets.checksum(guard['path']) != guard['sha256']:
            raise ValueError('Recovered archive input changed since planning: ' + guard['path'])
