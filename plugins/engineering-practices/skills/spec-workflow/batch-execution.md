# Batch Task Execution Guide

## Syntax

The spec-workflow skill supports three batch execution formats:

### 1. Range Syntax (Hyphen)
```bash
/spec-workflow execute <spec-name> <start>-<end>
```
Examples:
- `/spec-workflow execute content-editing 1.3-1.6` → Executes tasks 1.3, 1.4, 1.5, 1.6
- `/spec-workflow execute chat-history 2.1-2.5` → Executes tasks 2.1, 2.2, 2.3, 2.4, 2.5

### 2. Range Syntax (Words)
```bash
/spec-workflow execute <spec-name> <start> to <end>
```
Examples:
- `/spec-workflow execute content-editing 1.3 to 1.6` → Same as 1.3-1.6
- `/spec-workflow execute bulk-operations 3.1 to 3.4` → Executes 3.1, 3.2, 3.3, 3.4

### 3. List Syntax (Comma or Space)
```bash
/spec-workflow execute <spec-name> <task1>,<task2>,<task3>
/spec-workflow execute <spec-name> <task1> <task2> <task3>
```
Examples:
- `/spec-workflow execute content-editing 1.3,1.5,1.6` → Executes only 1.3, 1.5, 1.6 (skips 1.4)
- `/spec-workflow execute content-editing 1.3 1.5 1.6` → Same as above

## Restrictions

**Range must be within same phase**:
- ✅ Valid: `1.3-1.6` (all in Phase 1)
- ✅ Valid: `2.1-2.5` (all in Phase 2)
- ❌ Invalid: `1.6-2.2` (crosses phases)

**Reason**: Different phases often have dependencies on previous phase completion.

## Batch Execution Flow

1. **Parse task specification** into task ID array
2. **Load all tasks** from tasks.md
3. **Validate all tasks exist** (fail early if any missing)
4. **Show batch summary**:
   ```
   📋 BATCH EXECUTION: content-editing

   Tasks to execute (6):
     1.1 ✓ Create database migration (already complete)
     1.2 ✓ Create TypeScript types (already complete)
     1.3 ○ Extend ContentSaveService
     1.4 ○ Create PATCH endpoint
     1.5 ○ Create GET versions endpoint
     1.6 ○ Create POST project association endpoint

   Estimated changes:
     - Modify: src/lib/services/content-save-service.ts
     - Create: src/app/api/content/[id]/route.ts
     - Create: src/app/api/content/[id]/versions/route.ts
     - Create: src/app/api/projects/[id]/content/route.ts

   Execute all 4 remaining tasks? [Yes/No/Review]
   ```

5. **Execute tasks sequentially**:
   - Skip already completed tasks [x]
   - Execute pending tasks [ ] in order
   - Show progress: "Task 1 of 4: 1.3 - Extend ContentSaveService"

6. **Handle failures**:
   - On task failure, pause and ask:
     ```
     ❌ Task 1.4 failed: Build error

     Options:
       [Continue] - Skip 1.4, continue with 1.5, 1.6
       [Stop] - Stop batch execution
       [Retry] - Fix error and retry task 1.4
       [Debug] - Show detailed error and open file
     ```

7. **Show completion summary**:
   ```
   ✅ BATCH COMPLETE: content-editing 1.3-1.6

   Results:
     ✓ 1.1 - Create database migration (skipped - already complete)
     ✓ 1.2 - Create TypeScript types (skipped - already complete)
     ✓ 1.3 - Extend ContentSaveService (success)
     ✓ 1.4 - Create PATCH endpoint (success)
     ✓ 1.5 - Create GET versions endpoint (success)
     ✓ 1.6 - Create POST project association endpoint (success)

   Total: 4 executed, 4 succeeded, 0 failed, 2 skipped
   Build: ✅ Passed
   Commits: 4 commits created
   ```

## Benefits of Batch Execution

1. **Efficiency**: Execute related tasks in one command
2. **Atomic commits**: Each task gets its own commit
3. **Progress tracking**: See overall progress across multiple tasks
4. **Error recovery**: Choose to continue or stop on failures
5. **Build optimization**: Build runs once after all tasks (not after each task)

## Best Practices

### When to Use Batch Execution

✅ **Good use cases**:
- Executing all tasks in a phase (e.g., "Phase 1: Infrastructure")
- Creating all API endpoints at once (e.g., "1.4-1.6")
- Implementing all component variations (e.g., "2.1-2.5")
- Setting up infrastructure tasks (migrations, types, services)

❌ **Avoid batching**:
- Tasks with unclear requirements (execute one at a time to review)
- Tasks that might need user input (approvals, confirmations)
- Tasks across different phases (dependencies might not be met)
- Complex tasks that need individual attention

### Recommended Workflow

1. **Review tasks first**: Read tasks.md to understand scope
2. **Execute in logical groups**: Group by functionality (DB → Types → Services → API)
3. **Monitor progress**: Watch for errors and fix before continuing
4. **Verify after batch**: Run tests or manual verification after all tasks complete

### Example Workflow: Content Editing Phase 1

```bash
# Step 1: Infrastructure (DB + Types + Services)
/spec-workflow execute content-editing 1.1-1.3

# Verify: Check migration applied, types compile, service tests pass

# Step 2: API Endpoints
/spec-workflow execute content-editing 1.4-1.6

# Verify: Test all endpoints work, check the connection doc is updated

# Step 3: Manual verification
npm test   # or the project's test command
# then verify the change in the running app
```

## Error Handling

### Invalid Range
```bash
/spec-workflow execute content-editing 1.6-2.2
```
```
❌ ERROR: Task range must be within same phase
   Range: 1.6-2.2 spans Phase 1 and Phase 2

   Valid examples:
     ✓ 1.3-1.6 (Phase 1 only)
     ✓ 2.1-2.5 (Phase 2 only)
```

### Missing Tasks
```bash
/spec-workflow execute content-editing 1.3-1.8
```
```
❌ ERROR: Tasks not found
   Missing: 1.7, 1.8

   Available tasks in Phase 1:
     1.1, 1.2, 1.3, 1.4, 1.5, 1.6
```

### Build Failure
```bash
# During batch execution
✓ Task 1.3 complete
✓ Task 1.4 complete
❌ Task 1.5 failed: Build error

Build output:
  src/app/api/content/[id]/versions/route.ts:15:3
  Type 'string' is not assignable to type 'number'

Options:
  [Fix] - Open file in editor and fix error
  [Skip] - Mark 1.5 as incomplete and continue with 1.6
  [Stop] - Stop batch execution
```

## Advanced Usage

### Selective Execution
```bash
# Execute only even-numbered tasks
/spec-workflow execute content-editing 1.2,1.4,1.6

# Execute first and last tasks in phase
/spec-workflow execute content-editing 2.1,2.9
```

### Cross-Spec Batching (Not Supported)
```bash
# This is NOT supported:
/spec-workflow execute content-editing,chat-history 1.1-1.3

# Instead, execute specs separately:
/spec-workflow execute content-editing 1.1-1.3
/spec-workflow execute chat-history 1.1-1.3
```

## Integration with Other Commands

### After Batch Execution
```bash
# Execute batch
/spec-workflow execute content-editing 1.3-1.6

# Check status
/spec-workflow status content-editing

# Verify changes in the running app, then run tests
npm test   # or the project's test command
```

### Resuming After Failure
```bash
# If batch fails at 1.5
# Fix the error manually, then:
/spec-workflow execute content-editing 1.5-1.6
```
