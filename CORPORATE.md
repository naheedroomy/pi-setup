# Corporate VDI profile (repo-only)

This is a separate, smaller Pi configuration in [`config/corporate/`](config/corporate/). **Nothing here is applied to the personal Pi installation by this repository change.** Install it on the VDI only after your organization's approval. It does not include credentials, models hosted locally, preconfigured MCP servers, Designer/Observer, or Antigravity.

## Packages

| Package | Pinned source | Purpose |
| --- | --- | --- |
| Ponytail | `git:github.com/DietrichGebert/ponytail@v4.10.3` | Minimal coding guidance |
| Billion Context Pi | `npm:billion-context-pi@0.1.83` | Context compression; its delegation is off |
| Pi Subagents | `npm:pi-subagents@0.75.0` | Built-in roles and supervised children |
| Pi MCP Adapter | `npm:pi-mcp-adapter@5.0.0` | MCP gateway; no servers included |
| Pi Web Access | `npm:pi-web-access@0.35.0` | Search/fetch, subject to company policy |
| Pi Goal X | `npm:pi-goal-x@0.32.3` | The **only** goal/continuation package |
| RPIV Todo | `npm:@juicesharp/rpiv-todo@2.12.0` | Task list (the current setup's Pi Todo) |

The parent remains GPT-6.1 Sol/medium. The seven stock subagent overrides match the personal profile: scout Luna/low, researcher Luna/medium, worker Luna/high, evidence-auditor Sol/medium, reviewer Sol/high, oracle Sol/high, delegate Sol/medium. They inherit project context, cannot recursively delegate, and load only the relevant MCP/Web Access and Billion Context extensions. No custom agents are installed. The same scheduler settings permit **up to two concurrent child runs** with a 30-minute default timeout. That can still be too much for a VDI: reduce `parallel.concurrency`, `globalConcurrencyLimit`, and `maxActiveAsyncRunsPerSession` from `2` to `1` in `config/corporate/extensions/subagent/config.json` before installing if needed. `parallel.maxTasks: 8` is a queued-work limit, not eight simultaneous children.

## Install on the corporate machine

1. Review company policy for Pi, OpenAI Codex, web access, git/npm downloads and MCP tools. Use a supported Node/Pi installation; this profile was recorded against Node 24.21.0 and Pi 1.0.2. Do not copy personal `auth.json`, sessions or memory files. Back up the VDI's `~/.pi/agent` settings first.
2. Run `pi list`. **If any older goal extension is installed** (for example `@narumitw/pi-goal`), **ask the machine's owner before deleting it or its data**. After approval, remove that exact installed source with `pi remove <source-from-pi-list>`. Archive old `~/.pi/agent/pi-goal.json` or old goal state only with approval; neither script below deletes it. Do not run competing goal extensions beside Goal X.
3. Preview installs and destinations from this repo. Neither preview changes the machine:

   ```bash
   python3 scripts/install-packages.py --profile corporate
   python3 scripts/configure.py --profile corporate
   ```

4. On the corporate machine only, after reviewing and removing unwanted packages **with approval**, apply:

   ```bash
   python3 scripts/install-packages.py --profile corporate --apply
   python3 scripts/configure.py --profile corporate --apply
   ```

   The configuration helper **refuses to overwrite an existing package list containing extras** rather than silently removing them. Its apply step creates backups under `~/.pi/agent/backups/pi-setup-*` and merges other existing settings; inspect retained settings and any existing `mcp-adapter.json` servers before starting Pi. If an old adapter-only `mcp.json` exists, the helper imports its server settings into the new adapter config but leaves the old file untouched; review and archive it with approval. `__PI_AGENT_DIR__` paths are expanded by the helper. Avoid starting Pi between the install and configuration steps.
5. Restart Pi; verify `pi list`, `/subagents`, `/goal-status`, and only the corporate-approved MCP/web tools. Test one bounded scout run before considering two-way concurrency. Any GitHub/Google/other external research access remains subject to corporate policy.

Goal X commands are `/goal <idea>` (confirm the draft) or `/goal-direct <agreed objective>`. The former `goal_complete` and `goal_wait` tools are **not** Goal X tools. RPIV Todo remains separate from Goal X's task evidence. MCP tool approval is enabled by default (`approveTools: true`), adapter scripts are off, and no CodeGraph or Playwright server launches unless explicitly configured. No permanent machine-wide memory package or Lens processes are installed by this profile.
