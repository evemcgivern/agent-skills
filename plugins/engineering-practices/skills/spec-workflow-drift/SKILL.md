---
name: spec-workflow-drift
description: "Detect drift between spec-workflow specs (.spec-workflow/) and the code: map which source files each spec covers, list files no spec documents, flag stale specs, and write a coverage report. Companion to the spec-workflow MCP server. Use on /spec-workflow-drift and on phrases like 'check spec drift', 'which files aren't covered by a spec', 'spec coverage report', 'are the specs still accurate'."
---

# Spec-Workflow Drift Detection

> **Companion to the spec-workflow MCP server.** This skill reads the `.spec-workflow/`
> directory created by the open-source [spec-workflow MCP server](https://github.com/Pimzino/spec-workflow-mcp)
> by Pimzino. Install and use that server to create the specs this skill analyzes. The drift
> analysis itself only reads files and does not call the server's tools; the related
> `spec-workflow` skill does. This skill contains none of the server's code. The server is a
> separate project under its own license (GPL-3.0 at the time of writing); this skill is MIT-licensed.

Comprehensive drift detection and coverage mapping for any project that uses spec-workflow.

**When to run:** After implementation phases, during code reviews, or when investigating spec-code alignment

**Output** (default location; use the project's own reports folder if it has one):
- Full report: `docs/spec-drift-reports/spec-drift-report.md`
- Single spec: `docs/spec-drift-reports/spec-drift-report-<spec-name>.md` (e.g. `spec-drift-report-cascading-defaults.md`)

---

## Help (`--help`)

When invoked with `--help`, display this reference and stop (do not run any analysis):

```
spec-workflow-drift - Drift detection & coverage mapping for spec-workflow

USAGE:
  /spec-workflow-drift [OPTIONS]

OPTIONS:
  --help                     Show this help message
  --quick                    Summary stats only (no detailed file lists)
  --spec=<name>              Focus on a single spec (e.g. --spec=checkout-flow)
  --category=<cat>           Filter by file category
                             Categories: api, services, components, types, database,
                                         ai, auth, tests, config, docs
  --since=<YYYY-MM-DD>       Only show drift in files modified after this date
  --format=<fmt>             Output format: markdown (default), json, csv

EXAMPLES:
  /spec-workflow-drift                          Full report → docs/spec-drift-reports/spec-drift-report.md
  /spec-workflow-drift --quick                  One-page summary with coverage heat map
  /spec-workflow-drift --spec=checkout-flow     Single spec → docs/spec-drift-reports/spec-drift-report-checkout-flow.md
  /spec-workflow-drift --category=api           Only API route coverage
  /spec-workflow-drift --since=2026-02-01       Drift in recently modified files
  /spec-workflow-drift --format=json            Machine-readable output

REPORT SECTIONS:
  1. Coverage by Spec        Spec → files mapping with status
  2. Drift Detected          Files not documented in any spec
  3. File → Spec Mapping     Reverse index with risk levels (🟢 🟡 🔴)
  4. Coverage Statistics      Per-category stats + heat map
  5. Staleness Report         Specs with no recent implementation activity
  6. Action Items             Prioritized recommendations

CRITICAL FILE MONITORING:
  Files found at run time that enforce legal/licensing rules, AI safety
  (guardrails, sanitization), or authentication are always flagged if
  uncovered by a spec. See "Critical-File Drift" below.

OUTPUT FILES:
  Full report:   docs/spec-drift-reports/spec-drift-report.md
  Single spec:   docs/spec-drift-reports/spec-drift-report-<spec-name>.md
  This prevents overwriting when running for different specs.

INTEGRATION:
  Works with .spec-workflow/specs/ directory structure.
  Reads requirements.md, design.md, tasks.md, and the "Implementation Logs/" folder.

SEE ALSO:
  /spec-workflow guide       Workflow process documentation
  /spec-workflow status      Check spec progress
  /spec-workflow log         Record completed implementations
```

---

## What This Does

Analyzes the relationship between specifications in `.spec-workflow/specs/` and actual implementation:

1. **Spec → Files Coverage**: Which code files each spec covers
2. **Drift Detection**: Files that exist but aren't documented in any spec
3. **Reverse Index**: Which spec(s) document each file
4. **Coverage Statistics**: Percentages by category (API, services, components, etc.)
5. **Risk Assessment**: Shared files referenced by multiple specs
6. **Staleness Detection**: Specs with no recent implementation activity

---

## Usage

```bash
# Generate full drift report
/spec-workflow-drift

# Quick drift check (summary only)
/spec-workflow-drift --quick

# Focus on specific spec
/spec-workflow-drift --spec=<spec-name>

# Check specific category
/spec-workflow-drift --category=api
/spec-workflow-drift --category=components
```

---

## Process

### Step 1: Discover Active AND Archived Specifications

**IMPORTANT:** Before reporting a spec as "not found" or "not started", always check
`.spec-workflow/archive/specs/` for previously completed specs. Archived specs represent
fully implemented features — their file references are still valid coverage and should
be included in drift calculations. Failing to check the archive leads to false "drift"
on files that are actually covered by completed specs.

```bash
# Find all active specs in spec-workflow
find .spec-workflow/specs -mindepth 1 -maxdepth 1 -type d | sort

# ALSO check archived (completed) specs
find .spec-workflow/archive/specs -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort

# Count them
ACTIVE_COUNT=$(find .spec-workflow/specs -mindepth 1 -maxdepth 1 -type d | wc -l)
ARCHIVED_COUNT=$(find .spec-workflow/archive/specs -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
echo "Found $ACTIVE_COUNT active + $ARCHIVED_COUNT archived specifications"
```

When running `--spec=<name>`:
1. First check `.spec-workflow/specs/<name>/`
2. If not found, check `.spec-workflow/archive/specs/<name>/`
3. If found in archive, note in report: "Status: Archived (fully implemented)"
4. If not found in either location, report as "Spec not found"

### Step 2: Extract File References from Each Spec

For each spec, read these files and extract file paths:
- `requirements.md` - User stories may mention component files
- `design.md` - Architecture section lists implementation files
- `tasks.md` - Tasks reference specific files to modify/create
- `Implementation Logs/*.md` - One entry per logged task, written by the server's
  `log-implementation` tool; records files modified/created and artifacts.
  (Older projects may have a single `implementation-log.md` instead; read it if present.)

**Look for patterns:**
```markdown
# In design.md "Files" or "Implementation" sections:
- `src/app/api/foo/route.ts`
- `src/lib/services/bar-service.ts`
- `src/components/ui/baz.tsx`

# In tasks.md:
- [ ] 1.1: Create `src/lib/db/migrations/xxx.sql`
- [x] 1.2: Update `src/types/database.ts`

# In an Implementation Logs/ entry (exact layout depends on the server version):
Task 1.3, logged 2026-01-15
Files modified: src/services/foo.ts
Files created: src/api/bar/route.ts
```

### Step 3: Categorize Files by Project Structure

Derive the category → glob mapping from the live repo at run time (`ls src/`,
the framework's routing conventions, `package.json`) — do not assume paths from
a previous run. Categories to map: **API Routes**, **Services**,
**Components**, **Types**, **Database**, **AI/Guardrails**, **Auth**,
**Tests**, **Config**, **Docs**.

### Step 4: Generate Coverage Report

For each spec, create a section showing status, file count, and files by category.

(Output shape: see Complete Output Template, section "📋 Coverage by Spec".)

### Step 5: Detect Drift (Uncovered Files)

Use the project's real source roots and languages (detected in Step 3); the
TypeScript example below is only one case.

```bash
# Get all implementation files
find src -type f \( -name "*.ts" -o -name "*.tsx" \) | sort > /tmp/all-files.txt

# Compare against spec-referenced files
# Files not in any spec = DRIFT
```

**Report format:**

(Output shape: see Complete Output Template, section "🚨 Drift Detected".)

### Step 6: Reverse Index (File → Specs)

(Output shape: see Complete Output Template, section "📊 File → Spec Mapping".)

### Step 7: Coverage Statistics

(Output shape: see Complete Output Template, section "📈 Coverage Statistics".)

### Step 8: Staleness Detection

Check implementation logs for recent activity:

(Output shape: see Complete Output Template, section "⏰ Staleness Report".)

---

## Output File Naming

Determine the output file path based on arguments:

```
If --spec=<name> is provided:
  Output file: docs/spec-drift-reports/spec-drift-report-<name>.md
  Example: --spec=cascading-defaults → docs/spec-drift-reports/spec-drift-report-cascading-defaults.md

If no --spec (full report):
  Output file: docs/spec-drift-reports/spec-drift-report.md
```

This prevents single-spec reports from overwriting each other or the full report.

## Complete Output Template

```markdown
# Spec-Workflow Drift Report

**Generated:** 2026-02-09T14:30:00Z
**Project:** <project name>
**Total Specs:** 12 active
**Total Files:** 194
**Coverage:** 92% (179/194 files)
**Drift Files:** 15

---

## 📋 Coverage by Spec

[For each spec: status, file count, files by category]

---

## 🚨 Drift Detected

[Uncovered files by category with recommendations]

---

## 📊 File → Spec Mapping

[Reverse index table with risk assessment]

---

## 📈 Coverage Statistics

[Stats table and heat map]

---

## ⏰ Staleness Report

[Specs with no recent activity]

---

## 🎯 Action Items

1. **Immediate:**
   - Remove 2 deprecated files
   - Archive 1 stale spec

2. **This Sprint:**
   - Create utility spec for 3 infrastructure files
   - Document 2 dev tools

3. **Monitor:**
   - 2 high-risk shared files (4+ specs depend on them)
   - 1 aging spec (no activity in 56 days)

---

## ✅ Success Criteria

- [x] Coverage > 90%
- [x] All API routes documented
- [ ] All drift files resolved (15 remaining)
- [x] Database migrations 100% covered
```

---

## Integration with Spec-Workflow

### After Task Execution

After `/spec-workflow execute` completes tasks, suggest drift check:

```markdown
✅ Task 1.5 completed

Would you like me to run a drift check to ensure spec alignment?
/spec-workflow-drift --quick
```

### Before Spec Approval

Before approving design or tasks, check for drift:

```markdown
User: /spec-workflow approve checkout-flow design

Agent: "Let me check for any drift before approval..."

[Runs quick drift check]

✅ No drift detected. Proceeding with approval...
```

### After Major Implementation

When the implementation logs show significant work:

```markdown
Agent: "I notice we've completed 8 tasks. Let me generate a drift report to ensure everything is documented..."

[Runs full drift report]

📊 Drift Report: 95% coverage, 3 minor gaps identified
```

---

## Command Options

### Quick Mode
```bash
/spec-workflow-drift --quick
```
Output: Summary stats only, no detailed file lists

### Spec-Specific
```bash
/spec-workflow-drift --spec=checkout-flow
```
Output: Coverage for single spec only, saved to `docs/spec-drift-reports/spec-drift-report-checkout-flow.md`

### Category Focus
```bash
/spec-workflow-drift --category=api
/spec-workflow-drift --category=services
```
Output: Coverage for specific file category

### Diff Mode
```bash
/spec-workflow-drift --since=2026-02-01
```
Output: Only show drift in files modified since date

### Export Formats
```bash
/spec-workflow-drift --format=markdown  # Default
/spec-workflow-drift --format=json      # Machine-readable
/spec-workflow-drift --format=csv       # Spreadsheet
```

---

## Error Handling

**No specs found:**
```
⚠️ No specifications found in .spec-workflow/specs/
Cannot generate drift report without specs.

Create a spec first: /spec-workflow guide
```

**No implementation logs:**
```
⚠️ Specs have no implementation logs (no "Implementation Logs/" entries)
Cannot detect staleness without implementation logs.

Log implementations as you complete tasks: /spec-workflow log
```

**Very low coverage (< 70%):**
```
🚨 CRITICAL: Coverage is only 45%

149 files are not documented in any spec!

This indicates:
- Many features implemented without specs
- Specs may be outdated
- Consider running full spec audit

Next steps:
1. Run /spec-workflow status to check all specs
2. Create missing specs for undocumented features
3. Archive completed specs that are no longer active
```

---

## Critical-File Drift

Derive the critical set at run time — grep the live repo for guardrail,
sanitization, content-validation, rate-limiting, and auth/middleware modules
(e.g. `grep -ril 'guardrail\|sanitiz\|blocklist\|rate.limit' src/lib` plus the
auth middleware and DB client entry points). Always check that every file in
that set is spec-covered.

### Flag if Critical Files Show Drift

```
🚨 CRITICAL DRIFT DETECTED

The following critical files are not documented in any spec:

- <path> (SECURITY: guardrail | sanitization | rate limiting | auth)

These files MUST be documented before any changes are made!
```

---

## Success Criteria

After running drift detection:

✅ Drift report generated at `docs/spec-drift-reports/spec-drift-report.md` (or `docs/spec-drift-reports/spec-drift-report-<name>.md` for single-spec runs)
✅ Coverage statistics by category
✅ Reverse index (file → spec mapping)
✅ Drift files identified with recommendations
✅ Staleness report for inactive specs
✅ Risk assessment for shared files
✅ Action items prioritized by impact
✅ Coverage > 85% (target: 90%+)
✅ Zero drift in critical files (AI, auth, guardrails)

---

## Example Workflow

### 1. After Completing Features

```bash
# Complete a batch of tasks
/spec-workflow execute checkout-flow 1.5-1.8

# Check for drift
/spec-workflow-drift

# Review report
cat docs/spec-drift-reports/spec-drift-report.md

# Clean up any drift
rm src/components/temp/TestComponent.tsx
git add src/components/temp/TestComponent.tsx   # stage by name, never git add -A
git commit -m "chore: clean up drift files identified in drift report"
```

### 2. Before PR/Code Review

```bash
# Quick drift check
/spec-workflow-drift --quick

# If drift detected, get the machine-readable report and read its drift_files list
/spec-workflow-drift --format=json

# Clean up and document
# Then proceed with PR
```

### 3. Weekly/Sprint Cleanup

```bash
# Full drift report
/spec-workflow-drift

# Archive stale specs
mkdir -p .spec-workflow/archive/specs
mv .spec-workflow/specs/legacy-feature .spec-workflow/archive/specs/

# Create specs for undocumented utilities
/spec-workflow guide
# Follow process to document infrastructure code

# Verify
/spec-workflow-drift --quick
```

---

## Technical Implementation

### File Path Extraction

Parse markdown files for these patterns:

```markdown
# Backtick-wrapped paths
`src/app/api/foo/route.ts`

# Bold file references
**File:** src/services/bar.ts

# List items
- Created `src/components/Foo.tsx`
- Updated `src/types/database.ts`

# Code blocks with file comments
```typescript
// File: src/lib/utils.ts
export function helper() {}
```

# Implementation logs
Files: src/a.ts, src/b.tsx, src/c.sql
```

### Coverage Calculation

```typescript
// Calculate coverage percentage
const allFiles = getAllSourceFiles(['src/**/*.ts', 'src/**/*.tsx']);
const specFiles = extractFileReferencesFromAllSpecs();
const coveredFiles = allFiles.filter(f => specFiles.includes(f));
const coverage = (coveredFiles.length / allFiles.length) * 100;

// By category
const apiFiles = allFiles.filter(f => f.includes('/api/'));
const coveredApiFiles = coveredFiles.filter(f => f.includes('/api/'));
const apiCoverage = (coveredApiFiles.length / apiFiles.length) * 100;
```

### Staleness Detection

```typescript
// Parse Implementation Logs/ entries (or a legacy implementation-log.md) for last activity
const logs = parseImplementationLog(specPath);
const lastActivity = logs.sort((a, b) => b.date - a.date)[0];
const daysAgo = Math.floor((Date.now() - lastActivity.date) / (1000 * 60 * 60 * 24));

if (daysAgo > 90) return 'STALE';
if (daysAgo > 30) return 'AGING';
return 'ACTIVE';
```

---

**This drift detection tool keeps specs and implementation aligned, prevents documentation rot, and maintains high spec coverage!**
