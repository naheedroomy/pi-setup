#!/usr/bin/env python3
"""Preview or apply portable Pi configuration. Never reads or copies credentials."""
import argparse
import copy
import datetime
import json
from pathlib import Path
import shlex
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
    if source.startswith('git:'):
        return source.rsplit('@', 1)[0]
    if not source.startswith('npm:'):
        return source
    name = source[4:]
    return name.rsplit('@', 1)[0] if '@' in name[1:] else name


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Write files; default only previews destinations')
    parser.add_argument('--profile', choices=('personal', 'corporate'), default='personal')
    parser.add_argument('--home', type=Path, default=Path.home(), help='Target home directory (also useful for isolated validation)')
    args = parser.parse_args()
    home = args.home.expanduser().resolve()
    agent = home / '.pi/agent'
    profile_dir = ROOT / 'config' / ('pi-agent' if args.profile == 'personal' else 'corporate')
    mapping = [(p, agent / p.relative_to(profile_dir)) for p in sorted(profile_dir.rglob('*')) if p.is_file()]
    mapping += [(ROOT / 'config/acp.json', home / '.pi/acp.json'), (ROOT / 'config/todo.json', home / '.config/rpiv-todo/config.json')]
    if args.profile == 'personal':
        mapping.append((ROOT / 'config/lens.json', home / '.pi-lens/config.json'))
    plan = []
    for src, dest in mapping:
        # JSON escaping handles spaces, backslashes and quotes in a home directory.
        try:
            text = src.read_text()
        except OSError as exc:
            raise SystemExit(f'Cannot read {src}: {exc}') from exc
        text = text.replace('__PI_AGENT_DIR__', json.dumps(str(agent))[1:-1] if src.suffix == '.json' else str(agent))
        if src.suffix == '.json':
            try:
                template = json.loads(text)
            except json.JSONDecodeError as exc:
                raise SystemExit(f'Invalid JSON template {src}: {exc}') from exc
            new = template
            existing = dest
            if dest == agent / 'mcp-adapter.json' and not dest.exists():
                legacy = agent / 'mcp.json'
                if legacy.exists():
                    existing = legacy
            if existing.exists():
                try:
                    old = json.loads(existing.read_text())
                except (OSError, json.JSONDecodeError) as exc:
                    raise SystemExit(f'Cannot read {existing}: {exc}') from exc
                if existing == dest or 'hostConfigDiscovery' in old.get('settings', {}):
                    new = merge(old, new)
                if dest == agent / 'settings.json':
                    managed = {package_name(p) for p in template['packages']}
                    extras = [p for p in old.get('packages', []) if package_name(p) not in managed]
                    if args.profile == 'corporate':
                        if extras:
                            sources = [p if isinstance(p, str) else p['source'] for p in extras]
                            raise SystemExit(f'Corporate profile has extra packages. Ask before removing them: {sources}')
                        new['packages'] = template['packages']
                        new['subagents']['agentOverrides'] = template['subagents']['agentOverrides']
                    else:
                        retired = {'bigpowers', '@narumitw/pi-goal'}
                        new['packages'] += [p for p in extras if package_name(p) not in retired]
            text = json.dumps(new, indent=2) + '\n'
        if dest == agent / 'AGENTS.md':
            start, end = '<!-- pi-setup:start -->', '<!-- pi-setup:end -->'
            original = dest.read_text() if dest.exists() else ''
            if start in original and end in original:
                original = original.split(start, 1)[0] + original.split(end, 1)[1]
            text = original.rstrip() + '\n\n' + start + '\n' + text.rstrip() + '\n' + end + '\n'
        plan.append((dest, text))
    if args.profile == 'personal':
        shell = home / '.bashrc'
        start, end = '# pi-setup:environment:start', '# pi-setup:environment:end'
        original = shell.read_text() if shell.exists() else ''
        if start in original and end in original:
            original = original.split(start, 1)[0] + original.split(end, 1)[1]
        env_path = shlex.quote(str(agent / 'pi-setup-env.sh'))
        text = original.rstrip() + '\n\n' + start + f'\n[ ! -f {env_path} ] || . {env_path}\n' + end + '\n'
        plan.append((shell, text))
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
