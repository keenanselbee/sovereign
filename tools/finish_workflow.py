"""Durable VDB finalization of accepted immutable Sovereign packages."""
from pathlib import Path

import asset_workflow as assets
import vdb_workflow as vdb

CAPABILITY = 'profile-finish-v3'


def compatible_client(root):
    selected = vdb.client(root)
    response = vdb.invoke(selected, ['doctor'])
    data = response['result']
    if (response['exitCode'] or data.get('clientVersion') != selected['version']
            or CAPABILITY not in data.get('capabilities', [])):
        raise ValueError('Configure the VDB client with profile-finish-v3 support')
    snapshot = data.get('vortex', {})
    if not snapshot.get('stale', True) and CAPABILITY not in snapshot.get('capabilities', []):
        raise ValueError('Install the current VDB extension before finalization; the running consumer is too old')
    return selected


def submit(root, settings, stages, path, profile=None, stage_only=False):
    """Persist the exact scope and inputs before submitting once. No active profile needed."""
    path = assets.safe_path(root, Path(path).absolute().relative_to(root))
    if not path.is_relative_to(root / '.vdb/finalizations') or path.exists():
        raise ValueError('Use a new repo-local finalization receipt; resume existing requests')
    selected = compatible_client(root)
    with assets.lock(root):
        prepared = [vdb.load_prepared(root, settings, stage) for stage in stages]
        if not prepared or len({doc['packageId'] for _, doc in prepared}) != len(prepared):
            raise ValueError('Finalization requires distinct prepared packages')
        for stage, doc in prepared:
            if doc['status'] not in ('prepared', 'completed'):
                raise ValueError('Stage already has a pending or uncertain operation; resume its original receipt')
            vdb.reserve_version(root, settings, stage, doc)
        registration = vdb.invoke(selected, ['register', '--config', root / 'vdb.json'])
        if registration['exitCode']:
            raise ValueError('VDB registration failed')
        path.parent.mkdir(parents=True)
        builds_path = path.parent / 'builds.json'
        assets.save(builds_path, [{'packageId': doc['packageId'], 'artifact': str(stage.parent / 'payload'),
                                 'version': doc['version']} for stage, doc in prepared])
        receipt = {'schemaVersion': 1, 'status': 'submitting', 'client': selected,
                   'profileId': profile, 'stageOnly': stage_only,
                   'profileScope': 'stage-only' if stage_only else 'profile' if profile else 'all',
                   'stages': [str(stage) for stage, _ in prepared], 'requests': []}
        assets.save(path, receipt)
        arguments = ['finish-batch', '--project', 'sovereign', '--builds', builds_path]
        if profile and not stage_only:
            arguments += ['--profile', profile]
        if stage_only:
            arguments += ['--stage-only']
        response = vdb.invoke(selected, arguments)
        receipt['requests'].append(response)
        receipt['requestId'] = response['result'].get('id')
        receipt['status'] = response['result'].get('status', 'unknown')
        receipt['builds'] = response['result'].get('builds', [])
        assets.save(path, receipt)
        if response['exitCode'] or receipt['status'] != 'queued' or not receipt['requestId']:
            raise ValueError('Finalization submission failed or is uncertain; inspect its receipt before recovery')
        for stage, doc in prepared:
            match = [b for b in receipt['builds'] if b['packageId'] == doc['packageId']]
            if len(match) != 1 or not vdb.re.fullmatch(r'[a-f0-9]{24}', match[0].get('buildId', '')):
                raise ValueError('VDB omitted the exact package build identity; inspect the queued receipt')
            doc.update(buildId=match[0]['buildId'], requestId=receipt['requestId'], client=selected, finishReceipt=str(path))
            assets.save(stage, doc)
        return receipt


def refresh(root, settings, path, seconds=0):
    path = Path(path).absolute()
    if not path.is_relative_to(root / '.vdb/finalizations'):
        raise ValueError('Use a repo-local finalization receipt')
    path = assets.safe_path(root, path.relative_to(root))
    with assets.lock(root):
        receipt = assets.read(path)
        if receipt['status'] in ('queued', 'pending', 'running'):
            response = vdb.invoke(receipt['client'], ['wait', '--request', receipt['requestId'], '--seconds', seconds])
            receipt['requests'].append(response)
            receipt['status'] = response['result'].get('status', 'unknown')
            assets.save(path, receipt)
        response = receipt['requests'][-1] if receipt['requests'] else {'result': {}}
        result = response['result']
        if (result.get('id') == receipt.get('requestId') and result.get('operation') == 'finish'
                and result.get('projectId') == 'sovereign'):
            for stage_path in receipt['stages']:
                stage, doc = vdb.load_prepared(root, settings, stage_path)
                expected = next((b for b in receipt['builds'] if b['packageId'] == doc['packageId']), {})
                matches = [b for b in result.get('result', {}).get('builds', [])
                           if b.get('packageId') == doc['packageId'] and b.get('buildId') == expected.get('buildId')
                           and b.get('version') == doc['version'] and b.get('staging') == 'completed']
                if len(matches) == 1:
                    doc.update(status='completed', buildId=expected['buildId'], requestId=receipt['requestId'],
                               client=receipt['client'], finishReceipt=str(path))
                    if not doc['requests'] or doc['requests'][-1] != response:
                        doc['requests'].append(response)
                    assets.save(stage, doc)
                    vdb.staged_source(root, settings, stage)
        return receipt


def advance(root, settings, path, doc, profile, seconds, stage_only=False):
    scope = {'profileId': None if stage_only else profile, 'stageOnly': stage_only}
    if doc.get('finishScope', scope) != scope:
        raise ValueError('Propagation is bound to a different profile scope or stage-only mode')
    doc['finishScope'] = scope
    if doc['status'] == 'complete':
        return doc
    if doc['status'] == 'source-accepted':
        import propagate_workflow
        doc = propagate_workflow.apply(root, settings, path)
    doc['finishScope'] = scope
    if not doc.get('finishReceipt'):
        if doc['status'] != 'prepared':
            raise ValueError('Accepted source preparation must finish before finalization')
        doc['finishReceipt'] = str(root / '.vdb/finalizations' / vdb.uuid.uuid4().hex / 'receipt.json')
        assets.save(path, doc)
    finish_path = Path(doc['finishReceipt'])
    if not finish_path.exists():
        submit(root, settings, [doc['stageReceipt']], finish_path, **{'profile': scope['profileId'], 'stage_only': stage_only})
    receipt = refresh(root, settings, finish_path, seconds)
    doc['status'] = 'finalizing'
    doc['finishStatus'] = receipt['status']
    assets.save(path, doc)
    if receipt['status'] in ('queued', 'pending', 'running'):
        return doc
    if receipt['status'] != 'completed':
        raise ValueError('Finalization is ' + receipt['status'] + '; inspect its recorded request, do not resubmit')
    result = receipt['requests'][-1]['result']
    if (result.get('id') != receipt.get('requestId') or result.get('operation') != 'finish'
            or result.get('projectId') != 'sovereign'):
        raise ValueError('Finalization lacks a matching bridge acknowledgement')
    for verification in result.get('result', {}).get('verification', []):
        if verification.get('deployed') != 'verified' or verification.get('enabled') is not True or verification.get('differences'):
            raise ValueError('Finalization has unverified deployed bytes')
    vdb.staged_source(root, settings, doc['stageReceipt'])
    if not stage_only:
        vdb.select(root, settings, doc['stageReceipt'])
    doc.update(status='complete', note='Immutable stage verified; profile outcomes recorded in finalization receipt. Gameplay not verified.')
    assets.save(path, doc)
    return doc
