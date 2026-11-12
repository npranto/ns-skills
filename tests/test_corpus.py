"""Tests for the router corpus and its scorer."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import route_corpus as rc  # noqa: E402


def perfect(reqs):
    return {r["id"]: {"entry": r["expect"]["entry"][0], "phases": list(r["expect"]["must_include"])} for r in reqs}


class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.reqs = rc.load()

    def test_corpus_is_well_formed_and_cites_real_ledger_rows(self):
        self.assertEqual(rc.check(self.reqs, rc.ledger_ids()), [])

    def test_corpus_covers_every_task_type_and_every_entry_command(self):
        types = {r["expect"]["task_type"] for r in self.reqs}
        for t in ["greenfield", "onboard", "feature", "ticket", "bug", "incident", "refactor", "restructure", "stack-move", "rebuild", "modernize", "architecture",
                  "performance", "dependency", "migration", "infrastructure", "spike", "proposal", "docs", "pr-review", "ship", "wayfinder"]:
            self.assertIn(t, types)
        entries = {e for r in self.reqs for e in r["expect"]["entry"]}
        self.assertEqual(entries, rc.ENTRIES)
        self.assertGreaterEqual(len(self.reqs), 60)

    def test_perfect_answers_pass(self):
        self.assertEqual(rc.score(self.reqs, perfect(self.reqs)), [])

    def test_wrong_entry_is_caught(self):
        a = perfect(self.reqs)
        a["bug-emoji"]["entry"] = "/ns-flow-feature"
        self.assertTrue(any("bug-emoji: entry" in f for f in rc.score(self.reqs, a)))

    def test_missing_phase_is_caught(self):
        a = perfect(self.reqs)
        a["incident-checkout"]["phases"].remove("mitigate-first")
        self.assertTrue(any("incident-checkout: missing phase mitigate-first" in f for f in rc.score(self.reqs, a)))

    def test_forbidden_phase_is_caught(self):
        a = perfect(self.reqs)
        a["spike-sqlite"]["phases"].append("pr")
        self.assertTrue(any("spike-sqlite: forbidden phase pr" in f for f in rc.score(self.reqs, a)))

    def test_phase_required_only_for_its_entry(self):
        a = perfect(self.reqs)
        a["docs-typo"] = {"entry": "/ns-flow-docs", "phases": ["branch", "docs", "save"]}
        self.assertEqual([f for f in rc.score(self.reqs, a) if f.startswith("docs-typo")], [])
        a["docs-typo"] = {"entry": "/ns-flow-ticket", "phases": ["branch", "implement", "save"]}
        self.assertTrue(any("docs-typo: missing phase scope-check" in f for f in rc.score(self.reqs, a)))

    def test_missing_answer_is_caught(self):
        a = perfect(self.reqs)
        del a["menu"]
        self.assertTrue(any("menu: no answer" in f for f in rc.score(self.reqs, a)))

    def test_bad_corpus_entry_is_caught(self):
        bad = [{"id": "x", "request": "r", "expect": {"entry": ["/nope"], "must_include": ["ghost"], "must_exclude": []}, "source": []}]
        errs = rc.check(bad, set())
        self.assertTrue(any("entry must be" in e for e in errs))
        self.assertTrue(any("unknown phase" in e for e in errs))
        self.assertTrue(any("no ledger source" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
