#!/usr/bin/env python3
"""Install the captured Pi packages. Run configure.py --apply before starting Pi."""
import argparse
import datetime
import json
import shlex
import shutil
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--apply', action='store_true', help='Execute installs; default prints commands')
parser.add_argument('--profile', choices=('personal', 'corporate'), default='personal')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
profile_dir = 'pi-agent' if args.profile == 'personal' else 'corporate'
try:
    settings = json.loads((root / 'config' / profile_dir / 'settings.json').read_text())
except (OSError, json.JSONDecodeError) as exc:
    raise SystemExit(f'Cannot read {args.profile} package list: {exc}') from exc
overrides = {}
if args.profile == 'personal':
    try:
        overrides = json.loads((root / 'config/npm-overrides.json').read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f'Cannot read personal npm overrides: {exc}') from exc
for item in settings['packages']:
    source = item if isinstance(item, str) else item['source']
    command = ['pi', 'install', source]
    print(shlex.join(command), flush=True)
    if args.apply:
        subprocess.run(command, check=True, cwd=Path.home())
if args.profile == 'personal':
    npm_dir = Path.home() / '.pi/agent/npm'
    commands = [
        ['npm', 'pkg', 'set', *[f'overrides.{name}={version}' for name, version in overrides.items()]],
        ['npm', 'install', '--ignore-scripts'],
    ]
    if args.apply:
        backup = Path.home() / '.pi/agent/backups' / ('pi-setup-npm-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
        backup.mkdir(parents=True, exist_ok=True)
        for name in ('package.json', 'package-lock.json'):
            source = npm_dir / name
            if source.exists():
                shutil.copy2(source, backup / name)
        print('npm metadata backup:', backup, flush=True)
    for command in commands:
        print(f'(cd {shlex.quote(str(npm_dir))} && {shlex.join(command)})', flush=True)
        if args.apply:
            subprocess.run(command, check=True, cwd=npm_dir)
print(f'Next: python3 scripts/configure.py --profile {args.profile} --apply (required to restore extension filters).')
