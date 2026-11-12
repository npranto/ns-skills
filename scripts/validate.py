#!/usr/bin/env python3
"""validate.py: structural validation for the ns-skills package. Standard library only, Python 3.9+.

    python3 scripts/validate.py                 # validate this package
    python3 scripts/validate.py --root DIR      # another checkout (or a fixture)
    python3 scripts/validate.py --strict        # warnings fail too

Strict frontmatter parser, call graph, link and reference checks, manifest checks, and these rules for ns-skills:
  - skills are manual-only, so `disable-model-invocation: true` is required and no "Use when" wording is imposed;
  - SKILL.md size budget 4.5 KB warn, 6.5 KB fail, with a written exception in the manifest;
  - the always-read core `ns-route/references/core.md` is capped at 13 KB;
  - every SKILL.md carries a `Read first:` line (which must include the core) and the set preflight;
  - every skill ships `agents/openai.yaml` with implicit invocation off, for Codex;
  - Claude-only concepts are confined to `topic-harnesses.md`, and no absolute home paths appear in skill text;
  - `.claude-plugin/plugin.json` and marketplace.json must agree with the manifest and the skills folders;
  - `migration.pending` in ns-skills.json (optional) lists skills not built yet; `--release` fails while any remain.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

HERE = Path(__file__).resolve().parent
PREFIX = "ns"
MAX_DESC = 1024
WARN_BYTES = 4500
MAX_BYTES = 6500
MAX_CORE_BYTES = 13 * 1024
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PREFLIGHT_MARK = "ns-skills is a set"
CORE_REL = "references/core.md"
HARNESS_FILE = "topic-harnesses.md"
FM_ALLOWED = {"name", "description", "disable-model-invocation", "argument-hint"}
# Never allowed in skill Markdown: absolute home paths and harness plumbing.
BANNED_EVERYWHERE = [
    "~/.claude", "~/.codex", "~/.agents", "~/.cursor", "${CLAUDE_", "$ARGUMENTS", "subagent_type", "mcp__",
    "TodoWrite", "SendMessage", "EnterPlanMode", "ExitPlanMode", "CLAUDE_SKILL_DIR", ".cursor/rules", "Task(",
    # old-layout leftovers: these files no longer exist, so any mention is a stale path
    "ns-shared/", "CONVENTIONS.md", "WORKFLOWS.md",
]
# Claude Code concepts: allowed only in the harness map, where each is mapped per harness (P3.4).
RESTRICTED = ["AskUserQuestion", "Skill tool", "Edit/Write", "ReportFindings", "claude -p", "allowed-tools", "disable-model-invocation"]
TEXT_SUFFIXES = {".md", ".py", ".json", ".txt", ".html", ".toml", ".yml", ".yaml", ".sh", ".csv"}
EM_DASH = chr(0x2014)
SKILL_NAME_RE = re.compile(r"\bns-(?:to|flow)-[a-z][a-z0-9]*(?:-[a-z0-9]+)*\b|\bns-route\b")
LINK_PATH_RE = re.compile(
    r"(?<![\w/.-])((?:\.\./)+[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*\.(?:md|py|json|ya?ml|html|sh)"
    r"|(?:references|scripts|assets)/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*\.(?:md|py|json|ya?ml|html|sh))")
MD_LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


class Report:
    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


# ------------------------------------------------------------ frontmatter

def parse_frontmatter(text: str) -> Tuple[Dict[str, str], str, List[str]]:
    """Strict subset: --- fence, single-line `key: value` pairs, double-quoted or plain values."""
    errs: List[str] = []
    if not text.startswith("---\n"):
        return {}, text, ["file must start with a --- frontmatter fence"]
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text, ["frontmatter is not closed with ---"]
    block, body = text[4:end], text[end + 5:]
    data: Dict[str, str] = {}
    for line in block.split("\n"):
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not m:
            errs.append("unparseable frontmatter line: %r" % line[:60])
            continue
        key, val = m.group(1), m.group(2).strip()
        if val.startswith('"'):
            try:
                val = json.loads(val)
            except ValueError:
                errs.append("%s: invalid double-quoted string" % key)
                continue
        elif val.startswith(("'", "|", ">", "[", "{")):
            errs.append("%s: use a single-line plain or double-quoted value" % key)
            continue
        if key in data:
            errs.append("duplicate key %s" % key)
        data[key] = val
    return data, body, errs


def skill_kind(name: str) -> Optional[str]:
    if name == PREFIX + "-route":
        return "route"
    if re.match(r"^%s-flow-[a-z0-9]" % PREFIX, name):
        return "flow"
    if re.match(r"^%s-to-[a-z0-9]" % PREFIX, name):
        return "phase"
    return None


def section(text: str, names: Tuple[str, ...]) -> str:
    m = re.search(r"^##\s+(?:%s)\b.*?(?=^## |\Z)" % "|".join(names), text, re.S | re.M)
    return m.group(0) if m else ""


def read_manifest(root: Path, rep: Report) -> Dict[str, Any]:
    mf = root / "ns-skills.json"
    if not mf.is_file():
        rep.err("ns-skills.json missing")
        return {}
    try:
        return json.loads(mf.read_text(encoding="utf-8"))
    except ValueError as e:
        rep.err("ns-skills.json: %s" % e)
        return {}


# ----------------------------------------------------------------- skills

def check_skills(skills_dir: Path, rep: Report, manifest: Dict[str, Any], pending: Set[str]) -> Dict[str, Dict[str, Any]]:
    dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith("."))
    names = [d.name for d in dirs]
    known = names + sorted(pending)
    exceptions = manifest.get("size_exceptions", {}) if isinstance(manifest.get("size_exceptions"), dict) else {}
    info: Dict[str, Dict[str, Any]] = {}
    for d in dirs:
        n = d.name
        kind = skill_kind(n)
        if kind is None or not NAME_RE.match(n) or len(n) > 64:
            rep.err("%s: name must be %s-route, %s-flow-<name>, or %s-to-<name> (lowercase, digits, single hyphens)" % (n, PREFIX, PREFIX, PREFIX))
        sm = d / "SKILL.md"
        if not sm.is_file():
            rep.err("%s: folder has no SKILL.md (a folder without one is not installed by skill-folder installers)" % n)
            continue
        text = sm.read_text(encoding="utf-8")
        fm, body, errs = parse_frontmatter(text)
        for e in errs:
            rep.err("%s: %s" % (n, e))
        extra = set(fm) - FM_ALLOWED
        if extra:
            rep.err("%s: unsupported frontmatter keys: %s" % (n, ", ".join(sorted(extra))))
        if fm.get("name") != n:
            rep.err("%s: frontmatter name %r must equal the folder name" % (n, fm.get("name")))
        desc = fm.get("description", "")
        if not desc:
            rep.err("%s: description missing" % n)
        if len(desc) > MAX_DESC:
            rep.err("%s: description is %d characters (max %d)" % (n, len(desc), MAX_DESC))
        if fm.get("disable-model-invocation") != "true":
            rep.err("%s: disable-model-invocation: true is required (skills are manual-only)" % n)
        size = len(text.encode("utf-8"))
        if size > MAX_BYTES:
            if n in exceptions and str(exceptions[n]).strip():
                rep.warn("%s: SKILL.md is %d bytes (max %d), allowed by a manifest exception" % (n, size, MAX_BYTES))
            else:
                rep.err("%s: SKILL.md is %d bytes (max %d); move detail to references/ or add a written size exception to ns-skills.json" % (n, size, MAX_BYTES))
        elif size > WARN_BYTES:
            rep.warn("%s: SKILL.md is %d bytes (aim for %d or fewer)" % (n, size, WARN_BYTES))
        if PREFLIGHT_MARK not in body:
            rep.err("%s: missing the set preflight (the line containing %r)" % (n, PREFLIGHT_MARK))
        yml = d / "agents" / "openai.yaml"
        if not yml.is_file():
            rep.err("%s: agents/openai.yaml missing (Codex would invoke this manual-only skill on its own)" % n)
        elif not re.search(r"^\s*allow_implicit_invocation:\s*false\s*$", yml.read_text(encoding="utf-8"), re.M):
            rep.err("%s: agents/openai.yaml must set policy.allow_implicit_invocation: false" % n)
        # Read first line
        rf = re.findall(r"^Read first:\s*(.+)$", body, re.M)
        if len(rf) != 1:
            rep.err("%s: needs exactly one 'Read first:' line listing its reference files in backticks" % n)
            read_first: List[str] = []
        else:
            read_first = re.findall(r"`([^`]+)`", rf[0])
            want = ["../%s-route/%s" % (PREFIX, CORE_REL)] + ([CORE_REL] if kind == "route" else [])
            if not any(w in read_first for w in want):
                rep.err("%s: 'Read first:' must include %s" % (n, want[0] if kind != "route" else CORE_REL))
            for rel in read_first:
                if not (d / rel).is_file():
                    rep.err("%s: 'Read first:' names a file that does not exist: %s" % (n, rel))
        calls_m = re.findall(r"^Calls:\s*(.*)$", body, re.M)
        calls: List[str] = []
        if kind in ("flow", "route") and len(calls_m) != 1:
            rep.err("%s: needs exactly one 'Calls:' line (comma-separated skill names, or 'none')" % n)
        elif len(calls_m) > 1:
            rep.err("%s: more than one 'Calls:' line" % n)
        if len(calls_m) == 1:
            raw = calls_m[0].strip()
            calls = [] if raw == "none" else [c.strip().strip("`") for c in raw.split(",") if c.strip()]
        info[n] = {"fm": fm, "calls": calls, "text": text, "body": body, "dir": d, "kind": kind, "read_first": read_first}
    route = PREFIX + "-route"
    for n, it in info.items():
        for c in it["calls"]:
            if c not in known:
                rep.err("%s: Calls names unknown skill %s" % (n, c))
            if c == n:
                rep.err("%s: calls itself" % n)
            if c == route:
                rep.err("%s: calls %s; only the user enters through the router" % (n, route))
    color: Dict[str, int] = {}

    def visit(n: str, path: List[str]) -> None:
        color[n] = 1
        for c in info.get(n, {}).get("calls", []):
            if c not in info:
                continue
            if color.get(c) == 1:
                rep.err("call cycle: %s" % " -> ".join(path + [n, c]))
            elif color.get(c) is None:
                visit(c, path + [n])
        color[n] = 2

    for n in info:
        if color.get(n) is None:
            visit(n, [])
    for n, it in info.items():
        if it["kind"] != "flow":
            continue
        seq = section(it["text"], ("Sequence", "Phases"))
        # only the phase table rows and list items count as running a skill; a paragraph that merely mentions one does not
        steps = "\n".join(l for l in seq.splitlines() if re.match(r"^\s*(\||\d+\.|[-*]\s)", l))
        used = {m for m in SKILL_NAME_RE.findall(steps) if m in known and m != n and m != route}
        for u in sorted(used - set(it["calls"])):
            rep.err("%s: the Sequence runs %s but Calls does not list it" % (n, u))
        for u in sorted(set(it["calls"]) - used):
            rep.warn("%s: Calls lists %s but the Sequence never runs it" % (n, u))
    if route in info:
        for n in names:
            if skill_kind(n) == "flow" and n not in info[route]["calls"]:
                rep.err("%s must list %s in Calls (the router can choose it)" % (route, n))
    return info


def md_files(skill_dir: Path) -> List[Path]:
    return sorted(f for f in skill_dir.rglob("*.md") if f.is_file())


def check_text(info: Dict[str, Dict[str, Any]], names: List[str], rep: Report, skills_dir: Path, pending: Set[str], external: Set[str] = frozenset()) -> None:
    for n, it in info.items():
        skill_dir: Path = it["dir"]
        for f in md_files(skill_dir):
            text = f.read_text(encoding="utf-8")
            rel = f.relative_to(skills_dir)
            for m in sorted(set(SKILL_NAME_RE.findall(text))):
                if m not in names and m not in pending:
                    rep.err("%s: mentions unknown skill %s" % (rel, m))
            for m in LINK_PATH_RE.finditer(text):
                token = m.group(1)
                if not any(c.exists() for c in (f.parent / token, skill_dir / token)):
                    if any(seg in pending or seg in external for seg in Path(token).parts):
                        continue  # a skill not migrated yet, or a required third-party skill named in the manifest
                    rep.err("%s: referenced path does not exist: %s" % (rel, token))
            unfenced = re.sub(r"(?s)(`{3,}|~{3}).*?\1", "", text)  # links inside code fences are template examples
            for m in MD_LINK_RE.finditer(unfenced):
                target = m.group(1)
                if re.match(r"^(https?:|mailto:|#)", target):
                    continue
                path = target.split("#", 1)[0]
                if path and not (f.parent / path).exists() and not any(seg in pending for seg in Path(path).parts):
                    rep.err("%s: broken markdown link %s" % (rel, target))
            for banned in BANNED_EVERYWHERE:
                if banned in text:
                    rep.err("%s: not portable, contains %r" % (rel, banned))
            if f.name != HARNESS_FILE:
                body = text
                if f.name == "SKILL.md":
                    body = text.split("\n---\n", 1)[-1] if text.startswith("---\n") else text
                for tok in RESTRICTED:
                    if tok in body:
                        rep.err("%s: %r is a Claude Code concept and belongs only in %s (say the capability instead)" % (rel, tok, HARNESS_FILE))
    core = skills_dir / (PREFIX + "-route") / CORE_REL
    if core.is_file() and core.stat().st_size > MAX_CORE_BYTES:
        rep.err("%s: core is %d bytes (max %d)" % (core.relative_to(skills_dir), core.stat().st_size, MAX_CORE_BYTES))


def check_scripts(root: Path, rep: Report) -> None:
    pys = list((root / "skills").rglob("*.py")) + list((root / "scripts").glob("*.py")) + list((root / "tests").glob("*.py")) + list((root / "parity" / "tools").glob("*.py"))
    # extensionless scripts with a python shebang (skills/<name>/scripts/ns)
    for p in sorted((root / "skills").glob("*/scripts/*")):
        if p.is_file() and not p.suffix:
            try:
                if p.read_text(encoding="utf-8").startswith("#!") and "python" in p.read_text(encoding="utf-8").split("\n", 1)[0]:
                    pys.append(p)
            except UnicodeDecodeError:
                pass
    for p in sorted(pys):
        try:
            ast.parse(p.read_text(encoding="utf-8"), filename=str(p))
        except SyntaxError as e:
            rep.err("%s: syntax error: %s" % (p.relative_to(root), e))


def check_style(root: Path, rep: Report) -> None:
    skip = {".git", "node_modules", "__pycache__"}
    skip_paths = {("parity", "baseline"), ("parity", "ledger"), ("parity", "reports"), ("tests", "fixtures", "broken")}
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root).parts
        dirnames[:] = [d for d in dirnames if d not in skip and (rel_dir + (d,)) not in skip_paths]
        for fn in filenames:
            p = Path(dirpath) / fn
            if p.suffix not in TEXT_SUFFIXES and fn not in ("LICENSE", "VERSION"):
                continue
            try:
                text = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if EM_DASH in text:
                rep.err("%s: contains an em dash; use a plain hyphen" % p.relative_to(root))


def check_map(root: Path, rep: Report, names: List[str]) -> None:
    """docs/workflow-map.html must list the same workflows as the catalog and a station for every phase skill (decision P3.8)."""
    mp = root / "docs" / "workflow-map.html"
    idx = root / "skills" / (PREFIX + "-route") / "references" / "workflows" / "index.md"
    if not mp.is_file() or not idx.is_file():
        return
    html = mp.read_text(encoding="utf-8")
    block = re.search(r"const WORKFLOWS = \[(.*?)\n\];", html, re.S)
    ids = set(re.findall(r'\{ id: "([a-z-]+)"', block.group(1))) if block else set()
    cat = set()
    for line in idx.read_text(encoding="utf-8").splitlines():
        if line.startswith("|"):
            cat |= set(re.findall(r"\[([a-z-]+)\]\([a-z-]+\.md(?:#[a-z-]+)?\)", line))
    for w in sorted(cat - ids):
        rep.err("docs/workflow-map.html: missing workflow %s from the catalog" % w)
    for w in sorted(ids - cat):
        rep.err("docs/workflow-map.html: lists workflow %s that the catalog does not" % w)
    info = re.search(r"const INFO = \{(.*?)\n\};", html, re.S)
    # a station is a phase when its command is /ns-to-<name>; other stations name a flow or the router
    mapped = set(re.findall(r'cmd: "/(%s-to-[a-z-]+)[ \"]' % PREFIX, info.group(1))) if info else set()
    phases = {n for n in names if skill_kind(n) == "phase"}
    for n in sorted(phases - mapped):
        rep.err("docs/workflow-map.html: no station for phase skill %s" % n)
    for n in sorted(mapped - phases):
        rep.err("docs/workflow-map.html: a station names %s, which is not a phase skill" % n)


def check_manifest(root: Path, manifest: Dict[str, Any], rep: Report, names: List[str]) -> None:
    if not manifest:
        return
    ver = (root / "VERSION").read_text(encoding="utf-8").strip() if (root / "VERSION").is_file() else None
    if manifest.get("name") != "ns-skills":
        rep.err("ns-skills.json: name must be ns-skills")
    if not re.match(r"^\d+\.\d+\.\d+$", str(manifest.get("version", ""))):
        rep.err("ns-skills.json: version must be MAJOR.MINOR.PATCH")
    if ver != manifest.get("version"):
        rep.err("VERSION (%s) and ns-skills.json (%s) disagree" % (ver, manifest.get("version")))
    if sorted(manifest.get("skills", [])) != sorted(names):
        rep.err("ns-skills.json skills do not match the skills/ folders")
    for rel in manifest.get("docs", []):
        if not (root / rel).is_file():
            rep.err("ns-skills.json lists missing file %s" % rel)
    exc = manifest.get("size_exceptions", {})
    if not isinstance(exc, dict):
        rep.err("ns-skills.json: size_exceptions must be an object of skill -> written reason")
    else:
        for k, v in exc.items():
            if k not in names:
                rep.err("ns-skills.json: size exception for unknown skill %s" % k)
            if not str(v).strip():
                rep.err("ns-skills.json: size exception for %s needs a written reason" % k)
    mig = manifest.get("migration", {})
    if mig and (not isinstance(mig.get("pending", []), list) or set(mig.get("pending", [])) & set(names)):
        rep.err("ns-skills.json: migration.pending must list only skills that are not in skills/ yet")
    if not isinstance(manifest.get("requirements"), dict):
        rep.err("ns-skills.json: requirements must be an object (plugins and tools, each with required_by)")
    plug = root / ".claude-plugin" / "plugin.json"
    mkt = root / ".claude-plugin" / "marketplace.json"
    for p in (plug, mkt):
        if not p.is_file():
            rep.err("%s missing" % p.relative_to(root))
    if plug.is_file():
        try:
            pj = json.loads(plug.read_text(encoding="utf-8"))
        except ValueError as e:
            rep.err(".claude-plugin/plugin.json: %s" % e)
            pj = {}
        if pj.get("name") != manifest.get("name"):
            rep.err(".claude-plugin/plugin.json: name differs from ns-skills.json")
        if pj.get("version") != manifest.get("version"):
            rep.err(".claude-plugin/plugin.json: version differs from ns-skills.json")
        if sorted(pj.get("skills", [])) != sorted("./skills/" + n for n in names):
            rep.err(".claude-plugin/plugin.json: skills list does not match the skills/ folders")
    if mkt.is_file():
        try:
            mj = json.loads(mkt.read_text(encoding="utf-8"))
        except ValueError as e:
            rep.err(".claude-plugin/marketplace.json: %s" % e)
            mj = {}
        if not any(p.get("name") == manifest.get("name") for p in mj.get("plugins", [])):
            rep.err(".claude-plugin/marketplace.json: does not list the plugin %s" % manifest.get("name"))


def check_parity(root: Path, rep: Report) -> None:
    tool = root / "parity" / "tools" / "ledger.py"
    if not tool.is_file():
        return
    for args in (["coverage", "--require-reviewed"], ["targets"]):
        r = subprocess.run([sys.executable, "-I", str(tool)] + args, cwd=str(root), capture_output=True, text=True)
        if r.returncode != 0:
            lines = [l for l in r.stdout.splitlines() if l.startswith("ERROR")][:20]
            rep.err("parity ledger %s failed:\n    %s" % (args[0], "\n    ".join(lines) or r.stdout.strip()[-300:] or r.stderr.strip()[-300:]))


# ------------------------------------------------------------------- main

def validate_package(root: Path, parity: bool = True, release: bool = False) -> Report:
    rep = Report()
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        rep.err("skills/ directory missing")
        return rep
    manifest = read_manifest(root, rep)
    pending = set(manifest.get("migration", {}).get("pending", [])) if isinstance(manifest.get("migration"), dict) else set()
    if release and pending:
        rep.err("release: %d skills are still pending migration (ns-skills.json migration.pending)" % len(pending))
    info = check_skills(skills_dir, rep, manifest, pending)
    names = sorted(p.name for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith("."))
    reqs = manifest.get("requirements", {}) if isinstance(manifest.get("requirements"), dict) else {}
    external = set(reqs.get("tools", {}) if isinstance(reqs.get("tools"), dict) else {}) | set(reqs.get("plugins", {}) if isinstance(reqs.get("plugins"), dict) else {})
    check_text(info, names, rep, skills_dir, pending, external)
    check_scripts(root, rep)
    check_style(root, rep)
    check_manifest(root, manifest, rep, names)
    check_map(root, rep, names)
    if parity:
        check_parity(root, rep)
    return rep


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", default=str(HERE.parent))
    p.add_argument("--no-parity", action="store_true")
    p.add_argument("--strict", action="store_true", help="treat warnings as errors")
    p.add_argument("--release", action="store_true", help="fail while any skill is still pending migration")
    a = p.parse_args(argv)
    rep = validate_package(Path(a.root).resolve(), parity=not a.no_parity, release=a.release)
    for w in rep.warnings:
        print("warning: " + w)
    for e in rep.errors:
        print("error: " + e)
    print("%d error(s), %d warning(s)" % (len(rep.errors), len(rep.warnings)))
    return 1 if rep.errors or (a.strict and rep.warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
