# Spec Approval Workflow

## Quick Reference

```bash
# Create → Requirements → Design → Tasks → Implementation
/spec-workflow create my-feature              # Create new spec
/spec-workflow approve my-feature requirements # Approve requirements
/spec-workflow approve my-feature design      # Approve design
/spec-workflow approve my-feature tasks       # Approve tasks
/spec-workflow execute my-feature 1.1-1.6     # Execute implementation
```

## Complete Workflow

### 1. Create Spec
```bash
/spec-workflow create my-feature
```
Creates the spec directory and requirements.md from the template. design.md and tasks.md are created in order, each after the previous document is approved.

### 2. Requirements → Approve
Fill in requirements.md (user stories, acceptance criteria), then:
```bash
/spec-workflow approve my-feature requirements
```

### 3. Design → Approve
Fill in design.md (architecture, leverage analysis), then:
```bash
/spec-workflow approve my-feature design
```

### 4. Tasks → Approve
Fill in tasks.md (implementation breakdown), then:
```bash
/spec-workflow approve my-feature tasks
```

### 5. Implementation
```bash
/spec-workflow execute my-feature 1.1      # Single task
/spec-workflow execute my-feature 1.1-1.6  # Batch execution
```

## How approval works

`approve` calls the spec-workflow MCP server's `approvals` tool with `action: "request"` and the document's file path (never its content). The reviewer approves, rejects, or asks for revision in the server's dashboard or VS Code extension. Poll with `action: "status"`. On `needs-revision`, update the document and request a new approval. Once approved, clean up with `action: "delete"` before starting the next phase. A user saying "approved" in chat is not an approval.

## Approval Criteria

**Requirements**: User stories, acceptance criteria, vision alignment
**Design**: Code reuse analysis, no duplication, follows patterns
**Tasks**: Clear descriptions, file paths, role prompts, success criteria

See `instructions.md` for detailed approval gates and `examples.md` for examples.
