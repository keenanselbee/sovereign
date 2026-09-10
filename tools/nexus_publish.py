"""Review (default) or explicitly publish an exact verified Vortex release ZIP."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

import nexus_workflow as workflow
import sovereign as core


def api(method, path, body=None):
    key = core.os.environ.get('NEXUS_API_KEY', '').strip()
    if not key:
        raise ValueError('NEXUS_API_KEY is required in the environment')
    request = urllib.request.Request('https://api.nexusmods.com/v3' + path,
                                    data=json.dumps(body).encode() if body is not None else None,
                                    headers={'apikey': key, 'Accept': 'application/json', 'Content-Type': 'application/json'},
                                    method=method)
    try:
        with urllib.request.build_opener(core.NoNexusRedirect()).open(request, timeout=45) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        raise ValueError(f'Nexus {method} failed (HTTP {error.code}); inspect upload journal before retrying') from None
    except (urllib.error.URLError, OSError):
        raise ValueError('Nexus request failed; inspect upload journal before retrying') from None
    if not isinstance(result, dict) or not isinstance(result.get('data'), dict):
        raise ValueError('Unexpected Nexus API response')
    return result['data']


def storage(method, url, data, content_type):
    if not isinstance(url, str) or not url.startswith('https://'):
        raise ValueError('Upload storage must use HTTPS')
    request = urllib.request.Request(url, data=data, method=method, headers={'Content-Type': content_type})
    try:
        # Storage requests never carry the Nexus API key; signed URLs are not logged.
        with urllib.request.build_opener(core.NoNexusRedirect()).open(request, timeout=180) as response:
            return response.headers.get('ETag'), response.read()
    except (urllib.error.URLError, OSError):
        raise ValueError('Upload storage request failed; signed URL omitted') from None


def upload_parts(archive, invoke=api, send=storage):
    archive = Path(archive)
    upload = invoke('POST', '/uploads/multipart', {'size_bytes': archive.stat().st_size, 'filename': archive.name})
    size, urls = upload.get('part_size_bytes'), upload.get('part_presigned_urls')
    if not isinstance(size, int) or isinstance(size, bool) or not 0 < size <= 128 * 1024 * 1024:
        raise ValueError('Unexpected multipart part size')
    if not isinstance(urls, list) or len(urls) != (archive.stat().st_size + size - 1) // size:
        raise ValueError('Multipart URL count does not match archive size')
    document = ET.Element('CompleteMultipartUpload')
    with archive.open('rb') as stream:
        for number, url in enumerate(urls, 1):
            content = stream.read(size)
            etag, _ = send('PUT', url, content, 'application/octet-stream')
            if not etag:
                raise ValueError('Missing multipart ETag')
            part = ET.SubElement(document, 'Part')
            ET.SubElement(part, 'PartNumber').text = str(number)
            ET.SubElement(part, 'ETag').text = etag.strip('"')
    _, response = send('POST', upload['complete_presigned_url'], ET.tostring(document), 'application/xml')
    if response and ET.fromstring(response).tag.rsplit('}', 1)[-1] == 'Error':
        raise ValueError('Storage rejected multipart completion')
    upload_id = upload['id']
    if not isinstance(upload_id, str) or not core.re.fullmatch(r'[a-zA-Z0-9-]+', upload_id):
        raise ValueError('Unexpected upload ID')
    invoke('POST', f'/uploads/{upload_id}/finalise')
    deadline = time.monotonic() + 180
    while time.monotonic() < deadline:
        state = invoke('GET', f'/uploads/{upload_id}').get('state')
        if state == 'available':
            return upload_id
        if state in ('failed', 'error', 'rejected'):
            raise ValueError('Nexus rejected the uploaded archive')
        time.sleep(2)
    raise ValueError('Upload availability timed out; do not create a version yet')


def verified_archive(archive, manifest):
    archive = Path(archive).resolve()
    if not archive.is_relative_to(core.contained(core.ROOT, '.codex-temp/vortex-packages')):
        raise ValueError('Upload archive must be a repository Vortex package candidate')
    receipt = core.read_json(archive.parent / 'receipt.json')
    if (receipt.get('kind') != 'vortex-package' or receipt.get('draft') is not False
            or receipt.get('archive') != archive.name or receipt.get('version') != manifest.get('version')
            or receipt.get('sha256') != core.digest(archive)):
        raise ValueError('Archive is draft, changed, or does not match the selected release receipt')
    source = workflow.vortex_root()
    current = workflow.inventory(source, manifest)
    if str(source) != receipt['source'] or current['files'] != receipt['files']:
        raise ValueError('Vortex source differs from the verified release ZIP; rebuild/review')
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


def publish_plan(archive, manifest):
    if not manifest.get('releaseReady') or any(not row.get('verified') for row in manifest['dependencies']):
        raise ValueError('Release readiness and dependency verification are required')
    issues = core.nexus_issues(core.ROOT, manifest)
    if issues:
        raise ValueError('\n'.join(issues))
    archive, receipt = verified_archive(archive, manifest)
    remote = core.nexus_status(manifest)
    if not remote['current']:
        raise ValueError('Active remote version is ambiguous')
    if remote['current']['version'] == manifest['version']:
        raise ValueError('Version label is already active; reconcile bytes and use description-only updates')
    versions = api('GET', f"/mod-files/{manifest['nexus']['groupId']}/versions")['versions']
    if any(row.get('version') == manifest['version'] for row in versions):
        raise ValueError('Target version label already exists in this group; reconcile instead of uploading again')
    directory = core.contained(core.ROOT, manifest['nexus']['descriptionDirectory'])
    changelog = reviewed_changelog(directory, manifest['version'], remote['current']['version'])
    paths = [core.ROOT / 'mod.json', directory / 'nexus-file-desc.txt', directory / 'nexus-changelog.txt']
    return {'archive': str(archive), 'archiveSha256': receipt['sha256'], 'version': manifest['version'],
            'groupId': manifest['nexus']['groupId'], 'modId': manifest['nexus']['modId'],
            'baseline': remote['current'], 'description': (directory / 'nexus-file-desc.txt').read_text(encoding='utf-8-sig').strip(),
            'name': manifest['displayName'], 'changelog': changelog,
            'sourceHashes': {str(path): core.digest(path) for path in paths}}


def publish(plan, invoke=api, uploader=upload_parts):
    archive = Path(plan['archive'])
    journal = archive.parent / 'upload-journal.json'
    if journal.exists():
        raise ValueError('An upload journal already exists. Reconcile its remote outcome before any retry')
    state = {'status': 'upload-started', 'plan': plan, 'versionId': None}
    core.write_json(journal, state)
    upload_id = uploader(archive)
    if core.digest(archive) != plan['archiveSha256'] or any(core.digest(path) != expected for path, expected in plan['sourceHashes'].items()):
        raise ValueError('Release input changed during upload; no file version was created')
    latest = invoke('GET', f"/mod-files/{plan['groupId']}/versions")['versions']
    active = [row for row in latest if row.get('category') in ('main', 'update', 'optional', 'miscellaneous')]
    if (any(row.get('version') == plan['version'] for row in latest)
            or {row['id'] for row in active} != {plan['baseline']['id']}):
        raise ValueError('Remote release changed during upload; reconcile before creating a version')
    state.update(status='version-post-started', uploadId=upload_id)
    core.write_json(journal, state)
    created = invoke('POST', f"/mod-files/{plan['groupId']}/versions", {
        'upload_id': upload_id, 'name': plan['name'], 'version': plan['version'], 'description': plan['description'],
        'file_category': 'main', 'primary_mod_manager_download': True, 'allow_mod_manager_download': True,
        'show_requirements_pop_up': True, 'update_mod_version': True, 'archive_existing_file': True,
        'previous_version_id': plan['baseline']['id']})
    version_id = created.get('version', {}).get('id')
    state.update(status='version-created', versionId=version_id)
    core.write_json(journal, state)
    if not version_id:
        raise ValueError('Version POST succeeded without an immutable ID; do not repeat it')
    state['status'] = 'changelog-post-started'
    core.write_json(journal, state)
    invoke('POST', f"/mods/{plan['modId']}/changelogs", {'version': plan['version'], 'changelog': plan['changelog']})
    state['status'] = 'changelog-posted'
    core.write_json(journal, state)
    versions = invoke('GET', f"/mod-files/{plan['groupId']}/versions")['versions']
    matches = [row for row in versions if row.get('id') == version_id]
    if len(matches) != 1 or matches[0].get('version') != plan['version']:
        raise ValueError('Upload/changelog completed but version reread is unverified; do not retry writes')
    state.update(status='version-read-verified', remoteVersion=matches[0], descriptions='Page descriptions pending separate browser save')
    core.write_json(journal, state)
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', required=True)
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    with core.operation('nexus'):
        plan = publish_plan(args.archive, core.read_json(core.ROOT / 'mod.json'))
        core.emit(publish(plan) if args.publish else plan, True)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f'ERROR: {error}', file=core.sys.stderr)
        core.sys.exit(1)
