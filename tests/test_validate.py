"""Tests for scripts/validate.py: the intact fixture passes, and each rule fails when deliberately broken.

    python3 -m unittest discover -s tests
"""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate  # noqa: E402

GOOD = ROOT / "tests" / "fixtures" / "pkg-good"


class Pkg:
    """A throwaway copy of the good fixture that a test can break."""

    def __enter__(self):
        self.tmp = tempfile.mkdtemp(prefix="nspkg-")
        self.root = Path(self.tmp) / "pkg"
        shutil.copytree(GOOD, self.root)
        return self

    def __exit__(self, *a):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def path(self, rel):
        return self.root / rel

    def read(self, rel):
        return self.path(rel).read_text(encoding="utf-8")

    def write(self, rel, text):
        p = self.path(rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def sub(self, rel, old, new):
        t = self.read(rel)
        assert old in t, "test setup: %r not in %s" % (old, rel)
        self.write(rel, t.replace(old, new, 1))

    def json_edit(self, rel, fn):
        d = json.loads(self.read(rel))
        fn(d)
        self.write(rel, json.dumps(d, indent=2))

    def run(self):
        return validate.validate_package(self.root, parity=False)


class ValidateTests(unittest.TestCase):
    def assertFails(self, pkg, needle):
        rep = pkg.run()
        self.assertTrue(any(needle in e for e in rep.errors), "expected an error containing %r, got %r" % (needle, rep.errors))

    def test_good_fixture_is_clean(self):
        with Pkg() as p:
            rep = p.run()
            self.assertEqual(rep.errors, [])
            self.assertEqual(rep.warnings, [])

    def test_real_package_is_clean(self):
        rep = validate.validate_package(ROOT, parity=True)
        self.assertEqual(rep.errors, [])

    # --- frontmatter and names
    def test_name_must_match_folder(self):
        with Pkg() as p:
            p.sub("skills/ns-to-demo/SKILL.md", "name: ns-to-demo", "name: ns-to-other")
            self.assertFails(p, "must equal the folder name")

    def test_manual_only_is_required(self):
        with Pkg() as p:
            p.sub("skills/ns-to-demo/SKILL.md", "disable-model-invocation: true\n", "")
            self.assertFails(p, "disable-model-invocation: true is required")

    def test_unknown_frontmatter_key(self):
        with Pkg() as p:
            p.sub("skills/ns-to-demo/SKILL.md", "description:", "model: opus\ndescription:")
            self.assertFails(p, "unsupported frontmatter keys")

    def test_bad_skill_name(self):
        with Pkg() as p:
            shutil.copytree(p.path("skills/ns-to-demo"), p.path("skills/helper"))
            self.assertFails(p, "name must be ns-route")

    def test_folder_without_skill_md(self):
        with Pkg() as p:
            p.path("skills/ns-shared").mkdir()
            p.write("skills/ns-shared/delegate.md", "x")
            self.assertFails(p, "folder has no SKILL.md")

    # --- size budgets
    def test_skill_md_over_budget(self):
        with Pkg() as p:
            p.write("skills/ns-to-demo/SKILL.md", p.read("skills/ns-to-demo/SKILL.md") + "x" * 7000 + "\n")
            self.assertFails(p, "SKILL.md is")

    def test_size_exception_allows_over_budget_with_reason(self):
        with Pkg() as p:
            p.write("skills/ns-to-demo/SKILL.md", p.read("skills/ns-to-demo/SKILL.md") + "x" * 7000 + "\n")
            p.json_edit("ns-skills.json", lambda d: d["size_exceptions"].update({"ns-to-demo": "the router-like table must stay whole"}))
            rep = p.run()
            self.assertEqual(rep.errors, [])
            self.assertTrue(any("manifest exception" in w for w in rep.warnings))

    def test_size_exception_needs_a_reason(self):
        with Pkg() as p:
            p.json_edit("ns-skills.json", lambda d: d["size_exceptions"].update({"ns-to-demo": " "}))
            self.assertFails(p, "needs a written reason")

    def test_core_over_13kb(self):
        with Pkg() as p:
            p.write("skills/ns-route/references/core.md", "x" * (13 * 1024 + 1))
            self.assertFails(p, "core is")

    # --- preflight, read first, codex policy
    def test_missing_preflight(self):
        with Pkg() as p:
            p.sub("skills/ns-to-demo/SKILL.md", "Preflight: ns-skills is a set.", "Preflight: n/a.")
            self.assertFails(p, "missing the set preflight")

    def test_missing_read_first(self):
        with Pkg() as p:
            p.sub("skills/ns-to-demo/SKILL.md", "Read first: `../ns-route/references/core.md`\n", "")
            self.assertFails(p, "needs exactly one 'Read first:'")

    def test_read_first_must_include_core(self):
        with Pkg() as p:
            p.sub("skills/ns-to-demo/SKILL.md", "`../ns-route/references/core.md`", "`../ns-route/references/topic-harnesses.md`")
            self.assertFails(p, "must include ../ns-route/references/core.md")

    def test_read_first_file_must_exist(self):
        with Pkg() as p:
            p.sub("skills/ns-to-demo/SKILL.md", "Read first: `../ns-route/references/core.md`", "Read first: `../ns-route/references/core.md`, `../ns-route/references/missing.md`")
            self.assertFails(p, "does not exist: ../ns-route/references/missing.md")

    def test_missing_openai_yaml(self):
        with Pkg() as p:
            p.path("skills/ns-to-demo/agents/openai.yaml").unlink()
            self.assertFails(p, "agents/openai.yaml missing")

    def test_openai_yaml_must_disable_implicit_invocation(self):
        with Pkg() as p:
            p.write("skills/ns-to-demo/agents/openai.yaml", "policy:\n  allow_implicit_invocation: true\n")
            self.assertFails(p, "allow_implicit_invocation: false")

    # --- links and references
    def test_broken_relative_path(self):
        with Pkg() as p:
            p.write("skills/ns-to-demo/SKILL.md", p.read("skills/ns-to-demo/SKILL.md") + "\nSee `references/nothing.md`.\n")
            self.assertFails(p, "referenced path does not exist: references/nothing.md")

    def test_broken_markdown_link(self):
        with Pkg() as p:
            p.write("skills/ns-to-demo/SKILL.md", p.read("skills/ns-to-demo/SKILL.md") + "\n[gone](nope.md)\n")
            self.assertFails(p, "broken markdown link")

    def test_link_inside_a_code_fence_is_a_template_not_a_link(self):
        with Pkg() as p:
            p.write("skills/ns-to-demo/SKILL.md", p.read("skills/ns-to-demo/SKILL.md") + "\n```markdown\n[example](wayfinder/01-slug.md)\n```\n")
            self.assertEqual(p.run().errors, [])

    def test_unknown_skill_mention(self):
        with Pkg() as p:
            p.write("skills/ns-to-demo/SKILL.md", p.read("skills/ns-to-demo/SKILL.md") + "\nSuggest /ns-to-nothing next.\n")
            self.assertFails(p, "mentions unknown skill ns-to-nothing")

    # --- call graph
    def test_flow_needs_calls_line(self):
        with Pkg() as p:
            p.sub("skills/ns-flow-demo/SKILL.md", "Calls: ns-to-demo\n", "")
            self.assertFails(p, "needs exactly one 'Calls:' line")

    def test_calls_unknown_skill(self):
        with Pkg() as p:
            p.sub("skills/ns-flow-demo/SKILL.md", "Calls: ns-to-demo", "Calls: ns-to-demo, ns-to-ghost")
            self.assertFails(p, "Calls names unknown skill ns-to-ghost")

    def test_sequence_must_match_calls(self):
        with Pkg() as p:
            p.sub("skills/ns-flow-demo/SKILL.md", "Calls: ns-to-demo", "Calls: none")
            self.assertFails(p, "the Sequence runs ns-to-demo but Calls does not list it")

    def test_a_paragraph_mention_is_not_a_call(self):
        with Pkg() as p:
            p.write("skills/ns-flow-demo/SKILL.md", p.read("skills/ns-flow-demo/SKILL.md") + "\nIn delegate mode the other flow ns-to-demo may be prompted.\n")
            self.assertEqual(p.run().errors, [])

    def test_call_cycle(self):
        with Pkg() as p:
            shutil.copytree(p.path("skills/ns-flow-demo"), p.path("skills/ns-flow-other"))
            p.sub("skills/ns-flow-other/SKILL.md", "name: ns-flow-demo", "name: ns-flow-other")
            p.sub("skills/ns-flow-other/SKILL.md", "Calls: ns-to-demo", "Calls: ns-flow-demo")
            p.sub("skills/ns-flow-other/SKILL.md", "`ns-to-demo`", "`ns-flow-demo`")
            p.sub("skills/ns-flow-demo/SKILL.md", "Calls: ns-to-demo", "Calls: ns-to-demo, ns-flow-other")
            p.sub("skills/ns-flow-demo/SKILL.md", "| 1 | `ns-to-demo` |", "| 1 | `ns-to-demo` |\n| 2 | `ns-flow-other` |")
            self.assertFails(p, "call cycle")

    def test_router_must_list_every_flow(self):
        with Pkg() as p:
            p.sub("skills/ns-route/SKILL.md", "Calls: ns-flow-demo", "Calls: none")
            self.assertFails(p, "must list ns-flow-demo in Calls")

    def test_nothing_calls_the_router(self):
        with Pkg() as p:
            p.sub("skills/ns-to-demo/SKILL.md", "Do the job", "Calls: ns-route\nDo the job")
            self.assertFails(p, "only the user enters through the router")

    # --- portability and style
    def test_home_path_is_banned(self):
        with Pkg() as p:
            p.write("skills/ns-to-demo/SKILL.md", p.read("skills/ns-to-demo/SKILL.md") + "\nRead ~/.claude/skills/x.\n")
            self.assertFails(p, "not portable, contains '~/.claude'")

    def test_old_layout_paths_are_stale(self):
        for mention, token in (("ns-shared/delegate.md", "ns-shared/"), ("CONVENTIONS.md", "CONVENTIONS.md"), ("WORKFLOWS.md", "WORKFLOWS.md")):
            with Pkg() as p:
                p.write("skills/ns-to-demo/SKILL.md", p.read("skills/ns-to-demo/SKILL.md") + "\nSee %s.\n" % mention)
                self.assertFails(p, "not portable, contains %r" % token)

    def test_claude_concept_outside_harness_file(self):
        with Pkg() as p:
            p.write("skills/ns-to-demo/SKILL.md", p.read("skills/ns-to-demo/SKILL.md") + "\nAsk via AskUserQuestion.\n")
            self.assertFails(p, "belongs only in topic-harnesses.md")

    def test_claude_concept_allowed_in_harness_file(self):
        with Pkg() as p:
            rep = p.run()  # the fixture's topic-harnesses.md already names AskUserQuestion
            self.assertEqual(rep.errors, [])

    def test_em_dash_is_banned(self):
        with Pkg() as p:
            p.write("skills/ns-route/references/core.md", p.read("skills/ns-route/references/core.md") + "A " + chr(0x2014) + " B\n")
            self.assertFails(p, "em dash")

    def test_python_syntax_error(self):
        with Pkg() as p:
            p.write("skills/ns-route/scripts/bad.py", "def (:\n")
            self.assertFails(p, "syntax error")

    def test_link_into_a_required_third_party_skill_is_allowed(self):
        with Pkg() as p:
            p.write("skills/ns-to-demo/SKILL.md", p.read("skills/ns-to-demo/SKILL.md") + "\nRead `../herdr/SKILL.md`.\n")
            self.assertFails(p, "referenced path does not exist: ../herdr/SKILL.md")
            p.json_edit("ns-skills.json", lambda d: d["requirements"]["tools"].update({"herdr": {"required_by": ["ns-to-demo"]}}))
            self.assertEqual(p.run().errors, [])

    # --- the workflow map
    MAP = 'const WORKFLOWS = [\n  { id: "demo", code: "DM" },\n];\nconst INFO = {\n  demo: { cmd: "/ns-to-demo [x]", does: "d" },\n  plan: { cmd: "/ns-flow-demo", does: "a flow station" },\n};\n'

    def with_map(self, p, html=None):
        p.write("skills/ns-route/references/workflows/index.md", "# Workflows\n\n| You have | Workflow |\n|---|---|\n| A demo | [demo](demo.md) |\n")
        p.write("skills/ns-route/references/workflows/demo.md", "# demo\n")
        p.write("docs/workflow-map.html", html if html is not None else self.MAP)

    def test_map_in_sync_is_clean(self):
        with Pkg() as p:
            self.with_map(p)
            self.assertEqual(p.run().errors, [])

    def test_map_missing_a_workflow(self):
        with Pkg() as p:
            self.with_map(p, self.MAP.replace('{ id: "demo", code: "DM" },', ''))
            self.assertFails(p, "missing workflow demo from the catalog")

    def test_map_with_an_extra_workflow(self):
        with Pkg() as p:
            self.with_map(p, self.MAP.replace('{ id: "demo", code: "DM" },', '{ id: "demo", code: "DM" },\n  { id: "ghost", code: "GH" },'))
            self.assertFails(p, "lists workflow ghost that the catalog does not")

    def test_map_missing_a_phase_station(self):
        with Pkg() as p:
            self.with_map(p, self.MAP.replace('  demo: { cmd: "/ns-to-demo [x]", does: "d" },\n', ''))
            self.assertFails(p, "no station for phase skill ns-to-demo")

    def test_map_station_for_an_unknown_skill(self):
        with Pkg() as p:
            self.with_map(p, self.MAP.replace('  plan:', '  ghost: { cmd: "/ns-to-ghost", does: "x" },\n  plan:'))
            self.assertFails(p, "a station names ns-to-ghost")

    # --- migration
    def test_pending_skill_mentions_are_allowed_during_migration(self):
        with Pkg() as p:
            p.write("skills/ns-to-demo/SKILL.md", p.read("skills/ns-to-demo/SKILL.md") + "\nSuggest /ns-to-later next, see `../ns-to-later/references/x.md`.\n")
            self.assertFails(p, "mentions unknown skill ns-to-later")
            p.json_edit("ns-skills.json", lambda d: d.update(migration={"pending": ["ns-to-later"]}))
            self.assertEqual(p.run().errors, [])

    def test_release_fails_while_skills_are_pending(self):
        with Pkg() as p:
            p.json_edit("ns-skills.json", lambda d: d.update(migration={"pending": ["ns-to-later"]}))
            rep = validate.validate_package(p.root, parity=False, release=True)
            self.assertTrue(any("still pending migration" in e for e in rep.errors))

    def test_pending_list_cannot_name_an_existing_skill(self):
        with Pkg() as p:
            p.json_edit("ns-skills.json", lambda d: d.update(migration={"pending": ["ns-to-demo"]}))
            self.assertFails(p, "migration.pending must list only skills that are not in skills/")

    def test_extensionless_python_script_syntax_error(self):
        with Pkg() as p:
            p.write("skills/ns-route/scripts/ns", "#!/usr/bin/env python3\ndef (:\n")
            self.assertFails(p, "syntax error")

    # --- manifest and plugin
    def test_version_mismatch(self):
        with Pkg() as p:
            p.write("VERSION", "9.9.9\n")
            self.assertFails(p, "VERSION (9.9.9) and ns-skills.json")

    def test_manifest_skills_must_match_folders(self):
        with Pkg() as p:
            p.json_edit("ns-skills.json", lambda d: d["skills"].remove("ns-to-demo"))
            self.assertFails(p, "ns-skills.json skills do not match")

    def test_plugin_skills_must_match_folders(self):
        with Pkg() as p:
            p.json_edit(".claude-plugin/plugin.json", lambda d: d["skills"].remove("./skills/ns-to-demo"))
            self.assertFails(p, "plugin.json: skills list does not match")

    def test_plugin_version_must_match(self):
        with Pkg() as p:
            p.json_edit(".claude-plugin/plugin.json", lambda d: d.update(version="0.0.2"))
            self.assertFails(p, "plugin.json: version differs")

    def test_marketplace_must_list_plugin(self):
        with Pkg() as p:
            p.json_edit(".claude-plugin/marketplace.json", lambda d: d.update(plugins=[]))
            self.assertFails(p, "marketplace.json: does not list the plugin")


if __name__ == "__main__":
    unittest.main()
