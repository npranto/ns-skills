"""Tests for scripts/setup-tools.sh and the `ns doctor` command: what gets installed, what is only checked, and that nothing runs without a yes."""
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT / "scripts" / "setup-tools.sh"
NS = ROOT / "skills" / "ns-route" / "scripts" / "ns"


def fake(bin_dir, name, body):
    p = Path(bin_dir) / name
    p.write_text("#!/bin/sh\n" + body + "\n", encoding="utf-8")
    p.chmod(p.stat().st_mode | stat.S_IEXEC)


class Sandbox:
    """A PATH holding only fake tools that record how they were called, and an empty HOME."""

    def __enter__(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="nssetup-"))
        self.bin = self.tmp / "bin"
        self.bin.mkdir()
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.log = self.tmp / "calls.log"
        return self

    def __exit__(self, *a):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def recorder(self, name, extra=""):
        fake(self.bin, name, extra + '\necho "%s $*" >> "%s"' % (name, self.log))

    def calls(self):
        """What the fake tools were asked to do. Read-only checks (claude plugin list) are not changes, so they are left out."""
        lines = self.log.read_text(encoding="utf-8").splitlines() if self.log.exists() else []
        return "".join(l + "\n" for l in lines if l != "claude plugin list")

    def env(self):
        # /usr/bin and /bin stay on PATH for sh, sed, grep and cat; the tools under test come first and are fakes
        return dict(os.environ, PATH="%s:/usr/bin:/bin" % self.bin, HOME=str(self.home), NO_COLOR="1")

    def run(self, cmd, **kw):
        r = subprocess.run(cmd, capture_output=True, text=True, env=self.env(), stdin=subprocess.DEVNULL, start_new_session=True, **kw)
        return r.returncode, r.stdout + r.stderr


class SetupScriptTests(unittest.TestCase):
    def sandbox(self):
        sb = Sandbox().__enter__()
        self.addCleanup(sb.__exit__)
        for t in ("brew", "npm", "npx", "claude"):
            sb.recorder(t)
        fake(sb.bin, "node", 'echo v22.1.0')
        return sb

    def test_script_has_valid_syntax_and_is_executable(self):
        self.assertEqual(subprocess.run(["bash", "-n", str(SETUP)]).returncode, 0)
        self.assertTrue(os.access(SETUP, os.X_OK))

    def test_unknown_option_is_refused(self):
        sb = self.sandbox()
        code, out = sb.run(["bash", str(SETUP), "--nope"])
        self.assertEqual(code, 2, out)

    def test_dry_run_changes_nothing(self):
        sb = self.sandbox()
        code, out = sb.run(["bash", str(SETUP), "--dry-run"])
        self.assertEqual(code, 0, out)
        self.assertEqual(sb.calls(), "")
        self.assertIn("lighthouse", out)
        self.assertIn("mattpocock/skills", out)

    def test_without_a_yes_nothing_is_installed(self):
        sb = self.sandbox()
        code, out = sb.run(["bash", str(SETUP), "--only", "ui"])
        self.assertEqual(sb.calls(), "", out)

    def test_yes_installs_each_missing_tool_by_the_agreed_command(self):
        sb = self.sandbox()
        code, out = sb.run(["bash", str(SETUP), "--yes"])
        calls = sb.calls()
        for expected in ("npm i -g @playwright/cli", "npm i -g lighthouse", "npm i -g @axe-core/cli", "npm i -g vercel",
                         "brew install ffmpeg", "brew install gh", "brew install herdr",
                         "claude plugin install mattpocock-skills@claude-plugins-official",
                         "add mattpocock/skills -g -a codex -a opencode -a cursor -y"):
            self.assertIn(expected, calls, out)

    def test_only_limits_the_groups(self):
        sb = self.sandbox()
        sb.run(["bash", str(SETUP), "--yes", "--only", "ui"])
        calls = sb.calls()
        self.assertIn("npm i -g lighthouse", calls)
        self.assertNotIn("vercel", calls)
        self.assertNotIn("herdr", calls)
        self.assertNotIn("mattpocock", calls)

    def test_harness_limits_the_plugin_install(self):
        sb = self.sandbox()
        sb.run(["bash", str(SETUP), "--yes", "--only", "plugins", "--harness", "codex"])
        calls = sb.calls()
        self.assertIn("-a codex -y", calls)
        self.assertNotIn("-a cursor", calls)
        self.assertNotIn("claude plugin install", calls)

    def test_present_tools_are_left_alone(self):
        sb = self.sandbox()
        for t in ("lighthouse", "playwright-cli", "ffmpeg", "herdr", "vercel", "gh"):
            fake(sb.bin, t, "exit 0")
        sb.run(["bash", str(SETUP), "--yes", "--only", "ui,delegate,vercel"])
        calls = sb.calls()
        self.assertNotIn("lighthouse", calls)
        self.assertNotIn("herdr", calls)
        self.assertIn("@axe-core/cli", calls)

    def test_skills_already_in_agents_folder_are_not_reinstalled(self):
        sb = self.sandbox()
        (sb.home / ".agents" / "skills" / "grilling").mkdir(parents=True)
        sb.run(["bash", str(SETUP), "--yes", "--only", "plugins", "--harness", "codex,opencode,cursor"])
        self.assertNotIn("mattpocock", sb.calls())

    def test_a_failed_install_makes_the_script_fail(self):
        sb = self.sandbox()
        fake(sb.bin, "npm", "exit 1")
        code, out = sb.run(["bash", str(SETUP), "--yes", "--only", "ui"])
        self.assertEqual(code, 1, out)
        self.assertIn("failed:", out)


class DoctorTests(unittest.TestCase):
    def sandbox(self, tools):
        sb = Sandbox().__enter__()
        self.addCleanup(sb.__exit__)
        for t in tools:
            fake(sb.bin, t, "exit 0")
        return sb

    def doctor(self, sb, *args):
        env = dict(sb.env(), PATH=str(sb.bin))  # nothing else on PATH: only the fakes are "installed"
        r = subprocess.run([sys.executable, str(NS)] + list(args), capture_output=True, text=True, env=env, stdin=subprocess.DEVNULL)
        return r.returncode, r.stdout + r.stderr

    ALL = ["git", "gh", "npx", "playwright-cli", "lighthouse", "ffmpeg", "axe", "google-chrome"]

    def test_missing_core_tool_fails_and_names_the_fix(self):
        sb = self.sandbox([])
        code, out = self.doctor(sb, "doctor")
        self.assertEqual(code, 1, out)
        self.assertIn("✗ git", out)
        self.assertIn("brew install git", out)
        self.assertIn("setup-tools.sh", out)

    def test_everything_present_passes(self):
        sb = self.sandbox(self.ALL + ["herdr", "claude", "vercel"])
        fake(sb.bin, "node", "echo v22.1.0")
        (sb.home / ".agents" / "skills" / "grilling").mkdir(parents=True)
        code, out = self.doctor(sb, "doctor")
        self.assertNotIn("✗ git", out)
        self.assertNotIn("✗ lighthouse", out)
        self.assertNotIn("✗ herdr", out)
        self.assertIn("mattpocock-skills", out)

    def test_old_node_is_flagged(self):
        sb = self.sandbox(self.ALL)
        fake(sb.bin, "node", "echo v18.19.0")
        code, out = self.doctor(sb, "doctor")
        self.assertIn("needs 20 or newer", out)

    def test_quiet_is_silent_when_core_and_ui_tools_are_present(self):
        sb = self.sandbox(self.ALL)
        fake(sb.bin, "node", "echo v22.1.0")
        code, out = self.doctor(sb, "doctor", "--quiet")
        self.assertEqual((code, out.strip()), (0, ""), out)

    def test_quiet_prints_one_line_when_something_is_missing(self):
        sb = self.sandbox([t for t in self.ALL if t != "lighthouse"])
        fake(sb.bin, "node", "echo v22.1.0")
        code, out = self.doctor(sb, "doctor", "--quiet")
        self.assertEqual(code, 0, out)
        self.assertEqual(len(out.strip().splitlines()), 1)
        self.assertIn("lighthouse", out)
        self.assertNotIn("herdr", out)  # delegate and vercel are reported by their own phases, not at every start


if __name__ == "__main__":
    unittest.main()
