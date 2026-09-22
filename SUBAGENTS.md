# How my Pi subagents work

This is the general design behind my personal Pi setup, captured on 2026-09-19. For installation commands and exact configuration, see [the setup guide](README.md).

## The idea

I use one main agent to own the task, with specialist subagents for bounded pieces of work. The main agent keeps the full objective in view, decides what to delegate, checks the results, and carries the work through verification. Delegation should reduce effort or improve confidence; a simple question does not need a team.

I keep Pi Subagents' existing core roles and prompts, then choose models and thinking levels for their jobs. Designer and Observer are the two custom additions. This keeps exploration, research, implementation, review and decision support available without writing a large new prompt framework.

The setup is cost-conscious: routine exploration and implementation go to GPT-6 Luna, coordination, review and difficult questions go to GPT-6 Sol, and visual/UI work goes to Gemini Flash. GPT-6 Astra is reserved for explicit escalation on unusually hard bounded tasks rather than a standing role.

## Intelligence and reasoning allocation

“Intelligence” here means how I allocate model capability and reasoning effort to different jobs. These are practical role choices, not benchmark scores or a claim that one model is universally better. Thinking levels are provider/model settings, not directly comparable measurements of intelligence. High thinking does not guarantee correctness.

| Agent | Configured model | Thinking | Why it has this job |
| --- | --- | --- | --- |
| Main agent | `openai-codex/gpt-6-sol` | medium | Owns the overall task, coordinates specialists, integrates results and verifies completion. |
| Scout | `openai-codex/gpt-6-luna` | low | Finds relevant files, symbols and existing patterns quickly; this is the explorer role. |
| Researcher | `openai-codex/gpt-6-luna` | medium | Looks up documentation and external information; this is the librarian role. |
| Worker | `openai-codex/gpt-6-luna` | high | Implements a clearly scoped change, diagnoses failures and runs relevant checks. |
| Evidence Auditor | `openai-codex/gpt-6-sol` | high | Checks whether sources and evidence actually support a claim. |
| Reviewer | `openai-codex/gpt-6-sol` | high | Independently inspects implementation for defects, missed requirements and weak verification. |
| Oracle | `openai-codex/gpt-6-sol` | high | Helps with difficult design decisions, ambiguity and problems that need another approach. |
| Delegate | `openai-codex/gpt-6-sol` | medium | Handles a general bounded assignment that does not fit another specialist. |
| Designer | `antigravity/gemini-3.8-flash` | high | Implements UI using project design guidance and checks the rendered result. |
| Observer | `antigravity/gemini-3.8-flash` | high | Inspects supplied screenshots/images and reports concrete visual findings. |

The main agent chooses a role based on the work. These mappings do not implement automatic model escalation: GPT-6 Astra is an explicit hard-task escalation, and asking Oracle for help is a coordination decision, not a guaranteed fallback built into every failed Worker run.

## How a task moves through the team

For a substantive implementation task, the intended flow is:

1. The main agent reads the objective and project instructions, identifies acceptance criteria, and maintains the Todo list.
2. Scout locates the relevant code when exploration is useful. Researcher checks external documentation when needed.
3. Worker receives a bounded implementation assignment. Designer takes UI work that benefits from its specialization.
4. The main agent consumes the result and its verification evidence. Reviewer can independently inspect the changed code; Evidence Auditor can examine source-backed claims. Oracle helps when a difficult issue needs a different approach.
5. Findings become follow-up work. Failed tests lead to diagnosis, repair and another test run, rather than a claim that the task is finished.
6. The main agent integrates the results and checks the original acceptance criteria before declaring completion.

This is an example workflow, not a compulsory sequence. The parent can implement directly, omit unnecessary specialists, or run independent investigations concurrently. A review is useful evidence, not proof of correctness by itself.

A good child assignment names the objective, scope, constraints, expected output and checks. For example: “Fix the draft-save failure in this feature; preserve the existing authorization rules; add or run the relevant regression check; return changed files, results and remaining issues.” Avoid giving multiple writers overlapping ownership of the same changes.

## Background execution and coordination

The setup uses `pi-subagents` for delegation. Top-level runs are asynchronous for the configured MCP/provider extensions: a child works in the background and Pi delivers its completion or attention notification to the parent.

The parent should do useful independent work while a child runs. If it can only wait, it should wait for the native notification instead of repeatedly polling. A final-looking message such as “the review is running” can therefore mean that background work is still active.

Normal coordination aims for at most two children at a time. The configuration has concurrency and active-run limits of two, but these are separate scheduler limits, not a guaranteed machine-wide maximum of two processes. The default timeout is 30 minutes; a specific workflow can set a shorter deadline.

Children are not intended to recursively delegate. Stock roles have nested delegation disabled, and custom agents are instructed not to delegate. The parent remains responsible for the original objective and the relationship between tasks.

If a worker times out, the parent should inspect its partial changes and diagnostics, confirm the previous writer has stopped, then narrow the task or change the approach before retrying. It should not discard useful work automatically or launch competing writers. Explicit user cancellation must still be respected.

## What each agent can see and use

Roles receive project context through the configured inheritance settings. Worker, Delegate and Designer also explicitly inherit skills. Project instructions and specifications remain authoritative; a generic package workflow should not overwrite them.

Children have explicit extension and tool lists rather than automatically receiving every parent capability:

- Code-oriented roles load MCP Adapter and Billion Context. Their listed tools include code inspection and shell access; writing roles also expose file-editing tools.
- Researcher and Evidence Auditor load Web Access and Billion Context for research and evidence work.
- Designer loads MCP Adapter, Billion Context and the Antigravity provider, with editing tools and Playwright available through MCP.
- Observer loads Billion Context and the Antigravity provider with image/file reading, without editing or browser tools. It reports on images supplied to it; Designer can operate the browser.

CodeGraph helps understand already indexed repositories, and Playwright supplies browser verification. These are exposed through the MCP gateway rather than loaded as a large set of direct tools at startup.

A role described as read-only is a workflow intention, not a sandbox guarantee: a role with shell access can still execute commands that write files. Completion guards and output settings also support the workflow; they do not independently prove that the implementation is correct.

## Memory, context, tasks and autonomy

Each supporting package has a distinct job:

| Component | Responsibility |
| --- | --- |
| Pi Subagents | Dispatch and supervise specialist work. |
| RPIV Todo | Track the substantive tasks and required verification. |
| Billion Context Pi | Compress and retrieve conversation context during long work. Its own delegation is disabled. |
| Pi Memory | Store durable facts and notes across sessions; its scratchpad is not the main task list. |
| Pi Goal | Continue an explicitly activated session objective when Pi becomes idle. |

A Todo list does not itself force continuation. For sustained work, start `/goal <objective and acceptance criteria>`. The parent should keep todos synchronized with that goal and only record completion after the required work and verification are done.

Goal is configured for 100 automatic model responses and a repeated-no-progress guard. It is not loaded into children. The parent is responsible for coordinating the whole objective; every child does not run its own independent Goal loop.

When only an external/subagent result remains, the parent is instructed to use `goal_wait` with the run ID and a fallback wake deadline. This reduces the chance of waiting indefinitely if a notification is missed. The deadline policy is guidance, not a code patch that mechanically inserts a timer into every wait call.

The desired behavior is persistent repair and verification within authorized scope. The actual system can still pause for limits, errors, missing credentials, genuine external blockers or cancellation. Goal and Todo are not hard acceptance gates, and a model can misjudge completion. Required tests and other concrete evidence remain essential.

## What I intentionally avoid

I avoid assigning the most expensive model to every role, replacing the stock agent roster with a large custom framework, making every task pass through every agent, and having children recursively spawn more children.

I also avoid competing delegation, task-list and continuation systems. Billion Context delegation is off; Pi Continue is inactive because it requires native compaction; Bigpowers contributes skills/prompts with its blocking extension hooks disabled. Ralph loops were considered but are not part of this setup.

The governing preference is simple: concise coordination, bounded assignments, appropriate model cost, independent checks where useful, and continued repair until the agreed work is verified or a real stopping condition is reached.
