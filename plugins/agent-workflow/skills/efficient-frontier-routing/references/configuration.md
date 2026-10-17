# Efficient Frontier Routing: configuration help

Run `/efficient-frontier-routing help` in Claude Code (or
`/agent-workflow:efficient-frontier-routing help` when installed as a plugin),
or ask your agent to show this skill's help. In Codex, invoke
`$efficient-frontier-routing` and ask for help.
This displays guidance; it does not change settings or launch agents.

The skill tells an assistant how to choose workers. The host launches those
workers. It does not install a runtime router, change subscription limits, or
guarantee a particular saving.

## Quick start: one session

Start Claude Code with an explicit main model and effort:

```sh
claude --model sonnet --effort medium
```

Then give the task with the preferences you want:

```text
/efficient-frontier-routing Fix the failing tests in src/example.test.ts.
Use Haiku for discovery, Sonnet for implementation, and Opus at high effort
only for difficult decisions or risky reviews. Keep at most two subagents
running concurrently. Keep the main model unchanged. Do not use xhigh.
```

These are suggested starting choices. Pick a stronger main model when the
whole task needs it. Starting with a cheaper model does not prevent an explicit
stronger subagent request. [Model controls](https://code.claude.com/docs/en/model-config),
[subagent model selection](https://code.claude.com/docs/en/sub-agents#choose-a-model).

## Save the main model and effort

Merge these keys into the existing settings object, preserving hooks,
permissions, plugins, and other settings:

```json
{
  "model": "sonnet",
  "effortLevel": "medium"
}
```

Choose the scope:

| File | Applies to |
| --- | --- |
| `~/.claude/settings.json` | Your projects by default |
| `.claude/settings.json` | Everyone using the repository's shared settings |
| `.claude/settings.local.json` | Your settings for this repository |

Local project settings override shared project settings, which override user
settings. Startup flags can override these for a session; organization policy
and relevant environment variables can also affect the result. Saved per-model
effort can override the general effort default. In the user settings file, a
top-level `effortLevel` does not apply to Opus 5.5 or newer models; choose
their effort with `/effort` or the `/model` picker, which saves it per model.
Use `/status` and `/model` to inspect the effective setup.
[Settings scope](https://code.claude.com/docs/en/settings#settings-precedence),
[effort controls](https://code.claude.com/docs/en/model-config#adjust-effort-level).

## Save routing preferences

Put a short section in `~/.claude/CLAUDE.md` for global preferences, or the
repository's `CLAUDE.md` for project preferences. In Codex, use the applicable
`AGENTS.md`. No special configuration file or parser is required.

Example policy to adapt:

```markdown
## Efficient frontier routing

Always use /efficient-frontier-routing for every task.
Keep the chosen main model unchanged and handle small tasks directly.
- Discovery: Haiku.
- Implementation and tests: Sonnet at medium effort.
- Difficult decisions and risky reviews: Opus at high effort.
- Escalate for architectural uncertainty, conflicting evidence, or two
  failed approaches to the same problem.
- Maximum concurrent subagents: 2, including background workers.
- Escalation within these tiers is permitted without asking.
- Use xhigh or a model above Opus (such as Fable) only when I explicitly
  request it.
```

This skill applies task-specific preferences before project preferences,
project before global, and global before its defaults. These are model-followed
instructions, not enforced budget controls or Claude settings keys.

| Preference | What users can change |
| --- | --- |
| Worker tiers | Model for discovery, implementation, and review |
| Effort | Per-worker effort supported by the selected model and host |
| Escalation | Triggers, failed-attempt threshold, and approval requirement |
| Concurrency | Maximum simultaneous workers, including background agents |
| Model ceiling | Highest allowed model; whether exceptional effort is allowed |
| Delegation | Allow workers, or keep the task in the main session |

To override a saved preference for one task, state it in the prompt. For example:
“Use only Sonnet for this task; if a stronger review is needed, report that it
remains outstanding.” A model restriction must not become a claim that a
required review was completed.

## Codex routing preferences

Edit `~/.codex/AGENTS.md` for global preferences, or a project's `AGENTS.md`
for that project. Invoke `$efficient-frontier-routing` in Codex. The skill
uses Codex models available in that host; Claude aliases such as `haiku` and
`opus` do not configure Codex workers.

Example to adapt with model names shown by your Codex host:

```markdown
## Efficient frontier routing

Always use $efficient-frontier-routing for every task.
Keep the selected main model and handle small tasks directly.
- Discovery: the fastest available model suitable for factual checks.
- Implementation: an available coding model with medium reasoning effort.
- Difficult decisions and risky reviews: a stronger available reasoning model
  with high effort. Do not use xhigh or max unless I request it.
- Maximum concurrent subagents: 2, including background workers.
- Escalate for architectural uncertainty, conflicting evidence, or two failed
  approaches to the same problem.
- Use explicit supported model IDs and report the model actually selected.
```

For fixed routing, replace the role descriptions with exact model IDs your
host offers. Existing organization and runtime restrictions still apply.
If the host offers only one model or cannot override a worker's model, the
skill cannot create that capability. Increasing effort is not changing models.
The main session's actual model is selected in the host, separately from these
routing instructions. Ordinary routing uses the current provider; a separately
required different-vendor review can use another provider when available.

## Pin a reusable review agent

For repeated specialist work, create `~/.claude/agents/routing-reviewer.md`:

```markdown
---
name: routing-reviewer
description: Review difficult or risky code changes when explicitly delegated.
tools: Read, Grep, Glob
model: opus
effort: high
---

Review the assigned files and evidence. Return concrete findings with file
and line references, unresolved questions, and missing verification. Do not edit.
```

An invocation can override the agent file's model. Without an explicit model,
a worker may inherit the main model. Effort can also inherit unless specified.
A conversation fork uses the main model; use an ordinary subagent for upward
routing. [Agent configuration](https://code.claude.com/docs/en/sub-agents).

## Verify and troubleshoot

- Run `/tasks` while a worker is active to inspect its reported model and
  explicitly configured effort. Do not assume a requested model was available.
- If every worker uses one model, check `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` and
  model restrictions. The force option can override per-agent choices.
- Use `/usage` for plan consumption and `/context` for context size. Agent work
  consumes usage too; a concurrency preference is not a hard spending limit.
- If the skill is missing, check that it is installed as
  `~/.claude/skills/efficient-frontier-routing/` (or the project's
  `.claude/skills/`), or that its plugin is enabled. Restart the host if
  discovery has not refreshed. Keep one installed copy so copies do not drift.

Other hosts may expose different model names or no per-agent selector. Use
available equivalents and report restrictions; Claude settings do not configure
Codex. See [usage monitoring](https://code.claude.com/docs/en/costs) and
[subagent controls](https://code.claude.com/docs/en/sub-agents).
