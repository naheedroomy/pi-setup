# Portable Pi setup guide

This repository describes and reproduces the Pi personal setup updated on **2026-10-07**. It is a deployment specification for a human or a setup agent, with copyable configuration and optional helper scripts. It covers Pi, not the earlier OMP/OpenCode installations. The target is a personal Linux workstation using the default `~/.pi/agent` directory. For the separate, reduced-resource **corporate VDI** profile, see [CORPORATE.md](CORPORATE.md); the commands below default to the personal profile.

For a plain-language explanation of the team, model choices and delegation workflow, read [How my Pi subagents work](SUBAGENTS.md).

## Design and operating contract

Use a concise GPT-6.1 Sol coordinating parent at medium thinking, retain the stock Pi Subagents role roster, and delegate bounded work when useful. Keep two children active in normal operation. Use GPT-6 Luna for routine implementation and exploration, GPT-6.1 Sol for review/advice, and Gemini Flash for UI/image tasks. Reserve GPT-6 Astra for explicit hard-task escalation. Preserve the user's full objective through implementation and verification.

The package responsibilities are deliberately separate:

- **Pi Subagents** dispatches children; Billion Context's separate delegation is disabled.
- **RPIV Todo** is the task tracker. Memory's scratchpad is not the authoritative task list.
- **Billion Context Pi (ACP)** owns context compression. Native compaction remains enabled as a fallback if ACP is removed.
- **Pi Goal X** drives explicit goals, persistent tasks, continuation, and optional independent completion auditing. Tests and acceptance criteria still need real evidence.
- **MCP Adapter** supplies lazy CodeGraph/Playwright tools. Web Access supplies research tools.
- **OpenWiki** supplies host-native repository-wiki tools. Its global CLI handles standalone wiki and integration commands; it is not another continuation engine.
- **Lens** supplies diagnostics on demand; startup scans, autoformat, autofix, automatic tests and its guard are disabled.
- **Ponytail** encourages minimal, correct changes. Its Pi extension injects the active mode into the parent prompt; use `/ponytail lite|full|ultra|off` to adjust it. It does not replace project requirements or verification.

This configuration avoids routine tool-approval prompts. It does not bypass provider authentication, operating-system permissions, explicit user cancellation, or real product decisions. Pi itself does not require an OpenCode-style `--dangerously-skip-permissions` flag. The [official Pi overview](https://pi.dev/) describes its extension-based approach to permissions and capabilities.

## Runtime and reproducibility

Observed runtime: Node.js **24.21.0**, npm **11.19.0**, Pi (`@earendil-works/pi-coding-agent`) **1.0.4**, CodeGraph (`@colbymchenry/codegraph`) **1.6.2**, qmd (`@tobilu/qmd`) **2.8.3**, OpenWiki CLI **0.7.1**, Python 3 for the helper scripts. `git` is useful for project workflows; `gh` is needed only for GitHub work.

Use the versions below for the closest reproduction. This is a top-level package snapshot, **not a full dependency lock or a guarantee of future provider availability**. Transitive dependencies and Playwright's `@latest` MCP command can change. Record intentional upgrades and rerun validation.

All package sources are pinned to the latest stable releases checked on 2026-10-07; `inventory.json` records the installed versions. Ponytail uses the latest GitHub release tag. Packages already at the latest version remain unchanged. This update applies to the personal profile; the corporate profile remains a separate snapshot.

The latest MCP Adapter and Web Access releases pin older MCP libraries with the OAuth advisory [GHSA-6qxp-vccf-f47h](https://github.com/advisories/GHSA-6qxp-vccf-f47h). `config/npm-overrides.json` pins the patched client/core **2.3.1** and SDK **1.32.1**. The personal installation helper applies these npm overrides and backs up the npm manifest/lockfile. This is a standard dependency override, not an edit to installed package source. Rerun MCP tests and `npm audit` after changes; do not use `npm audit fix --force` to downgrade the top-level extensions.

OpenWiki 0.7.1 introduces one unresolved advisory in `braces <=3.0.3` through `deepagents` → `fast-glob` → `micromatch`. npm reports **five high-severity affected packages**, all from that advisory; no fixed release was available on 2026-10-07. Do not feed untrusted, deeply nested glob patterns to these dependencies. The latest OpenWiki was installed at the user's request; this is a recorded upstream risk, not a clean audit.

## Packages

| Package | Version | Activation and purpose |
| --- | --- | --- |
| `pi-mcp-adapter` | 5.1.0 | Active; lazy MCP discovery and calls (replaces built-in MCP) |
| `pi-web-access` | 0.37.0 | Active; search, fetch and source checks |
| `pi-subagents` | 0.76.1 | Active; stock role prompts, async children and supervision |
| `@juicesharp/rpiv-ask-user-question` | 2.12.0 | Active; structured questions for material decisions |
| `@juicesharp/rpiv-todo` | 2.12.0 | Active; one substantive task list |
| `pi-lens` | 4.3.0 | Active; diagnostics loaded on demand |
| `ponytail` | git tag `v4.13.0` | Active; minimal implementation guidance and review commands |
| `billion-context-pi` | 0.1.83 | Active; context compression and retrieval |
| `pi-antigravity` | 0.9.0 | Active; Google Antigravity provider |
| `pi-memory` | 0.4.2 | Active; durable memory and scratchpad |
| `@narumitw/pi-btw` | 0.61.1 | Active; temporary side conversations |
| `pi-continue` | 0.9.3 | Installed but inactive; `extensions: []` |
| `pi-goal-x` | 0.32.3 | Active; explicit goal planning, continuation and optional auditing |
| `openwiki` | 0.7.1 | Active; six native Pi tools for repository wikis; also installed as a global CLI |

`pi-continue` requires native compaction and is excluded while ACP owns compression; keep its `extensions: []` filter. GSD and Bigpowers are not part of this setup. Superpowers, Ralph loops, Pi Til Done and a standalone background-tasks package are **not installed** in this snapshot. Native Subagents completion notifications handle child waits. Ponytail's git tag is pinned; update it intentionally rather than tracking the repository's moving default branch. Pi 1.0 removed `@earendil-works/pi-agent-core/node`; Subagents 0.75.0 makes that child-runner alias optional. Older Subagents (including 0.67.0) fails before launching background reviews on Pi 1.0. The three updated Web Access/RPIV packages and Subagents declare the host's `typebox` as a peer dependency.

## Models and agents

| Role | Provider/model | Thinking | Main responsibility |
| --- | --- | --- | --- |
| Parent | `openai-codex/gpt-6.1-sol` | medium | Coordination and implementation |
| scout | `openai-codex/gpt-6-luna` | low | Exploration (explorer equivalent) |
| researcher | `openai-codex/gpt-6-luna` | medium | Web/docs (librarian equivalent) |
| worker | `openai-codex/gpt-6-luna` | high | Bounded implementation/fixes |
| evidence-auditor | `openai-codex/gpt-6.1-sol` | medium | Source/evidence checks |
| reviewer | `openai-codex/gpt-6.1-sol` | high | Independent code review |
| oracle | `openai-codex/gpt-6.1-sol` | high | Difficult decisions |
| delegate | `openai-codex/gpt-6.1-sol` | medium | General bounded work |
| designer | `antigravity/gemini-3.8-flash` | high | UI implementation and browser verification |
| observer | `antigravity/gemini-3.8-flash` | high | Image/screenshot inspection |

GPT-6 Astra is intentionally excluded from the standing roster because it is reserved for explicit hard-task escalation. These are the configured identifiers; verify availability in the target account's model catalog before claiming the setup works. Authentication and account entitlement are not transferable configuration.

Keep the seven stock role definitions from the package and override their settings. Only Designer and Observer are custom Markdown agents. Stock provider/CLI-specific auxiliary agents may also be listed; they are not replacements for this roster and may require separately installed/authenticated CLIs.

Explicit child extension allowlists are important: parent extensions are not assumed to be inherited. Code roles get MCP + ACP, research roles Web Access + ACP, and the custom Gemini roles explicitly load the Antigravity provider. Goal is a parent capability and is not added to children. `defaultExtensions: []` avoids incidental extension inheritance. Stock roles disable nested delegation; custom prompts also forbid it.

Subagents 0.76.1's stock Reviewer requires `watchdog_diff`. Its explicit tool allowlist includes that native bounded diff tool; omitting it prevents a real review. SDK wrapper hosts outside Pi's npm package may need the supported `PI_SUBAGENTS_PI_CODING_AGENT_PACKAGE_ROOT` environment override pointing to the actual Pi package root. Normal `pi` launches discover their host automatically.

Scout/reviewer/oracle have `output: false` to avoid requesting output-file writes without a write tool, and `completionGuard: false`. Worker/delegate keep completion guards and inherit skills. These are workflow restrictions, not an OS sandbox: roles with `bash` can still execute write-capable commands.

## Install on another workstation

### 1. Preflight and backup

Read this whole guide before changing an existing installation. Finish or pause live work before reloading. Check `pi --version`, `node --version`, `command -v pi`, and `pi list`. Identify any `PI_CODING_AGENT_DIR` override or project-local `.pi/settings.json`; the scripts below target the **default home layout only**. Adapt every destination and package path together if using a custom agent directory. Do not assume all extensions honor that environment variable for their own config paths.

Back up existing configuration before installing packages (the configuration helper also backs up files before it edits them):

```bash
python3 - <<'BACKUP'
from pathlib import Path
from datetime import datetime
import shutil
home = Path.home()
backup = home / '.pi' / ('before-pi-setup-' + datetime.now().strftime('%Y%m%d-%H%M%S'))
for relative in ['.pi/agent/settings.json', '.pi/agent/AGENTS.md', '.pi/agent/agents', '.pi/agent/extensions/subagent/config.json', '.pi/agent/mcp.json', '.pi/agent/mcp-adapter.json', '.pi/agent/pi-goal-x-settings.json', '.pi/acp.json', '.pi-lens/config.json', '.config/rpiv-todo/config.json']:
    source = home / relative
    if not source.exists():
        continue
    target = backup / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, target)
    else:
        shutil.copy2(source, target)
print(backup)
BACKUP
```

Do not export auth stores, sessions, memory contents, MCP caches, trust decisions or project secrets. New installations authenticate independently. The helper scripts never read these stores.

### 2. Install runtime and external CLI

With Node 24.21.0 selected using your normal Node installation/version manager:

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent@1.0.4
npm install -g @colbymchenry/codegraph@1.6.2
npm install -g openwiki@0.7.1
pi --version
codegraph --version
```

Both `codegraph` and `npx` must be on the PATH inherited by Pi and its children. Installing CodeGraph does not index every repository. Index only a repository the user wants indexed using `codegraph init /path/to/repo`; use `codegraph sync /path/to/repo` after changes when needed. In an already indexed repo (`.codegraph/` present), use `codegraph explore`/MCP before broad text searches to locate code. Do not auto-index unrelated repositories.

### 3. Install packages, then apply configuration

From this repository:

```bash
python3 scripts/install-packages.py          # Preview exact pi install commands
python3 scripts/install-packages.py --apply  # Install all captured versions
python3 scripts/configure.py                # Preview config destinations
python3 scripts/configure.py --apply        # Apply paths, filters and role overrides
```

Do not launch an interactive Pi task between installing packages and applying configuration: the package filters must be in place first. If installation fails partway, resolve that failure, rerun installation, then apply configuration. The installation script uses the official `pi install` command from your home directory and stops at the first failure. For the personal profile, it then applies the MCP dependency overrides and runs `npm install --ignore-scripts` in `~/.pi/agent/npm`. It backs up `package.json` and `package-lock.json` under `~/.pi/agent/backups/pi-setup-npm-*`. It does not upgrade the runtime, configure external CLI tools, authenticate, or run project tasks.

The configuration script expands `__PI_AGENT_DIR__` into the target absolute path, merges JSON mappings, replaces managed arrays/settings, replaces managed package versions by package identity (including git tags), retires Bigpowers and the previous `@narumitw/pi-goal` package, and retains unrelated packages. Adapter 5 uses `~/.pi/agent/mcp-adapter.json`, not the old adapter's `mcp.json`; the helper merges legacy adapter settings and servers into the new file when it does not exist. It does not delete the legacy file: archive a legacy adapter-only `mcp.json` after backing it up. Leave a genuine Pi built-in MCP file in place if you use `pi mcp` commands; the adapter can import its server definitions. The former `pi-goal.json` is not used by Goal X; the helper does not delete it or migrate old goal state. Back up or archive old goals separately before uninstalling if you need them. It backs up overwritten files with a manifest under `~/.pi/agent/backups/pi-setup-*`. Existing global AGENTS text is retained outside a managed section; existing custom Designer/Observer definitions are backed up and replaced. Inspect conflicting retained instructions, role overrides and unrelated extensions; preserving them does not establish compatibility. Existing extra keys inside managed role objects remain because JSON merging is recursive. The personal helper also installs `~/.pi/agent/pi-setup-env.sh` and adds one managed source block to `~/.bashrc`, with a backup. Corporate shell settings are not changed. Start a new Bash shell, or source that file, before launching Pi so memory-search settings take effect.

For a preview/fixture targeting another home directory, use `--home /path/to/home`. This only changes configuration destinations; the install script uses the actual user environment. The helper does not make a multi-file atomic transaction; its backups support recovery if a write fails.

For manual setup or when handing **only this Markdown file** to another agent: run `pi install` once for every version in the package table, then create every file in the configuration appendix. Replace `__PI_AGENT_DIR__` with the actual absolute agent directory, preserve unrelated settings, and keep the two `extensions: []` filters. The appendix contains all managed configuration; the scripts are conveniences.

### 4. Authenticate and verify models

Start Pi after applying configuration. Use `/login` and select the OpenAI Codex provider for the parent/stock roles. Use `/login antigravity` for Designer/Observer, complete the browser flow, then `/antigravity.doctor`. Check the configured models in `/model` before launching children.

Antigravity authenticates directly with Google through the provider extension's OAuth flow; it does not require Gemini CLI or an external Antigravity CLI. It keeps credentials in Pi's auth store and handles refresh. A suitable Google account and provider access are still required. See the [provider authentication documentation](https://github.com/Rahularya01/pi-antigravity#authentication-and-credential-safety). Never copy another machine's `auth.json` into this repository.

If a configured model is absent, report the exact missing provider/model and resolve account/catalog availability. Do not silently change Gemini Flash, GPT-6.1 Sol, GPT-6 Luna or GPT-6 Astra to something else.

### 5. Browser and research tools

Playwright is configured as a lazy local MCP server using `npx -y @playwright/mcp@latest`. First use downloads the server and may need browser/system dependencies. Try navigating to `about:blank` and closing the browser through MCP. If the server reports a missing browser, use its browser-install tool when available or follow the matching [Playwright MCP installation instructions](https://github.com/microsoft/playwright-mcp). The browser version must match the MCP runtime; do not assume a random globally installed Playwright browser is sufficient.

`approveTools: false` removes adapter tool approvals, `directTools: false` keeps discovery behind the `mcp` gateway, and `hostConfigDiscovery: off` prevents accidental import of another agent's MCP configuration. Pi 1.0's built-in MCP also registers `/mcp`; the template explicitly disables it with `"extensions": ["-builtin:mcp"]` so only the configured adapter owns that command. Do not enable both without choosing which server configuration to use. Lazy startup avoids paying server startup cost for tasks that never use them.

Web Access exposes `web_search`, `fetch_content`, `get_search_content`, and `source_check`; available search backends can have different account/API requirements. Public page extraction and Codex-backed search were tested on the configured account; no API secrets are included here. Web Access 0.37 starts with `web_enable`: invoke it to expose the research tools when they are not yet listed. Subagents similarly exposes `subagents_enable` before its `subagent` tool. These are lazy-tool activation helpers, not approval prompts.

### 6. Optional per-project and memory features

Ponytail defaults to `full`; `/ponytail lite` lets the agent suggest the simpler alternative without enforcing it, while `/ponytail off` disables its guidance for the session. Its extension adds `/ponytail-review`, `/ponytail-audit`, `/ponytail-debt`, `/ponytail-gain` and `/ponytail-help`. Parent extensions are not assumed to be inherited by subagents, so do not assume the Ponytail rules are injected into every child. Existing project skills, design guidance, AGENTS.md and specifications remain authoritative. This repo does not bundle the art marketplace's product documents or local Impeccable/Supabase skills.

Pi Memory's normal file tools need no extra backend. This personal workstation also has **qmd 2.8.3** for keyword and semantic memory search. Install it with `npm install -g @tobilu/qmd@2.8.3`, then run `qmd pull` to download its local models. Memory creates the `pi-memory` collection on session startup; use `qmd embed` after there is content to index. Follow [Pi Memory's qmd setup](https://github.com/jayzeng/pi-memory#optional-enable-search-with-qmd) and validate using `memory_status`.

Models consume several GB and need adequate CPU/RAM. The personal CPU baseline sets `QMD_FORCE_CPU=1` to avoid CUDA compilation probes and `PI_MEMORY_QMD_SEARCH_TIMEOUT_MS=300000`. A warmed semantic search took about 145 seconds on this workstation, so the default 60-second limit was insufficient. Both defaults preserve explicit environment overrides. Use GPU acceleration only after validating it. Keep this backend optional on resource-constrained machines. Do not migrate private memories by default.

OpenWiki is installed twice: `pi install npm:openwiki@0.7.1` loads its Pi extension, and `npm install -g openwiki@0.7.1` provides the CLI. The package installer covers the first; the runtime commands above cover the second. Restart Pi and verify `openwiki_begin`, `openwiki_submit_plan`, `openwiki_next_page`, `openwiki_inspect_page_claims`, `openwiki_submit_page`, and `openwiki_finish` are registered. The Pi host uses the existing model session and lazily starts a local OpenWiki MCP bridge. No second OpenWiki MCP entry or `openwiki integrations install pi` is needed. For a selected repository, load its `openwiki` skill and follow the durable planning/page workflow. Installation does not generate a wiki automatically. See the [OpenWiki instructions](https://github.com/langchain-ai/openwiki#readme).

BTW uses `/btw <question>` for a temporary side conversation. No custom `pi-btw.json` was present; it uses defaults, including the current model unless changed through its UI. Side-thread retention and full Memory behavior have not been exhaustively verified with this stack.

## Using autonomous work

Start a guided goal and confirm the draft before it begins:

```text
/goal Implement the agreed feature, fix verification failures, and complete all acceptance criteria in SPEC.md.
```

For an already agreed objective without drafting, use `/goal-direct <objective>`. Normal chat and an existing Todo list do not activate Goal mode. Use `/goal-status`, `/goal-pause`, `/goal-resume`, and `/goal-clear` for lifecycle management. `/goal` without draft confirmation is not an active goal; verify status. The old `@narumitw/pi-goal` commands and `goal_complete`/`goal_wait` tools do not apply to Pi Goal X.

`pi-goal-x-settings.json` caps **extension-started autonomous runs at 100**. This is not the old extension's 100 model responses: tool loops and external turns are outside this allowance. The old three-no-progress-run guard has no equivalent here. Goal X can also stop for provider failures, explicit cancellation, real blockers and token budgets. Its independent completion auditor is optional, and even approval is not a substitute for running checks. See the [Pi Goal X documentation](https://github.com/tmonk/pi-goal-x).

Expected behavior:

1. Derive requirements, maintain Goal X tasks/evidence and synchronize any separate RPIV todos, then implement and verify.
2. Treat failing tests/review findings as unfinished work; diagnose, repair and retest without needing another user prompt.
3. Preserve substantive requirements; never delete tasks, weaken tests or remove functionality just to claim success.
4. Use bounded subagents; inspect partial changes after timeout, confirm the previous writer stopped, then recover with a revised approach.
5. Continue independent work while children run; rely on native child-completion notifications, not polling or the removed `goal_wait` tool.
6. On child failure or deadline, inspect status and partial work once, then recover or wait for demonstrably active work. Do not start a competing writer.
7. Use `update_goal` to claim completion only with evidence for the full objective and required verification. Honor independent auditor feedback, explicit cancellation and real external dependencies.

`update_goal` wait declarations require opting into `strictExecutionContract`; the default goal continuation requires no explicit ready/wait call. Inspect `/goal-status` and child status if work appears stalled.

Top-level Subagents runs are forced async for this MCP/provider configuration. `parallel.concurrency: 2`, `globalConcurrencyLimit: 2` and two active async runs are different limits; they are not a proven machine-wide maximum of two OS processes. Default worker timeout is 30 minutes, but a particular workflow may choose a shorter deadline.

Do not enable Pi Continue alongside ACP. Do not add another auto-continuation engine as a presumed fix. Ralph was researched but not installed: it can supply stronger command-based acceptance gates, but the candidate's fresh children disable ambient extension discovery, so this stack would need deliberate integration. Neither Goal X nor Todo guarantees “never stop until everything is complete”; explicit checks and honest blocker reporting remain necessary.

## Acceptance checklist for the setup agent

Use a temporary fixture project for write/tool tests, not production data. Do not start the user's actual implementation objective as a setup test.

- `pi --version` is 1.0.4, `pi list` contains the captured packages, and every managed JSON file parses. Compare versions with `inventory.json`; run `npm audit` in `~/.pi/agent/npm` and report findings. This snapshot retains the five OpenWiki-related high-severity findings described above.
- Restart Pi and confirm no extension-loading errors. A Python/configuration check alone is not runtime validation.
- Inspect Subagents through its `subagent` tool (`action: "list", capabilities: true`); confirm all seven stock mappings plus Designer/Observer, thinking levels, tools and resolved extension paths. Use its doctor capability to diagnose launch issues when exposed by the installed version.
- Parent can access Todo, structured questions, `mcp`, web tools (after `web_enable`), ACP, `subagent` (after `subagents_enable`), Memory, Goal and `/ponytail`. `acp_delegate` must not be active; GSD and Bigpowers must not load. `/btw` should register.
- Discover MCP tools; CodeGraph responds for an intentionally indexed fixture, and Playwright opens/closes `about:blank`.
- Fetch a public documentation page and run one small search. Report authentication/backend failures separately.
- Create, update and complete a disposable Todo in a throwaway session.
- Launch one bounded scout to read a harmless fixture and return a known marker. Verify native async completion and exit status, not just “launched.” Inspect reviewer capabilities without paying for a full review. Test Designer/Observer only once provider login and model availability are established.
- In a disposable conversation, test ACP compress/decompress and confirm retrieval of the original text. Do not compress an unrelated user's live work for testing.
- For Goal X, use a disposable fixture and `/goal-direct`: initially fail a check, repair it, rerun it, record task evidence, and request audited completion. Exercise `/goal-pause` and `/goal-resume` in a separate bounded fixture; only test scheduled waits if you intentionally enable `strictExecutionContract`. Do not claim long-running compatibility based only on tool registration.
- Check `npm list -g openwiki --depth=0` (the CLI does not implement `--version`), six native Pi wiki tools, and `openwiki_begin` reaching planning in an explicitly selected disposable Git fixture. Do not generate production wikis as an installation test.
- Check `memory_status` and keyword/semantic/deep search against a disposable memory collection after downloading models. Keep private memories out of test artifacts.
- Run `python3 -m unittest discover -s tests -v` for portable-template/helper checks.
- Report changed files, installed/observed versions, exact checks performed, failures, and any account-dependent work still required.

On 2026-10-07, fresh SDK sessions passed startup, all nine role mappings, Todo create/update/complete, CodeGraph fixture lookup, Playwright `about:blank` open/close, public fetch/search, synthetic ACP compression and original-text restoration, and native async scout completion. A Gemini Observer read a disposable red-square PNG and completed successfully. A bounded Goal X fixture first failed an unchanged check, repaired its input, passed the same check, recorded task evidence and received independent audit approval; pause/resume was exercised in that fixture. These are bounded live checks, not proof of unlimited autonomous operation, new-account entitlement, or every UI command. Full BTW retention and Designer UI implementation were not tested. Disposable Memory keyword, semantic and deep searches returned the known marker, with the CPU timeout raised to 300 seconds. All six OpenWiki tools loaded without extension errors; its native bridge reached planning in a disposable Git fixture, and the global CLI integration-list command passed. Full wiki generation was not tested.

## Troubleshooting

| Symptom | Check/action |
| --- | --- |
| Plain “Continuing” reply, then silence | Inspect Goal status and active child; a task prompt is not `/goal` |
| Goal inactive/blocked after an error | Read the error; fix recoverable cause and explicitly resume; do not override user cancellation |
| Goal paused at 100 autonomous runs | Inspect `/goal-status`, review progress, and deliberately use `/goal-resume` to renew the allowance |
| Parent waiting indefinitely | Inspect child status and native completion notifications; recover the actual failed run |
| Test failures reported as final | Keep failed checks on Todo and resume the full objective; instructions are not a hard acceptance gate |
| Missing MCP tools in children | Verify absolute paths, explicit extension lists, tools and forced async mode |
| Background children fail on `@earendil-works/pi-agent-core/node` | Pi 1.0 removed this export; use Subagents 0.75.0 or newer, then verify with a fresh child launch |
| Child cannot write its requested output file | Check role output/tool settings; do not enable write everywhere by default |
| Gemini missing/auth failure | `/login antigravity`, `/antigravity.doctor`, inspect exact model catalog |
| CodeGraph spawn fails | Check inherited PATH and external CLI installation |
| Playwright browser missing | Install the browser compatible with the actual MCP server version |
| Memory search unavailable | Check qmd PATH, model downloads, `qmd embed` and `memory_status`; qmd remains optional |
| Duplicate prompts or competing loops | Disable extra continuation/delegation packages; retain one owner per responsibility |
| Unexpected model/agent settings | Inspect project-local settings, custom agent files and retained override keys |
| Changes not picked up | `/reload` or restart after work finishes; already-running children keep launch configuration |

## Rollback and updates

The pre-install backup is the clean rollback point because `pi install` itself changes package settings. The configuration helper's backup manifest lists each destination and whether it previously existed: restore saved files to their original relative home paths, and remove only newly created files listed with `existed: false`. Preserve later intentional edits and credentials. Restart Pi after restoring settings. Installed package files may remain on disk but become inactive when removed from package settings. Do not delete session/memory/auth directories.

For updates, back up first, upgrade intentionally, check installed versions against settings (particularly ACP), reapply activation filters if needed, and rerun the acceptance checklist. Recheck absolute extension entrypoints after package upgrades. No package-source patches are part of this reproduction; the customized behavior is supplied by settings, custom agents and global instructions.

## Exact configuration appendix

Every block below maps to its stated destination. `__PI_AGENT_DIR__` is a template token, **not an environment variable Pi expands**: replace it with the absolute target `~/.pi/agent` path before saving. These blocks match the committed templates in `config/`. Merge with an existing setup as described above instead of overwriting unrelated configuration blindly.

### `~/.pi/agent/AGENTS.md`

```markdown
# Working style

Keep replies concise: outcome, relevant verification, and genuine blockers. Follow the target repository's instructions. Carry authorized implementation through verification; a completed subtask is not a reason to stop. Use todo for substantive multi-step work, update it after progress, and never delete unfinished tasks merely to claim completion. Ask user questions only for material missing decisions, never for repeated approval of authorized work.

# Delegation

Use pi-subagents' built-in roles and prompts: scout for exploration, researcher for web/docs, evidence-auditor for source checks, worker for implementation, reviewer for independent review, oracle for difficult decisions, delegate for general bounded work. Designer owns UI implementation; observer inspects images. Use the parent's GPT-6.1 Sol model at medium thinking for coordination; reserve GPT-6 Astra for explicit hard-task escalation. Delegate only useful bounded work, normally at most two children concurrently. Preserve the original objective when reconciling results. Do independent work while children run; consume their native completion notifications instead of repeatedly polling. Use bg_wait only when appropriate. Children must follow project instructions and must not recursively delegate.

# Tools

MCP servers are lazily available through mcp: CodeGraph for indexed repositories and Playwright for browsers. Search/discover relevant MCP tools before calling them. Use web_search and fetch_content for external research. Lens diagnostics are available on demand; load relevant Lens tools when needed, and run project-required checks before completion. Do not impose a fixed multi-agent ceremony on simple tasks.

# Additional packages

Ponytail encourages the smallest correct implementation: reuse existing code and native facilities before introducing new abstractions. Preserve requested scope, security, accessibility and project-required verification; `/ponytail lite|full|ultra|off` controls its intensity.

Billion Context Pi owns context compression; use compress/decompress/search_context/acp_status for long sessions. Its delegation feature is disabled: use pi-subagents for delegation. Preserve task status, decisions and verification evidence when compressing.

# Goal continuation (pi-goal-x)

For sustained autonomous work, the user starts `/goal <idea>` and confirms its proposed plan, or explicitly starts `/goal-direct <objective>` without drafting. Ordinary prompts and a Todo list do not activate Goal mode. Check `/goal-status` or `get_goal` before acting on a goal; respect its current ID and lifecycle. Track the original objective, requirements, task evidence, and verification; keep any separate Pi Todo list synchronized. Report completion through `update_goal` only when all requirements are verified; completion may be independently audited. Never substitute a milestone or a "Continuing" message for completion evidence.

Continue useful independent work while subagents run. If only a native child result remains, rely on its completion notification and return control; do not busy-poll or invent a `goal_wait` call. `update_goal` waits require the optional `strictExecutionContract` setting; do not enable it just to wait for a child. Waiting for a child is not a blocked goal. Respect `/goal-pause`, autonomous-run/token limits, real blockers and explicit cancellation; never restart stopped goals without authorization.

# Failure recovery during active goals

Failing tests, lint errors, review findings, and incomplete implementation are remaining work: diagnose, fix, rerun the relevant checks, then advance to the next open task. Do not weaken tests, remove requirements or roll back required functionality merely to obtain green output. Keep verification failures open until resolved with evidence. After a worker timeout or recoverable failure, inspect its partial diff and diagnostics, confirm the previous writer has stopped, then narrow the task or change the approach before retrying. Do not launch competing writers. Honor explicit user cancellation; never reinterpret it as permission to restart. If Goal mode is inactive because a command was misspelled or a draft was not confirmed, state that explicitly rather than promising autonomous continuation.
```

### `~/.pi/agent/agents/designer.md`

```markdown
---
name: designer
description: Design and implement user-facing interfaces and verify them in a browser
model: antigravity/gemini-3.8-flash
thinking: high
tools: read, grep, find, ls, bash, write, edit, mcp, compress, decompress, search_context, acp_status
extensions: __PI_AGENT_DIR__/npm/node_modules/pi-mcp-adapter/index.ts, __PI_AGENT_DIR__/npm/node_modules/billion-context-pi/dist/index.js, __PI_AGENT_DIR__/npm/node_modules/pi-antigravity/src/index.ts
inheritProjectContext: true
inheritSkills: true
---
Design and implement the assigned UI using the project design guidance and real content. Check mobile layout, accessibility and failure states. Use Playwright through mcp for browser verification. Return changed files, verification and remaining issues concisely. Do not delegate.
```

### `~/.pi/agent/agents/observer.md`

```markdown
---
name: observer
description: Inspect screenshots and images and report concrete visual findings
model: antigravity/gemini-3.8-flash
thinking: high
tools: read, compress, decompress, search_context, acp_status
extensions: __PI_AGENT_DIR__/npm/node_modules/billion-context-pi/dist/index.js, __PI_AGENT_DIR__/npm/node_modules/pi-antigravity/src/index.ts
inheritProjectContext: true
completionGuard: false
---
Inspect the supplied images and report concrete visual findings relevant to the assignment. Do not edit files or delegate. State what cannot be verified from the images. Keep the result concise.
```

### `~/.pi/agent/extensions/subagent/config.json`

```json
{
  "forceTopLevelAsync": true,
  "parallel": {
    "maxTasks": 8,
    "concurrency": 2
  },
  "timeoutMs": 1800000,
  "globalConcurrencyLimit": 2,
  "maxActiveAsyncRunsPerSession": 2
}
```

### `~/.pi/agent/mcp-adapter.json`

```json
{
  "settings": {
    "approveTools": false,
    "directTools": false,
    "scriptMode": true,
    "hostConfigDiscovery": "off",
    "mcpFooterStatus": "compact",
    "notifyOnStartupConnect": false
  },
  "mcpServers": {
    "codegraph": {
      "command": "codegraph",
      "args": [
        "serve",
        "--mcp"
      ],
      "lifecycle": "lazy"
    },
    "playwright": {
      "command": "npx",
      "args": [
        "-y",
        "@playwright/mcp@latest"
      ],
      "lifecycle": "lazy"
    }
  }
}
```

### `~/.pi/agent/pi-goal-x-settings.json`

```json
{
  "maxAutonomousRuns": 100
}
```

### `~/.pi/agent/settings.json`

```json
{
  "theme": "light",
  "defaultProvider": "openai-codex",
  "defaultModel": "gpt-6.1-sol",
  "compaction": {
    "enabled": true
  },
  "tuiMode": "regular",
  "enableSkillCommands": true,
  "extensions": ["-builtin:mcp"],
  "packages": [
    "npm:pi-mcp-adapter@5.1.0",
    "npm:pi-web-access@0.37.0",
    "npm:pi-subagents@0.76.1",
    "npm:@juicesharp/rpiv-ask-user-question@2.12.0",
    "npm:@juicesharp/rpiv-todo@2.12.0",
    "npm:pi-lens@4.3.0",
    "npm:billion-context-pi@0.1.83",
    "npm:pi-antigravity@0.9.0",
    "npm:pi-memory@0.4.2",
    "npm:@narumitw/pi-btw@0.61.1",
    {
      "source": "npm:pi-continue@0.9.3",
      "extensions": []
    },
    "npm:pi-goal-x@0.32.3",
    "npm:openwiki@0.7.1",
    "git:github.com/DietrichGebert/ponytail@v4.13.0"
  ],
  "defaultThinkingLevel": "medium",
  "subagents": {
    "agentOverrides": {
      "scout": {
        "model": "openai-codex/gpt-6-luna",
        "thinking": "low",
        "inheritProjectContext": true,
        "allowNestedSubagents": false,
        "extensions": [
          "__PI_AGENT_DIR__/npm/node_modules/pi-mcp-adapter/index.ts",
          "__PI_AGENT_DIR__/npm/node_modules/billion-context-pi/dist/index.js"
        ],
        "tools": [
          "read",
          "grep",
          "find",
          "ls",
          "bash",
          "mcp",
          "compress",
          "decompress",
          "search_context",
          "acp_status"
        ],
        "completionGuard": false,
        "output": false
      },
      "researcher": {
        "model": "openai-codex/gpt-6-luna",
        "thinking": "medium",
        "inheritProjectContext": true,
        "allowNestedSubagents": false,
        "extensions": [
          "__PI_AGENT_DIR__/npm/node_modules/pi-web-access/index.ts",
          "__PI_AGENT_DIR__/npm/node_modules/billion-context-pi/dist/index.js"
        ],
        "tools": [
          "read",
          "write",
          "web_search",
          "fetch_content",
          "get_search_content",
          "source_check",
          "compress",
          "decompress",
          "search_context",
          "acp_status"
        ]
      },
      "evidence-auditor": {
        "model": "openai-codex/gpt-6.1-sol",
        "thinking": "medium",
        "inheritProjectContext": true,
        "allowNestedSubagents": false,
        "extensions": [
          "__PI_AGENT_DIR__/npm/node_modules/pi-web-access/index.ts",
          "__PI_AGENT_DIR__/npm/node_modules/billion-context-pi/dist/index.js"
        ],
        "tools": [
          "read",
          "write",
          "web_search",
          "fetch_content",
          "get_search_content",
          "source_check",
          "compress",
          "decompress",
          "search_context",
          "acp_status"
        ]
      },
      "worker": {
        "model": "openai-codex/gpt-6-luna",
        "thinking": "high",
        "inheritProjectContext": true,
        "allowNestedSubagents": false,
        "extensions": [
          "__PI_AGENT_DIR__/npm/node_modules/pi-mcp-adapter/index.ts",
          "__PI_AGENT_DIR__/npm/node_modules/billion-context-pi/dist/index.js"
        ],
        "tools": [
          "read",
          "grep",
          "find",
          "ls",
          "bash",
          "mcp",
          "write",
          "edit",
          "compress",
          "decompress",
          "search_context",
          "acp_status"
        ],
        "completionGuard": true,
        "inheritSkills": true
      },
      "reviewer": {
        "model": "openai-codex/gpt-6.1-sol",
        "thinking": "high",
        "inheritProjectContext": true,
        "allowNestedSubagents": false,
        "extensions": [
          "__PI_AGENT_DIR__/npm/node_modules/pi-mcp-adapter/index.ts",
          "__PI_AGENT_DIR__/npm/node_modules/billion-context-pi/dist/index.js"
        ],
        "tools": [
          "read",
          "grep",
          "find",
          "ls",
          "bash",
          "mcp",
          "compress",
          "decompress",
          "search_context",
          "acp_status",
          "watchdog_diff"
        ],
        "completionGuard": false,
        "output": false
      },
      "oracle": {
        "model": "openai-codex/gpt-6.1-sol",
        "thinking": "high",
        "inheritProjectContext": true,
        "allowNestedSubagents": false,
        "extensions": [
          "__PI_AGENT_DIR__/npm/node_modules/pi-mcp-adapter/index.ts",
          "__PI_AGENT_DIR__/npm/node_modules/billion-context-pi/dist/index.js"
        ],
        "tools": [
          "read",
          "grep",
          "find",
          "ls",
          "bash",
          "mcp",
          "compress",
          "decompress",
          "search_context",
          "acp_status"
        ],
        "completionGuard": false,
        "output": false
      },
      "delegate": {
        "model": "openai-codex/gpt-6.1-sol",
        "thinking": "medium",
        "inheritProjectContext": true,
        "allowNestedSubagents": false,
        "extensions": [
          "__PI_AGENT_DIR__/npm/node_modules/pi-mcp-adapter/index.ts",
          "__PI_AGENT_DIR__/npm/node_modules/billion-context-pi/dist/index.js"
        ],
        "tools": [
          "read",
          "grep",
          "find",
          "ls",
          "bash",
          "mcp",
          "write",
          "edit",
          "compress",
          "decompress",
          "search_context",
          "acp_status"
        ],
        "completionGuard": true,
        "inheritSkills": true
      }
    },
    "defaultExtensions": []
  }
}
```

### npm dependency overrides (`config/npm-overrides.json`)

The personal install helper merges these keys into the `overrides` field of `~/.pi/agent/npm/package.json`, then runs `npm install --ignore-scripts`. For manual installation, use the same npm overrides after installing the packages:

```json
{
  "@modelcontextprotocol/client": "2.3.1",
  "@modelcontextprotocol/core": "2.3.1",
  "@modelcontextprotocol/sdk": "1.32.1"
}
```

```bash
cd ~/.pi/agent/npm
npm pkg set overrides.@modelcontextprotocol/client=2.3.1 overrides.@modelcontextprotocol/core=2.3.1 overrides.@modelcontextprotocol/sdk=1.32.1
npm install --ignore-scripts
npm audit
```

### `~/.pi/acp.json`

```json
{
  "delegate": false
}
```

### `~/.pi-lens/config.json`

```json
{
  "startup": {
    "mode": "minimal",
    "scans": {
      "enabled": false
    }
  },
  "tools": {
    "lazy": true
  },
  "format": {
    "enabled": false
  },
  "autofix": {
    "enabled": false
  },
  "tests": {
    "enabled": false
  },
  "contextInjection": {
    "enabled": false
  },
  "guard": {
    "enabled": false
  },
  "widget": {
    "visible": false
  }
}
```

### `~/.config/rpiv-todo/config.json`

```json
{
  "maxWidgetLines": 6,
  "guidance": "Track substantive multi-step work and verification. Update after progress. Continue authorized work across milestones without asking the user to say continue. Mark tasks complete only with evidence. Report genuine blockers clearly; never delete tasks just to claim completion. Do not create todo lists for ordinary questions or trivial edits. Failing tests and review findings remain open work: diagnose, repair, verify, and continue. Do not mark complete, abandon requirements, or weaken checks to obtain green output. A recoverable worker timeout requires inspection and a revised recovery attempt, not a final handoff. Respect explicit user cancellation and genuine external blockers."
}
```

### `~/.pi/agent/pi-setup-env.sh` and personal Bash startup

```bash
# Personal Linux CPU baseline. Source this before starting Pi.
# Set either variable before sourcing to retain a deliberate override.
export QMD_FORCE_CPU="${QMD_FORCE_CPU:-1}"
export PI_MEMORY_QMD_SEARCH_TIMEOUT_MS="${PI_MEMORY_QMD_SEARCH_TIMEOUT_MS:-300000}"
```

The helper adds a backed-up, idempotent source block to `~/.bashrc`. For manual installation, add:

```bash
[ ! -f "$HOME/.pi/agent/pi-setup-env.sh" ] || . "$HOME/.pi/agent/pi-setup-env.sh"
```

Non-Bash shells, desktop launchers, services and direct SDK callers must source this file or pass the two environment variables explicitly. Existing Pi processes do not receive environment changes.

## Upstream references

These links document the package behavior; the local snapshot and pinned templates define this setup. Recheck upstream when upgrading.

- [Pi](https://pi.dev/)
- [MCP Adapter](https://github.com/nicobailon/pi-mcp-adapter)
- [Web Access](https://github.com/nicobailon/pi-web-access)
- [Subagents](https://github.com/nicobailon/pi-subagents)
- [RPIV Todo / Ask User Question](https://github.com/juicesharp/rpiv-mono)
- [Lens](https://github.com/apmantza/pi-lens)
- [Ponytail](https://github.com/DietrichGebert/ponytail)
- [Billion Context Pi](https://github.com/ranxianglei/billion-context-pi)
- [Antigravity](https://github.com/Rahularya01/pi-antigravity)
- [Memory](https://github.com/jayzeng/pi-memory)
- [Pi Goal X](https://github.com/tmonk/pi-goal-x) and [BTW](https://github.com/narumiruna/pi-extensions)
- [Pi Continue (inactive)](https://github.com/Tiziano-AI/pi-continue)
- [CodeGraph](https://github.com/colbymchenry/codegraph)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [OpenWiki](https://github.com/langchain-ai/openwiki)
- [qmd](https://github.com/tobi/qmd)

## Repository validation record

On 2026-10-07, the personal installation helper was executed on the source workstation with the latest pins and patched MCP overrides. Reapplying configuration preserved activation filters and role mappings. After the overrides, fresh MCP/browser/fetch/ACP and native async scout checks passed again. The MCP advisories were resolved; adding OpenWiki then produced the five unresolved high-severity findings documented above. OpenWiki's six tools and native planning bridge passed a disposable fixture check. Memory keyword/semantic/deep searches passed with the recorded CPU settings. A fresh native async Reviewer inspected the final diff and reported no actionable issues after its required diff tool was restored. The parent ran all eleven offline regression tests successfully; active LSP diagnostics found no issues across the seven changed Python/JSON/shell files. The tests cover fresh/repeated application, a home path containing spaces, unrelated-settings preservation, retired packages, credential-file exclusion, legacy adapter migration, personal npm backups/overrides, idempotent shell-environment setup, corporate isolation and Markdown/template/inventory agreement.

Run the offline regression tests before committing configuration changes:

```bash
python3 -m unittest discover -s tests -v
```

The corporate profile was not deployed or upgraded in this personal update. No credentials, memory files, session history or production project data were copied into this repository. Runtime tests used temporary fixtures and existing account authentication; they do not establish entitlement on a new account.
