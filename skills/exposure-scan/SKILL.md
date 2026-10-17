---
name: exposure-scan
description: Scan installed packages against bumblebee threat-intelligence exposure catalogs to detect known-compromised dependency releases (supply-chain campaigns like shai-hulud, node-ipc, gemstuffer). Use when checking for compromised packages, running a supply-chain or dependency security scan, auditing the machine after a reported npm/PyPI/Go/gem/extension compromise, or refreshing threat-intel catalogs.
---

# Exposure Scan

Machine-wide supply-chain check. Runs [bumblebee](https://github.com/perplexityai/bumblebee) to inventory every installed package (npm, Go, PyPI, RubyGems, MCP servers, editor + browser extensions) and match them against maintained **exposure catalogs** of known-compromised `(ecosystem, name, version)` releases. Emits findings only when a real match exists.

This is a personal/machine-level tool — it is global on purpose, not tied to any project.

## When to use

- "Am I running any compromised packages?" / "scan for the shai-hulud worm" / supply-chain audit
- After news of an npm/PyPI/Go/gem or VS Code extension compromise — refresh catalogs, then scan
- Periodic hygiene check (the underlying scan is ~13s)

## Prerequisites (one-time)

`bumblebee` must be installed and on PATH:

```bash
go install github.com/perplexityai/bumblebee/cmd/bumblebee@latest
# add to ~/.zshrc so it persists:  export PATH="$HOME/go/bin:$PATH"
```

The script auto-adds `$(go env GOPATH)/bin` to PATH for its own run and prints these instructions if the binary is missing.

## How to run

The script lives next to this file. Invoke it via its absolute path:

```bash
bash ~/.claude/skills/exposure-scan/scan.sh <command>
```

| Command | What it does | Speed |
|---|---|---|
| `quick` (default) | Baseline package roots (the standard global/user dirs) | ~13s |
| `deep` | Full `$HOME` walk — catches packages outside standard roots | minutes |
| `project <path>` | Scan one project/dir tree | seconds–minutes |
| `refresh` | Pull the latest catalogs from GitHub `main` into `~/.config/bumblebee/threat_intel` | seconds |
| `catalogs` | Show which catalogs are in use + entry counts | instant |

**Recommended flow:**
1. `bash ~/.claude/skills/exposure-scan/scan.sh refresh` — get current threat intel (do this first; intel updates faster than the binary).
2. `bash ~/.claude/skills/exposure-scan/scan.sh quick` — fast match against installed packages.
3. Only escalate to `deep` if quick is clean but you want full `$HOME` coverage, or you're investigating a specific reported compromise.

## Catalog freshness (the one thing to understand)

Catalogs bundled in the Go module cache are **pinned to the installed bumblebee version**. Threat intel is published via PRs on `main` much more often. So the script prefers a **refreshable local cache** at `~/.config/bumblebee/threat_intel/` and only falls back to the bundled (pinned) catalogs when that cache is empty or you're offline. Run `refresh` to stay current. Override the cache location with `BUMBLEBEE_CATALOG_DIR`.

## Reading the result

- **`✅ CLEAN`** — no installed package matches a known-compromised release. (This is exact name+version matching, not a general CVE scan — clean here means you dodged these *named campaigns*, not that every dependency is vuln-free.)
- **`🚨 N EXPOSURE FINDING(S)`** — for each: severity, `ecosystem:package@version`, the campaign it belongs to, the evidence, and the exact `source_file` it was found in. Act on these: remove/downgrade the package, rotate any credentials it could have touched, and read the named campaign's report.

Exit codes: `0` clean · `2` findings present · `1` setup error. (Useful if wiring into cron or CI.)

## Notes

- Findings-only mode keeps output tiny; the script never persists the full 46MB inventory.
- The scan reports `diagnostic` records for configs it couldn't parse (e.g. array-shaped MCP configs) — transparency, not failure.
- To inventory everything (not just findings), run `bumblebee scan` directly without `--findings-only`.
