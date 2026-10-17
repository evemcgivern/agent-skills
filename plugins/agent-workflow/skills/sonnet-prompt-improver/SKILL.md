---
name: sonnet-prompt-improver
description: "Improves a prompt, system prompt, agent definition or skill for Claude Sonnet 5.5 by applying problem-first framing, adding only the Sonnet 5.5 fixes that match an observed symptom, and suggesting effort and thinking settings. Use when writing or fixing a prompt for Sonnet 5.5. Triggers on /sonnet-prompt-improver and on phrases like 'improve this prompt for Sonnet', 'why does Sonnet keep stopping to ask', 'tune this system prompt for 5.5'."
---

# Sonnet 5.5 Prompt Improver

Rewrite a prompt so Claude Sonnet 5.5 does what the user meant. Source: Anthropic's "Prompting Claude Sonnet 5.5" guide (https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5), read 2026-10-03; claims rechecked against it 2026-10-17. If the target model is newer than Sonnet 5.5, say the guide may be stale and stop adding model-specific snippets.

This skill rewrites a prompt. It does not run the task and does not send it.

## Core rule

Existing Sonnet 5 prompts work on 5.5 without changes. Add a fix only when the user names a symptom or the draft clearly shows one. A longer prompt is not a better prompt.

## Steps

1. **Identify the kind of prompt:**
   - **A. A message the user will type to an agent** (Claude Code, chat).
   - **B. A standing prompt** (system prompt, agent definition, SKILL.md, CLAUDE.md block).
   - **C. An API call that must return JSON.**
   If unclear, assume A and say so.
2. **Frame it problem-first** (the `problem-first` skill, if installed, holds the full rules): the user's problem and evidence in their own words, their fix ideas labelled as ideas, an autonomy line, and a finish line they stated. A fully specified mechanical edit stays as is. Leave `[ ]` slots for missing facts; never invent them.
3. **Match symptoms to fixes.** Use only the rows that apply:

   | Symptom | Fix |
   |---|---|
   | Stops to check in before the work is done, asks things it could answer | Raise effort first. Else add: keep working until everything asked is done, stop to ask only when blocked or before a risky step. |
   | Adds tests, docs, files or refactors nobody asked for | Add: when the asked work is done and checked, stop and report; mention extras at the end instead of doing them. |
   | Starts self-review rounds or reviewer subagents (mostly at xhigh or max) | Add: once the work and its checks pass, stop and report; no extra review rounds or reviewer subagents unless asked. |
   | Builds something when you only wanted ideas | Add: when asked for ideas, options or a plan, give them and stop until told to go ahead. |
   | Reports code as done with no test or build run (mostly at low effort) | Add: run a real check that exercises the change (tests, type-check, build, or the changed command) before reporting done. A syntax-only check does not count. If the only blocker is missing declared dependencies, install them with the project's own package manager and lockfile, never with sudo or the system package manager. If no real check can run, say which one was skipped and why. |
   | JSON answer to a multi-step task is wrong | Prefer structured outputs. Use adaptive thinking, not the lowest thinking setting. Add one line at the end of the system prompt: "Think the problem through before you answer." Or use xhigh. |
   | JSON does not parse because working-out comes before it | Parse the last JSON value in the text blocks, and treat stop_reason max_tokens as failed. |
   | Answers from memory when details may have changed | Remove "only use tools when strictly necessary" or "minimize tool calls". Add: check specifics that may have changed (what is allowed, required or charged) with search, even when confident. |
   | Long agentic turn looks silent | Remove "hold all findings for the final response". Ask for a one-line update before the first tool call and a short recap at the end. |
   | Output carries stray internal XML tags (mostly with `between_tools` thinking) | Remove any "do not think" or "think less" instruction. Lower effort instead. |
   | Refusal with `reasoning_extraction` | Remove instructions that ask the model to reproduce its reasoning in the reply. Ask for a short explanation or action summary instead. |

   Do not add "think less" lines: they do not reliably cut thinking. Lower the effort setting instead.
4. **Suggest settings** (one line, only for B and C):
   - Effort levels are recalibrated for 5.5, so sweep them against real evals instead of reusing the Sonnet 5 setting.
   - Start at high. For agentic coding, start at medium for well-specified tasks and high for harder ones. For chat or latency-sensitive work, medium or low.
   - Reserve xhigh and max for cases where a quality gain was measured.
   - Leave room in max_tokens for thinking plus the reply.
   - Changing the top-level effort between requests breaks the prompt cache; a per-message effort change (beta, adaptive thinking only) keeps it.
5. **Show** the improved prompt in one code block, then one line per change, each tied to its symptom. Ask at most two questions, only for slots that block the prompt.

## Repo rules win

If the prompt belongs to a repo with its own prompt rules, follow them over this skill. For example, a repo may require that behavior that must hold goes in schema fields, not prompt prose; that positive examples replace negative instructions; or that guardrails constrain model output, never what a user typed.

## Rules

- Keep the user's own wording, names and titles exactly as typed. Move and label them; do not rewrite them.
- Add no check, step or requirement the user did not ask for, other than a snippet from the table that matches a stated symptom.
- Keep the reply under 150 words plus the code block.
