"""Sovereign adapter for the shared VDB client; no Vortex database/file writes."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid

import asset_workflow as assets

ROOT = Path(__file__).resolve().parents[1]


def project(root):
    data = assets.read(root / 'vdb.json')
    manifest = assets.read(root / 'mod.json')
    if (data.get('schemaVersion') != 1 or data.get('id') != manifest['id'].lower()
            or data.get('gameId') != manifest['gameDomain'] or data['id'] != 'sovereign'):
        raise ValueError('VDB project identity differs from Sovereign mod.json')
    if sorted(p['id'] for p in data['packages']) != ['main', 'textures']:
        raise ValueError('Expected main and textures package identities')
    for package in data['packages']:
        if (package.get('modType') != '' or package.get('activation') != 'stage-only'
                or package.get('installation') != 'prepared-directory'):
            raise ValueError('Sovereign requires explicit default mod type and stage-only activation')
        expected = manifest['displayName'] + (' - Textures' if package['id'] == 'textures' else '')
        if package['displayName'] != expected or package['logicalFileName'] != expected:
            raise ValueError('Package display/logical name differs from declared identity')
        nexus = manifest['nexus'] if package['id'] == 'main' else manifest['nexus']['textures']
        if package.get('nexus') != {
                'gameDomain': manifest['gameDomain'], 'gameScopedModId': manifest['nexus']['gameScopedModId'],
                'groupId': nexus['groupId']}:
            raise ValueError('VDB Nexus identity differs from mod.json')
    return data


def receipt_project_matches(data, receipt):
    if receipt['projectHash'] == assets.fingerprint(data):
        return True
    # Correct publishing metadata without rewriting submitted builds' provenance.
    # Unsubmitted candidates must be prepared again with the corrected metadata.
    if receipt['status'] in ('preparing', 'prepared'):
        return False
    legacy = json.loads(json.dumps(data))
    packages = {package['id']: package for package in legacy['packages']}
    if (packages['main']['nexus']['groupId'] != '7949853'
            or packages['textures']['nexus']['groupId'] != '893965'):
        return False
    packages['main']['nexus']['groupId'] = '893965'
    del packages['textures']['nexus']
    return receipt['projectHash'] == assets.fingerprint(legacy)


def client(root):
    local = assets.read(root / 'vdb.local.json') if (root / 'vdb.local.json').is_file() else {}
    configured = os.environ.get('VORTEX_DEVELOPMENT_BRIDGE_ROOT') or local.get('toolRoot')
    if not configured or not Path(configured).is_absolute():
        raise ValueError('Configure absolute toolRoot in ignored vdb.local.json')
    tool = Path(configured).resolve()
    if assets.read(tool / 'package.json')['name'] != 'vortex-development-bridge':
        raise ValueError('Configured tool is not Vortex Development Bridge')
    latest = assets.read(tool / 'dist/latest.json')
    run = Path(latest['run']).absolute()
    if not run.is_relative_to(tool / 'dist'):
        raise ValueError('VDB build is outside the configured dist directory')
    executable = assets.safe_path(tool, run.relative_to(tool) / 'extension/client/vdb.cjs')
    matches = [item for item in latest['files'] if item['path'] == 'client/vdb.cjs']
    if len(matches) != 1 or assets.checksum(executable) != matches[0]['sha256']:
        raise ValueError('Bundled VDB client differs from verified build receipt')
    node = shutil.which('node')
    if not node:
        raise ValueError('Node.js 22 or newer is required by VDB')
    return {'node': node, 'path': str(executable), 'sha256': matches[0]['sha256'],
            'version': latest['version'], 'bridge': local.get('bridgeRoot')}


def invoke(selected, arguments):
    if assets.checksum(selected['path']) != selected['sha256']:
        raise ValueError('Selected VDB client changed during operation')
    command = [selected['node'], selected['path'], *map(str, arguments), '--json']
    if selected.get('bridge'):
        command.extend(['--bridge', selected['bridge']])
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', timeout=70)
    try:
        document = json.loads(result.stdout or result.stderr)
    except json.JSONDecodeError as error:
        raise ValueError(f'VDB returned invalid JSON (exit {result.returncode})') from error
    return {'exitCode': result.returncode, 'result': document}


def doctor(selected):
    response = invoke(selected, ['doctor'])
    data = response['result']
    if response['exitCode'] or data.get('protocolVersion') not in (1, 2, 3) or data.get('clientVersion') != selected['version']:
        raise ValueError('VDB client/protocol check failed')
    state = data['vortex']
    if state.get('protocolVersion') != 1 or state.get('stale', True):
        raise ValueError('Vortex bridge status is unavailable/stale; open Vortex with the extension enabled')
    return data


def inventory(source, root, package):
    """Exact legacy package inventory, retaining its dependency and excluding authoring."""
    import nexus_workflow
    if package == 'main':
        return nexus_workflow.inventory(source, assets.read(root / 'mod.json'))
    expected = {'mod/' + name for group in assets.catalog(root)['groups'] if group['package'] == package
                for name in group['files']}
    files = {}
    for directory, directories, names in os.walk(source, followlinks=False):
        for name in [*directories, *names]:
            assets.safe_path(source, (Path(directory) / name).relative_to(source))
        for name in names:
            path = Path(directory) / name
            relative = path.relative_to(source).as_posix()
            if relative not in expected:
                raise ValueError('Unexpected texture package file: ' + relative)
            files[relative] = {'size': path.stat().st_size, 'sha256': assets.checksum(path)}
    if set(files) != expected:
        raise ValueError('Texture package is missing a required companion')
    return {'source': str(source), 'files': dict(sorted(files.items())), 'excluded': []}


def prepare(root, settings, package, version, source_role, scope=None):
    if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+(?:-[A-Za-z0-9.-]+)?', version):
        raise ValueError('Pass an explicit semantic development/release version')
    project_data = project(root)
    data = assets.catalog(root)
    runtime = Path(settings['roots']['vortex' if package == 'main' else 'vortexTextures'])
    if runtime.name.casefold() != 'mod':
        raise ValueError('Configured Vortex runtime must end in mod')
    selected_package = selected_source(root, settings, package)
    source_package = selected_package or runtime.parent
    baseline = inventory(source_package, root, package)
    owned = {'mod/' + name for group in data['groups'] if group['package'] == package for name in group['files']}
    baseline_runtime = {name for name in baseline['files'] if name.startswith('mod/')}
    if baseline_runtime - owned:
        raise ValueError('Vortex/catalog membership differs; review ownership before preparing a stage')
    sources = {name: assets.safe_path(source_package, name) for name in baseline['files']}
    replacement_names = owned if scope is None else {
        'mod/' + name for group in data['groups'] if group['package'] == package
        for name in group['files'] if assets.matches_scope(data, scope,
            {'scope': group['scope'], 'group': group['id'], 'kind': 'runtime', 'file': name})}
    if scope and (source_role != 'repo' or not replacement_names):
        raise ValueError('Scoped staging requires repo source and a runtime scope in the selected package')
    additions = owned - baseline_runtime
    if additions and (selected_package is None or source_role != 'repo' or not additions <= replacement_names):
        raise ValueError('New runtime membership requires a verified selected stage and acceptance of every added file')
    if source_role == 'repo':
        sources.update({name: assets.safe_path(assets.runtime_root(root, package), name[4:]) for name in replacement_names})
    elif source_role != 'vortex':
        raise ValueError('Choose repo or vortex as the explicit stage source')
    expected = {name: {'size': path.stat().st_size, 'sha256': assets.checksum(path)} for name, path in sources.items()}
    directory = assets.safe_path(root, '.vdb/prepared/' + uuid.uuid4().hex)
    payload = directory / 'payload'
    payload.mkdir(parents=True)
    receipt = {'schemaVersion': 1, 'status': 'preparing', 'packageId': package, 'version': version,
               'sourceRole': source_role, 'scope': scope, 'baselinePackage': str(source_package),
               'replacedRuntimePaths': sorted(replacement_names) if source_role == 'repo' else [],
               'addedRuntimePaths': sorted(additions),
               'projectHash': assets.fingerprint(project_data),
               'catalogHash': assets.fingerprint(data), 'settingsHash': assets.fingerprint(settings),
               'sources': {name: str(path) for name, path in sources.items()}, 'files': expected,
               'gameplayVerified': False, 'requests': []}
    assets.save(directory / 'receipt.json', receipt)
    for name, src in sources.items():
        dst = assets.safe_path(payload, name)
        dst.parent.mkdir(parents=True, exist_ok=True)
        with src.open('rb') as incoming, dst.open('xb') as outgoing:
            shutil.copyfileobj(incoming, outgoing)
        if assets.checksum(dst) != expected[name]['sha256']:
            raise ValueError('File changed during stage preparation: ' + name)
    if inventory(source_package, root, package) != baseline or any(
            assets.checksum(src) != expected[name]['sha256'] for name, src in sources.items()):
        raise ValueError('Stage input changed; reject the prepared candidate')
    receipt['status'] = 'prepared'
    assets.save(directory / 'receipt.json', receipt)
    return directory / 'receipt.json'


def load_prepared(root, settings, path):
    base = assets.safe_path(root, '.vdb/prepared')
    path = Path(path).absolute()
    if not path.is_relative_to(base):
        raise ValueError('Use a receipt under this repo\'s .vdb/prepared directory')
    path = assets.safe_path(base, path.relative_to(base))
    receipt = assets.read(path)
    if (receipt['schemaVersion'] != 1 or not receipt_project_matches(project(root), receipt)
            or (receipt['status'] == 'prepared' and (receipt['catalogHash'] != assets.fingerprint(assets.catalog(root))
                or receipt['settingsHash'] != assets.fingerprint(settings)))):
        raise ValueError('Stage configuration changed since preparation')
    if inventory(path.parent / 'payload', root, receipt['packageId'])['files'] != receipt['files']:
        raise ValueError('Prepared payload changed')
    return path, receipt


def reserve_version(root, settings, path, receipt):
    """Under the asset lock, bind a version before any bridge submission."""
    record_path = assets.safe_path(root, f".vdb/staged-versions/{receipt['packageId']}/{receipt['version']}.json")
    previous = []
    if record_path.exists():
        record = assets.read(record_path)
        if (record.get('packageId') != receipt['packageId'] or record.get('version') != receipt['version']
                or record.get('files') != receipt['files']):
            raise ValueError('Version already reserved with different contents; use a new version')
        previous.append(Path(record['receipt']))
    # Include older receipts so installing the guard cannot erase existing version ownership.
    for candidate in sorted((root / '.vdb/prepared').glob('*/receipt.json')):
        old = assets.read(candidate)
        if (old.get('packageId') == receipt['packageId'] and old.get('version') == receipt['version']
                and old.get('status') not in ('preparing', 'prepared')):
            if old.get('files') != receipt['files']:
                raise ValueError('Version already staged with different contents; use a new version')
            if candidate not in previous:
                previous.append(candidate)
    retained = None
    for candidate in previous:
        old_path, old = load_prepared(root, settings, candidate)
        if old.get('packageId') != receipt['packageId'] or old.get('version') != receipt['version'] or old['files'] != receipt['files']:
            raise ValueError('Reserved stage identity changed; inspect its receipt')
        if old['status'] == 'completed':
            staged_source(root, settings, old_path)
        if retained is None:
            retained = (old_path, old)
    if not record_path.exists():
        record_path.parent.mkdir(parents=True, exist_ok=True)
        assets.save(record_path, {'schemaVersion': 1, 'packageId': receipt['packageId'],
            'version': receipt['version'], 'files': receipt['files'],
            'receipt': str((retained[0] if retained else path).absolute())})
    return retained


def stage(root, settings, path):
    with assets.lock(root):
        path, receipt = load_prepared(root, settings, path)
        if receipt['status'] != 'prepared':
            raise ValueError('Stage already submitted/interrupted; inspect or wait on its recorded request')
        retained = reserve_version(root, settings, path, receipt)
        if retained and retained[0] != path:
            old_path, old = retained
            if old['status'] not in ('queued', 'pending', 'running', 'completed') or not old.get('requestId'):
                raise ValueError(f'Reserved stage needs inspection; resume its original receipt: {old_path}')
            for key in ('status', 'client', 'requests', 'requestId', 'buildId'):
                receipt[key] = old[key]
            receipt['reusedStageReceipt'] = str(old_path)
            assets.save(path, receipt)
            return receipt['requests'][-1]
        selected = client(root)
        doctor(selected)
        registration = invoke(selected, ['register', '--config', root / 'vdb.json'])
        if registration['exitCode']:
            raise ValueError('VDB registration failed: ' + str(registration['result']))
        receipt.update(status='submitting', client=selected)
        assets.save(path, receipt)
        # No profile argument: stage-only does not select or activate a profile.
        response = invoke(selected, ['stage', '--project', 'sovereign', '--package', receipt['packageId'],
                                    '--artifact', path.parent / 'payload', '--version', receipt['version']])
        receipt['requests'].append(response)
        receipt['status'] = response['result'].get('status', 'unknown')
        receipt['requestId'] = response['result'].get('id')
        receipt['buildId'] = response['result'].get('buildId')
        assets.save(path, receipt)
        return response


def wait(root, settings, path, seconds):
    if not 0 <= seconds <= 45:
        raise ValueError('Wait must be 0 to 45 seconds')
    with assets.lock(root):
        path, receipt = load_prepared(root, settings, path)
        if not receipt.get('requestId'):
            raise ValueError('No recorded request; inspect bridge queue before resubmitting')
        response = invoke(receipt['client'], ['wait', '--request', receipt['requestId'], '--seconds', seconds])
        receipt['requests'].append(response)
        receipt['status'] = response['result'].get('status', 'unknown')
        assets.save(path, receipt)
    return response


def staged_source(root, settings, path):
    path, receipt = load_prepared(root, settings, path)
    if receipt['status'] != 'completed' or not re.fullmatch(r'[a-f0-9]{24}', receipt.get('buildId') or ''):
        raise ValueError('A completed stage receipt is required')
    confirmations = [r['result'] for r in receipt['requests'] if r['result'].get('status') == 'completed'
                     and r['result'].get('operation') == 'stage' and r['result'].get('projectId') == 'sovereign'
                     and r['result'].get('packageId') == receipt['packageId']
                     and r['result'].get('result', {}).get('buildId') == receipt['buildId']]
    confirmations += [r['result'] for r in receipt['requests']
                      if r['result'].get('operation') == 'finish' and r['result'].get('projectId') == 'sovereign'
                      and any(b.get('packageId') == receipt['packageId'] and b.get('buildId') == receipt['buildId']
                              and b.get('version') == receipt['version'] and b.get('staging') == 'completed'
                              for b in r['result'].get('result', {}).get('builds', []))]
    if not confirmations:
        raise ValueError('Missing matching completed VDB stage acknowledgement')
    key = 'vortex' if receipt['packageId'] == 'main' else 'vortexTextures'
    stage_root = Path(settings['roots'][key]).resolve().parent.parent
    name = f"vdb-sovereign-{receipt['packageId']}-{receipt['buildId']}"
    source = assets.safe_path(stage_root, name)
    if inventory(source, root, receipt['packageId'])['files'] != receipt['files']:
        raise ValueError('Vortex staged build differs from its immutable receipt')
    return source, receipt


def select(root, settings, path):
    with assets.lock(root):
        source, receipt = staged_source(root, settings, path)
        destination = assets.safe_path(root, '.vdb/selected.json')
        selected = assets.read(destination) if destination.is_file() else {}
        selected[receipt['packageId']] = {'receipt': str(Path(path).absolute()), 'buildId': receipt['buildId'], 'source': str(source)}
        assets.save(destination, selected)
        return selected


def selected_source(root, settings, package):
    path = root / '.vdb/selected.json'
    selected = assets.read(path).get(package) if path.is_file() else None
    if not selected:
        return None
    source, receipt = staged_source(root, settings, selected['receipt'])
    if selected['buildId'] != receipt['buildId'] or Path(selected['source']) != source:
        raise ValueError('Selected Vortex identity is inconsistent')
    return source


def deployment_context(root, profile, operation='deploy'):
    selected = client(root)
    state = doctor(selected)['vortex']
    if state.get('activeGameId') != 'eldenring' or state.get('activeProfileId') != profile:
        raise ValueError('Select the explicitly requested Elden Ring profile in Vortex first')
    legacy = [m['id'] for m in state.get('activeMods', []) if m['id'] in ('Sovereign', 'Sovereign - Textures')]
    if operation != 'verify' and legacy:
        raise ValueError('Disable legacy duplicate providers in Vortex first: ' + ', '.join(legacy))
    return selected, state


def operate(root, settings, path, operation, profile, operation_id=None):
    with assets.lock(root):
        source, receipt = staged_source(root, settings, path)
        selected, state = deployment_context(root, profile, operation)
        operation_id = operation_id or uuid.uuid4().hex
        if not re.fullmatch('[a-f0-9]{32}', operation_id):
            raise ValueError('Expected a unique local operation ID')
        directory = assets.safe_path(root, '.vdb/operations/' + operation_id)
        directory.mkdir(parents=True)
        document = {'status': 'submitting', 'operation': operation, 'profileId': profile,
                    'packageId': receipt['packageId'], 'buildId': receipt['buildId'],
                    'stageReceipt': str(Path(path).absolute()), 'beforeEnabledMods': state.get('activeMods', []),
                    'client': selected, 'requests': []}
        assets.save(directory / 'receipt.json', document)
        response = invoke(selected, [operation, '--project', 'sovereign', '--package', receipt['packageId'],
                                     '--build', receipt['buildId'], '--profile', profile])
        document['requests'].append(response)
        document['requestId'] = response['result'].get('id')
        document['status'] = response['result'].get('status', 'unknown')
        assets.save(directory / 'receipt.json', document)
        return {'receipt': str(directory / 'receipt.json'), **response}


def wait_operation(root, path, seconds):
    if not 0 <= seconds <= 45:
        raise ValueError('Wait must be 0 to 45 seconds')
    with assets.lock(root):
        base = assets.safe_path(root, '.vdb/operations')
        path = Path(path).absolute()
        if not path.is_relative_to(base):
            raise ValueError('Use a .vdb/operations receipt')
        path = assets.safe_path(base, path.relative_to(base))
        document = assets.read(path)
        if not document.get('requestId'):
            raise ValueError('Missing request ID; inspect interrupted submission before retrying')
        response = invoke(document['client'], ['wait', '--request', document['requestId'], '--seconds', seconds])
        document['requests'].append(response)
        document['status'] = response['result'].get('status', 'unknown')
        assets.save(path, document)
        return response


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor')
    command = sub.add_parser('prepare')
    command.add_argument('--package', choices=('main', 'textures'), required=True)
    command.add_argument('--version', required=True)
    command.add_argument('--from', dest='source', choices=('repo', 'vortex'), required=True)
    command.add_argument('--scope', help='Replace only this accepted repo scope; keep other selected-stage bytes')
    for name in ('stage', 'wait', 'select', 'deploy', 'verify', 'rollback', 'wait-operation'):
        command = sub.add_parser(name)
        command.add_argument('--receipt', required=True)
        if name in ('wait', 'wait-operation'):
            command.add_argument('--seconds', type=int, default=15)
        if name in ('deploy', 'verify', 'rollback'):
            command.add_argument('--profile', required=True)
    args = parser.parse_args()
    settings = assets.read(ROOT / 'tools/eldenring-paths.local.json')
    if args.command == 'doctor':
        selected = client(ROOT)
        data = doctor(selected)
        state = data['vortex']
        print(json.dumps({'clientVersion': data['clientVersion'], 'clientHash': selected['sha256'],
                          **{key: state.get(key) for key in ('extensionVersion', 'protocolVersion', 'observedAt',
                              'activeGameId', 'activeProfileId', 'profiles', 'stale')}}, indent=2))
    elif args.command == 'prepare':
        print(prepare(ROOT, settings, args.package, args.version, args.source, args.scope))
    elif args.command == 'select':
        print(json.dumps(select(ROOT, settings, args.receipt), indent=2))
    else:
        if args.command == 'stage':
            result = stage(ROOT, settings, args.receipt)
        elif args.command == 'wait':
            result = wait(ROOT, settings, args.receipt, args.seconds)
        elif args.command == 'wait-operation':
            result = wait_operation(ROOT, args.receipt, args.seconds)
        else:
            result = operate(ROOT, settings, args.receipt, args.command, args.profile)
        print(json.dumps(result, indent=2))
        if result['result'].get('status') in ('queued', 'pending', 'running'):
            return 2
        return result['exitCode']
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, subprocess.TimeoutExpired) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)
