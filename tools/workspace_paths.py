"""Inspect workspace paths and open a verified selected VDB folder. Never deploy."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

import asset_workflow as assets
import sovereign as core
import vdb_workflow as vdb


def stage_folder(root, settings, package, folder):
    source = vdb.selected_source(root, settings, package)
    if source is None:
        raise ValueError(f'No verified selected VDB stage for {package}; select a completed retained stage first')
    destination = assets.safe_path(source / 'mod', folder)
    if not destination.is_dir():
        raise ValueError('Selected VDB folder is missing: ' + str(destination))
    return destination


def shortcut_specs(root, settings):
    # Retain source/destination choices explicitly instead of relying on numeric names.
    groups = [
        ('smithbox', '_msg0.lnk', 'Live Messages.lnk', 'live', 'msg/engus'),
        ('smithbox', '_msg1.lnk', 'Selected Vortex Messages.lnk', 'stage', 'msg/engus'),
        ('smithbox', '_msg2.lnk', 'Repository Messages.lnk', 'repo', 'mod/msg/engus'),
        ('smithbox', '_regulation0.lnk', 'Live Regulation.lnk', 'live', ''),
        ('smithbox', '_regulation1.lnk', 'Repository Regulation.lnk', 'repo', 'mod'),
        ('scripts', '_event0.lnk', 'Live Events.lnk', 'live', 'event'),
        ('scripts', '_event1.lnk', 'Selected Vortex Events.lnk', 'stage', 'event'),
        ('scripts', '_event2.lnk', 'Repository Events.lnk', 'repo', 'mod/event'),
        ('scripts', '_script0.lnk', 'Live Scripts.lnk', 'live', 'action/script'),
        ('scripts', '_script1.lnk', 'Selected Vortex Scripts.lnk', 'stage', 'action/script'),
        ('scripts', '_script2.lnk', 'Repository Scripts.lnk', 'repo', 'mod/action/script'),
        ('animations', '_0.lnk', 'Live Player Files.lnk', 'live', 'chr'),
        ('animations', '_1.lnk', 'Selected Vortex Player Files.lnk', 'stage', 'chr'),
        ('animations', '_2.lnk', 'Repository Player Files.lnk', 'repo', 'mod/chr'),
        ('sfx', '_sfx0.lnk', 'Live Effects.lnk', 'live', 'sfx'),
        ('sfx', '_sfx1.lnk', 'Selected Vortex Effects.lnk', 'stage', 'sfx'),
        ('sfx', '_sfx2.lnk', 'Repository Effects.lnk', 'repo', 'mod/sfx'),
    ]
    result = []
    for workspace, old, name, kind, folder in groups:
        directory = Path(settings['roots'][workspace])
        if kind == 'stage':
            target = Path(sys.executable).with_name('pythonw.exe')
            arguments = f'"{root / "tools/workspace_paths.py"}" open-stage --folder "{folder}"'
        else:
            base = root if kind == 'repo' else Path(settings['roots']['live'])
            target = assets.safe_path(base, folder)
            arguments = ''
        result.append({'path': str(directory / name), 'oldPath': str(directory / old),
                       'target': str(target), 'arguments': arguments, 'workingDirectory': str(root)})
    return result


def check(root, settings):
    findings = []
    for group in ('roots', 'tools'):
        for name, value in settings[group].items():
            if not Path(value).exists():
                findings.append(f'Missing {group}.{name}: {value}')
    rows = list(assets.locations(root, settings, assets.catalog(root), True))
    for row in rows:
        for role in ('repo', 'editor'):
            path = row['paths'].get(role)
            if path is not None and not path.is_file():
                findings.append(f'Missing {role} asset: {path}')
    stages = {}
    for package in ('main', 'textures'):
        try:
            stages[package] = str(stage_folder(root, settings, package, ''))
        except (ValueError, OSError, KeyError) as error:
            findings.append(str(error))
    for key, relative, fields in [
            ('smithbox', 'project.json', ('GameRoot',)),
            ('animations', '_DSAS_PROJECT.json', ('GameDirectory', 'ModEngineDirectory')),
            ('animations', '_DSAS_WORKSPACE.json', ('GameDirectory', 'ModEngineDirectory'))]:
        path = Path(settings['roots'][key]) / relative
        if not path.is_file():
            findings.append('Missing editor configuration: ' + str(path))
            continue
        data = assets.read(path)
        for field in fields:
            if not data.get(field) or not Path(data[field]).is_dir():
                findings.append(f'Invalid {path.name} {field}: {data.get(field)}')
    launcher = root / 'tools/Propagate-Sovereign.ps1'
    launchers = [
        ('smithbox', 'propagate-regulation.bin.vbs', 'params'),
        ('smithbox', 'propagate-map.vbs', 'maps'),
        ('smithbox', 'propagate-item.msgbnd.dcx.vbs', 'item-text'),
        ('scripts', 'propagate-event.vbs', 'events'),
        ('scripts', 'propagate-c0000.hks.vbs', 'hks'),
        ('scripts', 'propagate-c9997.hks.vbs', 'hks'),
        ('animations', 'propagate-c0000.anibnd.vbs', 'animations'),
        ('animations', 'propagate-c0000.behbnd.vbs', 'animations'),
        ('sfx', 'propagate-sfxbnd_commoneffects.ffxbnd.vbs', 'sfx'),
    ]
    for workspace, name, scope in launchers:
        path = Path(settings['roots'][workspace]) / name
        content = path.read_text(encoding='utf-8-sig') if path.is_file() else ''
        if not launcher.is_file() or str(launcher).casefold() not in content.casefold() or f'-Scope {scope}"' not in content:
            findings.append('Missing or stale propagation launcher: ' + str(path))
    specs = shortcut_specs(root, settings)
    if os.name == 'nt':
        script = '''$rows = [Console]::In.ReadToEnd() | ConvertFrom-Json
$reader = New-Object -ComObject WScript.Shell
$results = @(foreach ($row in $rows) {
    if (Test-Path -LiteralPath $row.path -PathType Leaf) {
        $link = $reader.CreateShortcut($row.path)
        @{path=$row.path; target=$link.TargetPath; arguments=$link.Arguments; workingDirectory=$link.WorkingDirectory}
    } else { @{path=$row.path; target=''; arguments=''; workingDirectory=''} }
})
ConvertTo-Json -InputObject $results -Compress'''
        response = subprocess.run(['powershell.exe', '-NoProfile', '-Command', script],
                                  input=json.dumps(specs), capture_output=True, text=True, check=True)
        actual = {row['path']: row for row in json.loads(response.stdout)}
        for spec in specs:
            row = actual[spec['path']]
            if (os.path.normcase(row['target']) != os.path.normcase(spec['target'])
                    or row['arguments'] != spec['arguments']
                    or os.path.normcase(row['workingDirectory']) != os.path.normcase(spec['workingDirectory'])):
                findings.append('Missing or stale shortcut: ' + spec['path'])
            if not Path(spec['target']).exists():
                findings.append('Missing shortcut target: ' + spec['target'])
            if Path(spec['oldPath']).exists():
                findings.append('Obsolete shortcut remains: ' + spec['oldPath'])
    else:
        findings.append('Windows shortcut validation requires Windows')
    return {'findings': findings, 'cataloguedLocations': len(rows), 'selectedStages': stages,
            'shortcuts': len(specs), 'propagationLaunchers': len(launchers),
            'note': 'Path and file checks only; editors and deployment were not launched.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('check')
    sub.add_parser('shortcuts', help='Print intended shortcuts without creating them')
    command = sub.add_parser('open-stage')
    command.add_argument('--package', choices=('main', 'textures'), default='main')
    command.add_argument('--folder', default='')
    args = parser.parse_args()
    root = core.ROOT
    settings = assets.read(root / 'tools/eldenring-paths.local.json')
    try:
        if args.command == 'open-stage':
            os.startfile(stage_folder(root, settings, args.package, args.folder))
        elif args.command == 'shortcuts':
            print(json.dumps(shortcut_specs(root, settings), indent=2))
        else:
            report = check(root, settings)
            print(json.dumps(report, indent=2))
            return bool(report['findings'])
    except (ValueError, OSError, KeyError) as error:
        if args.command == 'open-stage' and os.name == 'nt':
            import ctypes
            ctypes.windll.user32.MessageBoxW(None, str(error), 'Sovereign folder unavailable', 16)
        else:
            print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
