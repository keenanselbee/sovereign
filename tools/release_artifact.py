"""Retain one verified release ZIP per version, bound to its selected VDB build."""
import re
from pathlib import Path
import shutil

import asset_workflow as assets
import vdb_workflow as vdb


def selected_stage(root, settings, version, package_id="main"):
    if package_id not in ("main", "textures"):
        raise ValueError("Unknown release package")
    if not re.fullmatch(r'[0-9]+\.[0-9]\.[0-9]', version):
        raise ValueError('Release version must use X.Y.Z with single-digit minor and patch components')
    source = vdb.selected_source(root, settings, package_id)
    if source is None:
        raise ValueError('Release packaging requires a completed selected VDB stage')
    selected = assets.read(root / '.vdb/selected.json')[package_id]
    path, receipt = vdb.load_prepared(root, settings, selected['receipt'])
    if receipt['version'] != version:
        raise ValueError('Selected stage version differs from release version; freeze and select a matching stage first')
    return source, receipt, {'projectId': 'sovereign', 'packageId': package_id, 'buildId': receipt['buildId'],
        'version': version, 'stageReceipt': receipt.get('reusedStageReceipt', str(path))}


def verify(root, settings, archive, manifest, package_id="main", require_selected=True):
    import nexus_workflow as workflow
    version = manifest['version']
    directory = assets.safe_path(root, f'.vdb/releases/{package_id}/{version}')
    archive = Path(archive).resolve()
    if archive != directory / f'Sovereign{"-Textures" if package_id == "textures" else ""}-{version}.zip':
        raise ValueError('Upload archive must be the retained VDB release ZIP; run release packaging first')
    receipt = assets.read(directory / 'receipt.json')
    if require_selected:
        source, stage, identity = selected_stage(root, settings, version, package_id)
    else:
        source, stage = vdb.staged_source(root, settings, receipt['stage']['stageReceipt'])
        identity = {'projectId': 'sovereign', 'packageId': stage['packageId'], 'buildId': stage['buildId'],
                    'version': stage['version'], 'stageReceipt': receipt['stage']['stageReceipt']}
        if identity['packageId'] != package_id or identity['version'] != version:
            raise ValueError('Retained stage does not belong to this package/version')
    if (receipt.get('kind') != 'vortex-package' or receipt.get('draft') is not False
            or receipt.get('archive') != archive.name or receipt.get('version') != version
            or receipt.get('stage') != identity or receipt.get('source') != str(source)
            or receipt.get('files') != stage['files'] or receipt.get('sha256') != assets.checksum(archive)):
        raise ValueError('Retained release identity or contents changed; inspect receipts and use a new version for changed builds')
    if workflow.package_inventory(source, manifest, package_id)['files'] != receipt['files']:
        raise ValueError('Release package inventory differs from its selected stage')
    return archive, receipt


def package(root, settings, source, manifest, run, version, package_id="main"):
    import nexus_workflow as workflow
    with assets.lock(root):
        selected, stage, identity = selected_stage(root, settings, version, package_id)
        if Path(source).resolve() != selected.resolve():
            raise ValueError('Release source is not the exact selected VDB stage')
        # Adopt pre-guard stages too; conflicting historical versions fail closed.
        stage_path = Path(assets.read(root / '.vdb/selected.json')[package_id]['receipt'])
        vdb.reserve_version(root, settings, stage_path, stage)
        directory = assets.safe_path(root, f'.vdb/releases/{package_id}/{version}')
        retained = directory / f'Sovereign{"-Textures" if package_id == "textures" else ""}-{version}.zip'
        if directory.exists():
            return verify(root, settings, retained, manifest, package_id)[0]
        archive = workflow.write_vortex_package(selected, manifest, run, version, draft=False, package_id=package_id)
        receipt = assets.read(Path(run) / 'receipt.json')
        if receipt['files'] != stage['files'] or selected_stage(root, settings, version, package_id)[2] != identity:
            raise ValueError('Selected release stage changed during packaging')
        receipt['stage'] = identity
        assets.save(Path(run) / 'receipt.json', receipt)
        directory.mkdir(parents=True)
        # An interrupted retention fails closed on retry; never overwrite retained bytes.
        with archive.open('rb') as incoming, retained.open('xb') as outgoing:
            shutil.copyfileobj(incoming, outgoing)
        if assets.checksum(retained) != receipt['sha256']:
            raise ValueError('Retained release ZIP differs from the verified candidate')
        assets.save(directory / 'receipt.json', receipt)
        return verify(root, settings, retained, manifest, package_id)[0]
