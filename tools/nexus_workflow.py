"""Sovereign Nexus audit, browser descriptions and Vortex-backed packaging."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
import zipfile

import sovereign as core

ROOT = core.ROOT


def vortex_root(config_path=None):
    settings = core.config(argparse.Namespace(config=config_path))
    runtime = Path(settings['roots']['vortex']).resolve()
    if runtime.name.lower() != 'mod':
        raise ValueError('Configured Vortex runtime root must end in mod; its parent is the package source')
    if not (runtime / 'regulation.bin').is_file():
        raise ValueError('Vortex source is unavailable or lacks mod/regulation.bin')
    return runtime.parent


def inventory(source, manifest):
    source = Path(source).resolve()
    if manifest.get('package', {}).get('source') != 'vortex':
        raise ValueError('Package source must be explicitly configured as vortex')
    excluded_dirs = {name.lower() for name in manifest['package']['excludeDirectories']}
    included, excluded = {}, []
    seen = set()
    for directory, directories, filenames in os.walk(source, followlinks=False):
        base = Path(directory)
        for name in directories:
            if (base / name).is_symlink() or (hasattr(Path, 'is_junction') and (base / name).is_junction()):
                raise ValueError(f'Package source contains a directory link: {base / name}')
        for name in filenames:
            path = base / name
            relative = path.relative_to(source).as_posix()
            core.contained(source, relative)
            if path.is_symlink():
                raise ValueError(f'Package source contains a file link: {relative}')
            key = relative.lower()
            if key in seen:
                raise ValueError(f'Case-colliding package path: {relative}')
            seen.add(key)
            if {part.lower() for part in path.relative_to(source).parts[:-1]} & excluded_dirs:
                excluded.append(relative)
                continue
            if path.relative_to(source).parts[0] not in ('mod', 'mods'):
                raise ValueError(f'Unexpected top-level Vortex file; review explicitly: {relative}')
            if any(part.lower() in ('.git', '.codex-temp', 'node_modules') for part in path.relative_to(source).parts) or any(
                    fnmatch.fnmatch(name.lower(), pattern) for pattern in ('.env*', '*.secret*', '*.local.json', 'api.txt')):
                raise ValueError(f'Private/development file in package source: {relative}')
            included[relative] = {'size': path.stat().st_size, 'sha256': core.digest(path)}
    if 'mod/regulation.bin' not in included:
        raise ValueError('Vortex package lacks mod/regulation.bin')
    return {'source': str(source), 'files': dict(sorted(included.items())), 'excluded': sorted(excluded)}


def package_plan(manifest, config_path=None):
    result = inventory(vortex_root(config_path), manifest)
    differences = []
    for name, entry in result['files'].items():
        if not name.startswith('mod/'):
            continue
        repo_path = core.contained(ROOT, name[4:])
        if not repo_path.is_file():
            differences.append({'file': name, 'state': 'Vortex only'})
        elif core.digest(repo_path) != entry['sha256']:
            differences.append({'file': name, 'state': 'Different repo bytes; Vortex is package source'})
    result['repoDifferences'] = differences
    result['fileCount'] = len(result['files'])
    result['bytes'] = sum(row['size'] for row in result['files'].values())
    return result


def build_vortex_package(source, manifest, run, version, draft=True):
    if not core.re.fullmatch(r'[0-9]+(?:\.[0-9]+){1,3}(?:-[A-Za-z0-9.-]+)?', version):
        raise ValueError('Use an explicit numeric version with optional prerelease suffix')
    if not draft and (not manifest.get('releaseReady') or manifest.get('version') != version
                      or any(not row.get('verified') for row in manifest['dependencies'])):
        raise ValueError('Release version, releaseReady and dependency verification gates must pass')
    before = inventory(source, manifest)
    run = Path(run)
    archive = run / f"Sovereign-{version}{'-DRAFT' if draft else ''}.zip"
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as zipped:
        for name, expected in before['files'].items():
            # Stream large archives instead of loading them into memory.
            with core.contained(source, name).open('rb') as stream, zipped.open(name, 'w', force_zip64=True) as output:
                shutil.copyfileobj(stream, output)
    with zipfile.ZipFile(archive) as zipped:
        if sorted(zipped.namelist()) != sorted(before['files']) or zipped.testzip():
            raise ValueError('ZIP entry/CRC verification failed')
        for name, expected in before['files'].items():
            with zipped.open(name) as stream:
                actual = hashlib.file_digest(stream, 'sha256').hexdigest()
            if actual != expected['sha256']:
                raise ValueError(f'ZIP content differs from Vortex snapshot: {name}')
    if inventory(source, manifest) != before:
        raise ValueError('Vortex files changed during packaging; reject this candidate')
    receipt = {**before, 'kind': 'vortex-package', 'draft': draft, 'version': version,
               'archive': archive.name, 'sha256': core.digest(archive),
               'createdAt': datetime.now(timezone.utc).isoformat(), 'gameplayVerified': False}
    core.write_json(run / 'receipt.json', receipt)
    return archive


def setup_browser():
    npm = shutil.which('npm.cmd') or shutil.which('npm')
    if not npm or not shutil.which('node'):
        raise ValueError('Node.js and npm are required')
    root = core.contained(ROOT, '.codex-temp/nexus-description-tool')
    root.mkdir(parents=True, exist_ok=True)
    core.write_json(root / 'package.json', {'name': 'sovereign-nexus-browser', 'private': True,
                                         'dependencies': {'playwright': '1.62.0'}})
    subprocess.run([npm, 'install', '--ignore-scripts', '--no-audit', '--no-fund'], cwd=root, check=True)


def chrome_arguments(executable, profile, port):
    return [str(executable), '--remote-debugging-address=127.0.0.1', f'--remote-debugging-port={port}',
            f'--user-data-dir={profile}', '--no-first-run', '--disable-background-mode',
            '--hide-crash-restore-bubble', '--window-size=1300,1044', '--new-window', 'about:blank']


def start_chrome(profile, interactive=False):
    candidates = [Path(os.environ[key]) / tail for key, tail in (
        ('PROGRAMFILES', 'Google/Chrome/Application/chrome.exe'),
        ('PROGRAMFILES(X86)', 'Google/Chrome/Application/chrome.exe'),
        ('LOCALAPPDATA', 'Google/Chrome/Application/chrome.exe')) if os.environ.get(key)]
    executable = next((path for path in candidates if path.is_file()), None)
    if executable is None:
        raise ValueError('Installed Google Chrome was not found')
    Path(profile).mkdir(parents=True, exist_ok=True)
    with socket.socket() as reservation:
        reservation.bind(('127.0.0.1', 0))
        port = reservation.getsockname()[1]
    startup = subprocess.STARTUPINFO() if os.name == 'nt' else None
    if startup is not None and not interactive:
        startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup.wShowWindow = 0
    env = os.environ.copy()
    env.pop('NEXUS_API_KEY', None)
    process = subprocess.Popen(chrome_arguments(executable, profile, port), startupinfo=startup, env=env,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise ValueError('Dedicated Chrome exited; close any window using the Sovereign profile and retry')
            try:
                with urllib.request.urlopen(f'http://127.0.0.1:{port}/json/version', timeout=1) as response:
                    endpoint = json.load(response)
                if endpoint.get('webSocketDebuggerUrl'):
                    return process, port
            except (OSError, ValueError):
                pass
            time.sleep(0.2)
        raise ValueError('Dedicated Chrome debugging endpoint did not become ready')
    except Exception:
        if process.poll() is None:
            process.terminate()
        raise


def descriptions(manifest, save=False, login=False, backup=None):
    core.validate_nexus_metadata(manifest)
    tool_root = core.contained(ROOT, '.codex-temp/nexus-description-tool')
    if not (tool_root / 'node_modules/playwright/package.json').is_file():
        raise ValueError('Run tools/Update-NexusDescription.ps1 -Setup once to install local browser tooling')
    directory = core.contained(ROOT, manifest['nexus']['descriptionDirectory'])
    if not login and not backup:
        issues = core.nexus_issues(ROOT, manifest, descriptions_only=True)
        if issues:
            raise ValueError('\n'.join(issues))
    paths = [ROOT / 'mod.json']
    source_hashes = {str(ROOT / 'mod.json'): core.digest(ROOT / 'mod.json')}
    desired = {}
    if not login and not backup:
        for name in ('short', 'full'):
            path = directory / f'nexus-{name}-desc.txt'
            paths.append(path)
            data = path.read_bytes()
            source_hashes[str(path)] = hashlib.sha256(data).hexdigest()
            desired[f'desired{name.title()}Description'] = data.decode('utf-8-sig').strip()
    if backup:
        candidate = Path(backup).resolve()
        backup_root = core.contained(ROOT, '.codex-temp/nexus-description-backups')
        if not candidate.is_relative_to(backup_root):
            raise ValueError('Restore backup must be under this repository Nexus backup directory')
        stored = core.read_json(candidate)
        if stored.get('nexusUrl') != manifest['nexus']['url'] or stored.get('packageName') != 'Sovereign':
            raise ValueError('Restore backup belongs to another target')
        paths.append(candidate)
        source_hashes[str(candidate)] = core.digest(candidate)
        backup = str(candidate)
    with core.operation('nexus'):
        if core.read_json(ROOT / 'mod.json') != manifest or any(core.digest(path) != expected for path, expected in source_hashes.items()):
            raise ValueError('Description inputs changed; rerun the review')
        run = core.new_run('nexus-description-requests')
        request = {'action': 'login' if login else ('revert-' if backup else '') + ('save' if save else 'review'),
                   'repoRoot': str(ROOT), 'packageName': 'Sovereign', 'displayName': manifest['displayName'],
                   'nexusUrl': manifest['nexus']['url'], 'browser': 'Chrome', 'timeoutSeconds': 180,
                   'profileRoot': str(core.contained(ROOT, '.codex-temp/nexus-browser-profile-chrome')),
                   'backupRoot': str(core.contained(ROOT, '.codex-temp/nexus-description-backups')),
                   'resultPath': str(run / 'result.json'), 'restoreBackupPath': backup,
                   'sourceHashes': source_hashes, **desired}
        env = os.environ.copy()
        env['NEXUS_DESCRIPTION_TOOL_ROOT'] = str(tool_root)
        # Browser authentication uses its isolated profile; it does not need the API key.
        env.pop('NEXUS_API_KEY', None)
        # Launch regular installed Chrome, like Grailwright; Playwright only attaches.
        # Do not use its launchPersistentContext defaults (--no-sandbox/automation flags).
        chrome, port = start_chrome(request['profileRoot'], interactive=login)
        request['remoteDebuggingPort'] = port
        core.write_json(run / 'request.json', request)
        try:
            subprocess.run(['node', str(ROOT / 'tools/nexus/update-nexus-description.mjs'),
                            '--request', str(run / 'request.json')], cwd=ROOT, env=env, check=True, timeout=600)
        except subprocess.CalledProcessError:
            progress = core.contained(ROOT, '.codex-temp/nexus-description-progress/Sovereign.json')
            reason = core.read_json(progress).get('error', 'Browser review failed') if progress.is_file() else 'Browser review failed'
            raise ValueError(f'{reason} Evidence: {run}') from None
        finally:
            try:
                chrome.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Only the process launched above; never close the user's personal Chrome.
                chrome.terminate()
        result = core.read_json(run / 'result.json')
        if result.get('status') not in ('reviewed', 'already-current', 'saved-and-verified', 'logged-in'):
            raise ValueError('Browser did not verify completion; inspect its progress/backup before retrying')
        result['sourceHashes'] = request['sourceHashes']
        result['observedAt'] = datetime.now(timezone.utc).isoformat()
        core.write_json(run / 'result.json', result)
        print(f'Browser evidence: {run / "result.json"}', file=sys.stderr)
        return result


def published_payload_matches(package, remote):
    """An observed immutable version plus an exact local upload receipt can establish Current."""
    if not remote.get('current'):
        return False
    for journal in core.contained(ROOT, '.codex-temp/vortex-packages').glob('*/upload-journal.json'):
        try:
            state = core.read_json(journal)
            plan = state['plan']
            if (state.get('versionId') != remote['current']['id'] or plan['groupId'] != remote['groupId']
                    or plan['modId'] != remote['modId'] or plan['version'] != remote['current']['version']):
                continue
            receipt = core.read_json(journal.parent / 'receipt.json')
            archive = core.contained(journal.parent, receipt['archive'])
            if (receipt.get('kind') == 'vortex-package' and receipt.get('draft') is False
                    and receipt['version'] == plan['version'] and receipt['files'] == package['files']
                    and receipt['sha256'] == plan['archiveSha256'] == core.digest(archive)):
                return True
        except (OSError, ValueError, KeyError, TypeError):
            continue
    return False


def audit(manifest, skip_browser=False, config_path=None):
    report = {'mod': manifest['displayName'], 'localVersion': manifest['version'],
              'localIssues': core.nexus_issues(ROOT, manifest), 'surfaces': {
                  key: 'Verify' for key in ('file', 'shortDescription', 'fileDescription', 'fullDescription', 'changelog')}}
    try:
        remote = core.nexus_status(manifest)
        report['remote'] = remote
        if remote['current'] and manifest['version'] and remote['current']['version'] != manifest['version']:
            report['surfaces']['file'] = 'Update: version differs; review package and intended version'
    except ValueError as error:
        report['apiIssue'] = str(error)
    try:
        plan = package_plan(manifest, config_path)
        report['package'] = {key: value for key, value in plan.items() if key != 'files'}
        if 'remote' in report and published_payload_matches(plan, report['remote']):
            report['surfaces']['file'] = 'Current'
    except (ValueError, OSError) as error:
        report['packageIssue'] = str(error)
    if not skip_browser:
        try:
            page = descriptions(manifest)
            for name in ('shortDescription', 'fullDescription'):
                report['surfaces'][name] = 'Update' if page[name + 'Changed'] else 'Current'
        except (ValueError, OSError, subprocess.SubprocessError) as error:
            report['browserIssue'] = str(error)
    report['note'] = 'A matching version label does not verify archive contents. File pitch/changelog need browser evidence.'
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config')
    commands = parser.add_subparsers(dest='command', required=True)
    desc = commands.add_parser('descriptions')
    modes = desc.add_mutually_exclusive_group()
    modes.add_argument('--save', action='store_true')
    modes.add_argument('--login', action='store_true')
    modes.add_argument('--setup', action='store_true')
    desc.add_argument('--backup')
    review = commands.add_parser('audit')
    review.add_argument('--skip-browser', action='store_true')
    commands.add_parser('package-plan')
    package = commands.add_parser('package')
    package.add_argument('--version', required=True)
    package.add_argument('--release', action='store_true')
    args = parser.parse_args()
    manifest = core.read_json(ROOT / 'mod.json')
    if args.command == 'descriptions':
        if args.backup and (args.setup or args.login):
            raise ValueError('Backup cannot be combined with setup/login')
        if args.setup:
            with core.operation('nexus'):
                setup_browser()
        else:
            descriptions(manifest, args.save, args.login, args.backup)
    elif args.command == 'audit':
        core.emit(audit(manifest, args.skip_browser, args.config), True)
    elif args.command == 'package-plan':
        core.emit(package_plan(manifest, args.config), True)
    elif args.command == 'package':
        if args.release:
            issues = core.nexus_issues(ROOT, manifest)
            if issues:
                raise ValueError('\n'.join(issues))
        with core.operation('package'):
            run = core.new_run('vortex-packages')
            archive = build_vortex_package(vortex_root(args.config), manifest, run, args.version, not args.release)
            print(archive)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)
