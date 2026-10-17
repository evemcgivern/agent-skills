---
name: pr-wait
description: Wait for GitHub PR CI checks to complete, then optionally merge
color: blue
---

# Wait for PR Checks

Monitor GitHub PR CI checks and wait for them to complete. Optionally auto-merge when all checks pass.

## Usage

```bash
/pr-wait <pr_number> [auto_merge] [max_wait_minutes] [check_interval]
```

## Arguments

- **pr_number** (required): GitHub PR number to monitor
- **auto_merge** (optional, default: false): Set to "true" to auto-merge after checks pass
- **max_wait_minutes** (optional, default: 20): Maximum time to wait in minutes
- **check_interval** (optional, default: 60): Seconds between status checks

## Examples

```bash
# Monitor the pull request (manual merge)
/pr-wait 172

# Monitor and auto-merge the pull request
/pr-wait 172 true

# Wait up to 30 minutes, check every 90 seconds
/pr-wait 172 false 30 90

# Auto-merge with custom timing
/pr-wait 172 true 15 45
```

## Behavior

1. **Initial Status**: Shows current state of all CI checks
2. **Polling**: Periodically checks status at specified interval
3. **Progress Updates**: Shows which checks are still running
4. **Completion**:
   - If `auto_merge=false`: Reports final status and exits
   - If `auto_merge=true`: Merges PR and optionally deletes branch
5. **Timeout**: If checks don't complete within max_wait_minutes, reports status and exits

## Implementation

### Step 0: Handle --help flag

**FIRST**: Check if the first argument is `--help`, `-h`, or `help`. If so, display usage and exit:

```
pr-wait - Monitor GitHub PR CI checks and optionally auto-merge

Usage:
  /pr-wait <pr_number> [auto_merge] [max_wait_minutes] [check_interval]
  /pr-wait --help

Arguments:
  pr_number         GitHub PR number to monitor (required)
  auto_merge        Auto-merge after checks pass: true|false (default: false)
  max_wait_minutes  Maximum wait time in minutes (default: 20)
  check_interval    Seconds between status checks (default: 60)

Examples:
  # Monitor PR (manual merge)
  /pr-wait 123

  # Monitor and auto-merge
  /pr-wait 123 true

  # Custom timing: 30 min max, check every 90s
  /pr-wait 123 false 30 90

  # Auto-merge with custom timing
  /pr-wait 123 true 15 45

Features:
  ⏱️  Configurable check interval (default: 60s)
  ⏰ Timeout protection (default: 20 minutes)
  🤖 Auto-merge option (squash + delete branch)
  📊 Real-time progress with timestamps
  ✅ Success validation (won't merge if checks fail)
```

Then **exit immediately** without running any checks.

### Step 1: Validate and parse arguments

Validate that pr_number is provided and is numeric.

### Step 2-8: Monitor and merge

1. Use `gh pr view <pr_number> --json statusCheckRollup` to get check statuses
2. Parse the JSON to find checks with `status != "COMPLETED"`
3. Poll at the specified interval using `sleep <check_interval>`
4. Calculate timeout based on `max_wait_minutes * 60 / check_interval` iterations
5. Show progress with timestamps and check names
6. If all checks complete:
   - Show final status (SUCCESS/FAILURE/etc)
   - If `auto_merge=true` and all checks passed:
     - Run `gh pr merge <pr_number> --squash --delete-branch`
     - Confirm merge success
7. Handle edge cases:
   - PR doesn't exist
   - No CI checks configured
   - Checks fail
   - Timeout reached

## Output Format

```
Monitoring the pull request CI checks...
Check interval: 60s | Max wait: 20 minutes | Auto-merge: enabled

=== Initial Status ===
✅ Build and Test: COMPLETED SUCCESS
⏳ E2E Tests: IN_PROGRESS
⏳ Lighthouse CI: IN_PROGRESS

[1] 09:50:00 - 2 checks still running:
  ⏳ E2E Tests
  ⏳ Lighthouse CI

[2] 09:51:00 - 1 check still running:
  ⏳ Lighthouse CI

[3] 09:52:00 - All checks complete!

=== Final Status ===
✅ Build and Test: SUCCESS
✅ E2E Tests: SUCCESS
✅ Lighthouse CI: SUCCESS

🎉 All checks passed! Merging the pull request...
✅ the pull request merged and branch deleted successfully!
```

## Error Handling

- **PR not found**: Exit with clear error message
- **Checks failed**: Show which checks failed, do NOT merge
- **Timeout**: Show current status, exit without merging
- **Merge conflict**: Show error, suggest resolution steps
