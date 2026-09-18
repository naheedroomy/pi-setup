#!/usr/bin/env python3
"""Preview or apply portable Pi configuration. Never reads or copies credentials."""
import argparse
import copy
import datetime
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def merge(old, new):
    result = copy.deepcopy(old)
    for key, value in new.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def package_name(item):
    source = item if isinstance(item, str) else item['source']
    if not source.startswith('npm:'):
        return source
    name = source[4:]
    return name.rsplit('@', 1)[0] if '@' in name[1:] else name


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Write files; default only previews destinations')
    parser.add_argument('--home', type=Path, default=Path.home(), help='Target home directory (also useful for isolated validation)')
    args = parser.parse_args()
    home = args.home.expanduser().resolve()
    agent = home / '.pi/agent'
    mapping = [(p, agent / p.relative_to(ROOT / 'config/pi-agent')) for p in sorted((ROOT / 'config/pi-agent').rglob('*')) if p.is_file()]
    mapping += [(ROOT / 'config/acp.json', home / '.pi/acp.json'), (ROOT / 'config/lens.json', home / '.pi-lens/config.json'), (ROOT / 'config/todo.json', home / '.config/rpiv-todo/config.json')]
    plan = []
    for src, dest in mapping:
        # JSON escaping handles spaces, backslashes and quotes in a home directory.
        text = src.read_text().replace('__PI_AGENT_DIR__', json.dumps(str(agent))[1:-1] if src.suffix == '.json' else str(agent))
        if src.suffix == '.json':
            new = json.loads(text)
            if dest.exists():
                old = json.loads(dest.read_text())
                new = merge(old, new)
                if dest == agent / 'settings.json':
                    managed = {package_name(p) for p in new['packages']}
                    new['packages'] += [p for p in old.get('packages', []) if package_name(p) not in managed]
            text = json.dumps(new, indent=2) + '\n'
        if dest == agent / 'AGENTS.md':
            start, end = '<!-- pi-setup:start -->', '<!-- pi-setup:end -->'
            original = dest.read_text() if dest.exists() else ''
            if start in original and end in original:
                original = original.split(start, 1)[0] + original.split(end, 1)[1]
            text = original.rstrip() + '\n\n' + start + '\n' + text.rstrip() + '\n' + end + '\n'
        plan.append((dest, text))
    backup = agent / 'backups' / ('pi-setup-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    manifest = []
    for dest, text in plan:
        print(('WRITE ' if args.apply else 'PLAN  ') + str(dest))
        if not args.apply:
            continue
        existed = dest.exists()
        relative = dest.relative_to(home)
        if existed:
            saved = backup / relative
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dest, saved)
        manifest.append({'path': str(relative), 'existed': existed})
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text)
    if args.apply:
        backup.mkdir(parents=True, exist_ok=True)
        (backup / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
        print('Backup:', backup)
        print('Restart Pi after installation and authentication. Existing live sessions are not changed.')


if __name__ == '__main__':
    main()
