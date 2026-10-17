---
name: spec-workflow
description: "Drive spec-driven development through the spec-workflow MCP server: create specs, request approvals, check status, execute tasks from tasks.md and log implementations. Requires the open-source spec-workflow MCP server. Use on /spec-workflow and on phrases like 'create a spec for', 'what's the status of the spec', 'execute task 1.2 of the spec', 'run tasks 1.3-1.6', 'log this task as implemented'."
---

# Spec-Workflow Management

> **Requires the spec-workflow MCP server.** This skill is a companion to the open-source
> [spec-workflow MCP server](https://github.com/Pimzino/spec-workflow-mcp) by Pimzino. Install
> and configure that server first; without it, approvals, status and implementation logging
> do not work. This skill only calls the server's tools and reads the `.spec-workflow/` files
> it manages. It contains none of the server's code. The server is a separate project under
> its own license (GPL-3.0 at the time of writing); this skill is MIT-licensed.

Workflow management for specification development in any project that uses the spec-workflow MCP server.

## Capabilities

- **Workflow Guidance**: Get step-by-step workflow instructions
- **Spec Status**: Check current spec status and progress
- **Approvals**: Request and track approvals for requirements, design, and tasks
- **Implementation Logging**: Record completed implementations with context
- **Task Execution**: Execute individual spec tasks following the spec-workflow pattern
- **Project-Aware**: Auto-detects and adapts to project guidance files (vision.md, CLAUDE.md, AGENTS.md, API or service connection docs)

## When to Use This Skill

Use this skill when you need to:
- Navigate the spec-workflow process (requirements → design → tasks → implementation)
- Check the status of a specification
- Submit documents for approval
- Log completed implementations
- Execute tasks from a spec's tasks.md file

## Usage Examples

```bash
# Get workflow guidance
/spec-workflow guide

# Check spec status
/spec-workflow status <spec-name>

# Submit for approval
/spec-workflow approve <spec-name> <document-type>
# Example: /spec-workflow approve content-editing requirements

# Log an implementation
/spec-workflow log <spec-name> <task-id> "Implementation summary"
# Example: /spec-workflow log content-editing 1.1 "Created database migration"

# Execute a specific task
/spec-workflow execute <spec-name> <task-id>
# Example: /spec-workflow execute content-editing 1.2

# Execute a batch of tasks (range or list)
/spec-workflow execute <spec-name> <task-range>
# Examples:
#   Range: /spec-workflow execute content-editing 1.3-1.6
#   Range: /spec-workflow execute content-editing 1.3 to 1.6
#   List: /spec-workflow execute content-editing 1.3,1.4,1.5
#   List: /spec-workflow execute content-editing 1.3 1.4 1.5
```

## Spec-Workflow Process

The standard workflow follows these phases:

1. **Requirements**: Define user stories and acceptance criteria
2. **Design**: Create technical architecture and implementation approach
3. **Tasks**: Break down into concrete implementation tasks
4. **Implementation**: Execute tasks, log progress, commit changes
5. **Archive**: Move completed specs to archive

## Integration with MCP Tools

This skill wraps the spec-workflow MCP server tools:
- `spec-workflow-guide`: Get workflow documentation
- `steering-guide`: Get guidance for optional steering documents (product, tech, structure)
- `spec-status`: Check spec progress
- `approvals`: Request, check, and clean up approvals (`action`: `request`, `status`, `delete`)
- `log-implementation`: Record completed work, including structured artifacts

Approval happens in the server's dashboard or VS Code extension. A user saying "approved" in chat does not count; check the `approvals` status instead.

## Best Practices

1. **Always check workflow guide first** if unfamiliar with the process
2. **Get approvals** before moving to next phase (requirements → design → tasks)
3. **Log implementations immediately** after completing tasks, before marking them `[x]`
4. **Update tasks.md** to mark tasks in progress `[-]` and complete `[x]`
5. **Commit after logging** to maintain audit trail

## Directory Structure

```
.spec-workflow/
├── specs/               # Active specifications
│   └── <spec-name>/
│       ├── requirements.md
│       ├── design.md
│       ├── tasks.md
│       └── Implementation Logs/   # Written by log-implementation
├── approvals/           # Approval requests managed by the server
├── archive/             # Completed specs
├── templates/           # Document templates
├── user-templates/      # Optional custom templates
└── steering/            # Steering documents
```

## Task Execution Pattern

When executing a task from tasks.md:

1. **Read the task** to understand requirements and role
2. **Mark it in progress**: change `[ ]` to `[-]` in tasks.md
3. **Assume the specified role** if one is provided
4. **Implement the task** following the restrictions
5. **Verify success** against success criteria
6. **Log implementation** with the `log-implementation` tool (file paths, summary, artifacts)
7. **Update tasks.md** to mark complete `[x]`, only after the log succeeds
8. **Commit changes** with descriptive message

## Notes

- Tasks often include a `_Prompt:` section with role, restrictions, and success criteria
- Database migrations should be flagged to the user for manual application
- Build verification is required unless changes are docs-only
- **Auto-detects project guidance**: vision.md, CLAUDE.md, AGENTS.md, and any API/service connection doc the project keeps
- Follow project-specific guidelines when detected
- Verifies feature alignment with product vision (if vision.md exists)
- Offers to update the project's API/service connection doc when creating new API endpoints

See `instructions.md` for full command behavior, `approval-workflow.md`, `batch-execution.md`, `examples.md`, and `help-template.md`.
