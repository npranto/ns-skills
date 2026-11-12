#!/usr/bin/env python3
"""route_corpus.py: the router corpus (tests/router-corpus.json) as a routing check. Standard library only.

    python3 scripts/route_corpus.py check               # the corpus itself is well-formed and is well-formed
    python3 scripts/route_corpus.py prompts             # one JSON line per request, to feed an agent that only has the skills
    python3 scripts/route_corpus.py score ANSWERS.json  # score answers {id: {"entry": "/ns-flow-x", "phases": ["scope-check", ...]}}

The corpus holds what the BASELINE router and WORKFLOWS.md did for about 60 requests: the first command, the phases that must
appear, and the phases that must not. Phase 7 asks an agent to route each request using only the new skills, then scores it here.
A request passes when the entry is one of the allowed ones, every must_include phase is present and no must_exclude phase is.
`include_if_entry` maps an allowed entry to phases required only when the answer chose that entry (a docs flow has no scope-check, a ticket flow does).
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "tests" / "router-corpus.json"
ENTRIES = {"/ns-route", "/ns-flow-new-project", "/ns-flow-existing-project", "/ns-flow-feature", "/ns-flow-ticket", "/ns-flow-delegate",
           "/ns-flow-bugfix", "/ns-flow-architecture", "/ns-flow-wayfinder", "/ns-flow-docs", "/ns-to-understand", "/ns-to-deploy"}
PHASES = {"start", "capture", "wayfinder", "grill", "discover", "architect", "design", "spec", "tickets", "split-ticket", "branch", "scope-check",
          "implement", "verify", "understand", "review", "quality-check", "integration-check", "stakeholder-brief", "postmortem", "save", "pr",
          "rollback", "deploy", "observe", "docs", "close", "mitigate-first", "verify:baseline", "diagnose", "research", "prototype", "security-review"}


def load() -> List[dict]:
    return json.loads(CORPUS.read_text(encoding="utf-8"))["requests"]


def ledger_ids() -> set:
    ids = set()
    for f in sorted((ROOT / "parity" / "ledger").glob("*.csv")):
        with f.open(newline="", encoding="utf-8") as fh:
            ids |= {r["id"] for r in csv.DictReader(fh)}
    return ids


def check(reqs: List[dict], ids: set) -> List[str]:
    errs: List[str] = []
    seen = set()
    for r in reqs:
        i = r.get("id", "?")
        if i in seen:
            errs.append("%s: duplicate id" % i)
        seen.add(i)
        e = r.get("expect", {})
        if not r.get("request"):
            errs.append("%s: empty request" % i)
        if not e.get("entry") or any(x not in ENTRIES for x in e["entry"]):
            errs.append("%s: entry must be a non-empty list of known commands" % i)
        for k in ("must_include", "must_exclude"):
            for p in e.get(k, []):
                if p not in PHASES:
                    errs.append("%s: unknown phase %r in %s" % (i, p, k))
        for ent, phs in e.get("include_if_entry", {}).items():
            if ent not in e.get("entry", []):
                errs.append("%s: include_if_entry names %s, which is not an allowed entry" % (i, ent))
            for p in phs:
                if p not in PHASES:
                    errs.append("%s: unknown phase %r in include_if_entry" % (i, p))
        if set(e.get("must_include", [])) & set(e.get("must_exclude", [])):
            errs.append("%s: a phase is both included and excluded" % i)
        if not r.get("source"):
            errs.append("%s: no ledger source" % i)
        if ids:
            for s in r.get("source", []):
                if s not in ids:
                    errs.append("%s: cites unknown ledger row %s" % (i, s))
    return errs


def score(reqs: List[dict], answers: Dict[str, dict]) -> List[str]:
    fails: List[str] = []
    for r in reqs:
        i, e = r["id"], r["expect"]
        a = answers.get(i)
        if a is None:
            fails.append("%s: no answer" % i)
            continue
        if a.get("entry") not in e["entry"]:
            fails.append("%s: entry %r not in %s" % (i, a.get("entry"), e["entry"]))
        got = set(a.get("phases", []))
        for p in e.get("must_include", []):
            if p not in got:
                fails.append("%s: missing phase %s" % (i, p))
        for p in e.get("include_if_entry", {}).get(a.get("entry"), []):
            if p not in got:
                fails.append("%s: missing phase %s (required for entry %s)" % (i, p, a.get("entry")))
        for p in e.get("must_exclude", []):
            if p in got:
                fails.append("%s: forbidden phase %s present" % (i, p))
    return fails


def main(argv: List[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "check"
    reqs = load()
    if cmd == "check":
        errs = check(reqs, ledger_ids())
        for e in errs:
            print("error:", e)
        print("%d requests, %d error(s)" % (len(reqs), len(errs)))
        return 1 if errs else 0
    if cmd == "prompts":
        for r in reqs:
            print(json.dumps({"id": r["id"], "request": r["request"]}))
        return 0
    if cmd == "score":
        answers = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
        fails = score(reqs, answers)
        for f in fails:
            print("FAIL:", f)
        print("%d of %d requests pass" % (len(reqs) - len({f.split(":")[0] for f in fails}), len(reqs)))
        return 1 if fails else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
