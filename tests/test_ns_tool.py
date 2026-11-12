"""Tests for skills/ns-route/scripts/ns, the usage tool behind every phase footer.

Transcripts are built here in the shape Claude Code writes them, so the tool is exercised on the three ways a run
appears: a typed command, a typed plugin command (/plugin:ns-x), and a read of a skill's SKILL.md in a plugin cache.
"""
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NS = Path(os.environ.get("NS_UNDER_TEST") or ROOT / "skills" / "ns-route" / "scripts" / "ns")


def now(offset=0):
    return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=offset)).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def user(content, offset):
    return {"type": "user", "timestamp": now(offset), "message": {"role": "user", "content": content}}


def call(mid, offset, tool_path=None, out=400):
    content = [{"type": "tool_use", "id": "t" + mid, "name": "Read", "input": {"file_path": tool_path}}] if tool_path else [{"type": "text", "text": "ok"}]
    return {"type": "assistant", "timestamp": now(offset), "message": {"id": mid, "model": "claude-sonnet-5-5", "content": content,
            "usage": {"input_tokens": 1200, "output_tokens": out, "cache_read_input_tokens": 20000, "cache_creation_input_tokens": 500,
                      "cache_creation": {"ephemeral_5m_input_tokens": 500, "ephemeral_1h_input_tokens": 0}}}}


def typed(name, offset):
    return user("<command-message>%s</command-message>\n<command-name>/%s</command-name>" % (name, name), offset)


def run_ns(args, projects, home=None):
    env = dict(os.environ, NS_PROJECTS_DIR=str(projects), NO_COLOR="1", COLUMNS="140")
    if home is not None:
        env["HOME"] = str(home)  # an empty home, so only the folder the script lives in (and plugin folders) can hold skills
    r = subprocess.run([sys.executable, str(NS)] + args, capture_output=True, text=True, env=env)
    return r.returncode, r.stdout + r.stderr


class NsToolTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="nsprojects-"))
        self.proj = self.tmp / "-tmp-demo-project"
        self.proj.mkdir()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def session(self, name, records):
        p = self.proj / (name + ".jsonl")
        p.write_text("\n".join(json.dumps(r, separators=(",", ":")) for r in records) + "\n", encoding="utf-8")  # compact, as Claude Code writes it
        return p

    def test_selftest_passes(self):
        code, out = run_ns(["selftest"], self.tmp)
        self.assertEqual(code, 0, out)
        self.assertIn("all checks passed", out)

    def test_typed_command_is_a_run(self):
        p = self.session("a1", [typed("ns-to-save", 0), call("m1", 5), call("m2", 9)])
        code, out = run_ns(["usage", str(p)], self.tmp)
        self.assertEqual(code, 0, out)
        self.assertIn("ns-to-save", out)

    def test_typed_plugin_command_is_a_run(self):
        # under a plugin install the transcript records /ns-skills:ns-to-save, which the previous patterns missed
        p = self.session("a2", [typed("ns-skills:ns-to-save", 0), call("m1", 5), call("m2", 9)])
        code, out = run_ns(["usage", str(p)], self.tmp)
        self.assertEqual(code, 0, out)
        self.assertIn("ns-to-save", out)
        self.assertNotIn("no ns-* skill runs", out)

    def test_skill_read_in_a_plugin_cache_is_a_run(self):
        # guards the plugin-cache path shape (it already worked in the original tool; the typed-plugin test is the one that failed before)
        path = "/home/u/.claude/plugins/cache/ns-skills/ns-skills/0.1.0/skills/ns-to-docs/SKILL.md"
        p = self.session("a3", [user("do the docs", 0), call("m1", 2, tool_path=path), call("m2", 6), call("m3", 9)])
        code, out = run_ns(["usage", str(p)], self.tmp)
        self.assertEqual(code, 0, out)
        self.assertIn("ns-to-docs", out)

    def test_a_session_without_runs_says_so(self):
        p = self.session("a4", [user("hello", 0), call("m1", 2)])
        code, out = run_ns(["usage", str(p)], self.tmp)
        self.assertIn("no ns-* skill runs", out)

    def test_repeated_reads_of_a_nested_workflow_file_are_noted(self):
        # references/workflows/<file> is one level deeper than the other shared files; the note counts repeated reads of it
        deep = "/h/.claude/skills/ns-route/references/workflows/ticket.md"
        p = self.session("a5", [typed("ns-to-save", 0), call("m1", 2, tool_path=deep), call("m2", 4, tool_path=deep), call("m3", 8)])
        code, out = run_ns(["usage", str(p)], self.tmp)
        self.assertEqual(code, 0, out)
        self.assertIn("ticket.md was read 2x", out)

    def test_other_skills_label_ignores_the_plugin_prefix(self):
        r = call("m1", 5)
        r["message"]["usage"]["input_tokens"] = 1300
        r["attributionSkill"] = "acme:ns-to-save"  # a plugin name that does not itself start with ns-
        q = call("m2", 8)
        q["attributionSkill"] = "mattpocock-skills:tdd"
        p = self.session("a7", [typed("acme:ns-to-save", 0), r, q])
        code, out = run_ns(["usage", str(p)], self.tmp)
        self.assertEqual(code, 0, out)
        other = out.split("OTHER SKILLS")[-1] if "OTHER SKILLS" in out else ""
        self.assertIn("mattpocock-skills:tdd", other)
        self.assertNotIn("acme:ns-to-save", other)

    def test_trend_finds_a_session_that_only_has_a_plugin_command(self):
        # trend and sessions pre-filter transcripts by bytes; a /plugin:ns-x typed command must pass that filter
        self.session("a8", [typed("acme:ns-to-save", 0), call("m1", 3), call("m2", 7)])  # a plugin name that does not start with ns-
        code, out = run_ns(["trend", "--days", "30"], self.tmp, home=self.tmp / "emptyhome")
        self.assertEqual(code, 0, out)
        self.assertNotIn("no ns-* runs", out)
        self.assertIn("ns-to-save", out)

    def test_trend_retired_check_uses_the_script_folder_not_the_home(self):
        # with an empty home, ns-to-save is known only because it sits in the skills folder next to the script
        (self.tmp / "emptyhome").mkdir()
        self.session("a6", [typed("ns-to-save", 0), call("m1", 3), call("m2", 7), typed("ns-to-ghost", 20), call("m3", 23), call("m4", 27)])
        code, out = run_ns(["trend", "--days", "30"], self.tmp, home=self.tmp / "emptyhome")
        self.assertEqual(code, 0, out)
        self.assertIn("1 retired skills hidden (ns-to-ghost)", out)
        self.assertNotIn("2 retired", out)
        code, out = run_ns(["trend", "--days", "30", "--retired"], self.tmp, home=self.tmp / "emptyhome")
        self.assertIn("ns-to-ghost", out)

    def test_trend_does_not_hide_skills_installed_by_a_plugin(self):
        home = self.tmp / "plughome"
        skill = home / ".claude" / "plugins" / "cache" / "mkt" / "ns-skills" / "0.1.0" / "skills" / "ns-to-plugged"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: ns-to-plugged\n---\n", encoding="utf-8")
        self.session("a9", [typed("ns-skills:ns-to-plugged", 0), call("m1", 3), call("m2", 7)])
        code, out = run_ns(["trend", "--days", "30"], self.tmp, home=home)
        self.assertEqual(code, 0, out)
        self.assertNotIn("retired skills hidden", out)
        self.assertIn("ns-to-plugged", out)

    def test_script_is_executable(self):
        self.assertTrue(os.access(NS, os.X_OK))


if __name__ == "__main__":
    unittest.main()
