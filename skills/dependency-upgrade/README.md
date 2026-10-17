# Dependency Upgrade

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE) [![Version](https://img.shields.io/badge/version-0.1.0-informational.svg)](CHANGELOG.md)

Safe batch dependency upgrades across projects — inventory outdated packages (npm outdated / uv lock --upgrade), group by risk (patch/minor/major), upgrade in waves with tsc/test/Playwright gates, read changelogs for majors, run /exposure-scan for supply-chain checks, and land one PR per wave. Use when asked to "upgrade dependencies," "bump packages," "clear npm outdated," or on a periodic maintenance pass.

## Install

Copy this complete folder to `~/.claude/skills/dependency-upgrade/` for Claude Code CLI and local Claude Code desktop sessions, or to `~/.agents/skills/dependency-upgrade/` for personal Codex use. For repository-only use, copy to `.claude/skills/dependency-upgrade/` or `.agents/skills/dependency-upgrade/` respectively. Supporting files in this folder may be required. See the [collection README](../../README.md) for current platform notes.

## Contents

- `SKILL.md` — skill instructions and metadata.
- `VERSION` and `CHANGELOG.md` — package version history.
