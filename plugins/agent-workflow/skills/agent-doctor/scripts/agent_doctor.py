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


def parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(
        description="Read-only, bounded discovery of agent instructions and skills."
    )
    argument_parser.add_argument("--project", required=True, help="Project directory to inspect.")
    argument_parser.add_argument("--home", default=str(Path.home()), help="Home directory for allowlisted global discovery.")
    argument_parser.add_argument("--skill-root", action="append", default=[], help="Additional skill root to inspect; repeatable.")
    argument_parser.add_argument("--model", help="Caller-supplied model role for literal advisory comparison.")
    argument_parser.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES, help="Maximum discovered files to read (1-10000).")
    argument_parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="Maximum source bytes to read (1-67108864).")
    argument_parser.add_argument("--max-directories", type=int, default=DEFAULT_MAX_DIRECTORIES, help="Maximum project directories to traverse (1-10000).")
    argument_parser.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format.")
    return argument_parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parser().parse_args(argv)
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


if __name__ == "__main__":
    sys.exit(main())
