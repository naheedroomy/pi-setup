"""Offline regression checks for the portable setup helpers and snapshots."""
import contextlib
import io
import json
import re
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='pi setup test ')
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.agent = self.home / '.pi/agent'

    def configure(self, profile='personal'):
        return subprocess.run(
            [sys.executable, str(ROOT / 'scripts/configure.py'), '--apply',
             '--home', str(self.home), '--profile', profile],
            capture_output=True, text=True,
        )

    def seed(self, relative, value):
        path = self.home / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value) if isinstance(value, dict) else value)
        return path

    def test_fresh_home_and_reapply(self):
        self.assertEqual(self.configure().returncode, 0)
        settings_path = self.agent / 'settings.json'
        first = settings_path.read_text()
        self.assertEqual(self.configure().returncode, 0)
        self.assertEqual(first, settings_path.read_text())
        settings = json.loads(first)
        self.assertNotIn('__PI_AGENT_DIR__', first)
        self.assertEqual(settings['extensions'], ['-builtin:mcp'])
        for role in settings['subagents']['agentOverrides'].values():
            self.assertTrue(all(path.startswith(str(self.agent)) for path in role['extensions']))
        inactive = [p for p in settings['packages'] if isinstance(p, dict)]
        self.assertEqual(inactive, [{'source': 'npm:pi-continue@0.9.3', 'extensions': []}])
        agents_text = (self.agent / 'AGENTS.md').read_text()
        self.assertEqual(agents_text.count('<!-- pi-setup:start -->'), 1)
        self.assertTrue(list((self.agent / 'backups').glob('pi-setup-*/manifest.json')))

    def test_preserve_unrelated_and_replace_retired(self):
        self.seed('.pi/agent/settings.json', {
            'customFlag': True,
            'packages': ['npm:pi-web-access@0.1.0', 'npm:bigpowers',
                         'npm:@narumitw/pi-goal', 'npm:unrelated-package@1.2.3'],
        })
        self.seed('.pi/agent/AGENTS.md', '# Private retained guidance\n')
        auth = self.seed('.pi/agent/auth.json', {'privateFixture': 'not-a-credential'})
        self.assertEqual(self.configure().returncode, 0)
        settings = json.loads((self.agent / 'settings.json').read_text())
        self.assertTrue(settings['customFlag'])
        self.assertIn('npm:unrelated-package@1.2.3', settings['packages'])
        self.assertNotIn('npm:bigpowers', settings['packages'])
        self.assertNotIn('npm:@narumitw/pi-goal', settings['packages'])
        self.assertNotIn('npm:pi-web-access@0.1.0', settings['packages'])
        self.assertIn('# Private retained guidance', (self.agent / 'AGENTS.md').read_text())
        self.assertEqual(json.loads(auth.read_text()), {'privateFixture': 'not-a-credential'})
        self.assertFalse(list((self.agent / 'backups').rglob('auth.json')))

    def test_reviewer_has_required_native_diff_tool(self):
        self.assertEqual(self.configure().returncode, 0)
        settings = json.loads((self.agent / 'settings.json').read_text())
        self.assertIn('watchdog_diff', settings['subagents']['agentOverrides']['reviewer']['tools'])

    def test_personal_memory_environment_is_idempotent_and_backed_up(self):
        shell = self.seed('.bashrc', '# Retained shell settings\nexport EXISTING_SETTING=yes\n')
        self.assertEqual(self.configure().returncode, 0)
        first = shell.read_text()
        self.assertIn('export EXISTING_SETTING=yes', first)
        self.assertIn('pi-setup-env.sh', first)
        self.assertEqual(first.count('# pi-setup:environment:start'), 1)
        self.assertEqual(self.configure().returncode, 0)
        self.assertEqual(shell.read_text(), first)
        self.assertTrue(list((self.agent / 'backups').glob('pi-setup-*/.bashrc')))
        result = subprocess.run(['bash', '-c', f'source {str(self.agent / "pi-setup-env.sh")!r}; printf "%s %s" "$QMD_FORCE_CPU" "$PI_MEMORY_QMD_SEARCH_TIMEOUT_MS"'], capture_output=True, text=True, env={'PATH': '/usr/bin:/bin'})
        self.assertEqual(result.stdout, '1 300000')

    def test_corporate_does_not_change_shell_environment(self):
        shell = self.seed('.bashrc', '# Corporate shell unchanged\n')
        self.assertEqual(self.configure('corporate').returncode, 0)
        self.assertEqual(shell.read_text(), '# Corporate shell unchanged\n')
        self.assertFalse((self.agent / 'pi-setup-env.sh').exists())

    def test_legacy_adapter_migration(self):
        self.seed('.pi/agent/mcp.json', {
            'settings': {'hostConfigDiscovery': 'off', 'customFlag': True},
            'mcpServers': {'fixture': {'command': 'fixture-command'}},
        })
        self.assertEqual(self.configure().returncode, 0)
        adapter = json.loads((self.agent / 'mcp-adapter.json').read_text())
        self.assertTrue(adapter['settings']['customFlag'])
        self.assertIn('fixture', adapter['mcpServers'])
        self.assertTrue((self.agent / 'mcp.json').exists())

    def test_corporate_refuses_extra_packages(self):
        self.seed('.pi/agent/settings.json', {'packages': ['npm:unrelated-package@1.2.3']})
        result = self.configure('corporate')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Ask before removing them', result.stderr)

    def run_installer(self, profile='personal', apply=False):
        argv = ['install-packages.py', '--profile', profile] + (['--apply'] if apply else [])
        with patch.object(sys, 'argv', argv), patch.object(Path, 'home', return_value=self.home), \
                patch('subprocess.run') as run, contextlib.redirect_stdout(io.StringIO()) as output:
            runpy.run_path(str(ROOT / 'scripts/install-packages.py'), run_name='__main__')
        return run, output.getvalue()

    def test_install_preview_does_not_write(self):
        run, output = self.run_installer()
        run.assert_not_called()
        self.assertIn('npm pkg set overrides.', output)
        self.assertIn(f"(cd '{self.agent / 'npm'}' &&", output)
        self.assertFalse((self.agent / 'backups').exists())

    def test_personal_install_applies_overrides_with_backup(self):
        manifest = self.seed('.pi/agent/npm/package.json', {'fixture': True})
        self.seed('.pi/agent/npm/package-lock.json', {'lockfileVersion': 3})
        run, _ = self.run_installer(apply=True)
        calls = run.call_args_list
        self.assertEqual(calls[-1].args[0], ['npm', 'install', '--ignore-scripts'])
        self.assertEqual(calls[-1].kwargs['cwd'], manifest.parent)
        self.assertEqual(calls[-2].args[0][:3], ['npm', 'pkg', 'set'])
        backup = list((self.agent / 'backups').glob('pi-setup-npm-*/package.json'))
        self.assertEqual(len(backup), 1)
        self.assertEqual(backup[0].read_text(), manifest.read_text())

    def test_corporate_install_has_no_personal_overrides(self):
        run, _ = self.run_installer('corporate', apply=True)
        self.assertTrue(all(call.args[0][0] == 'pi' for call in run.call_args_list))
        self.assertFalse((self.agent / 'backups').exists())

    def test_snapshot_and_readme_match_templates(self):
        inventory = json.loads((ROOT / 'inventory.json').read_text())
        settings = json.loads((ROOT / 'config/pi-agent/settings.json').read_text())
        sources = [p if isinstance(p, str) else p['source'] for p in settings['packages']]
        self.assertCountEqual(sources, [p['portableSource'] for p in inventory['packages']])
        overrides = json.loads((ROOT / 'config/npm-overrides.json').read_text())
        self.assertEqual(inventory['npmOverrides'], overrides)
        blocks = [json.loads(s) for s in re.findall(r'```json\n(.*?)\n```', (ROOT / 'README.md').read_text(), re.S)]
        for template in [ROOT / 'config/acp.json', ROOT / 'config/todo.json',
                         ROOT / 'config/lens.json', ROOT / 'config/npm-overrides.json',
                         *sorted((ROOT / 'config/pi-agent').rglob('*.json'))]:
            self.assertIn(json.loads(template.read_text()), blocks, str(template))


if __name__ == '__main__':
    unittest.main()
