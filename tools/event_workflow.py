"""Verify that saved event binaries implement the selected saved DarkScript sources."""
from pathlib import Path
import shutil

import asset_workflow as assets
import sovereign as core


def inputs(root, settings, role):
    if role not in ('repo', 'editor'):
        raise ValueError('Choose repo or editor event sources')
    data = assets.catalog(root)
    group = next((s for s in data['sources'] if s['id'] == 'event-sources'), None)
    if group is None:
        raise ValueError('Catalog is missing the event-sources group')
    source = assets.safe_path(root, group['repo']) if role == 'repo' else assets.safe_path(
        settings['roots'][group['editorRoot']], group['editor'])
    files = {str(p): assets.checksum(p) for p in source.iterdir()
             if p.is_file() and p.name.endswith(('.emevd.dcx', '.emevd.dcx.js'))}
    for path in files:
        assets.safe_path(source, Path(path).relative_to(source))
    runtime = {r['file']: r['paths'][role] for r in assets.locations(root, settings, data)
               if r['scope'] == 'events'}
    files.update({str(p): assets.checksum(p) for p in runtime.values()})
    if not runtime or None in files.values():
        raise ValueError('Missing saved event inputs or runtime binaries')
    for name, binary in runtime.items():
        companion = source / Path(name).name
        if not (source / (companion.name + '.js')).is_file():
            raise ValueError('Missing event source: ' + str(companion) + '.js')
        if assets.checksum(companion) != files[str(binary)]:
            raise ValueError('Saved event source companion differs from runtime: ' + name + '; compile and reconcile before propagation')
    return source, runtime, files


def tool_hashes(root, settings):
    smithbox = Path(settings['tools']['smithbox'])
    darkscript = Path(settings['tools']['darkscript'])
    paths = [darkscript, *sorted(darkscript.parent.glob('*.dll')),
             root / 'tools/event_workflow.py', root / 'tools/sovereign.py',
             root / 'tools/inspection/Program.cs', root / 'tools/inspection/Inspect.csproj',
             smithbox / 'Andre.SoulsFormats.dll', smithbox / 'oo2core_9_win64.dll']
    result = {str(p): assets.checksum(p) for p in paths}
    if None in result.values():
        raise ValueError('Missing event compiler or inspection dependency')
    return result


def validate(root, settings, role, qualification):
    if not qualification:
        raise ValueError('Event handoff requires a current event qualification; run propagation plan again')
    base = assets.safe_path(root, '.codex-temp/event-qualifications')
    path = Path(qualification).absolute()
    if not path.is_relative_to(base):
        raise ValueError('Use a repo-local event qualification receipt')
    path = assets.safe_path(base, path.relative_to(base))
    proof = assets.read(path)
    if (proof.get('kind') != 'event-roundtrip' or proof.get('status') != 'qualified'
            or proof.get('sourceRole') != role):
        raise ValueError('Saved events did not qualify')
    if (proof['catalogHash'] != assets.fingerprint(assets.catalog(root))
            or proof['settingsHash'] != assets.fingerprint(settings)
            or proof['files'] != inputs(root, settings, role)[2]
            or proof['tools'] != tool_hashes(root, settings)):
        raise ValueError('Event sources, binaries or tools changed; rerun event qualification')
    return {'path': str(path), 'sha256': assets.checksum(path)}


def qualify(root, settings, role):
    source, runtime, files = inputs(root, settings, role)
    fingerprints = tool_hashes(root, settings)
    for path in sorted((root / '.codex-temp/event-qualifications').glob('*/receipt.json'),
                       key=lambda p: p.stat().st_mtime, reverse=True):
        try:
            validate(root, settings, role, path)
            print('Saved events/tools unchanged; reusing event qualification.', flush=True)
            return path
        except (ValueError, OSError, KeyError, TypeError):
            continue
    with core.operation('events'):
        run = core.new_run('event-qualifications')
        work, output = run / 'input', run / 'compiled'
        work.mkdir(); output.mkdir()
        for path in source.iterdir():
            if str(path) in files:
                shutil.copy2(path, work / path.name)
        executable = Path(settings['tools']['darkscript'])
        result = core.run_process([executable, '/cmd', '-compile', '-game', 'er', '-indir', work, '-outdir', output], executable.parent)
        (run / 'compiler.log').write_bytes(result.stdout + result.stderr)
        expected = sorted(p.name[:-3] for p in work.glob('*.emevd.dcx.js'))
        if sorted(p.name for p in output.iterdir() if p.is_file()) != expected:
            raise ValueError('Unexpected compiler output; inspect ' + str(run))
        helper, env = core.build_inspector(settings)
        reports = []
        for name, binary in runtime.items():
            candidate = output / Path(name).name
            before, after = core.event_data(binary, helper, env), core.event_data(candidate, helper, env)
            comparison = core.compare_events(before, after)
            reports.append({'file': name, **comparison})
            if not comparison['equal']:
                assets.save(run / (candidate.name + '.before.json'), before)
                assets.save(run / (candidate.name + '.after.json'), after)
        assets.save(run / 'comparison.json', reports)
        if any(not r['equal'] for r in reports):
            changed = ', '.join(r['file'] for r in reports if not r['equal'])
            raise ValueError('Saved event binaries are stale: ' + changed +
                             '. Compile/save these sources in DarkScript, then retry. Comparison: ' + str(run))
        if files != inputs(root, settings, role)[2] or fingerprints != tool_hashes(root, settings):
            raise ValueError('Event inputs changed during qualification; retry with saved stable files')
        proof = {'kind': 'event-roundtrip', 'status': 'qualified', 'sourceRole': role,
                 'catalogHash': assets.fingerprint(assets.catalog(root)), 'settingsHash': assets.fingerprint(settings),
                 'files': files, 'tools': fingerprints, 'reports': reports, 'gameplayVerified': False}
        assets.save(run / 'receipt.json', proof)
        return run / 'receipt.json'
