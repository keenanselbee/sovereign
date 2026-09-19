"""Review (default) or explicitly publish an exact verified Vortex release ZIP."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

import nexus_workflow as workflow
import sovereign as core


def api(method, path, body=None):
    if method != 'GET' or body is not None:
        raise ValueError('Nexus writes must use the journaled shared publishing operation')
    return workflow.automation.read(core.ROOT, path)


def verified_archive(archive, manifest, package_id='main'):
    import release_artifact
    archive, receipt = release_artifact.verify(core.ROOT, core.config(argparse.Namespace(config=None)), archive, manifest, package_id)
    with zipfile.ZipFile(archive) as zipped:
        if sorted(zipped.namelist()) != sorted(receipt['files']) or zipped.testzip():
            raise ValueError('Release archive entry/CRC mismatch')
        for name, entry in receipt['files'].items():
            with zipped.open(name) as stream:
                if hashlib.file_digest(stream, 'sha256').hexdigest() != entry['sha256']:
                    raise ValueError('Release archive payload mismatch')
    return archive, receipt


def reviewed_changelog(directory, target, baseline):
    lines = (directory / 'nexus-changelog.txt').read_text(encoding='utf-8-sig').strip().splitlines()
    if len(lines) < 3 or lines[:2] != [f'TargetVersion={target}', f'BaselineVersion={baseline}']:
        raise ValueError('nexus-changelog.txt needs matching TargetVersion/BaselineVersion headers and reviewed change lines')
    entries = [line.strip() for line in lines[2:] if line.strip()]
    if not entries or len(set(line.lower() for line in entries)) != len(entries) or any(
            core.re.match(r'^(Version\s|[-*]\s|work in progress|not yet released)', line, core.re.I) for line in entries):
        raise ValueError('Changelog contains duplicate, intermediate, Markdown or unfinished entries')
    return '\n'.join(entries)


def publish_plan(archive, manifest, package_id='main'):
    if package_id not in ('main', 'textures'):
        raise ValueError('Unknown release package')
    directory = core.contained(core.ROOT, manifest['nexus']['descriptionDirectory'])
    paths = [core.ROOT / 'mod.json', core.ROOT / 'changelog.txt'] + [directory / name for name in (
        'nexus-short-desc.txt', 'nexus-full-desc.txt', 'nexus-file-desc.txt', 'nexus-changelog.txt')]
    config_path = core.ROOT / 'tools/eldenring-paths.local.json'
    if config_path.is_file():
        paths.append(config_path)
    hashes = {str(path): core.digest(path) for path in paths}
    pitch = directory / ('nexus-textures-file-desc.txt' if package_id == 'textures' else 'nexus-file-desc.txt')
    hashes[str(pitch)] = core.digest(pitch)
    if core.read_json(core.ROOT / 'mod.json') != manifest:
        raise ValueError('Release manifest changed during planning; rerun the review')
    if not manifest.get('releaseReady') or any(not row.get('verified') for row in manifest['dependencies']):
        raise ValueError('Release readiness and dependency verification are required')
    issues = core.nexus_issues(core.ROOT, manifest)
    if issues:
        raise ValueError('\n'.join(issues))
    archive, receipt = verified_archive(archive, manifest, package_id)
    if receipt.get('stage'):
        for path in (core.ROOT / '.vdb/selected.json', Path(receipt['stage']['stageReceipt']), archive.parent / 'receipt.json'):
            hashes[str(path)] = core.digest(path)
    target = json.loads(json.dumps(manifest))
    if package_id == 'textures':
        target['nexus']['groupId'] = manifest['nexus']['textures']['groupId']
        del target['nexus']['textures']
    group_id = target['nexus']['groupId']
    remote = core.nexus_status(target)
    if not remote['current']:
        raise ValueError('Active remote version is ambiguous')
    if remote['current']['version'] == manifest['version']:
        raise ValueError('Version label is already active; reconcile bytes and use description-only updates')
    versions = api('GET', f"/mod-files/{group_id}/versions")['versions']
    if any(row.get('version') == manifest['version'] for row in versions):
        raise ValueError('Target version label already exists in this group; reconcile instead of uploading again')
    # Nexus changelogs belong to the mod, not a file group. Main posts the reviewed
    # release notes once; the companion upload must not append a duplicate block.
    changelog = reviewed_changelog(directory, manifest['version'], remote['current']['version']) if package_id == 'main' else None
    description = pitch.read_text(encoding='utf-8-sig').strip()
    if not description or len(description) > 255:
        raise ValueError('Package file description must be 1 to 255 characters')
    if any(core.digest(Path(name)) != digest for name, digest in hashes.items()):
        raise ValueError('Release inputs changed during planning; rerun the review')
    hashes.update({str(Path(receipt['source']) / name): entry['sha256'] for name, entry in receipt['files'].items()})
    return {'archive': str(archive), 'archiveSha256': receipt['sha256'], 'version': manifest['version'], 'packageId': package_id,
            'groupId': group_id, 'modId': manifest['nexus']['modId'],
            'baseline': remote['current'], 'description': description,
            'expectedActiveIds': sorted(row['id'] for row in remote['activeVersions']),
            'name': manifest['displayName'] + (' - Textures' if package_id == 'textures' else ''), 'changelog': changelog,
            'sourceHashes': hashes,
            'sourceInventory': {'root': receipt['source'], 'names': list(receipt['files']),
                                'excludeDirectories': manifest['package']['excludeDirectories']}}


def publish(plan):
    archive = Path(plan['archive'])
    # Legacy journals stay beside their exact package receipt; never replace them to permit a retry.
    journal = archive.parent / 'upload-journal.json'
    if journal.exists():
        raise ValueError('An upload journal already exists. Reconcile its remote outcome before any retry')
    manifest = core.read_json(core.ROOT / 'mod.json')
    request = {
        'schemaVersion': 1, 'apply': True, 'repoRoot': str(core.ROOT), 'packageName': manifest['id'] + ('-Textures' if plan.get('packageId') == 'textures' else ''),
        'nexusUrl': manifest['nexus']['url'], 'modId': plan['modId'], 'groupId': plan['groupId'],
        'version': plan['version'], 'archivePath': str(archive), 'archiveSha256': plan['archiveSha256'],
        'sourceHashes': plan['sourceHashes'], 'sourceInventory': plan.get('sourceInventory'),
        'baselineVersionId': plan['baseline']['id'], 'baselineVersion': plan['baseline']['version'],
        'expectedActiveIds': plan.get('expectedActiveIds'), 'journalPath': str(journal),
        'resultPath': str(archive.parent / 'upload-result.json'), 'changelog': plan['changelog'],
        'file': {'name': plan['name'], 'version': plan['version'], 'description': plan['description'],
                 'file_category': 'main', 'primary_mod_manager_download': plan.get('packageId') != 'textures', 'allow_mod_manager_download': True,
                 'show_requirements_pop_up': True, 'update_mod_version': plan.get('packageId') != 'textures', 'archive_existing_file': True,
                 'previous_version_id': plan['baseline']['id']}}
    request_path = archive.parent / 'upload-request.json'
    core.write_json(request_path, request)
    try:
        return workflow.automation.invoke(core.ROOT, 'publish', request_path)
    except workflow.subprocess.CalledProcessError:
        raise ValueError(f'Publish incomplete; inspect {journal} and upload-result.json before retrying') from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', required=True)
    parser.add_argument('--publish', action='store_true')
    parser.add_argument('--package', choices=('main', 'textures'), default='main')
    parser.add_argument('--textures-archive', help='Publish this companion before the main archive')
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    with core.operation('nexus'):
        import release_pipeline
        archives = {args.package: args.archive}
        if args.textures_archive:
            if args.package != 'main':
                raise ValueError('--textures-archive requires a main archive')
            archives['textures'] = args.textures_archive
        result = release_pipeline.release_batch(archives, core.config(argparse.Namespace(config=None)), args.publish, args.resume)
        core.emit(result, True)
        if result.get('status') == 'pending-promotion':
            core.sys.exit(2)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f'ERROR: {error}', file=core.sys.stderr)
        core.sys.exit(1)
