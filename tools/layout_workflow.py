"""Plan and recover the one-time, byte-preserving Sovereign mod/src migration."""
from __future__ import annotations

import argparse
import copy
import os
from pathlib import Path
import shutil
import sys
import uuid

import asset_workflow as assets

ROOT = Path(__file__).resolve().parents[1]
SOURCE_TARGETS = {
    'event-sources': 'src/events',
    'sfx-sources': 'src/sfx/sfxbnd_commoneffects-ffxbnd-dcx-wffxbnd',
    'row-names': 'src/smithbox/Project',
}


def target_catalog(original):
    result = copy.deepcopy(original)
    if original['runtimeRoot'] != '.' or original.get('packageRoots'):
        raise ValueError('Expected the original root layout; inspect before another migration')
    result['runtimeRoot'] = 'mod'
    result['packageRoots'] = {'textures': 'packages/textures/mod'}
    for group in result['sources']:
        if group['repo'].startswith('src/'):
            continue
        if group['id'] in SOURCE_TARGETS:
            group['repo'] = SOURCE_TARGETS[group['id']]
        elif group['id'].startswith('talk-source-'):
            group['repo'] = 'src/talk/' + Path(group['repo']).name
        else:
            raise ValueError('Unclassified source group: ' + group['id'])
    return result


def plan(root):
    original = assets.catalog(root)
    candidate = target_catalog(original)
    moves = []
    for group in original['groups']:
        target = candidate.get('packageRoots', {}).get(group['package'], candidate['runtimeRoot'])
        for name in group['files']:
            moves.append({'before': name, 'after': target + '/' + name, 'kind': 'runtime', 'group': group['id']})
    for old, new in zip(original['sources'], candidate['sources']):
        if old['repo'] == new['repo']:
            continue
        source = assets.safe_path(root, old['repo'])
        for path in sorted(source.rglob('*')):
            assets.safe_path(root, path.relative_to(root))
            if path.is_file():
                moves.append({'before': path.relative_to(root).as_posix(),
                              'after': new['repo'] + '/' + path.relative_to(source).as_posix(),
                              'kind': 'source', 'group': old['id']})
    seen = set()
    for row in moves:
        before, after = assets.safe_path(root, row['before']), assets.safe_path(root, row['after'])
        if after.exists() or row['after'].casefold() in seen:
            raise ValueError('Existing/colliding migration target: ' + str(after))
        seen.add(row['after'].casefold())
        row.update(sha256=assets.checksum(before), size=before.stat().st_size)
        if row['sha256'] is None:
            raise ValueError('Missing migration source: ' + str(before))
    directory = assets.safe_path(root, '.sovereign/layout/' + uuid.uuid4().hex)
    directory.mkdir(parents=True)
    document = {'schemaVersion': 2, 'status': 'planned', 'originalCatalog': original,
                'candidateCatalog': candidate, 'catalogFileHash': assets.checksum(root / 'asset-catalog.json'),
                'moves': moves, 'note': 'Apply only after VDB switch/rollback and replacement caller qualification. No files moved.'}
    assets.save(directory / 'receipt.json', document)
    return directory / 'receipt.json'


def load(root, receipt):
    base = assets.safe_path(root, '.sovereign/layout')
    path = Path(receipt).absolute()
    if not path.is_relative_to(base):
        raise ValueError('Use a receipt under this repository .sovereign/layout')
    path = assets.safe_path(base, path.relative_to(base))
    doc = assets.read(path)
    if doc.get('schemaVersion') != 2 or doc['candidateCatalog'] != target_catalog(doc['originalCatalog']):
        raise ValueError('Unexpected migration schema or catalog change')
    old_groups = {g['id']: g for g in doc['originalCatalog']['groups'] + doc['originalCatalog']['sources']}
    new_sources = {g['id']: g for g in doc['candidateCatalog']['sources']}
    expected_runtime = {(g['id'], name) for g in doc['originalCatalog']['groups'] for name in g['files']}
    actual_runtime, seen_before, seen_after = set(), set(), set()
    for row in doc['moves']:
        for key, seen in (('before', seen_before), ('after', seen_after)):
            assets.safe_path(root, row[key])
            if row[key].casefold() in seen:
                raise ValueError('Duplicate migration path')
            seen.add(row[key].casefold())
        group = old_groups[row['group']]
        if row['kind'] == 'runtime':
            actual_runtime.add((group['id'], row['before']))
            target = doc['candidateCatalog']['packageRoots'].get(group['package'], 'mod') + '/' + row['before']
        elif row['kind'] == 'source':
            suffix = Path(row['before']).relative_to(group['repo'])
            target = (Path(new_sources[group['id']]['repo']) / suffix).as_posix()
        else:
            raise ValueError('Unknown migration entry kind')
        if row['after'] != target:
            raise ValueError('Migration path is outside its catalog mapping')
    if actual_runtime != expected_runtime or seen_before & seen_after:
        raise ValueError('Incomplete or overlapping migration paths')
    return path, doc


def check_original(root, doc):
    if assets.checksum(root / 'asset-catalog.json') != doc['catalogFileHash']:
        raise ValueError('Catalog changed after migration planning')
    expected_sources = {r['before'] for r in doc['moves'] if r['kind'] == 'source'}
    current_sources = set()
    for old, new in zip(doc['originalCatalog']['sources'], doc['candidateCatalog']['sources']):
        if old['repo'] == new['repo']:
            continue
        base = assets.safe_path(root, old['repo'])
        for entry in base.rglob('*'):
            assets.safe_path(root, entry.relative_to(root))
            if entry.is_file():
                current_sources.add(entry.relative_to(root).as_posix())
    if current_sources != expected_sources:
        raise ValueError('Source membership changed after migration planning')
    for row in doc['moves']:
        if (assets.checksum(assets.safe_path(root, row['before'])) != row['sha256']
                or assets.safe_path(root, row['after']).exists()):
            raise ValueError('Migration source changed or target exists: ' + row['before'])


def apply(root, receipt):
    with assets.lock(root):
        path, doc = load(root, receipt)
        if doc['status'] != 'planned':
            raise ValueError('Migration already started; inspect or restore its existing receipt')
        check_original(root, doc)
        backup = path.parent / 'backup'
        backup.mkdir()
        shutil.copy2(root / 'asset-catalog.json', backup / 'asset-catalog.json')
        for row in doc['moves']:
            saved = assets.safe_path(backup, row['before'])
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(assets.safe_path(root, row['before']), saved)
            if assets.checksum(saved) != row['sha256']:
                raise ValueError('Backup verification failed: ' + row['before'])
        check_original(root, doc)
        doc['status'] = 'applying'
        assets.save(path, doc)
        try:
            for row in doc['moves']:
                before, after = assets.safe_path(root, row['before']), assets.safe_path(root, row['after'])
                if assets.checksum(before) != row['sha256'] or after.exists():
                    raise ValueError('File changed during migration: ' + row['before'])
                after.parent.mkdir(parents=True, exist_ok=True)
                before.rename(after)
            if any(assets.checksum(assets.safe_path(root, r['after'])) != r['sha256'] for r in doc['moves']):
                raise ValueError('Migrated output verification failed')
            if assets.checksum(root / 'asset-catalog.json') != doc['catalogFileHash']:
                raise ValueError('Catalog changed during migration')
            assets.save(root / 'asset-catalog.json', doc['candidateCatalog'])
            doc.update(status='complete', note='All listed files moved without byte changes. Historical receipts retain old paths; this manifest supplies the relocation map.')
            assets.save(path, doc)
        except BaseException:
            doc['status'] = 'interrupted'
            assets.save(path, doc)
            raise
    return doc


def restore(root, receipt):
    with assets.lock(root):
        path, doc = load(root, receipt)
        if doc['status'] not in ('applying', 'interrupted', 'complete', 'restoring'):
            raise ValueError('No applied migration to restore')
        if assets.catalog(root) not in (doc['originalCatalog'], doc['candidateCatalog']):
            raise ValueError('Catalog has later edits; reconcile before restoration')
        saved_catalog = path.parent / 'backup/asset-catalog.json'
        if assets.checksum(saved_catalog) != doc['catalogFileHash']:
            raise ValueError('Original catalog backup changed')
        pending = []
        for row in doc['moves']:
            before, after = assets.safe_path(root, row['before']), assets.safe_path(root, row['after'])
            if before.exists() and not after.exists() and assets.checksum(before) == row['sha256']:
                continue
            if before.exists() or assets.checksum(after) != row['sha256']:
                raise ValueError('Later edit or missing file; reconcile before restoration: ' + row['after'])
            pending.append((before, after, row['sha256']))
        doc['status'] = 'restoring'
        assets.save(path, doc)
        for before, after, expected in reversed(pending):
            if before.exists() or assets.checksum(after) != expected:
                raise ValueError('File changed during restoration: ' + str(after))
            before.parent.mkdir(parents=True, exist_ok=True)
            after.rename(before)
        if assets.catalog(root) not in (doc['originalCatalog'], doc['candidateCatalog']):
            raise ValueError('Catalog changed during restoration')
        temporary = root / 'asset-catalog.json.restoring'
        with saved_catalog.open('rb') as incoming, temporary.open('xb') as outgoing:
            shutil.copyfileobj(incoming, outgoing)
        os.replace(temporary, root / 'asset-catalog.json')
        if any(assets.checksum(assets.safe_path(root, r['before'])) != r['sha256'] for r in doc['moves']):
            raise ValueError('Restored file verification failed')
        doc['status'] = 'restored'
        assets.save(path, doc)
    return doc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('plan')
    for name in ('apply', 'restore'):
        commands.add_parser(name).add_argument('--receipt', required=True)
    args = parser.parse_args()
    if args.command == 'plan':
        print(plan(ROOT))
    else:
        result = (apply if args.command == 'apply' else restore)(ROOT, args.receipt)
        print(f"Layout {result['status']}: {len(result['moves'])} files; no external paths changed.")


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)
