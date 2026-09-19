"""Small repository adapter for the separately installed Nexus Automation package."""
import json
import os
from pathlib import Path
import subprocess


def tool_root(repo):
    root = os.environ.get('NEXUS_AUTOMATION_ROOT')
    if not root:
        config = Path(repo) / 'nexus-automation.local.json'
        if not config.is_file():
            raise ValueError('Configure nexus-automation.local.json toolRoot or NEXUS_AUTOMATION_ROOT; see Nexus Automation README')
        root = json.loads(config.read_text(encoding='utf-8-sig')).get('toolRoot')
    if not root or not Path(root).is_absolute():
        raise ValueError('Nexus Automation toolRoot must be absolute')
    root = Path(root).resolve()
    if json.loads((root / 'package.json').read_text(encoding='utf-8-sig')).get('name') != '@keenan/nexus-automation':
        raise ValueError('Configured toolRoot is not Nexus Automation')
    return root


def invoke(repo, command, request_path):
    cli = tool_root(repo) / 'bin/nexus.mjs'
    version = subprocess.run(['node', str(cli), 'version'], capture_output=True, text=True, check=True, timeout=30)
    if json.loads(version.stdout).get('protocolVersion') != 1:
        raise ValueError('Unsupported Nexus Automation protocol')
    result = subprocess.run(['node', str(cli), command, '--request', str(request_path)],
                            stdout=subprocess.PIPE, text=True, encoding='utf-8', check=True)
    return json.loads(result.stdout)


def read(repo, route):
    if not os.environ.get('NEXUS_API_KEY', '').strip():
        raise ValueError('NEXUS_API_KEY is required in the environment')
    cli = tool_root(repo) / 'bin/nexus.mjs'
    try:
        result = subprocess.run(['node', str(cli), 'api', '--path', route], capture_output=True,
                                text=True, encoding='utf-8', check=True, timeout=90)
        return json.loads(result.stdout)
    except (subprocess.SubprocessError, ValueError, OSError):
        raise ValueError('Nexus read failed; remote state remains Verify') from None
