# Changelog: repo-activity-summary

## 0.2.0 — 2026-10-17

- Fix the check-status jq so running checks (empty `conclusion`) and commit statuses (`state`) are reported.
- Add read-only `allowed-tools` for the gh and git commands.
- Add pass criteria and state truncation at the `--limit`.

## 0.1.0 — 2026-10-17

- Include the reviewed public version of `repo-activity-summary`.
- Generalize personal and project-specific references.
