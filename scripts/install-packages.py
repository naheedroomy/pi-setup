#!/usr/bin/env python3
"""Install the captured Pi packages. Run configure.py --apply before starting Pi."""
import argparse
import json
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
for item in settings['packages']:
    source = item if isinstance(item, str) else item['source']
    command = ['pi', 'install', source]
    print(' '.join(command), flush=True)
    if args.apply:
        subprocess.run(command, check=True, cwd=Path.home())
print(f'Next: python3 scripts/configure.py --profile {args.profile} --apply (required to restore extension filters).')
