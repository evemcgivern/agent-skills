# Spec-Workflow Examples

## Quick Start

### Check Workflow Guide
```bash
/spec-workflow guide
```
Shows the complete workflow process and available commands.

### Check Spec Status
```bash
/spec-workflow status content-editing
```
Displays current progress, phase, and next actionable task.

### Execute a Task
```bash
# Single task
/spec-workflow execute content-editing 1.2

# Batch execution (range)
/spec-workflow execute content-editing 1.3-1.6
/spec-workflow execute content-editing 1.3 to 1.6

# Batch execution (list)
/spec-workflow execute content-editing 1.3,1.4,1.5
/spec-workflow execute content-editing 1.3 1.4 1.5
```
Reads task(s), assumes the specified role(s), implements sequentially, and logs completion.

## Complete Workflow Example

### 1. Starting a New Spec

```bash
# After /spec-workflow create my-feature and filling in requirements.md
# (each approve waits for approval in the spec-workflow dashboard)
/spec-workflow approve my-feature requirements

# After requirements approved, create design.md
/spec-workflow approve my-feature design

# After design approved, create tasks.md
/spec-workflow approve my-feature tasks
```

### 2. Implementing Tasks

```bash
# Check what's next
/spec-workflow status my-feature

# Execute first task
/spec-workflow execute my-feature 1.1

# After task 1.1 completes, continue
/spec-workflow execute my-feature 1.2

# Check progress
/spec-workflow status my-feature
```

### 3. Manual Implementation (without /execute)

If you implement a task manually:

```bash
# Log the implementation
/spec-workflow log my-feature 1.3 "Created TypeScript types for content editing feature"
```

This will:
- Call the server's `log-implementation` tool to create an entry under `Implementation Logs/` (summary, files, line counts, artifacts)
- Then update tasks.md to mark task 1.3 complete [x]

## Batch Execution Examples

### Execute Phase 1 Infrastructure Tasks

```bash
# Execute all Phase 1 infrastructure tasks at once
/spec-workflow execute content-editing 1.1-1.6

# The skill will:
# 1. Parse range 1.1-1.6 -> [1.1, 1.2, 1.3, 1.4, 1.5, 1.6]
# 2. Load all tasks and show summary
# 3. Ask for confirmation
# 4. Execute sequentially:
#    - Task 1.1: Create database migration
#    - Task 1.2: Create TypeScript types
#    - Task 1.3: Extend ContentSaveService
#    - Task 1.4: Create PATCH endpoint
#    - Task 1.5: Create GET versions endpoint
#    - Task 1.6: Create POST project association endpoint
# 5. Show completion summary
```

### Execute Specific Tasks

```bash
# Execute only API endpoint tasks
/spec-workflow execute content-editing 1.4,1.5,1.6

# Or with spaces
/spec-workflow execute content-editing 1.4 1.5 1.6
```

### Handling Failures in Batch Mode

If a task fails during batch execution:
```
❌ Task 1.4 failed: Build error in route.ts line 23

Continue with remaining tasks?
  [Yes] - Skip 1.4, continue with 1.5, 1.6
  [No] - Stop batch execution
  [Retry] - Fix error and retry task 1.4
```

## Real-World Examples

### Database Migration (Task 1.1)

```bash
# Execute the task
/spec-workflow execute content-editing 1.1

# The skill will:
# 1. Read task 1.1 from tasks.md
# 2. Assume "Database Engineer" role
# 3. Create the migration file
# 4. Log the implementation, then mark the task complete in tasks.md
# 5. Alert you to apply SQL manually
# 6. Commit changes
```

### TypeScript Types (Task 1.2)

```bash
/spec-workflow execute content-editing 1.2

# The skill will:
# 1. Assume "TypeScript Developer" role
# 2. Create src/types/content-editing.ts
# 3. Define all required interfaces
# 4. Run the build to verify
# 5. Log the implementation and update tasks.md
# 6. Commit changes
```

### API Endpoint (Task 1.4)

```bash
/spec-workflow execute content-editing 1.4

# The skill will:
# 1. Assume "API Developer" role
# 2. Create PATCH /api/content/[id] route
# 3. Implement validation and versioning
# 4. Run the build
# 5. Log the implementation and update tasks.md
# 6. Commit changes
```

## Common Patterns

### Check Before Execute
```bash
# Always check status first
/spec-workflow status my-spec

# Then execute next task
/spec-workflow execute my-spec 2.1
```

### Manual Task Completion
```bash
# If you complete a task manually (e.g., during experimentation)
/spec-workflow log my-spec 3.2 "Implemented auto-save hook with localStorage and 30s throttle"
```

### Progress Tracking
```bash
# Regular status checks throughout the day
/spec-workflow status content-editing
# Output: "Phase 1: Infrastructure - 3/6 tasks complete - Next: Task 1.4"
```

## Integration with Other Commands

### Committing
```bash
# Execute task (auto-commits)
/spec-workflow execute my-spec 1.1

# Or log, then commit yourself
/spec-workflow log my-spec 1.1 "Created migration"
git commit
```

### Verifying
```bash
# After UI changes, check the change in the running app
/spec-workflow execute content-editing 2.4
```

## Tips

1. **Use status frequently** - It helps track progress and identifies next steps
2. **Let execute handle commits** - It follows proper patterns automatically
3. **Log manual work** - Even quick fixes should be logged for audit trail
4. **Check guide when stuck** - `/spec-workflow guide` shows the full workflow
5. **Approvals before implementation** - Don't skip the approval gates

## Error Recovery

If a task execution fails:

```bash
# Check what went wrong
/spec-workflow status my-spec

# Task will still be marked incomplete [ ]
# Fix the issue manually, then:
/spec-workflow execute my-spec 1.1  # Try again

# Or mark complete manually if you fixed it:
/spec-workflow log my-spec 1.1 "Fixed and completed manually"
```

## Next Steps

After completing all tasks in a spec:

1. Final verification and testing
2. Update documentation
3. Move spec to archive (manually or via future command)
4. Celebrate! 🎉
