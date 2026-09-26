"""Sync saved assets; retain explicit VDB preparation/deployment and receipt recovery."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
import uuid
import xml.etree.ElementTree as ET

import asset_workflow as assets
import sovereign as core
import vdb_workflow as vdb


def sync(root, settings, scope, role, qualification=None):
    """Accept saved assets without release metadata, package preparation or Vortex."""
    if role not in ('repo', 'editor'):
        raise ValueError('Choose repo or editor as the source')
    data = assets.catalog(root)
    if scope == 'all' or not any(assets.matches_scope(data, scope,
            {'scope': g['scope'], 'group': g['id'], 'kind': 'runtime', 'file': name})
            for g in data['groups'] for name in g['files']):
        raise ValueError('Choose a specific catalog runtime scope')
    # Reject conflicts before qualification or SFX saves can mutate editor output.
    assets.check_sync_conflicts(root, settings, scope, role, require_known=True)
    scopes = data.get('coordinatedScopes', {}).get(scope, [scope])
    path = assets.safe_path(root, '.sovereign/sync/' + uuid.uuid4().hex + '/receipt.json')
    path.parent.mkdir(parents=True)
    doc = {'schemaVersion': 1, 'kind': 'repository-sync', 'status': 'validating',
           'scope': scope, 'sourceRole': role, 'handoff': None, 'sfxEditorSave': None,
           'note': 'Saved-file synchronization only. Build and deployment remain separate.'}
    assets.save(path, doc)
    print(f'Sync receipt: {path}', flush=True)
    try:
        if not qualification and any(s in ('animations', 'hks') for s in scopes):
            import player_workflow
            print('Qualifying coordinated player sources and packed outputs...', flush=True)
            qualification = str(player_workflow.qualify(root, settings, role))
        elif not qualification and 'talk' in scopes:
            if role != 'repo':
                raise ValueError('Dialogue synchronization currently requires the accepted repo source')
            import format_workflow
            qualification = str(format_workflow.qualify_talk(root, settings))
        if 'sfx' in scopes and role == 'editor':
            import sfx_workflow
            doc['sfxEditorSave'] = str(sfx_workflow.build_and_save(root, settings))
            assets.save(path, doc)
            sfx_workflow.validate_saved(root, settings, doc['sfxEditorSave'])
        # Qualification also runs for unchanged files; events qualify in the handoff.
        assets.check_sync_conflicts(root, settings, scope, role, require_known=True)
        handoff = assets.prepare_handoff(root, settings, scope, role, qualification, allow_unchanged=True)
        doc.update(status='planned', handoff=str(handoff))
        assets.save(path, doc)
        if doc['sfxEditorSave']:
            sfx_workflow.validate_saved(root, settings, doc['sfxEditorSave'])
        accepted = assets.apply_handoff(root, settings, handoff)
        if doc['sfxEditorSave']:
            sfx_workflow.validate_saved(root, settings, doc['sfxEditorSave'])
        doc.update(status='complete', changedFiles=[entry['destination'] for entry in accepted['entries']],
                   qualification=accepted['qualification'])
        assets.save(path, doc)
    except (ValueError, OSError, KeyError, subprocess.TimeoutExpired, ET.ParseError) as error:
        doc.update(status='interrupted', error=str(error))
        assets.save(path, doc)
        raise
    count = len(doc['changedFiles'])
    print(f'Synced {count} file(s).' if count else 'Already synchronized.', flush=True)
    print('Build and deployment remain separate.', flush=True)
    return path


def scoped_inputs(root, settings, data, scope):
    rows = [row for row in assets.locations(root, settings, data, True)
            if assets.matches_scope(data, scope, row)]
    guards = {str(path): assets.checksum(path) for row in rows
              for role, path in row['paths'].items() if role in ('repo', 'editor')}
    return rows, guards


def prepare(root, settings, scope, role, package, version, qualification=None):
    if role not in ('repo', 'editor'):
        raise ValueError('Choose repo or editor as the source')
    data = assets.catalog(root)
    scopes = data.get('coordinatedScopes', {}).get(scope, [scope])
    if scope == 'all' or not any(g['package'] == package and assets.matches_scope(data, scope,
            {'scope': g['scope'], 'group': g['id'], 'kind': 'runtime', 'file': name})
            for g in data['groups'] for name in g['files']):
        raise ValueError('Choose a specific catalog runtime scope in the selected package')
    # Require package ownership/config before source acceptance, not after an external write.
    vdb.project(root)
    if not vdb.re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+(?:-[A-Za-z0-9.-]+)?', version):
        raise ValueError('Pass an explicit development/release version')
    assets.check_sync_conflicts(root, settings, scope, role, require_known=True)
    if any(s in ('animations', 'hks') for s in scopes):
        assets.validate_player_qualification(root, settings, role, qualification)
    if 'talk' in scopes:
        assets.validate_talk_qualification(root, settings, role, qualification)
    if 'events' in scopes:
        import event_workflow
        qualification = str(qualification or event_workflow.qualify(root, settings, role))
        event_workflow.validate(root, settings, role, qualification)
    differences = []
    destination = 'editor' if role == 'repo' else 'repo'
    rows, guards = scoped_inputs(root, settings, data, scope)
    for row in rows:
        if role not in row['paths'] or destination not in row['paths']:
            continue
        if assets.checksum(row['paths'][role]) != assets.checksum(row['paths'][destination]):
            differences.append(row['file'])
    directory = assets.safe_path(root, '.sovereign/propagation/' + uuid.uuid4().hex)
    directory.mkdir(parents=True)
    handoff = assets.prepare_handoff(root, settings, scope, role, qualification) if differences else None
    document = {'status': 'planned', 'scope': scope, 'sourceRole': role, 'packageId': package,
                'version': version, 'handoff': str(handoff) if handoff else None,
                'catalogHash': assets.fingerprint(data), 'settingsHash': assets.fingerprint(settings),
                'guards': guards,
                'qualification': qualification, 'note': 'Review/apply this receipt to accept the source and prepare a scoped stage. No deployment.'}
    assets.save(directory / 'receipt.json', document)
    return directory / 'receipt.json'


def apply(root, settings, receipt):
    base = assets.safe_path(root, '.sovereign/propagation')
    path = Path(receipt).absolute()
    if not path.is_relative_to(base):
        raise ValueError('Use a repo-local propagation receipt')
    path = assets.safe_path(base, path.relative_to(base))
    doc = assets.read(path)
    if doc['status'] not in ('planned', 'source-accepted') or doc['catalogHash'] != assets.fingerprint(assets.catalog(root)) or doc['settingsHash'] != assets.fingerprint(settings):
        raise ValueError('Propagation already applied or configuration changed; inspect before retrying')
    if doc.get('sfxEditorSave'):
        import sfx_workflow
        sfx_workflow.validate_saved(root, settings, doc['sfxEditorSave'])
    data = assets.catalog(root)
    rows, guards = scoped_inputs(root, settings, data, doc['scope'])
    expected_guards = doc.get('acceptedGuards') if doc['status'] == 'source-accepted' else doc['guards']
    if guards != expected_guards:
        raise ValueError('Scoped source/runtime changed since propagation plan')
    scopes = data.get('coordinatedScopes', {}).get(doc['scope'], [doc['scope']])
    if any(s in ('animations', 'hks') for s in scopes):
        assets.validate_player_qualification(root, settings, doc['sourceRole'], doc['qualification'])
    if 'talk' in scopes:
        assets.validate_talk_qualification(root, settings, doc['sourceRole'], doc['qualification'])
    if 'events' in scopes:
        import event_workflow
        event_workflow.validate(root, settings, doc['sourceRole'], doc.get('qualification'))
    expected_runtime = {'mod/' + row['file']: guards[str(row['paths'].get(doc['sourceRole'], row['paths']['repo']))]
                        for row in rows if row['kind'] == 'runtime' and row['package'] == doc['packageId']}
    # The source transaction has its own durable lock and drift-checked recovery.
    if doc['status'] == 'planned':
        accepted_guards = dict(guards)
        if doc['handoff']:
            handoff = assets.read(doc['handoff'])
            for entry in handoff['entries']:
                accepted_guards[entry['destination']] = entry['after']
            assets.apply_handoff(root, settings, doc['handoff'])
        else:
            assets.record_sync_baseline(root, settings, doc['scope'])
        doc.update(status='source-accepted', acceptedGuards=accepted_guards, expectedRuntime=expected_runtime)
        assets.save(path, doc)
    elif expected_runtime != doc.get('expectedRuntime'):
        raise ValueError('Accepted runtime differs from the preparation receipt')
    if scoped_inputs(root, settings, data, doc['scope'])[1] != doc['acceptedGuards']:
        raise ValueError('Accepted source changed; inspect before preparing a build')
    if doc.get('sfxEditorSave'):
        sfx_workflow.validate_saved(root, settings, doc['sfxEditorSave'])
    stage = doc.get('stageReceipt')
    if stage:
        _, prepared = vdb.load_prepared(root, settings, stage)
        if prepared['status'] not in ('prepared', 'completed'):
            raise ValueError('Preparation already submitted; inspect its recorded operation')
    else:
        stage = unchanged_stage(root, settings, doc, expected_runtime)
        if stage:
            doc['reusedBuild'] = True
            print('Payload unchanged; reusing the selected build for deployment.', flush=True)
        else:
            stage = vdb.prepare(root, settings, doc['packageId'], doc['version'], 'repo', doc['scope'])
    doc['stageReceipt'] = str(stage)
    assets.save(path, doc)
    stage_document = assets.read(stage)
    stage_files = stage_document['files']
    if any(stage_files.get(name, {}).get('sha256') != expected for name, expected in expected_runtime.items()):
        raise ValueError('Prepared runtime differs from reviewed source acceptance; inspect before staging')
    doc.update(status='prepared', stageReceipt=str(stage), buildVersion=stage_document.get('version'))
    assets.save(path, doc)
    return doc


def unchanged_stage(root, settings, doc, expected_runtime):
    # Release freezes and explicitly named test versions retain their requested identity.
    if not vdb.re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+-dev\..+', doc['version']):
        return None
    selected = vdb.selected_source(root, settings, doc['packageId'])
    if selected is None:
        return None
    path = assets.read(root / '.vdb/selected.json')[doc['packageId']]['receipt']
    _, stage = vdb.load_prepared(root, settings, path)
    owned = {'mod/' + name for group in assets.catalog(root)['groups']
             if group['package'] == doc['packageId'] for name in group['files']}
    if {name for name in stage['files'] if name.startswith('mod/')} != owned:
        return None
    if expected_runtime and all(stage['files'].get(name, {}).get('sha256') == value
                                for name, value in expected_runtime.items()):
        return path
    return None


def advance(root, settings, receipt, profile=None, seconds=15, stage_only=False):
    """Resume recorded requests; never infer failure from a wait timeout."""
    base = assets.safe_path(root, '.sovereign/propagation')
    path = Path(receipt).absolute()
    if not path.is_relative_to(base):
        raise ValueError('Use a repo-local propagation receipt')
    path = assets.safe_path(base, path.relative_to(base))
    # A separate lock covers the composition while child transactions use accept.lock.
    guard = assets.safe_path(root, '.sovereign/propagation.lock')
    with guard.open('x', encoding='utf-8') as stream:
        json.dump({'pid': vdb.os.getpid(), 'receipt': str(path)}, stream)
    try:
        doc = assets.read(path)
        if doc.get('finalizationMode') == 'profiles-v3':
            import finish_workflow
            return finish_workflow.advance(root, settings, path, doc, profile, seconds, stage_only)
        if stage_only:
            raise ValueError('Historical deployment receipts cannot become stage-only')
        if doc.get('profileId') not in (None, profile):
            raise ValueError('Propagation is bound to a different profile')
        if doc['status'] == 'complete':
            return doc
        if doc['status'] == 'source-accepted':
            doc = apply(root, settings, path)
        if doc['status'] not in ('prepared', 'staging', 'staged', 'deploying', 'deployed'):
            raise ValueError('Source preparation is incomplete; inspect the handoff before continuing')
        doc['profileId'] = profile
        _, stage = vdb.load_prepared(root, settings, doc['stageReceipt'])
        if stage['status'] == 'prepared':
            vdb.deployment_context(root, profile)
            if doc['status'] not in ('prepared', 'staging'):
                raise ValueError('Stage receipt unexpectedly returned to prepared')
            doc['status'] = 'staging'
            assets.save(path, doc)
            vdb.stage(root, settings, doc['stageReceipt'])
            stage = assets.read(doc['stageReceipt'])
        if stage['status'] in ('queued', 'pending', 'running'):
            vdb.wait(root, settings, doc['stageReceipt'], seconds)
            stage = assets.read(doc['stageReceipt'])
        if stage['status'] in ('queued', 'pending', 'running'):
            doc['status'] = 'staging'
            assets.save(path, doc)
            return doc
        if stage['status'] != 'completed':
            raise ValueError('Stage is ' + stage['status'] + '; inspect its recorded request, do not resubmit')
        vdb.staged_source(root, settings, doc['stageReceipt'])
        if not doc.get('deploymentReceipt'):
            vdb.deployment_context(root, profile)
            operation_id = uuid.uuid4().hex
            doc.update(status='deploying', deploymentReceipt=str(root / '.vdb/operations' / operation_id / 'receipt.json'))
            assets.save(path, doc)
            vdb.operate(root, settings, doc['stageReceipt'], 'deploy', profile, operation_id)
        operation_path = Path(doc['deploymentReceipt'])
        if not operation_path.is_file():
            raise ValueError('Deployment submission interrupted before its receipt; inspect before retrying')
        operation = assets.read(operation_path)
        if (operation['operation'] != 'deploy' or operation['profileId'] != profile
                or operation['packageId'] != doc['packageId'] or operation['buildId'] != stage['buildId']
                or Path(operation['stageReceipt']).absolute() != Path(doc['stageReceipt']).absolute()):
            raise ValueError('Deployment receipt does not belong to this propagation')
        if operation['status'] in ('queued', 'pending', 'running'):
            vdb.wait_operation(root, operation_path, seconds)
            operation = assets.read(operation_path)
        if operation['status'] in ('queued', 'pending', 'running'):
            return doc
        if operation['status'] != 'completed':
            raise ValueError('Deployment is ' + operation['status'] + '; inspect its recorded request, do not resubmit')
        result = operation['requests'][-1]['result']
        verification = result.get('result', {}).get('verification', {})
        if (result.get('operation') != 'deploy' or verification.get('deployed') != 'verified'
                or verification.get('enabled') is not True or verification.get('differences')):
            raise ValueError('Deployment completed without matching live bytes; inspect overrides before selecting this build')
        doc['status'] = 'deployed'
        assets.save(path, doc)
        vdb.select(root, settings, doc['stageReceipt'])
        doc.update(status='complete', note='Scoped source accepted; stage deployed and verified; exact build selected for packaging. Gameplay not verified.')
        assets.save(path, doc)
        return doc
    finally:
        guard.unlink()


def drive(root, settings, receipt, profile, wait_seconds, stage_only=False):
    if not 1 <= wait_seconds <= 600:
        raise ValueError('Wait must be 1 to 600 seconds')
    deadline = time.monotonic() + wait_seconds
    while True:
        doc = advance(root, settings, receipt, profile, min(15, max(0, int(deadline - time.monotonic()))), stage_only)
        print(f"Propagation {doc['status']}: {receipt}", flush=True)
        if doc['status'] == 'complete' or time.monotonic() >= deadline:
            return 0 if doc['status'] == 'complete' else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    synchronize = sub.add_parser('sync', help='Validate and sync saved files only; no build or deployment')
    synchronize.add_argument('--scope', required=True)
    synchronize.add_argument('--from', dest='source', choices=('repo', 'editor'), required=True)
    synchronize.add_argument('--qualification')
    for name in ('plan', 'run'):
        plan = sub.add_parser(name)
        plan.add_argument('--scope', required=True)
        plan.add_argument('--from', dest='source', choices=('repo', 'editor'), required=True)
        plan.add_argument('--package', choices=('main', 'textures'), default='main')
        plan.add_argument('--version', help='Defaults to the checked regular version from mod.json')
        plan.add_argument('--qualification')
        if name == 'run':
            plan.add_argument('--profile', help='Limit finalization to this profile; default is all game profiles')
            plan.add_argument('--stage-only', action='store_true')
            plan.add_argument('--wait-seconds', type=int, choices=range(1, 601), metavar='1..600', default=120)
    action = sub.add_parser('apply')
    action.add_argument('--receipt', required=True)
    resume = sub.add_parser('resume')
    resume.add_argument('--receipt', required=True)
    resume.add_argument('--profile', help='Use the original explicit profile, if any')
    resume.add_argument('--stage-only', action='store_true')
    resume.add_argument('--wait-seconds', type=int, choices=range(1, 601), metavar='1..600', default=120)
    args = parser.parse_args()
    settings = assets.read(core.ROOT / 'tools/eldenring-paths.local.json')
    if args.command in ('plan', 'run') and not args.version:
        import release_workflow
        args.version = release_workflow.check(core.ROOT)['targetVersion']
    if args.command == 'sync':
        sync(core.ROOT, settings, args.scope, args.source, args.qualification)
    elif args.command == 'plan':
        scopes = assets.catalog(core.ROOT).get('coordinatedScopes', {}).get(args.scope, [args.scope])
        if not args.qualification and any(s in ('animations', 'hks') for s in scopes):
            import player_workflow
            args.qualification = str(player_workflow.qualify(core.ROOT, settings, args.source))
        elif not args.qualification and 'talk' in scopes:
            if args.source != 'repo':
                raise ValueError('Dialogue preparation requires --from repo')
            import format_workflow
            args.qualification = str(format_workflow.qualify_talk(core.ROOT, settings))
        path = prepare(core.ROOT, settings, args.scope, args.source, args.package, args.version, args.qualification)
        document = assets.read(path)
        document['finalizationMode'] = 'profiles-v3'
        assets.save(path, document)
        print(path)
    elif args.command == 'apply':
        print(json.dumps(apply(core.ROOT, settings, args.receipt), indent=2))
    elif args.command == 'run':
        import finish_workflow
        finish_workflow.compatible_client(core.ROOT)
        # Check before SFX build/save can overwrite a saved editor output.
        assets.check_sync_conflicts(core.ROOT, settings, args.scope, args.source, require_known=True)
        scopes = assets.catalog(core.ROOT).get('coordinatedScopes', {}).get(args.scope, [args.scope])
        if not args.qualification and any(s in ('animations', 'hks') for s in scopes):
            import player_workflow
            print('Qualifying coordinated player sources and packed outputs...', flush=True)
            args.qualification = str(player_workflow.qualify(core.ROOT, settings, args.source))
        elif not args.qualification and 'talk' in scopes:
            if args.source != 'repo':
                raise ValueError('Dialogue propagation currently requires the accepted repo source')
            import format_workflow
            print('Qualifying dialogue sources and packed outputs...', flush=True)
            args.qualification = str(format_workflow.qualify_talk(core.ROOT, settings))
        sfx_save = None
        if 'sfx' in scopes and args.source == 'editor':
            import sfx_workflow
            sfx_save = sfx_workflow.build_and_save(core.ROOT, settings)
        path = prepare(core.ROOT, settings, args.scope, args.source, args.package, args.version, args.qualification)
        document = assets.read(path)
        document['finalizationMode'] = 'profiles-v3'
        assets.save(path, document)
        if sfx_save:
            document = assets.read(path)
            document['sfxEditorSave'] = str(sfx_save)
            assets.save(path, document)
        print(f'Propagation receipt: {path}', flush=True)
        apply(core.ROOT, settings, path)
        return drive(core.ROOT, settings, path, args.profile, args.wait_seconds, args.stage_only)
    else:
        return drive(core.ROOT, settings, args.receipt, args.profile, args.wait_seconds, args.stage_only)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, subprocess.TimeoutExpired, ET.ParseError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)
