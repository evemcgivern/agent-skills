#!/usr/bin/env python3
"""Validate every skill under plugins/*/skills/: frontmatter, versions, scripts, leaks,
plus marketplace and release-please config consistency, and the compatibility
badges in each skill README against compatibility.json.

Run from anywhere:  python3 -I tests/validate.py
Exit code 0 = all checks pass, 1 = at least one failure.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def skill_dirs():
    return sorted(p for p in ROOT.glob("plugins/*/skills/*") if p.is_dir())


ALLOWED_FIELDS = {"name", "description", "allowed-tools", "model"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
LEAKS = [
    (re.compile(r"[\w.+-]+@(?!users\.noreply\.github\.com)[\w-]+\.[\w.]+"), "email address"),
    (re.compile(r"/Users/[A-Za-z0-9_.-]+"), "absolute macOS home path"),
    (re.compile(r"/home/[A-Za-z0-9_.-]+"), "absolute Linux home path"),
    (re.compile(r"\b(?:sk|pk|rk)_(?:live|test)_[A-Za-z0-9]{8,}"), "Stripe-style key"),
    (re.compile(r"\bghp_[A-Za-z0-9]{20,}|\bsk-[A-Za-z0-9_-]{20,}"), "API token"),
]
# Addresses that are documentation placeholders (RFC 2606 names included), not leaks.
EMAIL_OK = re.compile(
    r"(@(example\.(com|org|net)|localhost)\b|\.(test|example|invalid|localhost)$|^noreply@anthropic\.com$)"
)

failures = []


def fail(skill, msg):
    failures.append(f"{skill}: {msg}")


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    fields = {}
    for line in m.group(1).splitlines():
        if re.match(r"^[A-Za-z][\w-]*:", line):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields, text


def check_skill(d):
    name = d.name
    skill_md = d / "SKILL.md"
    if not skill_md.is_file():
        return fail(name, "missing SKILL.md")

    fields, _ = parse_frontmatter(skill_md)
    if fields is None:
        return fail(name, "SKILL.md has no frontmatter block")
    if fields.get("name") != name:
        fail(name, f"frontmatter name {fields.get('name')!r} != directory name")
    desc = fields.get("description", "")
    if not desc:
        fail(name, "empty description")
    elif len(desc) > 1024:
        fail(name, f"description is {len(desc)} chars (max 1024)")
    extra = set(fields) - ALLOWED_FIELDS
    if extra:
        fail(name, f"unexpected frontmatter fields: {sorted(extra)}")

    version_file = d / "VERSION"
    version = version_file.read_text().strip() if version_file.is_file() else ""
    if not SEMVER.match(version):
        fail(name, f"VERSION {version!r} is not semver")
    changelog = d / "CHANGELOG.md"
    if not changelog.is_file():
        fail(name, "missing CHANGELOG.md")
    elif version and not re.search(rf"^## \[?{re.escape(version)}\]?", changelog.read_text(), re.M):
        fail(name, f"CHANGELOG.md has no '## {version}' entry")
    if not (d / "README.md").is_file():
        fail(name, "missing README.md")

    for script in sorted(d.glob("*.sh")):
        r = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True)
        if r.returncode:
            fail(name, f"{script.name} has a syntax error: {r.stderr.strip()}")
        if shutil.which("shellcheck"):
            r = subprocess.run(
                ["shellcheck", "-S", "warning", str(script)], capture_output=True, text=True
            )
            if r.returncode:
                fail(name, f"shellcheck findings in {script.name}:\n{r.stdout.strip()}")


def check_leaks():
    for path in sorted(ROOT.rglob("*")):
        rel_parts = path.relative_to(ROOT).parts
        # Only the repo's own test fixtures are exempt; skill tests ship and get scanned.
        if not path.is_file() or ".git" in path.parts or rel_parts[0] == "tests":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(ROOT)
        for pattern, label in LEAKS:
            for m in pattern.finditer(text):
                if label == "email address" and EMAIL_OK.search(m.group(0)):
                    continue
                fail(str(rel), f"possible {label}: {m.group(0)!r}")


def check_marketplace():
    mp = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    listed = {p["name"]: p for p in mp["plugins"] if isinstance(p["source"], str)}
    for p in mp["plugins"]:
        if isinstance(p["source"], dict) and not p["source"].get("repo"):
            fail("marketplace.json", f"external plugin {p['name']!r} has no repo")
    on_disk = {p.parent.parent.name for p in ROOT.glob("plugins/*/.claude-plugin/plugin.json")}
    for name in sorted(set(listed) ^ on_disk):
        fail("marketplace.json", f"plugin {name!r} is listed or on disk but not both")
    for name, entry in listed.items():
        src = ROOT / entry["source"]
        manifest = src / ".claude-plugin" / "plugin.json"
        if not manifest.is_file():
            fail("marketplace.json", f"{name}: missing {manifest.relative_to(ROOT)}")
            continue
        if json.loads(manifest.read_text()).get("name") != name:
            fail(name, "plugin.json name does not match marketplace entry")
        if not any(src.glob("skills/*/SKILL.md")):
            fail(name, "plugin has no skills")
    readme = (ROOT / "README.md").read_text()
    for d in skill_dirs():
        if d.name not in readme:
            fail("README.md", f"does not mention skill {d.name}")


def check_release_config():
    cfg = json.loads((ROOT / "release-please-config.json").read_text())["packages"]
    man = json.loads((ROOT / ".release-please-manifest.json").read_text())
    paths = {str(d.relative_to(ROOT)) for d in skill_dirs()}
    for path in sorted(paths - set(cfg)):
        fail("release-please-config.json", f"no package for {path}")
    for path in sorted(set(cfg) - paths):
        fail("release-please-config.json", f"package {path} has no skill folder")
    for path in sorted(paths & set(man)):
        vf = ROOT / path / "VERSION"
        if vf.is_file() and man[path] != vf.read_text().strip():
            fail(".release-please-manifest.json", f"{path}: {man[path]} != VERSION {vf.read_text().strip()}")
    for path in sorted(paths - set(man)):
        fail(".release-please-manifest.json", f"missing {path}")


COMPAT_COLUMNS = [  # JSON key, badge label, URL-encoded label
    ("claude", "Claude", "Claude"),
    ("codex_chatgpt", "Codex / ChatGPT", "Codex%20%2F%20ChatGPT"),
    ("other", "Other agents", "Other%20agents"),
]
COMPAT_COLORS = {"full": "brightgreen", "partial": "yellow", "no": "lightgrey"}


def check_compatibility():
    path = ROOT / "compatibility.json"
    try:
        skills = json.loads(path.read_text())["skills"]
    except (OSError, ValueError, KeyError) as e:
        return fail("compatibility.json", f"cannot read a 'skills' object: {e}")
    names = {d.name: d for d in skill_dirs()}
    for name in sorted(set(skills) - set(names)):
        fail("compatibility.json", f"entry {name!r} has no skill folder")
    for name, d in names.items():
        entry = skills.get(name)
        if not isinstance(entry, dict):
            fail(name, "no entry in compatibility.json")
            continue
        if entry.get("plugin") != d.parent.parent.name:
            fail(name, f"compatibility.json plugin {entry.get('plugin')!r} != {d.parent.parent.name!r}")
        readme_path = d / "README.md"
        readme = readme_path.read_text(encoding="utf-8") if readme_path.is_file() else ""
        for key, label, enc in COMPAT_COLUMNS:
            cell = entry.get(key)
            level = cell.get("level") if isinstance(cell, dict) else None
            if level not in COMPAT_COLORS:
                fail(name, f"compatibility.json {key}.level is {level!r} (use full, partial or no)")
                continue
            if not (isinstance(cell.get("note"), str) and cell["note"].strip()):
                fail(name, f"compatibility.json {key}.note is empty")
            found = re.findall(
                rf"\[!\[{re.escape(label)}: (\w+)\]\(https://img\.shields\.io/badge/{re.escape(enc)}-(\w+)-(\w+)\)\]"
                r"\(\.\./\.\./\.\./\.\./README\.md#compatibility\)",
                readme,
            )
            if not found:
                fail(name, f"README.md has no '{label}' compatibility badge linked to README.md#compatibility")
            elif found[0] != (level, level, COMPAT_COLORS[level]):
                alt, shown, color = found[0]
                fail(name, f"README.md '{label}' badge says {alt}/{shown}/{color}; "
                           f"compatibility.json says {level} ({COMPAT_COLORS[level]})")


def main():
    dirs = skill_dirs()
    if not dirs:
        print("no skills found", file=sys.stderr)
        return 1
    for d in dirs:
        check_skill(d)
    check_leaks()
    check_marketplace()
    check_release_config()
    check_compatibility()
    if failures:
        print(f"FAIL: {len(failures)} problem(s) across {len(dirs)} skills\n")
        print("\n".join(f"- {f}" for f in failures))
        return 1
    print(f"OK: {len(dirs)} skills passed all checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
