# Spec-Workflow Skill Instructions

These instructions assume the [spec-workflow MCP server](https://github.com/Pimzino/spec-workflow-mcp) is installed and connected. Its tools are `spec-workflow-guide`, `steering-guide`, `spec-status`, `approvals`, and `log-implementation`. If they are not available, tell the user the server is required and stop.

## Project Context Detection

Before executing any action, detect project-specific patterns by checking for these files:

```bash
# Check for project guidance files
- vision.md or VISION.md       # Product roadmap, business requirements, feature phases
- CLAUDE.md or claude.md       # Project-specific development guidelines
- AGENTS.md or agents.md       # AI assistant instructions and patterns
- ConnectionGuide.txt or connections.txt  # Example names for an API endpoints / ports / service connections doc, if the project keeps one
```

**If found, adapt behavior:**
1. **vision.md**: Reference for feature alignment, business requirements, and roadmap phases
2. **CLAUDE.md/claude.md**: Follow project-specific patterns, pre-commit checklists, and gotchas
3. **AGENTS.md/agents.md**: Reference AI-specific guidelines and requirements
4. **Connection doc** (e.g. ConnectionGuide.txt): Update when creating new API endpoints or services
5. **Build verification**: Use the project's build command, found in its guidance files or package/build config (for example `npm run build`)

**Store detected files in context for the session.**

## Command Parsing

When the user invokes `/spec-workflow` or uses this skill, parse the command arguments:

```
/spec-workflow <action> [spec-name] [additional-args]
```

**If no arguments provided**: Display the help menu (see below).

## Actions

### 0. Create (`create <spec-name>`)

**Usage**: `/spec-workflow create my-new-feature`

**Behavior**:
1. Prompt for spec type:
   - Feature spec (new functionality)
   - Technical spec (infrastructure/refactoring)
   - Bug fix spec (complex bug with multiple changes)
2. Ask for brief description (1-2 sentences)
3. Check if spec already exists in `.spec-workflow/specs/`
4. If doesn't exist:
   - Create `.spec-workflow/specs/<spec-name>/` directory (kebab-case name)
   - Use the template from `.spec-workflow/user-templates/` if present, else `.spec-workflow/templates/`
   - Create requirements.md from its template and fill in basic metadata (spec name, date, description)
   - Do not create design.md or tasks.md yet; each is created after the previous document is approved
5. Open requirements.md for user to fill in
6. Remind user of approval workflow: requirements → design → tasks

**Output**:
```
✅ Created spec: my-new-feature

Files created:
  - .spec-workflow/specs/my-new-feature/requirements.md

Next steps:
  1. Fill in requirements.md with user stories and acceptance criteria
  2. Submit for approval: /spec-workflow approve my-new-feature requirements
  3. After approval, draft design.md
  4. Submit design for approval: /spec-workflow approve my-new-feature design
  5. After approval, create tasks.md
  6. Submit tasks for approval: /spec-workflow approve my-new-feature tasks
  7. Start implementation: /spec-workflow execute my-new-feature 1.1
```

### 0.1. Help Menu (no arguments or `help`)

**Usage**: `/spec-workflow` or `/spec-workflow help`

**Behavior**: Display a formatted help menu with:
1. Project context detection results (which files were found)
2. List of available commands with syntax
3. Quick examples
4. List of available specs (from `.spec-workflow/specs/`)

**Output**:
```
╔══════════════════════════════════════════════════════════════╗
║                 SPEC-WORKFLOW COMMANDS                       ║
╚══════════════════════════════════════════════════════════════╝

📋 PROJECT CONTEXT DETECTED:
  ✓ vision.md         - Product roadmap available
  ✓ CLAUDE.md         - Development guidelines active
  ✓ ConnectionGuide.txt - Service documentation tracked

🔧 AVAILABLE COMMANDS:

  /spec-workflow status <spec-name>
    → Check spec progress and next actionable task
    Example: /spec-workflow status content-editing

  /spec-workflow execute <spec-name> <task-id>
    → Execute a specific task with project-aware patterns
    Example: /spec-workflow execute content-editing 1.2

  /spec-workflow log <spec-name> <task-id> "summary"
    → Log a completed implementation
    Example: /spec-workflow log content-editing 1.1 "Created migration"

  /spec-workflow approve <spec-name> <doc-type>
    → Submit document for approval (requirements|design|tasks)
    Example: /spec-workflow approve content-editing requirements

  /spec-workflow guide
    → Display complete workflow process documentation

📁 ACTIVE SPECS:
  • content-editing (3/20 tasks complete - Phase 1)
  • chat-history (Ready for implementation)
  • bulk-operations (Requirements phase)

💡 TIP: Run '/spec-workflow status <spec-name>' to see detailed progress
```

### 1. Guide (`guide`)

**Usage**: `/spec-workflow guide`

**Behavior**:
- Call the `spec-workflow-guide` MCP tool and present its guidance
- Display the complete workflow process
- Show phase transitions (requirements → design → tasks → implementation)
- Explain approval gates and logging requirements
- Provide examples of each command
- Show how project detection works

**Output**: Formatted guide showing the workflow steps with examples.

### 2. Status (`status <spec-name>`)

**Usage**: `/spec-workflow status content-editing`

**Behavior**:
1. Call the `spec-status` MCP tool with `specName`, then read `.spec-workflow/specs/<spec-name>/tasks.md`
2. Count total, completed `[x]`, in-progress `[-]`, pending `[ ]`, and blocked `[~]` tasks
3. Identify current phase based on task progress
4. Check whether the spec is in `archive/` and whether an approval request is pending
5. Display summary with:
   - Spec name and location
   - Phase (Infrastructure, Basic Editing, etc.)
   - Progress (e.g., "3/20 tasks complete")
   - Next actionable task
   - Approval status

**Output**: Formatted status report.

### 3. Approve (`approve <spec-name> <document-type>`)

**Usage**: `/spec-workflow approve content-editing requirements`

**Document Types**: `requirements`, `design`, `tasks`

**Behavior**:
1. Verify the document exists in `.spec-workflow/specs/<spec-name>/<document-type>.md`
2. Read the document to summarize
3. Show document summary to user
4. Call the `approvals` MCP tool with `action: "request"`, `type: "document"`, `category: "spec"`, `categoryName: <spec-name>`, a short `title`, and `filePath` relative to the project root. Never send the document content.
5. Tell the user to review it in the spec-workflow dashboard or VS Code extension, then poll with `action: "status"` and the returned `approvalId`. A user saying "approved" in chat does not count.
6. If the status is `needs-revision`, update the document from the reviewer's comments and request a new approval. Do not proceed.
7. Once approved, call `approvals` with `action: "delete"`. If the delete fails, do not start the next phase.

**Output**: Approval status and next steps.

### 4. Log (`log <spec-name> <task-id> "summary"`)

**Usage**: `/spec-workflow log content-editing 1.1 "Created database migration"`

**Behavior**:
1. Verify task exists in tasks.md
2. Call the `log-implementation` MCP tool with `specName`, `taskId`, `summary`, `filesModified`, `filesCreated`, `statistics` (`linesAdded`, `linesRemoved`), and `artifacts` (API endpoints, components, functions, classes, integrations that were created or changed). The server writes the entry under `.spec-workflow/specs/<spec-name>/Implementation Logs/`.
3. Mention the commit hash in the summary if one exists
4. Only after the log call succeeds, update tasks.md to mark the task complete `[x]`

**Output**: Confirmation with log entry.

### 5. Execute (`execute <spec-name> <task-id>` or `execute <spec-name> <task-range>`)

**Usage**:
- Single task: `/spec-workflow execute content-editing 1.2`
- Task range: `/spec-workflow execute content-editing 1.3-1.6` or `/spec-workflow execute content-editing 1.3 to 1.6`
- Multiple tasks: `/spec-workflow execute content-editing 1.3,1.4,1.5` or `/spec-workflow execute content-editing 1.3 1.4 1.5`

**Behavior**:

**Single Task Mode**:
1. **Detect project context** (check for CLAUDE.md, AGENTS.md, a connection doc)
2. Read `.spec-workflow/specs/<spec-name>/tasks.md`
3. Find task by ID (e.g., "1.2")
4. Extract task details (description, files, role, requirements, restrictions, success criteria)
5. Display task summary and ask for confirmation
6. If confirmed: Execute task (see execution steps below)

**Batch Mode** (range or multiple tasks):
1. **Parse task specification**:
   - Range: `1.3-1.6` or `1.3 to 1.6` → expands to [1.3, 1.4, 1.5, 1.6]
   - List: `1.3,1.4,1.5` or `1.3 1.4 1.5` → [1.3, 1.4, 1.5]
2. **Detect project context** once (reuse for all tasks)
3. **Read tasks.md** and extract all specified tasks
4. **Display batch summary**:
   - Total tasks: X
   - Task list with descriptions
   - Estimated changes (files to create/modify)
5. **Ask for confirmation**: "Execute all X tasks in sequence? [Yes/No/Review]"
   - Yes: Execute all tasks sequentially
   - No: Cancel batch
   - Review: Show detailed plan for each task first
6. **Execute tasks sequentially**:
   - For each task:
     - Show progress: "Task X of Y: [task-id]"
     - Execute task (see execution steps below)
     - If task fails: Ask "Continue with remaining tasks? [Yes/No/Skip this task]"
   - After all tasks: Show summary (completed, failed, skipped)

**Task Execution Steps** (single or batch):
1. **Read project guidance** (CLAUDE.md) for patterns and gotchas
2. Mark the task in progress: change `[ ]` to `[-]` in tasks.md
3. **Search existing implementation logs** in `.spec-workflow/specs/<spec-name>/Implementation Logs/` and **check `_Leverage` files** before implementing (don't recreate existing code)
4. Assume the specified role
5. Implement the task following project patterns
6. **Check if the connection doc needs updating** (new endpoints/services)
7. Verify against success criteria
8. **Run build verification** (unless docs-only or SQL)
9. Create the implementation log entry with the `log-implementation` tool
10. Only after the log succeeds, update tasks.md to mark complete `[x]`
11. Commit changes with project's commit format

**Output**:
- Single task: Task implementation with verification
- Batch: Summary of all tasks with success/failure status

## Special Handling

### Project-Specific Patterns

**CLAUDE.md Detection**:
When CLAUDE.md exists:
1. Read the file before implementing tasks
2. Follow its pre-commit checklist, if any:
   - Code changes: run the project's build command
   - Documentation only (.md files): Skip build
3. Reference any known-issues or gotchas section
4. Follow its git commit conventions
5. Check its critical development rules (for example licensing, AI safety, auth patterns)

**vision.md Detection**:
When vision.md exists:
1. Read product roadmap and business context
2. Verify spec aligns with product vision
3. Reference feature phases (Phase 0: MVP, Phase 1, etc.)
4. Check business requirements and value propositions
5. Ensure new features align with strategic goals

**AGENTS.md Detection**:
When AGENTS.md exists:
1. Read AI-specific guidelines
2. Follow required patterns for AI interactions
3. Reference for testing strategies

**Connection Doc Detection** (e.g. ConnectionGuide.txt):
When creating new endpoints/services:
1. Check if the project keeps a connection doc
2. If yes, prompt: "New API endpoint created. Should I update <connection doc>?"
3. If confirmed, add endpoint documentation to the file

### SQL Migrations
When a task involves SQL:
- Create the migration file following the project's migration naming (often a YYYYMMDDHHmmss timestamp)
- Alert user: "SQL migration created. You need to apply it to the database."
- Do NOT run the build
- Mark as docs-only for commit purposes
- **If CLAUDE.md exists**: Follow migration idempotency patterns

### Build Verification
After code changes (not docs):
- **Check CLAUDE.md or the build config for the build command** (for example `npm run build`)
- Run the build command to verify
- If build fails, report errors and do not proceed
- Only commit after successful build
- **If CLAUDE.md exists**: Follow pre-commit checklist

### Role Assumption
If task includes `_Prompt: Role: <role-description>`:
- Extract the role
- Assume that role's expertise and perspective
- Follow the role's constraints and guidelines
- **Read CLAUDE.md for role-specific patterns** if available

## Batch Task Parsing

Parse task specifications into task ID list:

```typescript
function parseTaskSpec(taskSpec: string): string[] {
  // Range: "1.3-1.6" or "1.3 to 1.6"
  if (taskSpec.includes('-') || taskSpec.includes(' to ')) {
    const [start, end] = taskSpec.split(/[-\s]+to\s+/);
    return expandRange(start, end); // [1.3, 1.4, 1.5, 1.6]
  }

  // List: "1.3,1.4,1.5" or "1.3 1.4 1.5"
  if (taskSpec.includes(',') || taskSpec.includes(' ')) {
    return taskSpec.split(/[,\s]+/).filter(Boolean);
  }

  // Single: "1.3"
  return [taskSpec];
}

function expandRange(start: string, end: string): string[] {
  // Parse "1.3" to "1.6" -> ["1.3", "1.4", "1.5", "1.6"]
  // Handle major.minor format
  const [startMajor, startMinor] = start.split('.').map(Number);
  const [endMajor, endMinor] = end.split('.').map(Number);

  const tasks: string[] = [];

  if (startMajor === endMajor) {
    // Same phase: 1.3 to 1.6
    for (let i = startMinor; i <= endMinor; i++) {
      tasks.push(`${startMajor}.${i}`);
    }
  } else {
    // Cross-phase: Not supported, show error
    throw new Error('Task ranges must be within same phase (e.g., 1.3-1.6, not 1.6-2.2)');
  }

  return tasks;
}
```

## Error Handling

- **Spec not found**: List available specs from `.spec-workflow/specs/`
- **Task not found**: Show task list for that spec
- **Invalid document type**: List valid types (requirements, design, tasks)
- **Build failure**: Report errors, do not commit
- **Batch task failure**: Ask user whether to continue with remaining tasks
- **Invalid range**: Show error and suggest valid format (e.g., "1.3-1.6" or "1.3 to 1.6")

## Integration with Other Tools

This skill should:
- Use Read/Write/Edit tools for file operations
- Use Bash for git operations and build verification
- **Auto-detect and follow CLAUDE.md guidelines** if present
- **Auto-detect and follow AGENTS.md patterns** if present
- **Prompt to update the connection doc** when creating endpoints
- Respect pre-commit checklist requirements
- Adapt commit messages to project's format

## Project Detection Algorithm

On skill invocation, run this detection:

```typescript
// Pseudo-code for detection
const projectContext = {
  visionMd: fileExists('vision.md') || fileExists('VISION.md'),
  claudeMd: fileExists('CLAUDE.md') || fileExists('claude.md'),
  agentsMd: fileExists('AGENTS.md') || fileExists('agents.md'),
  connectionGuide: fileExists('ConnectionGuide.txt') || fileExists('connections.txt'), // example names
  buildCommand: detectBuildCommand(), // from CLAUDE.md, package.json, Makefile, etc.
  commitFormat: 'conventional', // default
};

if (projectContext.visionMd) {
  // Read vision.md for:
  // - Product roadmap and phases
  // - Business requirements
  // - Feature alignment
  // - Strategic goals
  // - Value propositions
}

if (projectContext.claudeMd) {
  // Read CLAUDE.md for:
  // - Pre-commit checklist
  // - Build command
  // - Commit format
  // - Critical rules
  // - Common gotchas
}

if (projectContext.agentsMd) {
  // Read AGENTS.md for:
  // - AI interaction patterns
  // - Required reading sections
}
```

**Cache detection results** for the session to avoid repeated file reads.

## Example Workflows

### Starting a New Spec
```bash
# User creates spec with /spec-workflow create my-spec, or manually
# Submit requirements for approval
/spec-workflow approve my-spec requirements

# After approval, draft design
# Submit design for approval
/spec-workflow approve my-spec design

# After approval, create tasks
# Submit tasks for approval
/spec-workflow approve my-spec tasks
```

### Implementing Tasks
```bash
# Check what's next
/spec-workflow status my-spec

# Execute next task
/spec-workflow execute my-spec 1.1

# After implementation, status updates automatically
# Continue with next task
/spec-workflow execute my-spec 1.2
```

### Checking Progress
```bash
# Quick status check
/spec-workflow status my-spec

# See what's left to do
```

## Tasks.md Authoring Rules

### Task Format Requirements (Dashboard Visibility)

**Every task must have detail lines under it to appear in the dashboard as actionable.** The server treats a single-line task (checkbox + title only) as a header: it is counted in the total but does not render as an actionable item.

Status markers: `[ ]` pending, `[-]` in progress, `[x]` completed, `[~]` blocked (optionally with a `- _Blocked: reason_` sub-bullet).

A valid task follows the server's tasks template:
```markdown
- [ ] N.M Task title
  - File: path/to/file.ts
  - [Description of what to implement, with code snippets if helpful]
  - Purpose: [why this task exists]
  - _Leverage: path/to/existing-util.ts_
  - _Requirements: 1.1_
  - _Prompt: Spec <spec-name>. Read the workflow guide (spec-workflow-guide) before writing code. Role: [role] | Task: [instructions] | Restrictions: [constraints] | Success: [criteria]. Set this task to [-] before you begin; when it is finished, record it with log-implementation and set it to [x]._
```

**Task numbering**: Use purely numeric IDs (e.g., `7`, `7.1`, `8.2`). Alphanumeric IDs like `7b.1` are invalid — renumber phases sequentially instead.

**Completion/verification phases**: Do NOT write them as single-line checklist items. Convert to proper tasks with `_Prompt:` sections. Example: instead of `- [ ] 10.1 npm run build passes`, write a full verification task with run instructions, success criteria, and a prompt.

**When authoring tasks.md**, validate before committing by running:
```bash
/spec-workflow status <spec-name>
```
Check that the task total reported by `spec-status` matches your expected count, and that the number of header (single-line) tasks is what you intended. Expand any single-line items that should be actionable.

## Notes

- Always update tasks.md when marking tasks complete
- Create implementation logs with `log-implementation` for the audit trail
- Commit after each significant task completion
- Follow the project's git commit conventions
