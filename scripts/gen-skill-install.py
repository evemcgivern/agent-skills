#!/usr/bin/env python3
"""Write the `## Install` section of every skill README from compatibility.json.

Each section is one collapsed <details> block per platform, between
<!-- install:begin --> and <!-- install:end -->. Skill-specific facts live in
EXTRAS below. Running it twice changes nothing.

Usage:
  python3 -I scripts/gen-skill-install.py           # rewrite the READMEs
  python3 -I scripts/gen-skill-install.py --check   # exit 1 if any README is stale
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BEGIN = "<!-- install:begin -->"
END = "<!-- install:end -->"
MARKETPLACE = "evemcgivern-skills"
REPO = "evemcgivern/agent-skills"
CLONE = f"git clone https://github.com/{REPO}.git && cd agent-skills"
ROOT_INSTALL = "../../../../README.md#install"
DEMO_ESTATE = f"https://github.com/{REPO}/tree/main/plugins/app-governance-kit/demo-estate"
KIT_SITE = "https://evemcgivern.github.io/app-governance-kit/"
CHATGPT_HELP = "https://help.openai.com/en/articles/20001066-skills-in-chatgpt"
CODEX_DOCS = "https://developers.openai.com/codex/skills-and-plugins"

# Platform keys in display order, with the summary text and the compatibility.json cell.
PLATFORMS = [
    ("cli", "Claude Code (terminal CLI)", ("claude", "code")),
    ("desktop", "Claude Code desktop app", ("claude", "code")),
    ("codex", "Codex (CLI, IDE extension, desktop app)", ("codex_chatgpt", "codex")),
    ("other", "Other agents: Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, Windsurf, OpenCode, Cline", ("other", None)),
    ("app", "Claude app (claude.ai)", ("claude", "app")),
    ("chatgpt", "ChatGPT", ("codex_chatgpt", "chatgpt")),
]
SHORT_NAME = {"cli": "Claude Code (terminal CLI)", "desktop": "Claude Code desktop app", "codex": "Codex",
              "other": "Other agents", "app": "Claude app", "chatgpt": "ChatGPT"}

KIT_ALL = "access-review ai-intake app-governance cert-prep crosswalk hardware-lifecycle itam-maturity program-setup rationalization"
KIT_SITE_LINE = f"The kit's full site, with visuals and an interactive practicum: {KIT_SITE}"
KIT_SKILLS = KIT_ALL.split()

# Skill-specific facts. Keys are platform keys (lines added at the end of that
# section), "sections" (extra <details> blocks after the platforms) and
# "footer" (always-visible lines after every <details> block).
EXTRAS = {
    "efficient-frontier-routing": {
        "footer": [
            "Routing needs a host that lets you pick the model for each subagent. Claude Code, Codex, Gemini CLI, Antigravity CLI, Cursor and OpenCode document this. The Claude app and ChatGPT have no documented subagents, and GitHub Copilot, Windsurf and Cline are not verified; there the skill reports that it cannot route instead of routing.",
        ],
    },
    "fable-chief-agent": {
        "footer": [
            "The delegation needs subagents on a chosen model: Claude Code, Codex, Gemini CLI and Antigravity CLI have them; other agents are not verified.",
        ],
    },
    "handoff": {
        "other": [
            "The git and GitHub checks work in any local agent, and the project name comes from `CLAUDE.md`, `AGENTS.md` or `GEMINI.md`, whichever exists.",
        ],
    },
    "orchestrator": {
        "footer": [
            "The dispatcher needs subagents. Claude Code runs them in the background. Codex runs them in parallel but can hold its reply until they finish. In other agents, where work cannot run in the background, the skill says so and runs small batches.",
        ],
    },
    "stay-within-limits": {
        "footer": [
            "The usage checks (`ccusage` and `/usage`) read Claude Code only: in Codex and other agents it still runs work in waves, but you supply the usage numbers and no automatic wake-up is documented for those agents.",
        ],
    },
    "clearly": {
        "footer": [
            "The `--explain` video needs a local install: on a computer, the skill asks before installing `manim` and `ffmpeg`. In the Claude app and ChatGPT the writing rules work, and `--explain` uses a diagram or page instead.",
        ],
    },
    "app-governance": {
        "cli": [
            f"The router runs the kit's other skills, so all nine must be installed together. The plugin install does that. For single-skill copies, copy all nine: `scripts/install.sh {KIT_ALL}`.",
        ],
        "codex": [
            f"The router runs the kit's other skills, so install all nine together: `scripts/install.sh --target codex {KIT_ALL}`.",
        ],
        "other": [
            "The router runs the kit's other skills, so copy all nine kit skill folders into the same skills folder.",
        ],
        "app": [
            "Upload all nine kit skills, one ZIP each, so the router can run the one it picks.",
        ],
        "chatgpt": [
            "In ChatGPT each kit skill is a separate upload, and opening a second skill from this router is not verified, so it names the skill for you to open instead.",
        ],
        "footer": [
            f"With no data of your own, the router offers the fictional Halden demo estate. A single-skill install does not include it; download the files from [`demo-estate/`]({DEMO_ESTATE}).",
        ],
    },
    "cert-prep": {
        "footer": [
            f"Drills use the kit's fictional Halden demo estate. A single-skill install or upload does not include it: download the files from [`demo-estate/`]({DEMO_ESTATE}) and attach them to the session.",
        ],
    },
    "role-ready-application": {
        "cli": [
            "Start a session and ask, for example, \"tailor my resume to this job\", then paste the job description. Or run `/role-ready-application:role-ready-application`.",
            "Check it worked: `claude plugin list` shows `role-ready-application@evemcgivern-skills` as enabled.",
        ],
        "desktop": [
            "Then ask for a resume or cover letter tailored to a job.",
        ],
        "codex": [
            "Restart Codex if the skill does not appear.",
        ],
        "app": [
            "Start a chat and attach your resume and the job description.",
            "To update, delete the skill and upload the new ZIP.",
        ],
        "chatgpt": [
            "In a chat, type `@` to pick the skill, and attach your resume and the job description.",
            "No skill upload on your plan? Open a new chat or a project and paste the contents of [`COPY-PASTE.txt`](COPY-PASTE.txt) as the instructions, then attach your documents. It is the same workflow as one plain-text file.",
            "OpenAI does not list the file types the skill upload accepts, so the ZIP route is untested here.",
        ],
        "sections": [
            ("Any other assistant", [
                "1. Paste [`COPY-PASTE.txt`](COPY-PASTE.txt) at the start of a chat.",
                "2. Attach your resume and the job description, and ask for a tailored resume or cover letter.",
            ]),
        ],
        "footer": [
            "The skill works only with what you give it in the conversation. It does not need access to email, contacts or connected accounts.",
        ],
    },
}
for _kit_skill in KIT_SKILLS:
    EXTRAS.setdefault(_kit_skill, {}).setdefault("footer", []).append(KIT_SITE_LINE)


def details(summary, body_lines):
    return ["<details>", f"<summary>{summary}</summary>", "", *body_lines, "</details>"]


def cell(entry, where):
    col, sub = where
    c = entry[col] if sub is None else entry[col][sub]
    return c["level"], (c.get("note") or "").strip()


def summary_for(key, label, level, recommended=False):
    if level == "no":
        return f"<b>{SHORT_NAME[key]}: not supported</b>"
    text = f"<b>{label}</b>"
    if recommended:
        text += " — recommended"
    if level == "partial":
        text += " — works with a limit"
    return text


def platform_body(key, skill, plugin, siblings, level, note, extra):
    """Markdown lines inside one platform's <details> block."""
    if level == "no":
        return [note, "", "Use Claude Code or Codex on your computer instead.", ""]

    lines = []
    if key == "cli":
        if siblings:
            others = ", ".join(f"`{s}`" for s in siblings)
            also = f"This installs the whole `{plugin}` plugin, so you also get its other skills: {others}."
        else:
            also = f"The `{plugin}` plugin holds only this skill."
        lines += [
            "```bash",
            f"claude plugin marketplace add {REPO}",
            f"claude plugin install {plugin}@{MARKETPLACE}",
            "```",
            "",
            f"{also} Run it as `/{plugin}:{skill}`. Inside a session, the same thing is `/plugin marketplace add {REPO}`, then `/plugin install {plugin}@{MARKETPLACE}`.",
            "",
            f"Update later with `claude plugin marketplace update {MARKETPLACE}`, then `claude plugin update {plugin}@{MARKETPLACE}`.",
            "",
            "To install only this skill, copy it from a clone of the repo:",
            "",
            "```bash",
            CLONE,
            f"scripts/install.sh {skill}   # into ~/.claude/skills/{skill}",
            "```",
            "",
            "Add `--project <repo-path>` for one repository only, or `--force` to replace a copy you already have.",
            "",
        ]
    elif key == "desktop":
        lines += [
            f"In a local Code session choose **+ → Plugins → Add plugin**, enter `{REPO}` as the marketplace, then install **{plugin}**"
            + (" (it brings the plugin's other skills too)." if siblings else "."),
            "",
            f"Local desktop and CLI sessions share user-scope installs. Cloud Code sessions do not load local plugins; commit this skill folder to your repository's `.claude/skills/{skill}/` instead.",
            "",
        ]
    elif key == "codex":
        lines += [
            "```bash",
            CLONE,
            f"scripts/install.sh --target codex {skill}   # into ~/.agents/skills/{skill}",
            "```",
            "",
            f"Add `--project <repo-path>` to install into that repository's `.agents/skills/{skill}/` instead. Or copy this folder by hand to `~/.agents/skills/{skill}/`, or `.agents/skills/{skill}/` in a repository; keep every file in it together. Start a new session and invoke the skill by name. See the [Codex skills docs]({CODEX_DOCS}).",
            "",
        ]
    elif key == "other":
        lines += [
            "These agents load `SKILL.md` folders directly. Copy this whole folder to the place your agent reads:",
            "",
            f"- Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, OpenCode: `~/.agents/skills/{skill}/` for personal use (`scripts/install.sh --target codex {skill}` does this), or `<repo>/.agents/skills/{skill}/` for one repository.",
            f"- Windsurf: `<repo>/.agents/skills/{skill}/`.",
            f"- Cline: `<repo>/.cline/skills/{skill}/`, `<repo>/.claude/skills/{skill}/` or `~/.cline/skills/{skill}/`.",
            "",
        ]
    elif key == "app":
        lines += [
            "1. Zip this folder from a clone of the repo (the ZIP must contain the folder itself, with `SKILL.md` inside):",
            "   ```bash",
            f"   cd plugins/{plugin}/skills && zip -r {skill}.zip {skill}",
            "   ```",
            "2. Turn on code execution under **Settings → Capabilities**.",
            f"3. Open **Customize → Skills → + → Create skill → Upload a skill** and upload `{skill}.zip`.",
            "",
            "On Enterprise, an owner must first enable skills under Organization settings. The same upload works in Claude Cowork. Local `~/.claude/skills/` files do not sync to Claude.ai, so the upload is needed; or commit the folder to a project repository's `.claude/skills/`.",
            "",
        ]
    elif key == "chatgpt":
        lines += [
            "1. Skills in ChatGPT are in beta and available on Business, Enterprise, Edu, Teachers and Healthcare plans, not on personal Free, Plus or Pro plans. On Enterprise and Edu, a workspace admin must first turn skills on and allow skill uploading.",
            "2. Zip this folder (the ZIP must contain the folder itself, with `SKILL.md` inside):",
            "   ```bash",
            f"   cd plugins/{plugin}/skills && zip -r {skill}.zip {skill}",
            "   ```",
            "3. Open the **Plugins → Skills** tab, choose **+ → Upload from your computer** and upload the ZIP. ChatGPT scans each upload and can mark it Needs Review or Blocked.",
            "",
            f"The web and desktop apps do not sync skills. Menu labels change, so OpenAI's [Skills in ChatGPT]({CHATGPT_HELP}) article is the source of truth. ChatGPT runs skills in a remote sandbox with no access to your local files, repo or local shell. On other plans, use Codex, which reads skill folders directly.",
            "",
        ]
    if level == "partial":
        lines += [f"**Limit:** {note}", ""]
    for line in extra.get(key, []):
        lines += [line, ""]
    return lines


def render(skill, plugin, siblings, entry):
    extra = EXTRAS.get(skill, {})
    out = [
        BEGIN,
        f"Pick your platform. Steps expand below. The [Install section of the collection README]({ROOT_INSTALL}) has the full guide.",
        "",
    ]
    for i, (key, label, where) in enumerate(PLATFORMS):
        level, note = cell(entry, where)
        out += details(
            summary_for(key, label, level, recommended=(i == 0)),
            platform_body(key, skill, plugin, siblings, level, note, extra),
        ) + [""]
    for summary, body in extra.get("sections", []):
        out += details(f"<b>{summary}</b>", [*body, ""]) + [""]
    for line in extra.get("footer", []):
        out += [line, ""]
    out.append(END)
    return "\n".join(out)


INSTALL_SECTION = re.compile(r"(^## Install[ \t]*\n)(.*?)(?=^## |\Z)", re.S | re.M)
MARKED = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)


def updated_readme(text, block):
    if BEGIN in text and END in text:
        return MARKED.sub(lambda _: block, text, count=1)
    m = INSTALL_SECTION.search(text)
    if not m:
        raise ValueError("no '## Install' section")
    tail = "\n\n" if text[m.end():] else "\n"
    return text[: m.start()] + m.group(1) + "\n" + block + tail + text[m.end():]


def skills():
    """(skill, plugin, siblings, readme path) for every skill folder."""
    out = []
    for d in sorted(p for p in ROOT.glob("plugins/*/skills/*") if p.is_dir()):
        plugin = d.parent.parent.name
        siblings = sorted(p.name for p in d.parent.iterdir() if p.is_dir() and p.name != d.name)
        out.append((d.name, plugin, siblings, d / "README.md"))
    return out


def expected():
    """Map each README path to the text it should have."""
    data = json.loads((ROOT / "compatibility.json").read_text(encoding="utf-8"))["skills"]
    result = {}
    for skill, plugin, siblings, readme in skills():
        block = render(skill, plugin, siblings, data[skill])
        result[readme] = updated_readme(readme.read_text(encoding="utf-8"), block)
    return result


def main(argv):
    check = "--check" in argv[1:]
    stale = []
    for readme, want in expected().items():
        if readme.read_text(encoding="utf-8") == want:
            continue
        stale.append(readme.relative_to(ROOT))
        if not check:
            readme.write_text(want, encoding="utf-8")
    if check:
        for path in stale:
            print(f"stale install section: {path}", file=sys.stderr)
        if stale:
            print("run: python3 -I scripts/gen-skill-install.py", file=sys.stderr)
        return 1 if stale else 0
    print(f"updated {len(stale)} README(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
