---
name: stay-within-limits
description: Keeps long-running or parallel agent work inside 5-hour and weekly usage limits by running work in bounded waves, checking usage between waves, pausing at 95%, and resuming only after the window resets. Use for multi-wave subagent runs, overnight or unattended jobs, or when asked to "don't blow my usage", "watch my limits", "pause before the cap", or "resume when the window resets".
---

# Stay Within Limits

Keep long-running agent work inside the current 5-hour and weekly usage windows.
Check usage before launching substantial work and between waves of parallel
subagents. If either window is at or above 95%, stop launching new work until
it resets.

## Core Loop

1. Check usage before the first wave (see Usage Signals). Record the active
   window identifier.
2. Run a bounded wave. Default to at most 3 parallel subagents unless the user
   or host sets a different throttle.
3. Wait for the wave to finish. Do not interrupt in-flight subagents to save
   budget; that usually loses the work already paid for.
4. Check 5-hour and weekly usage again.
5. **Below 95% on both:** launch the next wave. **At or above 95% on either:**
   stop launching work, report, and schedule a self-contained resume for when
   that window should reset.
6. On resume, re-check the real usage before continuing. Elapsed wall-clock
   time alone is not evidence that the window reset.

## Usage Signals

Prefer a usage tool the host provides to the agent. In Claude Code, the
community `ccusage` CLI reads local session logs. It is third-party npm code,
so ask the user before the first run in a session, and run only this pinned
version:

```sh
npx ccusage@20.0.26 blocks --active --json
```

The user can instead install it once (`npm install -g ccusage@20.0.26`) and
let you run `ccusage blocks --active --json`. Do not switch to `@latest` or
add `-y`.

The JSON has a `blocks` array; the active block carries `startTime`,
`endTime`, `isActive`, `tokenCounts`, and `costUSD`. Use `endTime` for when
the 5-hour window should reset. On wake, compare the active block's
`startTime` with the one you recorded — a new start time is stronger evidence
of a reset than "enough time passed."

`ccusage` reports tokens and estimated cost, not a percentage of the plan
limit, and it does not track the weekly limit. To get a percentage, use the
host's own usage view (for example, ask the user to read it from `/usage` in
Claude Code) or a limit the user has given you. A user may also set an earlier
cost-based caution threshold; treat that as their guardrail, not a universal
rule. If no percentage is obtainable, say so and use the user's threshold or
ask for one before the next wave.

These usage checks work in Claude Code only: `ccusage` reads Claude Code's
session logs and `/usage` is a Claude Code command. On any other host (Codex,
Gemini CLI and others), ask the user to read their 5-hour and weekly usage from
that host's own usage view before each wave. If the user cannot or prefers not
to, skip the check, say so, and rely on the wave sizes alone.

## Pausing And Resuming

When a wake/resume tool is available, schedule the wakeup for:

```txt
min(3600, secondsUntilWindowClears)
```

If the runtime clamps wake delays (for example to 60–3600 seconds), chain
wakeups for longer waits. Each wakeup re-checks usage, reschedules if still at
or above the threshold, and continues only when below it.

A wake prompt must stand alone. Include:

- The remaining plan and the next verification steps.
- The check-then-reschedule rule, the 95% threshold, and the wave throttle.
- The exact usage command or host tool to run.
- The previous block/window identifier, when available.
- The next wave's handoff packets (scope, verification commands, stop
  conditions), if delegation will resume.

## Choosing The Wait Mechanism

- **Wake/resume tool:** when the agent needs instructions attached to the
  future resume.
- **Background sleep or watcher:** for fixed timers or things a process can
  observe directly.
- **Cron/recurring schedule:** only for recurring fresh-session work.

Do not poll for things the host notifies you about, such as background task or
subagent completion. For budget pauses, a prompt-cache miss after a long sleep
is acceptable; staying under the limit matters more.

## Pass / fail

- **Pass:** usage was checked before every wave; no wave launched with either
  window at or above the threshold; every pause was reported with window,
  observed usage, next check time, and remaining work.
- **Fail:** a wave launched without a usage check, a resume trusted elapsed
  time alone, or a wake prompt depended on conversation context.

## Common mistakes

- Treating `ccusage` cost as a plan percentage without a known limit.
- Ignoring the weekly window because the 5-hour window looks fine.
- Killing in-flight subagents at the threshold instead of letting the wave end.
- Short-interval polling while waiting for a reset.

## Reporting

When pausing, tell the user which window is over threshold, the observed usage,
when the next check is scheduled, and what work remains.
