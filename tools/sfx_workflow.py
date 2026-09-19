"""Build external SFX sources and save their packed editor output with recovery."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys
import uuid

import asset_workflow as assets
import format_workflow as formats

ROOT = Path(__file__).resolve().parents[1]


def editor_target(root, settings):
    matches = [row for row in assets.locations(root, settings, assets.catalog(root))
               if row['scope'] == 'sfx' and 'editor' in row['paths']]
    if len(matches) != 1:
        raise ValueError('Expected one catalogued SFX editor output')
    return matches[0]['paths']['editor']


def validate_build(root, settings, receipt):
    base = assets.safe_path(root, '.codex-temp/sfx-builds')
    path = Path(receipt).absolute()
    if not path.is_relative_to(base):
        raise ValueError('Use an isolated SFX build receipt from this repository')
    path = assets.safe_path(base, path.relative_to(base))
    result = assets.read(path)
    target = editor_target(root, settings)
    if (result.get('kind') != 'sfx-build' or result.get('sourceRole') != 'editor'
            or result['status'] != 'candidate' or Path(result['baselineFile']) != target
            or result['catalogHash'] != assets.fingerprint(assets.catalog(root))
            or result['settingsHash'] != assets.fingerprint(settings)):
        raise ValueError('SFX build role, paths or configuration changed')
    candidate = assets.safe_path(path.parent, target.name)
    if Path(result['candidate']) != candidate or assets.checksum(candidate) != result['sha256']:
        raise ValueError('SFX candidate changed or has an unexpected path')
    inputs = assets.read(path.parent / 'complete-source.json')
    group = next(g for g in assets.catalog(root)['sources'] if g['id'] == 'sfx-sources')
    complete = assets.safe_path(settings['roots'][group['editorRoot']], group['editor'])
    if Path(inputs['root']) != complete or formats.tree(complete) != inputs['files']:
        raise ValueError('SFX source membership or bytes changed after rebuilding')
    if any(assets.checksum(p) != h for p, h in result['toolFiles'].items()):
        raise ValueError('SFX tools changed after rebuilding')
    if assets.checksum(target) != result['sourceHash']:
        raise ValueError('Packed editor output changed after rebuilding')
    return path, result, target, candidate


def save_build(root, settings, receipt):
    with assets.lock(root):
        path, result, target, candidate = validate_build(root, settings, receipt)
        directory = assets.safe_path(root, '.sovereign/sfx-builds/' + uuid.uuid4().hex)
        directory.mkdir(parents=True)
        doc = {'kind': 'sfx-editor-save', 'status': 'prepared', 'destination': str(target),
               'before': result['sourceHash'], 'after': result['sha256'],
               'settingsHash': assets.fingerprint(settings), 'catalogHash': result['catalogHash'],
               'buildReceipt': str(path), 'note': 'Packed editor output only; repo acceptance/deployment are separate.'}
        for source, name in ((candidate, 'after.bin'), (path, 'build.json'),
                             (path.parent / 'complete-source.json', 'complete-source.json')):
            shutil.copy2(source, directory / name)
        if doc['before'] is not None:
            shutil.copy2(target, directory / 'before.bin')
            if assets.checksum(directory / 'before.bin') != doc['before']:
                raise ValueError('SFX backup changed while copying')
        if assets.checksum(directory / 'after.bin') != doc['after']:
            raise ValueError('SFX candidate backup differs')
        validate_build(root, settings, receipt)
        record = directory / 'receipt.json'
        doc['status'] = 'applying'
        assets.save(record, doc)
        try:
            if doc['before'] != doc['after']:
                temporary = target.with_name(target.name + '.sovereign-sfx-saving')
                with (directory / 'after.bin').open('rb') as source, temporary.open('xb') as output:
                    shutil.copyfileobj(source, output)
                if assets.checksum(temporary) != doc['after'] or assets.checksum(target) != doc['before']:
                    raise ValueError('SFX output changed before replacement')
                os.replace(temporary, target)
            if assets.checksum(target) != doc['after']:
                raise ValueError('Saved SFX output differs')
            doc['status'] = 'complete'
        except BaseException:
            doc['status'] = 'interrupted'
            raise
        finally:
            assets.save(record, doc)
    return record


def restore(root, settings, receipt):
    with assets.lock(root):
        base = assets.safe_path(root, '.sovereign/sfx-builds')
        path = Path(receipt).absolute()
        if not path.is_relative_to(base):
            raise ValueError('Use a durable SFX editor-save receipt')
        path = assets.safe_path(base, path.relative_to(base))
        doc = assets.read(path)
        target = editor_target(root, settings)
        if (doc.get('kind') != 'sfx-editor-save' or Path(doc['destination']) != target
                or doc['settingsHash'] != assets.fingerprint(settings)
                or doc['status'] not in ('complete', 'applying', 'interrupted')):
            raise ValueError('SFX restore identity/status changed')
        if assets.checksum(target) not in (doc['before'], doc['after']):
            raise ValueError('Packed SFX has later edits; restore refused')
        if doc['before'] is None:
            raise ValueError('Original SFX baseline is missing; inspect before removal')
        backup = path.parent / 'before.bin'
        if assets.checksum(backup) != doc['before']:
            raise ValueError('SFX restore backup differs')
        if assets.checksum(target) != doc['before']:
            temporary = target.with_name(target.name + '.sovereign-sfx-restoring')
            with backup.open('rb') as source, temporary.open('xb') as output:
                shutil.copyfileobj(source, output)
            if assets.checksum(temporary) != doc['before'] or assets.checksum(target) != doc['after']:
                raise ValueError('SFX changed during restore')
            os.replace(temporary, target)
        if assets.checksum(target) != doc['before']:
            raise ValueError('SFX restoration verification failed')
        doc['status'] = 'restored'
        assets.save(path, doc)
    return doc


def validate_saved(root, settings, receipt):
    base = assets.safe_path(root, '.sovereign/sfx-builds')
    path = Path(receipt).absolute()
    if not path.is_relative_to(base):
        raise ValueError('Use a durable SFX editor-save receipt')
    path = assets.safe_path(base, path.relative_to(base))
    doc = assets.read(path)
    if (doc.get('kind') != 'sfx-editor-save' or doc['status'] != 'complete'
            or doc['settingsHash'] != assets.fingerprint(settings)
            or Path(doc['destination']) != editor_target(root, settings)
            or assets.checksum(doc['destination']) != doc['after']):
        raise ValueError('Saved SFX output/configuration changed before source acceptance')
    inputs = assets.read(path.parent / 'complete-source.json')
    group = next(g for g in assets.catalog(root)['sources'] if g['id'] == 'sfx-sources')
    complete = assets.safe_path(settings['roots'][group['editorRoot']], group['editor'])
    if Path(inputs['root']) != complete or formats.tree(complete) != inputs['files']:
        raise ValueError('SFX source changed after the saved build; rebuild before propagation')


def build_and_save(root, settings):
    result = formats.build_sfx(root, settings, source_role='editor')
    print('SFX candidate: ' + result['receipt'], flush=True)
    receipt = save_build(root, settings, result['receipt'])
    print('SFX editor save: ' + str(receipt), flush=True)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('build-save')
    commands.add_parser('restore').add_argument('--receipt', required=True)
    args = parser.parse_args()
    settings = assets.read(ROOT / 'tools/eldenring-paths.local.json')
    if args.command == 'build-save':
        build_and_save(ROOT, settings)
    else:
        print(restore(ROOT, settings, args.receipt)['status'])


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)
