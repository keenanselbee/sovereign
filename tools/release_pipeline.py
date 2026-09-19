"""Review/publish Sovereign releases, resume exact operations, and report collection readiness."""
import argparse
import hashlib
import json
from pathlib import Path
import re

import asset_workflow as assets
import nexus_publish as publisher
import nexus_workflow as workflow
import release_artifact as artifacts
import sovereign as core
import vdb_workflow as vdb


def retained(archive, settings, require_selected=False):
    archive = Path(archive).resolve()
    base = core.ROOT / '.vdb/releases'
    if not archive.is_relative_to(base) or len(archive.relative_to(base).parts) != 3:
        raise ValueError('Use an exact retained release archive')
    package_id, version, _ = archive.relative_to(base).parts
    if package_id not in ('main', 'textures') or not re.fullmatch(r'[0-9]+\.[0-9]\.[0-9]', version):
        raise ValueError('Invalid retained release package/version')
    manifest = core.read_json(core.ROOT / 'mod.json')
    manifest['version'] = version
    _, receipt = artifacts.verify(core.ROOT, settings, archive, manifest, package_id, require_selected)
    return archive, receipt, manifest


def upload_evidence(archive, settings, save=False):
    archive, receipt, manifest = retained(archive, settings)
    package_id = receipt['stage']['packageId']
    journal = assets.read(archive.parent / 'upload-journal.json')
    plan = journal['plan']
    group = manifest['nexus'] if package_id == 'main' else manifest['nexus']['textures']
    with archive.open('rb') as stream:
        md5 = hashlib.file_digest(stream, 'md5').hexdigest()
    fingerprints = {'sha256': receipt['sha256'], 'md5': md5, 'sizeBytes': archive.stat().st_size}
    if (journal.get('schemaVersion') != 1 or journal.get('phase') != 'verified'
            or journal.get('status') != 'version-read-verified'
            or journal.get('archive') != fingerprints
            or Path(plan['archivePath']).resolve() != archive or plan['archiveSha256'] != receipt['sha256']
            or plan['groupId'] != group['groupId'] or plan['modId'] != manifest['nexus']['modId']
            or plan['file']['version'] != receipt['version']
            or plan['file']['primary_mod_manager_download'] != (package_id == 'main')
            or (plan.get('changelog') and journal.get('changelogStatus') != 'posted')):
        raise ValueError('Upload is incomplete or differs from this release; reconcile its journal')
    rows = publisher.api('GET', f"/mod-files/{group['groupId']}/versions")['versions']
    rows = [r for r in rows if r.get('id') == journal.get('versionId')]
    if (len(rows) != 1 or rows[0].get('file', {}).get('id') != group['groupId']
            or rows[0].get('version') != receipt['version']
            or rows[0].get('category') not in ('main', 'optional', 'update', 'miscellaneous')
            or rows[0].get('is_primary') != (package_id == 'main')):
        raise ValueError('Exact uploaded Nexus identity is unavailable or changed; never reupload it')
    file_id = rows[0].get('game_scoped_id')
    if not isinstance(file_id, str) or not re.fullmatch(r'[1-9][0-9]*', file_id):
        return {'status': 'pending-file-id', 'packageId': package_id, 'versionId': journal['versionId']}
    result = {'schemaVersion': 1, 'packageId': package_id, 'version': receipt['version'], 'stage': receipt['stage'],
              'archive': {'path': str(archive), **fingerprints}, 'nexus': {
                  'gameDomain': manifest['gameDomain'], 'gameScopedModId': manifest['nexus']['gameScopedModId'],
                  'modId': manifest['nexus']['modId'], 'groupId': group['groupId'],
                  'versionId': journal['versionId'], 'gameScopedFileId': file_id}}
    path = archive.parent / 'nexus-release.json'
    if path.exists() and assets.read(path) != result:
        raise ValueError('Confirmed release receipt differs; inspect without overwriting it')
    if save and not path.exists():
        assets.save(path, result)
    return result


def promotion_completed(response, release):
    result = response.get('result', {})
    return (result.get('status') == 'completed' and result.get('operation') == 'promote'
            and result.get('projectId') == 'sovereign' and result.get('packageId') == release['packageId']
            and result.get('result', {}).get('publication') == 'verified')


def promote(archive, settings, seconds=15):
    with assets.lock(core.ROOT):
        release = upload_evidence(archive, settings, save=True)
        if release.get('status') == 'pending-file-id':
            return release
        directory = Path(release['archive']['path']).parent
        path = directory / 'promotion.json'
        identity = assets.fingerprint(release)
        if path.exists():
            operation = assets.read(path)
            if operation.get('releaseHash') != identity or operation.get('buildId') != release['stage']['buildId']:
                raise ValueError('Promotion belongs to a different release/build')
            if operation['status'] == 'completed':
                if not promotion_completed(operation['responses'][-1], release):
                    raise ValueError('Promotion completion is not verified')
                return operation
            if operation['status'] not in ('queued', 'pending', 'running') or not operation.get('requestId'):
                raise ValueError('Promotion is interrupted/terminal; inspect its receipt, do not resubmit')
        else:
            selected = vdb.client(core.ROOT)
            vdb.doctor(selected)
            registered = vdb.invoke(selected, ['register', '--config', core.ROOT / 'vdb.json'])
            if registered['exitCode']:
                raise ValueError('VDB project registration failed')
            payload = {'archive': release['archive']['path'], 'sha256': release['archive']['sha256'],
                       'md5': release['archive']['md5'], 'size': release['archive']['sizeBytes'],
                       'version': release['version'], **{k: v for k, v in release['nexus'].items() if k != 'modId'}}
            payload_path = directory / 'vdb-release.json'
            if payload_path.exists() and assets.read(payload_path) != payload:
                raise ValueError('Promotion payload changed')
            if not payload_path.exists():
                assets.save(payload_path, payload)
            operation = {'schemaVersion': 1, 'releaseHash': identity, 'status': 'submitting',
                         'buildId': release['stage']['buildId'], 'client': selected, 'responses': []}
            assets.save(path, operation)
            response = vdb.invoke(selected, ['promote', '--project', 'sovereign', '--package', release['packageId'],
                                          '--build', release['stage']['buildId'], '--receipt', payload_path])
            operation.update(status=response['result'].get('status', 'unknown'), requestId=response['result'].get('id'))
            operation['responses'].append(response)
            assets.save(path, operation)
        if operation['status'] in ('queued', 'pending', 'running') and operation.get('requestId'):
            response = vdb.invoke(operation['client'], ['wait', '--request', operation['requestId'], '--seconds', seconds])
            if response['result'].get('id') != operation['requestId']:
                raise ValueError('Promotion wait returned a different request')
            operation['responses'].append(response)
            operation['status'] = response['result'].get('status', 'unknown')
            assets.save(path, operation)
        if operation['status'] == 'completed' and not promotion_completed(operation['responses'][-1], release):
            raise ValueError('VDB completed without verified publication')
        if operation['status'] not in ('queued', 'pending', 'running', 'completed'):
            raise ValueError('Promotion failed or is uncertain; inspect its durable receipt')
        return operation


def resume_upload(archive, settings):
    archive, receipt, _ = retained(archive, settings)
    journal = assets.read(archive.parent / 'upload-journal.json')
    if (journal.get('schemaVersion') != 1 or not journal.get('plan')
            or journal.get('phase') in ('version-post-started', 'changelog-post-started')
            or (not journal.get('versionId') and journal.get('phase') != 'available')):
        raise ValueError('Upload outcome is uncertain; reconcile before retrying, never repeat the upload')
    plan = journal['plan']
    if Path(plan['archivePath']).resolve() != archive or plan['archiveSha256'] != receipt['sha256']:
        raise ValueError('Upload journal belongs to a different archive')
    manifest = assets.read(core.ROOT / 'mod.json')
    package_id = receipt['stage']['packageId']
    group = manifest['nexus'] if package_id == 'main' else manifest['nexus']['textures']
    if (plan['groupId'] != group['groupId'] or plan['modId'] != manifest['nexus']['modId']
            or plan['file']['version'] != receipt['version']
            or Path(plan['journalPath']).resolve() != archive.parent / 'upload-journal.json'
            or plan['file']['primary_mod_manager_download'] != (package_id == 'main')):
        raise ValueError('Upload journal does not match this package identity')
    request = {**plan, 'apply': True, 'resume': True, 'deferChangelog': False}
    path = archive.parent / 'resume-request.json'
    assets.save(path, request)
    return workflow.automation.invoke(core.ROOT, 'publish', path)


def release_batch(archives, settings, apply=False, resume=False, seconds=15):
    """Caller holds the Nexus lock. Preflight all new uploads before any upload."""
    if not archives or set(archives) - {'main', 'textures'}:
        raise ValueError('Provide main and/or textures archives')
    order = [p for p in ('textures', 'main') if p in archives]
    plans, identities = {}, {}
    manifest = assets.read(core.ROOT / 'mod.json')
    for package_id in order:
        archive, receipt, _ = retained(archives[package_id], settings, require_selected=True)
        if receipt['stage']['packageId'] != package_id or receipt['version'] != manifest['version']:
            raise ValueError('Package/version does not match this release')
        identities[package_id] = {'archive': str(archive), 'sha256': receipt['sha256']}
        journal = archive.parent / 'upload-journal.json'
        if journal.exists():
            state = assets.read(journal)
            if state.get('phase') == 'verified':
                upload_evidence(archive, settings)
                plans[package_id] = {'status': 'already-uploaded'}
            elif not resume and apply:
                raise ValueError('Existing upload requires explicit --resume; no upload started')
            else:
                plans[package_id] = {'status': 'resume-required'}
        else:
            plans[package_id] = publisher.publish_plan(archive, manifest, package_id)
    batch_path = core.ROOT / '.vdb/release-batches' / (manifest['version'] + '.json')
    if batch_path.exists():
        old = assets.read(batch_path)
        if old['archives'] != identities and old.get('status') != 'completed':
            raise ValueError('Resume the existing release batch with its exact package set and archives')
    if not apply:
        return {'status': 'planned', 'order': order, 'packages': plans}
    batch_path.parent.mkdir(parents=True, exist_ok=True)
    batch = {'schemaVersion': 1, 'archives': identities, 'order': order, 'status': 'running', 'results': {}}
    assets.save(batch_path, batch)
    for package_id in order:
        archive = Path(identities[package_id]['archive'])
        if (archive.parent / 'upload-journal.json').exists():
            if assets.read(archive.parent / 'upload-journal.json').get('phase') != 'verified':
                resume_upload(archive, settings)
        else:
            publisher.publish(plans[package_id])
        evidence = upload_evidence(archive, settings, save=True)
        # Main must follow a verified texture upload, even if Vortex promotion waits.
        batch['results'][package_id] = evidence
        assets.save(batch_path, batch)
    for package_id in order:
        batch['results'][package_id] = promote(identities[package_id]['archive'], settings, seconds)
        assets.save(batch_path, batch)
    batch['status'] = 'completed' if all(r.get('status') == 'completed' for r in batch['results'].values()) else 'pending-promotion'
    assets.save(batch_path, batch)
    return batch


def collection_readiness(settings, snapshot=None):
    if snapshot is None:
        response = vdb.invoke(vdb.client(core.ROOT), ['status', '--project', 'sovereign'])
        if response['exitCode']:
            raise ValueError('VDB status unavailable')
        snapshot = response['result']
    if (snapshot.get('status') == 'unavailable' or snapshot.get('stale') is not False
            or snapshot.get('activeGameId') != 'eldenring' or not snapshot.get('activeProfileId')):
        return {'ready': False, 'status': 'unavailable', 'reason': 'A fresh active Elden Ring profile is required', 'packages': []}
    rows = []
    for mod in snapshot.get('activeMods', []):
        if (mod.get('vdbProjectId') != 'sovereign' and str(mod.get('modId')) != '201'
                and mod.get('logicalFileName') not in ('Sovereign', 'Sovereign - Textures')
                and mod.get('id') not in ('Sovereign', 'Sovereign - Textures')):
            continue
        row = {'mod': mod.get('id'), 'packageId': mod.get('vdbPackageId'), 'buildId': mod.get('vdbBuildId'), 'status': 'local', 'ready': False}
        try:
            package_id, version = mod.get('vdbPackageId'), mod.get('version')
            if package_id not in ('main', 'textures') or not re.fullmatch(r'[0-9]+\.[0-9]\.[0-9]', version or ''):
                raise ValueError('Enabled build has no release identity')
            directory = core.ROOT / '.vdb/releases' / package_id / version
            release = assets.read(directory / 'nexus-release.json')
            archive, receipt, manifest = retained(release['archive']['path'], settings)
            promotion = assets.read(directory / 'promotion.json')
            if promotion.get('status') in ('queued', 'pending', 'running'):
                row['status'] = 'pending'
            else:
                nexus = release['nexus']
                group = manifest['nexus'] if package_id == 'main' else manifest['nexus']['textures']
                row['ready'] = (mod.get('vdbProjectId') == 'sovereign' and promotion.get('status') == 'completed'
                    and release['stage'] == receipt['stage'] and receipt['stage']['buildId'] == mod.get('vdbBuildId')
                    and release['archive']['sha256'] == receipt['sha256'] and nexus['groupId'] == group['groupId']
                    and promotion.get('releaseHash') == assets.fingerprint(release)
                    and promotion.get('buildId') == mod.get('vdbBuildId')
                    and promotion_completed(promotion['responses'][-1], release)
                    and mod.get('source') == 'nexus' and mod.get('vdbPublication') == 'verified'
                    and str(mod.get('modId')) == nexus['gameScopedModId'] and str(mod.get('fileId')) == nexus['gameScopedFileId'])
                row['status'] = 'promoted' if row['ready'] else 'mismatched'
        except (ValueError, OSError, KeyError, TypeError, IndexError) as error:
            row['reason'] = str(error)
        rows.append(row)
    present = [r['packageId'] for r in rows]
    return {'ready': sorted(present, key=str) == ['main', 'textures'] and all(r['ready'] for r in rows),
            'profileId': snapshot['activeProfileId'], 'packages': rows,
            'missingPackages': [p for p in ('main', 'textures') if p not in present]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    release = sub.add_parser('release')
    release.add_argument('--main')
    release.add_argument('--textures')
    release.add_argument('--apply', action='store_true')
    release.add_argument('--resume', action='store_true')
    release.add_argument('--seconds', type=int, choices=range(61), default=15)
    retry = sub.add_parser('promote')
    retry.add_argument('--archive', required=True)
    retry.add_argument('--seconds', type=int, choices=range(61), default=15)
    sub.add_parser('readiness')
    args = parser.parse_args()
    settings = core.config(argparse.Namespace(config=None))
    if args.command == 'readiness':
        result = collection_readiness(settings)
        core.emit(result, True)
        return 0 if result['ready'] else 2
    with core.operation('nexus'):
        if args.command == 'promote':
            result = promote(args.archive, settings, args.seconds)
        else:
            archives = {p: getattr(args, p) for p in ('main', 'textures') if getattr(args, p)}
            result = release_batch(archives, settings, args.apply, args.resume, args.seconds)
        core.emit(result, True)
        return 0 if result.get('status') in ('planned', 'completed') else 2


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, TypeError, workflow.subprocess.SubprocessError) as error:
        print(f'ERROR: {error}', file=core.sys.stderr)
        raise SystemExit(1)
