# Review Older Issues

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Revalidates a bounded batch of open GitHub issues against current code, pull requests and related closed issues. Each issue gets one verdict: still valid, shipped, superseded or duplicate, needs rescoping, unwarranted, or unverified. The skill closes or rewrites issues only when the evidence supports it. It detects the repository's own labels, issue templates and branch conventions instead of assuming them, and needs the GitHub CLI (`gh`). Use on `/review-older-issues` or when asked to "review issues 1-100" or "clean up stale issues".

## Install

See [Install](../../../../README.md#install) in the collection README. Copy this complete folder as `review-older-issues/`; keep every file in it together.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
