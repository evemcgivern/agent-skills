---
name: audit-background-processes
description: Inventory and safely clean up stray background processes left by agent sessions — watch loops, tails, orphaned sleeps, detached runs — killing only by PID after confirming ownership. Use before any pkill/killall by pattern, when a machine feels loaded, when a run died for no clear reason, or when asked to "clean up stray processes", "kill leftover shells", or "what's still running in the background".
---

# Audit Background Processes

## Overview

Long agent sessions leak processes: watch loops whose target died, `tail -f` on
finished logs, orphaned `sleep`, detached runs nobody is reading. Cleaning them
is easy. Cleaning them **without killing someone else's live work** is the part
that needs care.

**Core principle: identify ownership before killing, and kill by PID, never by
a broad pattern.**

## When to Use

- Asked to "clean up shells / monitors / stray processes"
- A long-running job died with no explanation (something else may have killed it)
- Machine feels loaded and you suspect leftovers
- Before running any `pkill`/`killall` — read the Never-Do list first

Not for: killing a specific job you just started and can name by PID.

## The Rule That Matters

**Never `pkill -f <broad pattern>`.** A pattern like a repo name, a project
path, or a tool name matches every process whose *arguments* contain it —
including other agent sessions' monitors, editors, and shells.

Example incident: `pkill -9 -f my-project` was meant to stop one eval run. It
matched and killed two monitors belonging to a different session, because their
command lines contained the repo path. Nothing was lost only by luck — both had already
finished. The intent was one process; the blast radius was every session on the
machine.

## Quick Reference

| Signal | Meaning | Safe to kill? |
|---|---|---|
| `ppid = 1` and it's a watch/sleep you spawned | your orphan | yes, by PID |
| `ppid` is a live shell | part of something still running | no, deal with the parent |
| `/bin/zsh -i`, `-bash`, login shell | a human's terminal | **never** |
| an ancestor of your own shell or of a terminal (tmux, screen) | kills everything under it | **never** |
| you cannot tell whose it is | could be another session's | **ask first** |
| `tail -f` on a log that ended (`*_DONE`) | stale, but ownership still applies | only if yours |
| a test or benchmark run, even with `ppid = 1` | still doing work; killing it loses the in-flight results | **ask first, every time** |

## Procedure

1. **Inventory, don't guess.** `bash <this-skill-directory>/audit.sh` lists
   your own interactive shells, live test and benchmark runs, and suspected
   orphans with PID, parent PID, age and command. Other users' processes are
   left out, because their command lines can hold secrets. It never kills
   anything.
2. **Resolve each PID before acting.** `ps -o pid=,args= -p <pid>` — read what
   it actually is. A PID that looked like a watch loop turned out to be an
   interactive shell in the incident above.

   **Do not write `ps -Ao args -p <pid>`.** `-A` overrides `-p`, so it prints
   every process and any `tail -1`/`head -1` you pipe it into returns an
   unrelated one. This produced a kill log where every line was labelled
   `/bin/zsh -i` regardless of the real target — the kills were correct, the
   evidence was fabricated. A label you did not actually verify is worse than
   no label, because it reads as a check that happened.
3. **Kill by PID.** `bash <this-skill-directory>/audit.sh --kill <pid>...`
   takes only numeric PIDs. It rebuilds the suspect list, refuses any PID
   that is no longer on it, prints what it will kill, and sends SIGTERM. A
   live test or benchmark run can appear as a suspect when the shell that
   launched it has exited; ask its owner before passing its PID. Use `kill -9`
   by hand only if SIGTERM is ignored.
4. **Verify by listing, not counting.** `ps -Ao args | grep -c <pattern>` can
   match its own wrapper and report phantom survivors. Print the matches.

## Common Mistakes

**Counting instead of listing.** `grep -c` on a `ps` pipeline counts the
shell wrapper running the grep. It reported "2 processes remaining" when the
true answer was zero, twice in one session. Always print the rows.

**Assuming an empty grep means success.** Battery and CI logs can contain bytes
that make `grep` treat them as binary, where `-o` silently prints nothing. Use
`grep -a` on log files.

**Killing a run to "free the machine" mid-measurement.** Many harnesses write
results per unit of work; an interrupted run loses the in-flight unit entirely,
including the reason it stopped.

**Treating another session's stale process as yours.** Stale ≠ yours. A
`tail -f` on a finished log is harmless (no CPU); leaving it costs nothing,
killing it may confuse a session still open in another window.

## Script

`audit.sh` reports only, by default. A suspected orphan is a process you own
whose parent is PID 1, outside system and application paths, that is not an
interactive shell, not the script or one of its ancestors, and not an ancestor
of any interactive shell.

`audit.sh --kill <pid>...` kills only the PIDs you name, and only those still
on a fresh suspect list. It never matches by pattern or by session ID, and it
never escalates past SIGTERM. It prints the PIDs it refused, the ones it
signalled, and any still running afterwards.
