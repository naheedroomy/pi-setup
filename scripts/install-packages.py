#!/usr/bin/env python3
"""Install the captured Pi packages. Run configure.py --apply before starting Pi."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--apply', action='store_true', help='Execute installs; default prints commands')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
settings = json.loads((root / 'config/pi-agent/settings.json').read_text())
for item in settings['packages']:
    source = item if isinstance(item, str) else item['source']
    command = ['pi', 'install', source]
    print(' '.join(command), flush=True)
    if args.apply:
        subprocess.run(command, check=True, cwd=Path.home())
print('Next: python3 scripts/configure.py --apply (required to restore extension filters).')
