#!/usr/bin/env python3
"""Read-only, bounded discovery of agent instructions and skill definitions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


DEFAULT_MAX_FILES = 1_000
DEFAULT_MAX_BYTES = 4_194_304
DEFAULT_MAX_DIRECTORIES = 1_000
MAX_DEPTH = 5
INSTRUCTION_NAMES = {"AGENTS.md", "CLAUDE.md"}
SKIP_DIRECTORIES = {
    ".git", ".hg", ".svn", ".next", ".cache", ".pytest_cache",
    "node_modules", "vendor", "dist", "build", "coverage", "__pycache__",
    ".venv", "venv", "worktrees", ".worktrees",
    ".ssh", ".aws", ".gnupg", ".kube", ".docker", ".azure", ".npm",
}
ALLOWED_HIDDEN_DIRECTORIES = {".agents", ".claude", ".codex", ".github"}
SENSITIVE_DIRECTORIES = {".ssh", ".aws", ".gnupg", ".kube", ".docker", ".azure"}
SENSITIVE_FILE_NAMES = {"credentials", "credentials.json", "id_rsa", "id_ed25519"}
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
YAML_VALUE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*?)\s*$")
YAML_BLOCK_INDICATOR = re.compile(r"^[>|][+-]?[0-9]?[+-]?$")
URI_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
MODEL_IDENTITY = re.compile(
    r"\bYou are\s+(Fable(?:\s+\d+(?:\.\d+)*)?|Claude(?:\s+(?:Opus|Sonnet|Haiku)(?:\s+\d+(?:\.\d+)*)?)?|GPT(?:-\d+(?:\.\d+)*)?|Codex(?:\s+\d+(?:\.\d+)*)?|Gemini(?:\s+(?:\d+(?:\.\d+)*|Pro|Flash))?)\b",
    re.IGNORECASE,
)


def model_key(name: str) -> str:
    """Normalize a model name so 'claude-opus-5-5' matches 'Claude Opus 5.5'."""
    key = re.sub(r"[\s._-]+", " ", name.casefold()).strip()
    if key.startswith("claude "):
        key = key[len("claude "):]
    return key


class Scan:
    def __init__(
        self, project: Path, home: Path, skill_roots: Sequence[Path], model: Optional[str],
        max_files: int, max_bytes: int, max_directories: int,
    ) -> None:
        self.project = project.resolve()
        self.home = home.resolve()
        # Keep caller spelling for alias reporting; resolve only for containment.
        self.skill_roots = list(skill_roots)
        self.model = model
        self.max_files = max_files
        self.max_bytes = max_bytes
        self.max_directories = max_directories
        self.sources: Dict[str, dict] = {}
        self.findings: List[dict] = []
        self.files_seen = 0
        self.bytes_read = 0
        self.directories_seen = 0
        self.limit_reported = False

    def finding(self, code: str, severity: str, path: Path, line: int, message: str) -> None:
        item = {
            "code": code,
            "severity": severity,
            "path": str(path),
            "line": line,
            "message": message,
        }
        if item not in self.findings:
            self.findings.append(item)

    def limit(self, path: Path) -> None:
        if not self.limit_reported:
            self.finding(
                "scan_limit_reached", "observed", path, 1,
                "Discovery stopped at its directory, file, or byte limit.",
            )
            self.limit_reported = True

    @staticmethod
    def within(path: Path, root: Path) -> bool:
        try:
            path.relative_to(root)
            return True
        except ValueError:
            return False

    def allowed_for(self, candidate: Path, owner: Path) -> Optional[Path]:
        """Return a canonical path only when a candidate stays within its owner."""
        return self.allowed_for_roots(candidate, (owner,))

    def allowed_for_roots(self, candidate: Path, owners: Sequence[Path]) -> Optional[Path]:
        """Return a canonical path only when a candidate stays in an explicit root."""
        try:
            resolved = candidate.resolve(strict=True)
        except OSError:
            self.finding("unreadable_source", "observed", candidate, 1, "Source could not be read.")
            return None
        if not any(self.within(resolved, owner) for owner in owners):
            self.finding(
                "symlink_outside_allowed_root", "observed", candidate, 1,
                "Symlink target is outside the allowed discovery root and was skipped.",
            )
            return None
        return resolved

    @staticmethod
    def sensitive_source(path: Path) -> bool:
        return (
            any(part in SENSITIVE_DIRECTORIES for part in path.parts)
            or path.name == ".env"
            or path.name.startswith(".env.")
            or path.name in SENSITIVE_FILE_NAMES
        )

    def consume(self, path: Path) -> Optional[str]:
        if self.files_seen >= self.max_files:
            self.limit(path)
            return None
        try:
            size = path.stat().st_size
        except OSError:
            self.finding("unreadable_source", "observed", path, 1, "Source could not be read.")
            return None
        if self.bytes_read + size > self.max_bytes:
            self.limit(path)
            return None
        self.files_seen += 1
        self.bytes_read += size
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            self.finding("unreadable_source", "observed", path, 1, "Source could not be read.")
            return None

    def add_source(self, path: Path, kind: str, scope: str, text: Optional[str] = None) -> Optional[dict]:
        canonical = str(path)
        source = self.sources.get(canonical)
        if source is None:
            if text is None:
                text = self.consume(path)
            if text is None:
                return None
            source = {
                "kind": kind,
                "scope": scope,
                "path": canonical,
                "canonical_path": canonical,
                "aliases": [canonical],
                "size_bytes": path.stat().st_size,
                "discovery": "discovered",
                "content_hash": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            }
            self.sources[canonical] = source
        return source

    def add_alias(self, source: dict, alias: Path) -> None:
        alias_text = str(alias.absolute())
        if alias_text not in source["aliases"]:
            source["aliases"].append(alias_text)

    def inspect_instruction(self, candidate: Path, owner: Path, scope: str) -> None:
        resolved = self.allowed_for(candidate, owner)
        if resolved is None or not resolved.is_file():
            return
        if self.sensitive_source(resolved):
            self.finding(
                "sensitive_source_skipped", "observed", candidate, 1,
                "Instruction target is in a credential path or is a sensitive file and was skipped.",
            )
            return
        existing = self.sources.get(str(resolved))
        if existing is not None:
            self.add_alias(existing, candidate)
            return
        text = self.consume(resolved)
        if text is None:
            return
        source = self.add_source(resolved, "instruction", scope, text)
        if source is not None:
            self.add_alias(source, candidate)

    def ancestor_instructions(self) -> None:
        current = self.project
        while True:
            for name in sorted(INSTRUCTION_NAMES):
                candidate = current / name
                if candidate.exists() or candidate.is_symlink():
                    # Ancestors are deliberately examined one file at a time.
                    resolved = candidate.resolve(strict=False)
                    if candidate.is_symlink() and not self.within(resolved, current):
                        self.finding(
                            "symlink_outside_allowed_root", "observed", candidate, 1,
                            "Symlink target is outside the allowed discovery root and was skipped.",
                        )
                    elif resolved.exists():
                        self.inspect_instruction(candidate, current, "ancestor")
            if current.parent == current:
                return
            current = current.parent

    def nested_instructions(self) -> None:
        for directory, subdirs, filenames in os.walk(self.project, followlinks=False):
            if self.directories_seen >= self.max_directories:
                self.limit(Path(directory))
                return
            self.directories_seen += 1
            path = Path(directory)
            depth = len(path.relative_to(self.project).parts)
            subdirs[:] = sorted(
                name for name in subdirs
                if (
                    name not in SKIP_DIRECTORIES
                    and (not name.startswith(".") or name in ALLOWED_HIDDEN_DIRECTORIES)
                    and depth < MAX_DEPTH
                    and not (path / name).is_symlink()
                )
            )
            for name in sorted(filenames):
                if name in INSTRUCTION_NAMES:
                    self.inspect_instruction(path / name, self.project, "nested")
                if self.limit_reported:
                    return

    def global_instructions(self) -> None:
        for relative in (Path(".codex") / "AGENTS.md", Path(".claude") / "CLAUDE.md"):
            candidate = self.home / relative
            if candidate.exists() or candidate.is_symlink():
                resolved = self.allowed_global_instruction(candidate)
                if resolved is not None:
                    self.inspect_instruction(candidate, resolved.parent, "global")

    def allowed_global_instruction(self, candidate: Path) -> Optional[Path]:
        """Keep global instruction aliases on the documented global surfaces."""
        try:
            resolved = candidate.resolve(strict=True)
        except OSError:
            self.finding("unreadable_source", "observed", candidate, 1, "Source could not be read.")
            return None
        if resolved == candidate.absolute():
            return resolved
        agents_alias = self.home / ".agents" / candidate.name
        if candidate.parts[-2] == ".claude" and agents_alias.exists() and resolved == agents_alias.resolve():
            return resolved
        self.finding(
            "symlink_outside_allowed_root", "observed", candidate, 1,
            "Global instruction alias is outside the allowlisted global instruction files and was skipped.",
        )
        return None

    def skill_files_for_root(self, root: Path, alias_root: Path) -> Iterable[Tuple[Path, Path]]:
        direct = root / "SKILL.md"
        if direct.is_file() or direct.is_symlink():
            yield direct, alias_root / "SKILL.md"
        try:
            entries = sorted(root.iterdir(), key=lambda entry: entry.name)
        except OSError:
            self.finding("unreadable_source", "observed", alias_root, 1, "Skill root could not be read.")
            return
        for entry in entries:
            if entry.name in SKIP_DIRECTORIES or not entry.is_dir():
                continue
            yield entry / "SKILL.md", alias_root / entry.name / "SKILL.md"

    @staticmethod
    def metadata(text: str) -> Tuple[Dict[str, str], int]:
        """Read top-level frontmatter scalars, including block, folded, and continued values."""
        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            return {}, 1
        values: Dict[str, str] = {}
        key: Optional[str] = None
        style = ""
        parts: List[str] = []

        def flush() -> None:
            if key is None:
                return
            if style == "|":
                value = "\n".join(parts).strip()
            else:
                value = " ".join(part for part in parts if part)
            values[key] = value.strip('"\'')

        for number, line in enumerate(lines[1:], 2):
            if line.strip() == "---":
                flush()
                return values, number
            match = YAML_VALUE.match(line)
            if match:
                flush()
                key, rest = match.group(1), match.group(2)
                if YAML_BLOCK_INDICATOR.match(rest):
                    style, parts = rest[0], []
                else:
                    style, parts = "plain", [rest] if rest else []
            elif key is not None and (not line.strip() or line[:1] in (" ", "\t")):
                parts.append(line.strip())
            else:
                flush()
                key = None
        return {}, 1

    def inspect_skill(
        self, candidate: Path, owner: Path, alias: Path, native_namespace: str,
        allowed_roots: Optional[Sequence[Path]] = None,
    ) -> None:
        if not (candidate.exists() or candidate.is_symlink()):
            return
        resolved = self.allowed_for_roots(candidate, allowed_roots or (owner,))
        if resolved is None or not resolved.is_file():
            return
        source = self.sources.get(str(resolved))
        if source is not None:
            self.add_alias(source, alias)
            return
        text = self.consume(resolved)
        if text is None:
            return
        source = self.add_source(resolved, "skill", "skill_root", text)
        if source is None:
            return
        self.add_alias(source, alias)
        metadata, body_line = self.metadata(text)
        source["skill_name"] = metadata.get("name", "")
        if native_namespace:
            source["native_namespace"] = native_namespace
        if not metadata.get("name") or not metadata.get("description"):
            self.finding(
                "missing_skill_metadata", "observed", resolved, 1,
                "Skill metadata must include name and description in YAML frontmatter.",
            )
        self.inspect_model_identities(resolved, text)
        self.inspect_markdown_links(resolved, text, allowed_roots or (owner,))

    def inspect_model_identities(self, skill_file: Path, text: str) -> None:
        if not self.model:
            return
        in_code_block = False
        for line_number, line in enumerate(text.splitlines(), 1):
            stripped = line.lstrip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block or stripped.startswith(">"):
                continue
            match = MODEL_IDENTITY.search(line)
            if match and model_key(match.group(1)) != model_key(self.model):
                self.finding(
                    "model_role_mismatch", "advisory", skill_file, line_number,
                    "Literal skill model identity differs from the caller-supplied model.",
                )

    def inspect_markdown_links(self, skill_file: Path, text: str, allowed_roots: Sequence[Path]) -> None:
        skill_root = skill_file.parent
        in_code_block = False
        for line_number, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            for match in MARKDOWN_LINK.finditer(line):
                target = match.group(1).strip()
                if target.startswith("<") and ">" in target:
                    target = target[1:target.index(">")]
                else:
                    # Drop an optional link title: [text](path "title").
                    target = target.split(None, 1)[0] if target else ""
                target = target.split("#", 1)[0].strip()
                if not target or URI_SCHEME.match(target) or target.startswith("/"):
                    continue
                path = skill_root / target
                lexical = path.absolute()
                if not any(self.within(lexical, root) for root in allowed_roots):
                    continue
                try:
                    resolved = path.resolve(strict=True)
                except OSError:
                    self.finding(
                        "broken_markdown_reference", "observed", skill_file, line_number,
                        "Relative Markdown reference does not resolve within the skill.",
                    )
                    continue
                if not any(self.within(resolved, root) for root in allowed_roots):
                    continue
                if not (resolved.is_file() or resolved.is_dir()):
                    self.finding(
                        "broken_markdown_reference", "observed", skill_file, line_number,
                        "Relative Markdown reference does not resolve within the skill.",
                    )

    def accepted_native_skill_roots(
        self, roots: Sequence[Path], boundary: Path, label: str,
    ) -> Tuple[List[Path], Dict[str, Path]]:
        """Accept aliases only into a physical native agent skill root."""
        native: List[Path] = []
        resolved_roots: Dict[str, Path] = {}
        for root in roots:
            if not (root.exists() or root.is_symlink()):
                continue
            try:
                resolved = root.resolve(strict=True)
            except OSError:
                self.finding("unreadable_source", "observed", root, 1, "Skill root could not be read.")
                continue
            if resolved == root.absolute() and self.within(resolved, boundary):
                native.append(resolved)
        for root in roots:
            if not (root.exists() or root.is_symlink()):
                continue
            try:
                resolved = root.resolve(strict=True)
            except OSError:
                continue
            if any(self.within(resolved, allowed) for allowed in native):
                resolved_roots[str(root)] = resolved
            else:
                self.finding(
                    "symlink_outside_allowed_root", "observed", root, 1,
                    "%s skill alias is outside the explicit native skill roots and was skipped." % label,
                )
        return list(dict.fromkeys(native)), resolved_roots

    @staticmethod
    def native_namespace(root: Path) -> str:
        if root.name == "skills" and root.parent.parent.name == "plugins":
            return root.parent.name
        return ""

    def skills(self) -> None:
        global_roots = [
            self.home / ".agents" / "skills",
            self.home / ".codex" / "skills",
            self.home / ".claude" / "skills",
        ]
        project_roots = [
            self.project / ".agents" / "skills",
            self.project / ".codex" / "skills",
            self.project / ".claude" / "skills",
        ]
        accepted_global_roots, accepted_global_by_alias = self.accepted_native_skill_roots(
            global_roots, self.home, "Global",
        )
        accepted_project_roots, accepted_project_by_alias = self.accepted_native_skill_roots(
            project_roots, self.project, "Project",
        )
        roots = [(root, "global") for root in global_roots]
        roots += [(root, "project") for root in project_roots]
        roots += [(root, "explicit") for root in self.skill_roots]
        for alias_root, root_kind in roots:
            if not (alias_root.exists() or alias_root.is_symlink()):
                continue
            if root_kind == "global":
                resolved_root = accepted_global_by_alias.get(str(alias_root))
            elif root_kind == "project":
                resolved_root = accepted_project_by_alias.get(str(alias_root))
            else:
                resolved_root = self.allowed_for(alias_root, alias_root.resolve())
            if resolved_root is None or not resolved_root.is_dir():
                continue
            for candidate, alias in self.skill_files_for_root(resolved_root, alias_root):
                if root_kind == "global":
                    allowed_roots = accepted_global_roots
                elif root_kind == "project":
                    allowed_roots = accepted_project_roots
                else:
                    allowed_roots = None
                self.inspect_skill(
                    candidate, resolved_root, alias, self.native_namespace(resolved_root), allowed_roots,
                )
        groups: Dict[str, List[dict]] = {}
        for source in self.sources.values():
            if source["kind"] == "skill" and source.get("skill_name"):
                name = source["skill_name"]
                identity = name if ":" in name else ":".join(
                    part for part in (source.get("native_namespace", ""), name) if part
                )
                groups.setdefault(identity, []).append(source)
        for name, sources in groups.items():
            hashes = {source["content_hash"] for source in sources}
            if len(sources) > 1 and len(hashes) > 1:
                for source in sources:
                    self.finding(
                        "duplicate_skill_name", "observed", Path(source["path"]), 1,
                        "Discovered flat skill name conflicts with a different skill definition.",
                    )

    def report(self) -> dict:
        # A reached limit stops further reads (consume refuses them) but every
        # phase still runs, so already-discovered sources keep their checks.
        self.ancestor_instructions()
        self.nested_instructions()
        self.global_instructions()
        self.skills()
        sources = sorted(self.sources.values(), key=lambda item: (item["kind"], item["path"]))
        for source in sources:
            source["aliases"].sort()
            source.pop("content_hash", None)
        return {
            "discovery": "discovered",
            "project": str(self.project),
            "limits": {"max_files": self.max_files, "max_bytes": self.max_bytes, "max_directories": self.max_directories, "files_seen": self.files_seen, "bytes_read": self.bytes_read, "directories_seen": self.directories_seen},
            "sources": sources,
            "findings": sorted(self.findings, key=lambda item: (item["path"], item["line"], item["code"])),
        }


def markdown(report: dict) -> str:
    lines = ["# Agent Doctor", "", "Discovery status: discovered (not runtime loaded).", "", "## Sources", ""]
    if report["sources"]:
        for source in report["sources"]:
            source_data = dict(source)
            source_data["aliases"] = ", ".join(source["aliases"])
            lines.append(
                "- `{kind}` `{scope}` `{path}` ({size_bytes} bytes); aliases: {aliases}".format(
                    **source_data
                )
            )
    else:
        lines.append("No allowlisted sources discovered.")
    lines.extend(["", "## Findings", "", "| Severity | Code | File | Line | Message |", "| --- | --- | --- | ---: | --- |"])
    if report["findings"]:
        for finding in report["findings"]:
            lines.append("| {severity} | {code} | `{path}` | {line} | {message} |".format(**finding))
    else:
        lines.append("| observed | none | - | - | No findings. |")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# --usage: per-skill call counts from local session logs (names and counts only)
# ---------------------------------------------------------------------------

DAY = 86_400.0
USAGE_MAX_FILES = 10_000
USAGE_MAX_BYTES = 67_108_864
SKILL_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}(?::[A-Za-z0-9][A-Za-z0-9._-]{0,127})?$")
COMMAND_NAME = re.compile(r"<command-name>/?([^<\s]{1,200})</command-name>")
LOG_TIMESTAMP = re.compile(rb'"timestamp"\s*:\s*"([0-9T:.+Z-]{10,40})"')
CODEX_SKILL_READ = re.compile(r"skills/([A-Za-z0-9][A-Za-z0-9._-]{0,127})/SKILL\.md")
CODEX_DOLLAR = re.compile(r"(?<![\w$])\$([a-z][a-z0-9_-]{0,127})\b")
CODEX_TOOL_CALLS = {"function_call", "custom_tool_call", "local_shell_call"}
SKILL_MENTIONS = (
    re.compile(r"`[/$]?([a-z0-9][a-z0-9-]*(?::[a-z0-9][a-z0-9-]*)?)` skill\b"),
    re.compile(r"\bskill `[/$]?([a-z0-9][a-z0-9-]*(?::[a-z0-9][a-z0-9-]*)?)`"),
    re.compile(r"`\$([a-z0-9][a-z0-9-]*)`"),
)
VERDICT_ORDER = {"NO CALLS FOUND": 0, "RARELY USED": 1, "UNKNOWN-WINDOW": 2, "NEW": 3, "ACTIVE": 4}


def parse_time(value: object) -> Optional[float]:
    if not isinstance(value, str) or not value:
        return None
    try:
        from datetime import datetime, timezone
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.timestamp()
    except ValueError:
        return None


def iso_date(stamp: Optional[float]) -> str:
    if stamp is None:
        return "-"
    from datetime import datetime, timezone
    return datetime.fromtimestamp(stamp, timezone.utc).strftime("%Y-%m-%d")


def days_since(stamp: Optional[float], now: float) -> Optional[int]:
    return None if stamp is None else max(0, int((now - stamp) // DAY))


class LogTally:
    """Streams one log family; keeps only skill names, timestamps, and counts."""

    def __init__(self, label: str, cutoff: float) -> None:
        self.label = label
        self.cutoff = cutoff
        self.counts: Dict[str, int] = {}
        self.last: Dict[str, float] = {}
        self.seen_ids: set = set()
        self.files_found = 0
        self.files_read = 0
        self.files_skipped = 0
        self.malformed_lines = 0
        self.oldest: Optional[float] = None

    def note_time(self, stamp: Optional[float]) -> None:
        if stamp is not None and (self.oldest is None or stamp < self.oldest):
            self.oldest = stamp

    def credit(self, name: object, stamp: float, dedupe: object) -> None:
        if not isinstance(name, str):
            return
        name = name.strip().lstrip("/$")
        if not SKILL_NAME.match(name):
            return
        if dedupe is not None:
            if dedupe in self.seen_ids:
                return
            self.seen_ids.add(dedupe)
        names = [name]
        if ":" in name:
            names.append(name.split(":", 1)[1])
        for item in names:
            if stamp >= self.cutoff:
                self.counts[item] = self.counts.get(item, 0) + 1
            if stamp > self.last.get(item, 0.0):
                self.last[item] = stamp

    def files(self, root: Path) -> Iterable[Tuple[Path, float]]:
        if not root.is_dir():
            return
        for directory, subdirs, filenames in os.walk(root, followlinks=False):
            subdirs.sort()
            for name in sorted(filenames):
                if not name.endswith(".jsonl"):
                    continue
                path = Path(directory) / name
                try:
                    mtime = path.lstat().st_mtime
                except OSError:
                    continue
                if path.is_symlink():
                    continue
                self.files_found += 1
                self.note_time(mtime)
                if mtime < self.cutoff:
                    self.files_skipped += 1
                    continue
                yield path, mtime

    def stream(self, path: Path, prefilter, handle) -> None:
        try:
            stream = path.open("rb")
        except OSError:
            self.files_skipped += 1
            return
        self.files_read += 1
        with stream:
            for number, raw in enumerate(stream):
                if number < 5:
                    match = LOG_TIMESTAMP.search(raw[:65_536])
                    if match:
                        self.note_time(parse_time(match.group(1).decode("ascii", "replace")))
                if not prefilter(raw):
                    continue
                try:
                    entry = json.loads(raw)
                except ValueError:
                    self.malformed_lines += 1
                    continue
                if isinstance(entry, dict):
                    handle(entry)


def tally_claude(root: Path, cutoff: float) -> LogTally:
    tally = LogTally("claude", cutoff)

    def prefilter(raw: bytes) -> bool:
        return b'"name":"Skill"' in raw or b"<command-name>" in raw

    for path, mtime in tally.files(root):
        def handle(entry: dict, path: Path = path, mtime: float = mtime) -> None:
            stamp = parse_time(entry.get("timestamp")) or mtime
            message = entry.get("message")
            if not isinstance(message, dict):
                return
            content = message.get("content")
            if entry.get("type") == "assistant" and isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "tool_use" and item.get("name") == "Skill":
                        payload = item.get("input")
                        if isinstance(payload, dict):
                            tool_id = item.get("id")
                            tally.credit(payload.get("skill"), stamp, ("t", tool_id) if isinstance(tool_id, str) else None)
            elif entry.get("type") == "user" and message.get("role") == "user":
                if isinstance(content, str):
                    texts = [content]
                elif isinstance(content, list):
                    texts = [item.get("text") for item in content if isinstance(item, dict) and item.get("type") == "text"]
                else:
                    texts = []
                for text in texts:
                    if isinstance(text, str):
                        for match in COMMAND_NAME.finditer(text):
                            uuid = entry.get("uuid")
                            key = ("c", uuid if isinstance(uuid, str) else str(path), match.group(1))
                            tally.credit(match.group(1), stamp, key)

        tally.stream(path, prefilter, handle)
    return tally


def tally_codex(root: Path, cutoff: float) -> LogTally:
    tally = LogTally("codex", cutoff)

    def prefilter(raw: bytes) -> bool:
        if b"response_item" not in raw:
            return False
        return b"SKILL.md" in raw or (b"$" in raw and (b'"role":"user"' in raw or b'"role": "user"' in raw))

    for path, mtime in tally.files(root):
        def handle(entry: dict, path: Path = path, mtime: float = mtime) -> None:
            payload = entry.get("payload")
            if entry.get("type") != "response_item" or not isinstance(payload, dict):
                return
            stamp = parse_time(entry.get("timestamp")) or mtime
            kind = payload.get("type")
            if kind in CODEX_TOOL_CALLS:
                call = payload.get("arguments") or payload.get("input") or payload.get("action")
                text = call if isinstance(call, str) else json.dumps(call)
                call_id = payload.get("call_id") or payload.get("id")
                call_id = call_id if isinstance(call_id, str) else None
                for name in set(CODEX_SKILL_READ.findall(text)):
                    tally.credit(name, stamp, ("r", str(path), call_id, name) if call_id else None)
            elif kind == "message" and payload.get("role") == "user":
                content = payload.get("content")
                for item in content if isinstance(content, list) else []:
                    text = item.get("text") if isinstance(item, dict) else None
                    if not isinstance(text, str):
                        continue
                    head = text.lstrip()
                    # Injected instructions and harness notices are not owner requests.
                    if head.startswith("<") or head.startswith("# AGENTS.md"):
                        continue
                    for name in set(CODEX_DOLLAR.findall(text)):
                        tally.credit(name, stamp, None)

        tally.stream(path, prefilter, handle)
    return tally


def read_name_list(path: Path) -> List[str]:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    names = []
    for line in lines:
        line = line.split("#", 1)[0].strip()
        if line:
            names.append(line)
    return names


def load_skill_lock(home: Path) -> Dict[str, dict]:
    try:
        data = json.loads((home / ".agents" / ".skill-lock.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    skills = data.get("skills") if isinstance(data, dict) else None
    return skills if isinstance(skills, dict) else {}


def plugin_skill_roots(home: Path) -> List[Tuple[str, Path, Optional[float]]]:
    """Installed plugin skill folders from the Claude Code plugin registry."""
    plugins_dir = home / ".claude" / "plugins"
    try:
        data = json.loads((plugins_dir / "installed_plugins.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    plugins = data.get("plugins") if isinstance(data, dict) else None
    if not isinstance(plugins, dict):
        return []
    roots: Dict[str, Tuple[str, Path, Optional[float]]] = {}
    for key, installs in plugins.items():
        plugin = str(key).split("@", 1)[0]
        for install in installs if isinstance(installs, list) else []:
            if not isinstance(install, dict) or not isinstance(install.get("installPath"), str):
                continue
            skills = Path(install["installPath"]) / "skills"
            try:
                resolved = skills.resolve(strict=True)
            except OSError:
                continue
            if not Scan.within(resolved, plugins_dir.resolve()) or not resolved.is_dir():
                continue
            installed = parse_time(install.get("installedAt"))
            previous = roots.get(str(resolved))
            if previous is None or (installed is not None and (previous[2] is None or installed < previous[2])):
                roots[str(resolved)] = (plugin, resolved, installed)
    return sorted(roots.values(), key=lambda item: (item[0], str(item[1])))


def entry_birth(entry: Path, skill_file: Path) -> Optional[float]:
    """Oldest of the folder's creation time and the folder and SKILL.md modification times."""
    stamps = []
    for path in (entry, skill_file):
        try:
            info = path.lstat() if path == entry else path.stat()
        except OSError:
            continue
        stamps.append(info.st_mtime)
        if getattr(info, "st_birthtime", None):
            stamps.append(info.st_birthtime)
    return min(stamps) if stamps else None


def skill_mentions(text: str) -> List[str]:
    names: List[str] = []
    in_code_block = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        for pattern in SKILL_MENTIONS:
            for name in pattern.findall(line):
                if name not in names:
                    names.append(name)
    return names


def usage_report(args: argparse.Namespace, now: Optional[float] = None) -> dict:
    import time
    now = time.time() if now is None else now
    home = Path(args.home)
    project = Path(args.project or os.getcwd())
    cutoff = now - args.days * DAY
    plugin_roots = plugin_skill_roots(home)
    scan = Scan(
        project, home, [Path(root) for root in args.skill_root] + [root for _, root, _ in plugin_roots],
        None, USAGE_MAX_FILES, USAGE_MAX_BYTES, DEFAULT_MAX_DIRECTORIES,
    )
    scan.skills()
    lock = load_skill_lock(home)
    plugin_by_root = {str(root): (plugin, installed) for plugin, root, installed in plugin_roots}

    claude = tally_claude(Path(args.claude_logs or home / ".claude" / "projects"), cutoff)
    codex = tally_codex(Path(args.codex_logs or home / ".codex" / "sessions"), cutoff)
    present = [tally for tally in (claude, codex) if tally.files_found]
    coverage_days: Optional[int] = None
    if present and all(tally.oldest is not None for tally in present):
        coverage_days = min(days_since(tally.oldest, now) or 0 for tally in present)
    window_covered = coverage_days is not None and coverage_days >= args.days

    findings_by_path: Dict[str, List[str]] = {}
    for finding in scan.findings:
        findings_by_path.setdefault(finding["path"], []).append(finding["code"])

    # Group discovered skill files by the name a caller would invoke.
    rows: Dict[str, dict] = {}
    for source in scan.sources.values():
        if source["kind"] != "skill":
            continue
        skill_file = Path(source["path"])
        alias_entries = [Path(alias).parent for alias in source["aliases"]]
        folder = alias_entries[0].name if alias_entries else skill_file.parent.name
        declared = source.get("skill_name") or folder
        plugin = None
        installed = None
        for root, (plugin_name, plugin_installed) in plugin_by_root.items():
            if Scan.within(skill_file, Path(root)):
                plugin, installed = plugin_name, plugin_installed
        if plugin:
            display, scope, match_names = "%s:%s" % (plugin, declared), "plugin", ["%s:%s" % (plugin, declared)]
        else:
            display = declared
            scope = "project" if any(Scan.within(entry.absolute(), scan.project) for entry in alias_entries) else "global"
            match_names = list(dict.fromkeys([declared, folder]))
        lock_entry = lock.get(declared) or lock.get(folder) if not plugin else None
        if isinstance(lock_entry, dict):
            installed = parse_time(lock_entry.get("installedAt")) or installed
        if installed is None:
            births = [entry_birth(entry, skill_file) for entry in alias_entries]
            births = [stamp for stamp in births if stamp is not None]
            installed = min(births) if births else None
        try:
            changed = skill_file.stat().st_mtime
        except OSError:
            changed = None
        row = rows.setdefault(display, {
            "skill": display, "scopes": [], "match_names": [], "files": [], "installed": None,
            "changed": None, "lock": None, "folders": [],
        })
        row["scopes"] = sorted(set(row["scopes"]) | {scope})
        row["match_names"] = list(dict.fromkeys(row["match_names"] + match_names))
        row["files"].append(str(skill_file))
        row["folders"].append(folder)
        if installed is not None and (row["installed"] is None or installed < row["installed"]):
            row["installed"] = installed
        if changed is not None and (row["changed"] is None or changed > row["changed"]):
            row["changed"] = changed
        if isinstance(lock_entry, dict) and row["lock"] is None:
            row["lock"] = lock_entry

    flat_names = {name for row in rows.values() if "plugin" not in row["scopes"] for name in row["match_names"]}
    installed_names = set(flat_names) | set(rows)
    for row in rows.values():
        if "plugin" in row["scopes"]:
            installed_names.add(row["skill"].split(":", 1)[1])

    excluded_names = set(args.exclude or [])
    for ignore in (home / ".agent-doctor-ignore", project / ".agent-doctor-ignore"):
        excluded_names.update(read_name_list(ignore))

    skills: List[dict] = []
    excluded: List[str] = []
    for display in sorted(rows):
        row = rows[display]
        if display in excluded_names or any(name in excluded_names for name in row["match_names"]):
            excluded.append(display)
            continue
        uses_claude = sum(claude.counts.get(name, 0) for name in row["match_names"])
        uses_codex = sum(codex.counts.get(name, 0) for name in row["match_names"])
        lasts = [tally.last.get(name) for tally in (claude, codex) for name in row["match_names"]]
        lasts = [stamp for stamp in lasts if stamp]
        last_used = max(lasts) if lasts else None
        uses = uses_claude + uses_codex
        installed_days = days_since(row["installed"], now)
        if uses >= args.min_uses:
            verdict = "ACTIVE"
        elif installed_days is not None and installed_days < args.days:
            verdict = "NEW"
        elif not window_covered:
            verdict = "UNKNOWN-WINDOW"
        elif uses == 0:
            verdict = "NO CALLS FOUND"
        else:
            verdict = "RARELY USED"
        notes: List[str] = []
        lock_entry = row["lock"]
        source = "local"
        if "plugin" in row["scopes"]:
            source = "plugin"
        if isinstance(lock_entry, dict) and lock_entry.get("source"):
            source = str(lock_entry["source"])
            updated = days_since(parse_time(lock_entry.get("updatedAt")), now)
            notes.append(
                "installed from %s, last updated %s days ago: check upstream"
                % (source, "?" if updated is None else updated)
            )
        codes = [code for path in row["files"] for code in findings_by_path.get(path, [])]
        broken = codes.count("broken_markdown_reference")
        if broken:
            notes.append("%d broken relative link(s) or missing referenced file(s)" % broken)
        if "duplicate_skill_name" in codes:
            notes.append("another installed skill has the same name with different content")
        if "missing_skill_metadata" in codes:
            notes.append("SKILL.md frontmatter lacks name or description")
        missing: List[str] = []
        for path in row["files"]:
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as handle:
                    text = handle.read(1_048_576)
            except OSError:
                continue
            for name in skill_mentions(text):
                if name not in installed_names and name not in row["match_names"] and name not in missing:
                    missing.append(name)
        if missing:
            notes.append("mentions skill(s) not installed: %s" % ", ".join(missing[:5]))
        skills.append({
            "skill": display,
            "scope": ",".join(row["scopes"]),
            "uses": uses,
            "uses_claude": uses_claude,
            "uses_codex_best_effort": uses_codex,
            "last_used": iso_date(last_used) if last_used else None,
            "skill_md_changed_days": days_since(row["changed"], now),
            "installed_days": installed_days,
            "source": source,
            "verdict": verdict,
            "notes": notes,
        })
    skills.sort(key=lambda item: (
        VERDICT_ORDER[item["verdict"]], item["uses"], -(item["skill_md_changed_days"] or 0), item["skill"],
    ))
    verdicts: Dict[str, int] = {}
    for item in skills:
        verdicts[item["verdict"]] = verdicts.get(item["verdict"], 0) + 1

    def log_summary(tally: LogTally, heuristic: str) -> dict:
        return {
            "files_found": tally.files_found,
            "files_read": tally.files_read,
            "files_skipped": tally.files_skipped,
            "malformed_lines": tally.malformed_lines,
            "reaches_back_days": days_since(tally.oldest, now),
            "method": heuristic,
        }

    return {
        "mode": "usage",
        "window_days": args.days,
        "min_uses": args.min_uses,
        "coverage_days": coverage_days,
        "window_covered": window_covered,
        "logs": {
            "claude": log_summary(claude, "Skill tool calls and slash commands"),
            "codex": log_summary(codex, "best effort: SKILL.md reads and $name mentions"),
        },
        "totals": {
            "skills": len(skills),
            "excluded": len(excluded),
            "uses": sum(item["uses"] for item in skills),
            "verdicts": verdicts,
        },
        "excluded": excluded,
        "skills": skills,
    }


def usage_markdown(report: dict) -> str:
    days, logs = report["window_days"], report["logs"]
    lines = ["# Agent Doctor: skill usage", ""]
    lines.append(
        "Window: last %d days. RARELY USED means fewer than %d calls found. Names and counts only."
        % (days, report["min_uses"])
    )
    if report["coverage_days"] is None:
        lines.append("No session logs found, so no skill can be judged: verdicts are UNKNOWN-WINDOW.")
    elif not report["window_covered"]:
        lines.append(
            "Logs only reach back %d days, less than the %d-day window: skills with few or no calls "
            "are UNKNOWN-WINDOW." % (report["coverage_days"], days)
        )
    else:
        lines.append("Logs reach back %d days and cover the window." % report["coverage_days"])
    for label, key in (("Claude Code", "claude"), ("Codex (best effort)", "codex")):
        item = logs[key]
        reach = "-" if item["reaches_back_days"] is None else "%d days" % item["reaches_back_days"]
        lines.append(
            "- %s logs: %d found, %d read, %d skipped (older than the window or unreadable), "
            "%d malformed lines; reach back %s."
            % (label, item["files_found"], item["files_read"], item["files_skipped"], item["malformed_lines"], reach)
        )
    lines.extend([
        "", "| Skill | Uses in window | Last used | Days since SKILL.md changed | Source | Verdict |",
        "| --- | ---: | --- | ---: | --- | --- |",
    ])
    for item in report["skills"]:
        changed = "-" if item["skill_md_changed_days"] is None else str(item["skill_md_changed_days"])
        lines.append("| {skill} | {uses} | {last} | {changed} | {source} | {verdict} |".format(
            skill=item["skill"], uses=item["uses"], last=item["last_used"] or "-",
            changed=changed, source=item["source"], verdict=item["verdict"],
        ))
    if not report["skills"]:
        lines.append("| - | - | - | - | - | No installed skills discovered. |")
    noted = [item for item in report["skills"] if item["notes"]]
    if noted:
        lines.extend(["", "## Freshness notes", "", "| Severity | Skill | Note |", "| --- | --- | --- |"])
        for item in noted:
            for note in item["notes"]:
                lines.append("| advisory | %s | %s |" % (item["skill"], note))
    totals = report["totals"]
    verdicts = ", ".join("%s %d" % (name, totals["verdicts"][name]) for name in sorted(
        totals["verdicts"], key=lambda name: VERDICT_ORDER[name]))
    lines.extend([
        "", "Totals: %d skills, %d calls found in the window; %s." % (totals["skills"], totals["uses"], verdicts or "none"),
    ])
    if report["excluded"]:
        lines.append("Excluded by the owner (always kept): %s." % ", ".join(report["excluded"]))
    lines.append("No calls found in the logs is not proof a skill is unneeded; ask the owner before any change.")
    return "\n".join(lines) + "\n"


def parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(
        description="Read-only, bounded discovery of agent instructions and skills."
    )
    argument_parser.add_argument("--project", help="Project directory to inspect (required unless --usage; --usage defaults to the current directory).")
    argument_parser.add_argument("--home", default=str(Path.home()), help="Home directory for allowlisted global discovery.")
    argument_parser.add_argument("--skill-root", action="append", default=[], help="Additional skill root to inspect; repeatable.")
    argument_parser.add_argument("--model", help="Caller-supplied model role for literal advisory comparison.")
    argument_parser.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES, help="Maximum discovered files to read (1-10000).")
    argument_parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="Maximum source bytes to read (1-67108864).")
    argument_parser.add_argument("--max-directories", type=int, default=DEFAULT_MAX_DIRECTORIES, help="Maximum project directories to traverse (1-10000).")
    argument_parser.add_argument("--format", choices=("json", "markdown", "text"), default="markdown", help="Output format; text is the Markdown report.")
    usage = argument_parser.add_argument_group("skill usage (--usage)")
    usage.add_argument("--usage", action="store_true", help="Report per-skill call counts from local session logs (names and counts only).")
    usage.add_argument("--days", type=int, default=90, help="Usage window in days (1-3650, default 90).")
    usage.add_argument("--min-uses", type=int, default=3, help="Calls below this count are RARELY USED (1-100000, default 3).")
    usage.add_argument("--claude-logs", help="Claude Code session log folder (default <home>/.claude/projects).")
    usage.add_argument("--codex-logs", help="Codex session log folder (default <home>/.codex/sessions).")
    usage.add_argument("--exclude", action="append", default=[], help="Skill name the owner always keeps; repeatable.")
    return argument_parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parser().parse_args(argv)
    if args.usage:
        return usage_main(args)
    if not args.project:
        parser().error("the following arguments are required: --project")
    project = Path(args.project)
    home = Path(args.home)
    if not project.exists() or not project.is_dir():
        parser().error("--project must name a readable directory")
    if not home.exists() or not home.is_dir():
        parser().error("--home must name a readable directory")
    invalid_roots = [root for root in args.skill_root if not Path(root).exists() or not Path(root).is_dir()]
    if invalid_roots:
        parser().error("--skill-root must name readable directories")
    if not 1 <= args.max_files <= 10_000:
        parser().error("--max-files must be between 1 and 10000")
    if not 1 <= args.max_bytes <= 67_108_864:
        parser().error("--max-bytes must be between 1 and 67108864")
    if not 1 <= args.max_directories <= 10_000:
        parser().error("--max-directories must be between 1 and 10000")
    report = Scan(
        project, home, [Path(root) for root in args.skill_root], args.model,
        args.max_files, args.max_bytes, args.max_directories,
    ).report()
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(markdown(report), end="")
    return 0


def usage_main(args: argparse.Namespace) -> int:
    home = Path(args.home)
    if not home.is_dir():
        parser().error("--home must name a readable directory")
    if args.project and not Path(args.project).is_dir():
        parser().error("--project must name a readable directory")
    if not 1 <= args.days <= 3650:
        parser().error("--days must be between 1 and 3650")
    if not 1 <= args.min_uses <= 100_000:
        parser().error("--min-uses must be between 1 and 100000")
    if any(not Path(root).is_dir() for root in args.skill_root):
        parser().error("--skill-root must name readable directories")
    report = usage_report(args)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(usage_markdown(report), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
