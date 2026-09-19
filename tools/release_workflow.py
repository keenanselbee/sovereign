"""Check the local release target/history and print the current propagation version."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
# Match Grailwright's authored release numbering for propagation and releases.
VERSION = r'(?:0|[1-9][0-9]*)\.[0-9]\.[0-9]'


def read_history(path):
    text = Path(path).read_text(encoding='utf-8-sig').replace('\r\n', '\n').strip()
    blocks = []
    for block in text.split('\n\n'):
        lines = block.splitlines()
        match = re.fullmatch('Version (' + VERSION + ')', lines[0]) if lines else None
        if not match or len(lines) < 2:
            raise ValueError('changelog.txt needs Version X.Y.Z followed immediately by change lines; one blank line between blocks')
        changes = lines[1:]
        if any(not line.strip() or line != line.strip() or re.match(r'^(Version\s|[-*#]\s)', line)
               for line in changes):
            raise ValueError('changelog.txt must use plain change lines without Markdown or embedded version headers')
        if len(set(line.casefold() for line in changes)) != len(changes):
            raise ValueError('changelog.txt contains duplicate change lines within a version')
        blocks.append({'version': match[1], 'changes': changes})
    numbers = [tuple(map(int, block['version'].split('.'))) for block in blocks]
    if numbers != sorted(set(numbers), reverse=True):
        raise ValueError('changelog.txt versions must be unique and newest first')
    return blocks


def check(root, manifest=None):
    root = Path(root)
    if manifest is None:
        manifest = json.loads((root / 'mod.json').read_text(encoding='utf-8-sig'))
    version = manifest.get('version')
    if not isinstance(version, str) or not re.fullmatch(VERSION, version):
        raise ValueError('mod.json version must be X.Y.Z with single-digit minor and patch components')
    blocks = read_history(root / 'changelog.txt')
    if blocks[0]['version'] != version:
        raise ValueError('mod.json version and newest changelog.txt version differ')
    return {'targetVersion': version, 'historyVersions': [b['version'] for b in blocks],
            'releaseReady': manifest.get('releaseReady', False),
            'note': 'Local metadata consistency only; deployment, gameplay and publication are separate.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    # Keep the old command as a compatibility alias, without generating dev labels.
    parser.add_argument('command', choices=('check', 'target-version', 'dev-version'))
    args = parser.parse_args()
    if args.command == 'check':
        print(json.dumps(check(ROOT), indent=2))
    else:
        print(check(ROOT)['targetVersion'])


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)
