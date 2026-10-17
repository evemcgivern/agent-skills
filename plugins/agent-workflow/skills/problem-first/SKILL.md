---
name: problem-first
description: "Rewrites a draft agent prompt into problem, evidence, ideas, autonomy and done criteria, so you hand over the problem instead of your solution. Use when drafting a prompt for an agent. Triggers on /problem-first and on phrases like 'rewrite this prompt problem-first', 'am I prescribing a fix', 'tighten this prompt before I send it'."
---

# Problem First

Hand the agent the problem, not your solution. If the agent solves it, you saved your own thinking. If it fails, you learn the problem is hard and that is when you step in.

This skill rewrites a draft prompt. It does not run the task.

## Input

A draft prompt, from the arguments or pasted in the message. If there is none, use the user's most recent message that describes work to do.

## Steps

1. **Sort the draft** into four buckets: the problem, evidence (screenshot, error text, repro, link), the user's ideas for a fix, and constraints (must keep, must not touch).
2. **Check for the exception.** If the draft is a mechanical or fully specified change (rename, exact edit, known value, "run this command"), the user already knows the answer. Say "This one is already specific, send it as is" and stop. Do not force the format.
3. **Rewrite** in this order, dropping any empty section:
   - **Problem:** what is wrong or wanted, in the user's own words. Their names, titles and wording stay exactly as typed.
   - **Evidence:** what the user supplied. For anything missing that would help (screenshot, error, repro), leave a `[ ]` slot. Never invent facts.
   - **Ideas (not instructions):** the user's fix ideas, labelled as ideas the agent may ignore.
   - **Autonomy:** "If you have a solution you are happy with, do it. If you are unsure, give me options or mocks and stop."
   - **Done means:** the finish line the user stated (PR filed, tested, babysat, merge conditions). Keep only what they said. If none, leave one `[ ]` slot.
4. **Show** the rewrite in one code block, then one line per change ("moved your fix to Ideas", "added autonomy line"). Ask at most two questions, and only for slots that block the prompt.

## Rules

- Never alter the meaning, scope or wording of what the user typed. Move it, label it, do not edit it.
- Do not add checks, steps or requirements the user did not ask for.
- Keep the whole reply under 150 words plus the code block.
- Do not execute the prompt, and do not send it.
