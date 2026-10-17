# Spec-Workflow Help Template

When `/spec-workflow` is invoked without arguments, display this formatted help menu:

```
╔══════════════════════════════════════════════════════════════╗
║                 SPEC-WORKFLOW COMMANDS                       ║
╚══════════════════════════════════════════════════════════════╝

📋 PROJECT CONTEXT DETECTED:
{{PROJECT_DETECTION_RESULTS}}

🔧 AVAILABLE COMMANDS:

  /spec-workflow create <spec-name>
    → Create a new spec with templates
    📖 Example: /spec-workflow create my-feature

  /spec-workflow status <spec-name>
    → Check spec progress and next actionable task
    📖 Example: /spec-workflow status content-editing

  /spec-workflow execute <spec-name> <task-id-or-range>
    → Execute task(s) with project-aware patterns
    📖 Single: /spec-workflow execute content-editing 1.2
    📖 Batch: /spec-workflow execute content-editing 1.3-1.6

  /spec-workflow log <spec-name> <task-id> "summary"
    → Log a completed implementation manually
    📖 Example: /spec-workflow log content-editing 1.1 "Created migration"

  /spec-workflow approve <spec-name> <doc-type>
    → Submit document for approval (requirements|design|tasks)
    📖 Example: /spec-workflow approve content-editing requirements

  /spec-workflow guide
    → Display complete workflow process documentation

  /spec-workflow help
    → Show this help menu

📁 ACTIVE SPECS:
{{SPEC_LIST}}

💡 QUICK START:
  New spec: /spec-workflow create my-feature
  Check status: /spec-workflow status content-editing
  Execute single: /spec-workflow execute content-editing 1.2
  Execute batch: /spec-workflow execute content-editing 1.3-1.6
  Get help: /spec-workflow guide

📚 DOCUMENTATION:
  • approval-workflow.md - Spec creation and approval process
  • batch-execution.md - Batch task execution guide
  • examples.md - Real-world usage examples

🔗 WORKFLOW PHASES:
  Create → Requirements → Design → Tasks → Implementation → Archive
             ↓ Approve    ↓ Approve  ↓ Approve
```

## Template Variables

Replace these placeholders when displaying:

### {{PROJECT_DETECTION_RESULTS}}
Show detected project files with status:
```
  ✓ vision.md           - Product roadmap available
  ✓ CLAUDE.md           - Development guidelines active
  ✓ AGENTS.md           - AI patterns configured
  ✓ ConnectionGuide.txt - Service documentation tracked (example name)
```

Or if none found:
```
  ℹ  No project-specific files detected
  ℹ  Using default workflow patterns
```

### {{SPEC_LIST}}
List specs from `.spec-workflow/specs/` with status:
```
  • content-editing     [Phase 1: Infrastructure] 3/20 tasks ▓▓▓░░░░░░░ 15%
  • chat-history        [Ready] 0/15 tasks ░░░░░░░░░░ 0%
  • bulk-operations     [Requirements phase] Planning
```

Format:
- Active specs: Show phase, task count, progress bar
- Archived specs: Don't list (only active specs)
- Empty: "  No active specs found. Create one in .spec-workflow/specs/"

## Dynamic Elements

Calculate and display:
1. **Project detection**: Check for vision.md, CLAUDE.md, AGENTS.md, and a connection doc such as ConnectionGuide.txt
2. **Spec list**: Read `.spec-workflow/specs/` directory
3. **Task progress**: Parse tasks.md for each spec, count [x] vs [ ], [-], [~]
4. **Current phase**: Infer from task progress (tasks 1.x = Phase 1, etc.)

## Color/Formatting

Use markdown formatting:
- ✓ Green checkmark for detected files
- ℹ Info icon for missing files
- • Bullet for spec list
- → Arrow for command descriptions
- 📖 Book icon for examples
- 💡 Lightbulb for tips
- ▓ Filled blocks for progress
- ░ Empty blocks for remaining

## Example Output

```
╔══════════════════════════════════════════════════════════════╗
║                 SPEC-WORKFLOW COMMANDS                       ║
╚══════════════════════════════════════════════════════════════╝

📋 PROJECT CONTEXT DETECTED:
  ✓ vision.md           - Product roadmap available
  ✓ CLAUDE.md           - Development guidelines active
  ✓ ConnectionGuide.txt - Service documentation tracked (example name)
  ℹ  AGENTS.md          - Not found (using defaults)

🔧 AVAILABLE COMMANDS:

  /spec-workflow create <spec-name>
    → Create a new spec with templates
    📖 Example: /spec-workflow create my-feature

  /spec-workflow status <spec-name>
    → Check spec progress and next actionable task
    📖 Example: /spec-workflow status content-editing

  /spec-workflow execute <spec-name> <task-id-or-range>
    → Execute task(s) with project-aware patterns
    📖 Single: /spec-workflow execute content-editing 1.2
    📖 Batch: /spec-workflow execute content-editing 1.3-1.6

  /spec-workflow log <spec-name> <task-id> "summary"
    → Log a completed implementation manually
    📖 Example: /spec-workflow log content-editing 1.1 "Created migration"

  /spec-workflow approve <spec-name> <doc-type>
    → Submit document for approval (requirements|design|tasks)
    📖 Example: /spec-workflow approve content-editing requirements

  /spec-workflow guide
    → Display complete workflow process documentation

📁 ACTIVE SPECS:
  • content-editing     [Phase 1: Infrastructure] 2/6 tasks ▓▓░░░░░░░░ 33%
  • chat-history        [Phase 2: UI] 8/12 tasks ▓▓▓▓▓▓▓░░░ 67%
  • bulk-operations     [Requirements phase] Planning

💡 QUICK START:
  New spec: /spec-workflow create my-feature
  Check status: /spec-workflow status content-editing
  Execute single: /spec-workflow execute content-editing 1.2
  Execute batch: /spec-workflow execute content-editing 1.3-1.6
  Get help: /spec-workflow guide

📚 DOCUMENTATION:
  • approval-workflow.md - Spec creation and approval process
  • batch-execution.md - Batch task execution guide
  • examples.md - Real-world usage examples

🔗 WORKFLOW PHASES:
  Create → Requirements → Design → Tasks → Implementation → Archive
             ↓ Approve    ↓ Approve  ↓ Approve
```
