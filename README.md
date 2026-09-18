# Portable Pi setup guide

This repository describes and reproduces the Pi setup captured on **2026-09-19**. It is a deployment specification for a human or a setup agent, with copyable configuration and optional helper scripts. It covers Pi, not the earlier OMP/OpenCode installations. The target is a personal Linux workstation using the default `~/.pi/agent` directory.

## Design and operating contract

Use a concise coordinating parent, retain the stock Pi Subagents role roster, and delegate bounded work when useful. Keep two children active in normal operation. Use cheaper models for routine implementation and exploration, Sol for review/advice, and Gemini Flash for UI/image tasks. Preserve the user's full objective through implementation and verification.

The package responsibilities are deliberately separate:

- **Pi Subagents** dispatches children; Billion Context's separate delegation is disabled.
- **RPIV Todo** is the task tracker. Memory's scratchpad is not the authoritative task list.
- **Billion Context Pi (ACP)** owns context compression. Native compaction remains enabled as a fallback if ACP is removed.
- **Pi Goal** drives explicit session objectives and continuation. It does not enforce test success or independently audit every completion claim.
- **MCP Adapter** supplies lazy CodeGraph/Playwright tools. Web Access supplies research tools.
- **Lens** supplies diagnostics on demand; startup scans, autoformat, autofix, automatic tests and its guard are disabled.
- **Bigpowers** supplies skills and prompts only. Its extension hooks are disabled.

This configuration avoids routine tool-approval prompts. It does not bypass provider authentication, operating-system permissions, explicit user cancellation, or real product decisions. Pi itself does not require an OpenCode-style `--dangerously-skip-permissions` flag. The [official Pi overview](https://pi.dev/) describes its extension-based approach to permissions and capabilities.

## Runtime and reproducibility

Captured runtime: Node.js **24.21.0**, Pi (`@earendil-works/pi-coding-agent`) **0.85.1**, CodeGraph (`@colbymchenry/codegraph`) **1.6.0**, Python 3 for the helper scripts. `git` is useful for project workflows; `gh` is needed only for GitHub work.

Use the versions below for the closest reproduction. This is a top-level package snapshot, **not a full dependency lock or a guarantee of future provider availability**. Transitive dependencies and Playwright's `@latest` MCP command can change. Record intentional upgrades and rerun validation.

Two source entries were floating (`pi-memory`, `@narumitw/pi-btw`); this guide pins their installed versions. ACP was declared as 0.1.70 in settings but the installed package reported **0.1.71**. The reproduction pins 0.1.71 to match the installed files; the cause of that drift was not established. `inventory.json` preserves configured versus observed versions. The original workstation settings were not changed during documentation.

## Packages

| Package | Version | Activation and purpose |
| --- | --- | --- |
| `pi-mcp-adapter` | 2.33.0 | Active; lazy MCP discovery and calls |
| `pi-web-access` | 0.29.0 | Active; search, fetch and source checks |
| `pi-subagents` | 0.67.0 | Active; stock role prompts, async children and supervision |
| `@juicesharp/rpiv-ask-user-question` | 2.10.1 | Active; structured questions for material decisions |
| `@juicesharp/rpiv-todo` | 2.10.1 | Active; one substantive task list |
| `pi-lens` | 4.1.6 | Active; diagnostics loaded on demand |
| `bigpowers` | 2.88.6 | Skills/prompts only; `extensions: []` |
| `billion-context-pi` | 0.1.71 | Active; context compression and retrieval |
| `pi-antigravity` | 0.7.3 | Active; Google Antigravity provider |
| `pi-memory` | 0.4.2 | Active; durable memory and scratchpad |
| `@narumitw/pi-btw` | 0.58.1 | Active; temporary side conversations |
| `pi-continue` | 0.9.3 | Installed but inactive; `extensions: []` |
| `@narumitw/pi-goal` | 0.54.5 | Active; explicit goal continuation |

`pi-continue` requires native compaction and is excluded while ACP owns compression. Bigpowers' hooks were excluded because their blocking workflow conflicted with the desired approval-free routine. Do not replace either filtered entry with a plain package string after installing. Superpowers, Ralph loops, Pi Til Done and a standalone background-tasks package are **not installed** in this snapshot. Native Subagents completion notifications handle child waits.

## Models and agents

| Role | Provider/model | Thinking | Main responsibility |
| --- | --- | --- | --- |
| Parent | `openai-codex/gpt-5.6-terra` | high | Coordination and implementation |
| scout | `openai-codex/gpt-5.6-luna` | low | Exploration (explorer equivalent) |
| researcher | `openai-codex/gpt-5.6-luna` | medium | Web/docs (librarian equivalent) |
| worker | `openai-codex/gpt-5.6-luna` | high | Bounded implementation/fixes |
| evidence-auditor | `openai-codex/gpt-5.6-sol` | high | Source/evidence checks |
| reviewer | `openai-codex/gpt-5.6-sol` | high | Independent code review |
| oracle | `openai-codex/gpt-5.6-sol` | high | Difficult decisions |
| delegate | `openai-codex/gpt-5.6-terra` | medium | General bounded work |
| designer | `antigravity/gemini-3.8-flash` | high | UI implementation and browser verification |
| observer | `antigravity/gemini-3.8-flash` | high | Image/screenshot inspection |

Reviewer was deliberately moved off Astra for cost. Do not silently restore Astra or substitute another model. These are the configured identifiers; verify availability in the target account's model catalog before claiming the setup works. Authentication and account entitlement are not transferable configuration.

Keep the seven stock role definitions from the package and override their settings. Only Designer and Observer are custom Markdown agents. Stock provider/CLI-specific auxiliary agents may also be listed; they are not replacements for this roster and may require separately installed/authenticated CLIs.

Explicit child extension allowlists are important: parent extensions are not assumed to be inherited. Code roles get MCP + ACP, research roles Web Access + ACP, and the custom Gemini roles explicitly load the Antigravity provider. Goal is a parent capability and is not added to children. `defaultExtensions: []` avoids incidental extension inheritance. Stock roles disable nested delegation; custom prompts also forbid it.

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
for relative in ['.pi/agent/settings.json', '.pi/agent/AGENTS.md', '.pi/agent/agents', '.pi/agent/extensions/subagent/config.json', '.pi/agent/mcp.json', '.pi/agent/pi-goal.json', '.pi/acp.json', '.pi-lens/config.json', '.config/rpiv-todo/config.json']:
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
npm install -g --ignore-scripts @earendil-works/pi-coding-agent@0.85.1
npm install -g @colbymchenry/codegraph@1.6.0
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

Do not launch an interactive Pi task between installing packages and applying configuration: the package filters must be in place first. If installation fails partway, resolve that failure, rerun installation, then apply configuration. The installation script uses the official `pi install` command from your home directory and stops at the first failure. It does not upgrade the runtime, configure external CLI tools, authenticate, or run project tasks.

The configuration script expands `__PI_AGENT_DIR__` into the target absolute path, merges JSON mappings, replaces managed arrays/settings, replaces managed package versions by package name, and retains unrelated packages. It backs up overwritten files with a manifest under `~/.pi/agent/backups/pi-setup-*`. Existing global AGENTS text is retained outside a managed section; existing custom Designer/Observer definitions are backed up and replaced. Inspect conflicting retained instructions, role overrides and unrelated extensions; preserving them does not establish compatibility. Existing extra keys inside managed role objects remain because JSON merging is recursive.

For a preview/fixture targeting another home directory, use `--home /path/to/home`. This only changes configuration destinations; the install script uses the actual user environment. The helper does not make a multi-file atomic transaction; its backups support recovery if a write fails.

For manual setup or when handing **only this Markdown file** to another agent: run `pi install` once for every version in the package table, then create every file in the configuration appendix. Replace `__PI_AGENT_DIR__` with the actual absolute agent directory, preserve unrelated settings, and keep the two `extensions: []` filters. The appendix contains all managed configuration; the scripts are conveniences.

### 4. Authenticate and verify models

Start Pi after applying configuration. Use `/login` and select the OpenAI Codex provider for the parent/stock roles. Use `/login antigravity` for Designer/Observer, complete the browser flow, then `/antigravity.doctor`. Check the configured models in `/model` before launching children.

Antigravity authenticates directly with Google through the provider extension's OAuth flow; it does not require Gemini CLI or an external Antigravity CLI. It keeps credentials in Pi's auth store and handles refresh. A suitable Google account and provider access are still required. See the [provider authentication documentation](https://github.com/Rahularya01/pi-antigravity#authentication-and-credential-safety). Never copy another machine's `auth.json` into this repository.

If a configured model is absent, report the exact missing provider/model and resolve account/catalog availability. Do not silently change Gemini Flash, Sol, Luna or Terra to something else.

### 5. Browser and research tools

Playwright is configured as a lazy local MCP server using `npx -y @playwright/mcp@latest`. First use downloads the server and may need browser/system dependencies. Try navigating to `about:blank` and closing the browser through MCP. If the server reports a missing browser, use its browser-install tool when available or follow the matching [Playwright MCP installation instructions](https://github.com/microsoft/playwright-mcp). The browser version must match the MCP runtime; do not assume a random globally installed Playwright browser is sufficient.

`approveTools: false` removes adapter tool approvals, `directTools: false` keeps discovery behind the `mcp` gateway, and `hostConfigDiscovery: off` prevents accidental import of another agent's MCP configuration. Lazy startup avoids paying server startup cost for tasks that never use them.

Web Access exposes `web_search`, `fetch_content`, `get_search_content`, and `source_check`; available search backends can have different account/API requirements. The original setup's keyless search and page extraction were tested; no API secrets are included here.

### 6. Optional per-project and memory features

Bigpowers skills/prompts are available without its hook extension. Apply relevant skills on demand instead of imposing its entire workflow on every task. Any project-specific Bigpowers initialization is a separate decision: regenerate its integration for the new project if needed, and never copy an absolute scripts symlink from another machine. Existing project skills, design guidance, AGENTS.md and specifications remain authoritative. This repo does not bundle the art marketplace's product documents or local Impeccable/Supabase skills.

Pi Memory's normal file tools need no extra backend. Its search feature requires qmd; qmd was **not found on the source PATH** during this capture. Installing Memory does not prove semantic search works. If desired, follow [Pi Memory's qmd setup](https://github.com/jayzeng/pi-memory#optional-enable-search-with-qmd) and validate using `memory_status`. Do not migrate private memories by default.

BTW uses `/btw <question>` for a temporary side conversation. No custom `pi-btw.json` was present; it uses defaults, including the current model unless changed through its UI. Side-thread retention and full Memory behavior have not been exhaustively verified with this stack.

## Using autonomous work

Start an explicit objective in Pi:

```text
/goal Implement the agreed feature, fix verification failures, and complete all acceptance criteria in SPEC.md. Keep the todo list current and verify the result.
```

Normal prompts do not activate Goal mode. An existing task list alone does not enable continuation. Prefer an objective that names the actual specification and scope rather than just “resume.” Use `/goal status`, `/goal pause`, `/goal resume`, and `/goal clear` to inspect/manage it. A misspelled slash command can reach the model as plain chat instead of controlling the extension; verify the Goal status.

The configuration allows **100 automatic model responses**, including responses inside tool loops, and **3 repeated no-progress runs**. These are finite safeguards, not a cost cap or a guarantee of completion. Goal can also stop for provider failures, explicit cancellation, real blockers and budget limits. `rpc.enabled: false` leaves extension-managed Goal starts disabled. See the [Goal documentation](https://github.com/narumiruna/pi-extensions/tree/main/packages/pi-goal).

Expected behavior:

1. Derive requirements, create/update RPIV todos, implement and verify.
2. Treat failing tests/review findings as unfinished work; diagnose, repair and retest without needing another user prompt.
3. Preserve substantive requirements; never delete tasks, weaken tests or remove functionality just to claim success.
4. Use bounded subagents; inspect partial changes after timeout, confirm the previous writer stopped, then recover with a revised approach.
5. Continue independent work while children run. When only a native completion remains, `goal_wait` includes the run ID and a fallback deadline: child time remaining plus 60 seconds, or 1,860,000 ms if unknown.
6. On a fallback wake, inspect once and recover stale work or wait for demonstrably active work. Do not busy-poll or start a competing writer.
7. Call `goal_complete` only with evidence for the original objective and all required verification. Honor explicit cancellation and real external dependencies.

The fallback-wait behavior is instruction-level policy, not an automatic patch that adds deadlines to every tool call. A parent that displays a final-looking status while its child runs may be waiting correctly. Inspect `/goal status` and the child status before assuming it has stopped.

Top-level Subagents runs are forced async for this MCP/provider configuration. `parallel.concurrency: 2`, `globalConcurrencyLimit: 2` and two active async runs are different limits; they are not a proven machine-wide maximum of two OS processes. Default worker timeout is 30 minutes, but a particular workflow may choose a shorter deadline.

Do not enable Pi Continue alongside ACP. Do not add another auto-continuation engine as a presumed fix. Ralph was researched but not installed: it can supply stronger command-based acceptance gates, but the candidate's fresh children disable ambient extension discovery, so this stack would need deliberate integration. Neither Goal nor Todo guarantees “never stop until everything is complete”; explicit checks and honest blocker reporting remain necessary.

## Acceptance checklist for the setup agent

Use a temporary fixture project for write/tool tests, not production data. Do not start the user's actual implementation objective as a setup test.

- `pi --version` is 0.85.1, `pi list` contains the captured packages, and every managed JSON file parses.
- Restart Pi and confirm no extension-loading errors. A Python/configuration check alone is not runtime validation.
- Inspect Subagents through its `subagent` tool (`action: "list", capabilities: true`); confirm all seven stock mappings plus Designer/Observer, thinking levels, tools and resolved extension paths. Use its doctor capability to diagnose launch issues when exposed by the installed version.
- Parent can access Todo, structured questions, `mcp`, web tools, ACP, `subagent`, Memory and Goal. `acp_delegate` must not be active; Bigpowers' disabled hook must not load. `/btw` should register.
- Discover MCP tools; CodeGraph responds for an intentionally indexed fixture, and Playwright opens/closes `about:blank`.
- Fetch a public documentation page and run one small search. Report authentication/backend failures separately.
- Create, update and complete a disposable Todo in a throwaway session.
- Launch one bounded scout to read a harmless fixture and return a known marker. Verify native async completion and exit status, not just “launched.” Inspect reviewer capabilities without paying for a full review. Test Designer/Observer only once provider login and model availability are established.
- In a disposable conversation, test ACP compress/decompress and confirm retrieval of the original text. Do not compress an unrelated user's live work for testing.
- For Goal, use a disposable test fixture: a check initially fails, the agent repairs it, reruns it, updates the todo and records completion. Exercise pause/resume and a bounded external wait. Record whether this is a simulated or live-provider test. Do not claim long-running compatibility based only on tool registration.
- Report changed files, installed/observed versions, exact checks performed, failures, and any account-dependent work still required.

Historical validation on the source workstation: zero extension-loader errors; native async scout runs returned the expected marker; MCP/browser/web/Todo and synthetic ACP checks passed. Upstream Goal runtime smoke tests passed against installed Pi for continuation, queued input, pause, limits, retries and native compaction. Later session evidence showed Goal automatically continued and woke around async child work. This is not exhaustive live validation of ACP + Goal + all providers, or proof that every long task completes. The 0.1.71 ACP drift was observed during this documentation pass, not separately retested end-to-end.

## Troubleshooting

| Symptom | Check/action |
| --- | --- |
| Plain “Continuing” reply, then silence | Inspect Goal status and active child; a task prompt is not `/goal` |
| Goal inactive/blocked after an error | Read the error; fix recoverable cause and explicitly resume; do not override user cancellation |
| Goal paused at 100 responses | Inspect progress using `/goal`; resume deliberately after review |
| Parent waiting indefinitely | Inspect child status and whether `goal_wait` had a fallback deadline; recover the actual failed run |
| Test failures reported as final | Keep failed checks on Todo and resume the full objective; instructions are not a hard acceptance gate |
| Missing MCP tools in children | Verify absolute paths, explicit extension lists, tools and forced async mode |
| Child cannot write its requested output file | Check role output/tool settings; do not enable write everywhere by default |
| Gemini missing/auth failure | `/login antigravity`, `/antigravity.doctor`, inspect exact model catalog |
| CodeGraph spawn fails | Check inherited PATH and external CLI installation |
| Playwright browser missing | Install the browser compatible with the actual MCP server version |
| Memory search unavailable | qmd is optional and absent in the captured baseline; check `memory_status` |
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

Use pi-subagents' built-in roles and prompts: scout for exploration, researcher for web/docs, evidence-auditor for source checks, worker for implementation, reviewer for independent review, oracle for difficult decisions, delegate for general bounded work. Designer owns UI implementation; observer inspects images. Use the parent's Terra model for coordination. Delegate only useful bounded work, normally at most two children concurrently. Preserve the original objective when reconciling results. Do independent work while children run; consume their native completion notifications instead of repeatedly polling. Use bg_wait only when appropriate. Children must follow project instructions and must not recursively delegate.

# Tools

MCP servers are lazily available through mcp: CodeGraph for indexed repositories and Playwright for browsers. Search/discover relevant MCP tools before calling them. Use web_search and fetch_content for external research. Lens diagnostics are available on demand; load relevant Lens tools when needed, and run project-required checks before completion. Do not impose a fixed multi-agent ceremony on simple tasks.

# Additional packages

Bigpowers skills and prompt templates are available on demand. Apply relevant skills to the actual task and preserve the repository's foundation decisions and Impeccable design workflow. Existing user authorization takes precedence over generic skill approval stages. Do not impose the whole Bigpowers lifecycle on every question.

Billion Context Pi owns context compression; use compress/decompress/search_context/acp_status for long sessions. Its delegation feature is disabled: use pi-subagents for delegation. Preserve task status, decisions and verification evidence when compressing.

# Goal continuation

For sustained autonomous work, the user starts `/goal <objective>`. Ordinary prompts do not activate Goal mode. While a goal is active, keep the existing todo list synchronized with its full scope and verification requirements. Call goal_complete only after the original objective and all required work are verified complete. Milestones and statements such as "Continuing" are not completion.

While subagents run, continue useful independent work. If only an external result remains, use goal_wait after arranging its native completion notification; state the wake source and next action. Waiting for a child is not a goal_blocked condition. Respect explicit pause, safety-limit and blocker states; do not restart stopped goals or bypass their limits.

# Failure recovery during active goals

Failing tests, lint errors, review findings, and incomplete implementation are remaining work: diagnose, fix, rerun the relevant checks, then advance to the next open todo. Do not weaken tests, remove requirements or roll back required functionality merely to obtain green output. Keep verification failures open in todo until resolved with evidence. After a worker timeout or recoverable failure, inspect its partial diff and diagnostics, confirm the previous writer has stopped, then narrow the task or change the approach before retrying. Do not launch competing writers. Honor explicit user cancellation; never reinterpret it as permission to restart.

When goal_wait is needed for a native subagent completion, include the run ID in the reason and set resume_after_ms to the known remaining worker deadline plus 60 seconds (use 1860000 if no deadline is known). This is a fallback for a missing notification, not a frequent polling loop. On a deadline wake, inspect the run once; recover a failed/stale run or arrange a new bounded wait if it is demonstrably progressing. Never report completion while required todos or verification failures remain. If Goal mode is inactive because a command was misspelled or an operation was aborted, state that explicitly instead of promising autonomous continuation.
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

### `~/.pi/agent/mcp.json`

```json
{
  "settings": {
    "approveTools": false,
    "directTools": false,
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

### `~/.pi/agent/pi-goal.json`

```json
{
  "continuationLimits": {
    "automaticTurns": 100,
    "noProgressTurns": 3
  },
  "rpc": {
    "enabled": false
  }
}
```

### `~/.pi/agent/settings.json`

```json
{
  "theme": "light",
  "defaultProvider": "openai-codex",
  "defaultModel": "gpt-5.6-terra",
  "compaction": {
    "enabled": true
  },
  "tuiMode": "regular",
  "enableSkillCommands": true,
  "packages": [
    "npm:pi-mcp-adapter@2.33.0",
    "npm:pi-web-access@0.29.0",
    "npm:pi-subagents@0.67.0",
    "npm:@juicesharp/rpiv-ask-user-question@2.10.1",
    "npm:@juicesharp/rpiv-todo@2.10.1",
    "npm:pi-lens@4.1.6",
    {
      "source": "npm:bigpowers@2.88.6",
      "extensions": []
    },
    "npm:billion-context-pi@0.1.71",
    "npm:pi-antigravity@0.7.3",
    "npm:pi-memory@0.4.2",
    "npm:@narumitw/pi-btw@0.58.1",
    {
      "source": "npm:pi-continue@0.9.3",
      "extensions": []
    },
    "npm:@narumitw/pi-goal@0.54.5"
  ],
  "defaultThinkingLevel": "high",
  "subagents": {
    "agentOverrides": {
      "scout": {
        "model": "openai-codex/gpt-5.6-luna",
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
        "model": "openai-codex/gpt-5.6-luna",
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
        "model": "openai-codex/gpt-5.6-sol",
        "thinking": "high",
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
        "model": "openai-codex/gpt-5.6-luna",
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
        "model": "openai-codex/gpt-5.6-sol",
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
      "oracle": {
        "model": "openai-codex/gpt-5.6-sol",
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
        "model": "openai-codex/gpt-5.6-terra",
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

## Upstream references

These links document the package behavior; the local snapshot and pinned templates define this setup. Recheck upstream when upgrading.

- [Pi](https://pi.dev/)
- [MCP Adapter](https://github.com/nicobailon/pi-mcp-adapter)
- [Web Access](https://github.com/nicobailon/pi-web-access)
- [Subagents](https://github.com/nicobailon/pi-subagents)
- [RPIV Todo / Ask User Question](https://github.com/juicesharp/rpiv-mono)
- [Lens](https://github.com/apmantza/pi-lens)
- [Bigpowers](https://github.com/danielvm-git/bigpowers)
- [Billion Context Pi](https://github.com/ranxianglei/billion-context-pi)
- [Antigravity](https://github.com/Rahularya01/pi-antigravity)
- [Memory](https://github.com/jayzeng/pi-memory)
- [Goal / BTW](https://github.com/narumiruna/pi-extensions)
- [Pi Continue (inactive)](https://github.com/Tiziano-AI/pi-continue)
- [CodeGraph](https://github.com/colbymchenry/codegraph)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)

## Repository validation record

On 2026-09-19, the configuration helper was exercised against a temporary home directory, including a path containing spaces. Fresh application, repeated application, preservation of unrelated settings/packages and global guidance, replacement of managed package versions, activation filters, absolute-path substitution, and backup manifests passed. All JSON templates and JSON Markdown blocks parsed; the appendix matched every configuration template. A basic known-token/private-key and source-home-path scan passed. The package installation helper was previewed, not executed against a second workstation. No credentials, memory files, session history or project data were copied. These checks establish configuration portability, not authenticated end-to-end behavior on a new account.
