"""Tests for scripts/project_history.py (stdlib only; run: python3 -B -m unittest -q tests/test_project_history.py).

Live-repository checks are read-only. Acceptance cases that need a broken ledger run inside a
throwaway `git clone --local --no-checkout` of this repository under the system temp directory,
so the live tree and its history are never modified.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True  # never leave __pycache__ in the tree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import project_history as ph  # noqa: E402

SCRIPT = os.path.join(ROOT, "scripts", "project_history.py")


def run(args, cwd=ROOT):
    return subprocess.run([sys.executable, SCRIPT, *args], cwd=cwd, capture_output=True, text=True)


class ParserTests(unittest.TestCase):
    def test_mapping_sequence_scalars(self):
        d = ph.parse_yaml("a: 1\nb:\n  - x\n  - y: 2\n    z: [1, \"two\", 'three']\nc: \"q: r\"\nd: null\ne: true\n")
        self.assertEqual(d["a"], 1)
        self.assertEqual(d["b"][0], "x")
        self.assertEqual(d["b"][1]["z"], [1, "two", "three"])
        self.assertEqual(d["c"], "q: r")
        self.assertIsNone(d["d"])
        self.assertIs(d["e"], True)

    def test_block_scalars(self):
        d = ph.parse_yaml("t: |\n  one\n  two\nf: >\n  a\n  b\n\n  c\n")
        self.assertEqual(d["t"], "one\ntwo\n")
        self.assertEqual(d["f"], "a b\nc\n")

    def test_errors(self):
        for bad in ("a:\n\tb: 1\n", "a: 1\na: 2\n", "x: {a: 1}\n"):
            with self.assertRaises(ph.YamlError):
                ph.parse_yaml(bad)

    def test_front_matter(self):
        meta, body = ph.split_front_matter("---\nid: e\n---\n\n## Body\n")
        self.assertEqual(meta["id"], "e")
        self.assertIn("## Body", body)


class DeclarationTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(ph.parse_declaration("history:recorded proj-2026-01-01-thing")["kind"], "recorded")
        self.assertEqual(ph.parse_declaration("history:none — README typo only")["kind"], "none")
        self.assertEqual(ph.parse_declaration("history:defer — issue #12, owner nick, deadline 2099-01-01")["kind"], "defer")

    def test_invalid(self):
        for bad in ("history:none", "history:defer — later", "history:recorded x\nhistory:none — y", "no declaration"):
            with self.assertRaises(ValueError):
                ph.parse_declaration(bad)


class LiveRepositoryTests(unittest.TestCase):
    def test_validate_clean(self):
        p = run(["validate"])
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_render_is_clean_and_stable(self):
        p = run(["render", "--check"])
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_assess_and_context_and_audit(self):
        for args in (["assess"], ["context"], ["context", "README.md"], ["audit", "--full"]):
            p = run(args)
            self.assertEqual(p.returncode, 0, " ".join(args) + "\n" + p.stdout + p.stderr)


class FixtureTests(unittest.TestCase):
    """Broken-ledger acceptance cases inside a throwaway clone."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="project-history-test-")
        cls.fix = os.path.join(cls.tmp, "clone")
        subprocess.run(["git", "clone", "--quiet", "--local", "--no-checkout", ROOT, cls.fix], check=True, capture_output=True)
        # Mirror the source's remote-tracking refs too, so the fixture's reachable graph equals the live one
        # (a fetched-but-unmerged remote tip must count in both).
        subprocess.run(["git", "-C", cls.fix, "fetch", "--quiet", ROOT, "+refs/remotes/*:refs/remotes/*"], check=True, capture_output=True)
        for rel in (".project-history", os.path.join("docs", "history"), ".github", "scripts"):
            shutil.copytree(os.path.join(ROOT, rel), os.path.join(cls.fix, rel))
        for rel in ("PROJECT_HISTORY.md", "AGENTS.md"):
            shutil.copy2(os.path.join(ROOT, rel), os.path.join(cls.fix, rel))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _fresh(self, name):
        dst = os.path.join(self.tmp, name)
        shutil.copytree(self.fix, dst, symlinks=True)
        return dst

    def _first_event(self, root):
        base = os.path.join(root, ".project-history", "events")
        for dirpath, _d, files in os.walk(base):
            for f in sorted(files):
                if f.endswith(".md"):
                    return os.path.join(dirpath, f)
        raise AssertionError("no event capsule")

    def _validate(self, root, extra=()):
        return subprocess.run([sys.executable, os.path.join(root, "scripts", "project_history.py"), "validate", *extra], cwd=root, capture_output=True, text=True)

    def test_fixture_is_clean(self):
        root = self._fresh("clean")
        p = self._validate(root)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        r1 = subprocess.run([sys.executable, os.path.join(root, "scripts", "project_history.py"), "render"], cwd=root, capture_output=True, text=True)
        r2 = subprocess.run([sys.executable, os.path.join(root, "scripts", "project_history.py"), "render"], cwd=root, capture_output=True, text=True)
        self.assertIn("no changes", r1.stdout)
        self.assertIn("no changes", r2.stdout)

    def test_duplicate_event_id(self):
        root = self._fresh("dup")
        ev = self._first_event(root)
        shutil.copy2(ev, os.path.join(os.path.dirname(ev), "zz-copy.md"))
        p = self._validate(root)
        self.assertEqual(p.returncode, 1)
        self.assertIn("duplicate event id", p.stdout)

    def test_broken_supersedes(self):
        root = self._fresh("sup")
        path = os.path.join(root, ".project-history", "doctrine", "goals.yml")
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        text = text.replace("goals:\n", "goals:\n  - id: goal-ghost\n    version: 2\n    status: active\n    introduced_at: 2026-01-01\n    statement: ghost\n    supersedes: no-such-goal\n", 1)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        p = self._validate(root)
        self.assertEqual(p.returncode, 1)
        self.assertIn("supersedes unknown", p.stdout)

    def test_expired_deferral(self):
        root = self._fresh("defer")
        path = os.path.join(root, ".project-history", "policy.yml")
        block = "deferrals:\n  - id: d-old\n    owner: someone\n    deadline: 2000-01-01\n    tracking: issue-1\n    status: open\n"
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        if "deferrals: []" in text:
            text = text.replace("deferrals: []\n", block, 1)
        else:
            text += "\n" + block
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        p = self._validate(root)
        self.assertEqual(p.returncode, 1)
        self.assertIn("expired", p.stdout)

    def test_unreachable_anchor_and_audit(self):
        root = self._fresh("anchor")
        ev = self._first_event(root)
        with open(ev, encoding="utf-8") as fh:
            text = fh.read()
        text = text.replace("anchors:", "anchors:\n  - deadbeefdeadbeefdeadbeefdeadbeefdeadbeef", 1)
        with open(ev, "w", encoding="utf-8") as fh:
            fh.write(text)
        p = self._validate(root, ["--no-render-check"])
        self.assertEqual(p.returncode, 1)
        self.assertIn("unreachable", p.stdout)
        a = subprocess.run([sys.executable, os.path.join(root, "scripts", "project_history.py"), "audit", "--full"], cwd=root, capture_output=True, text=True)
        self.assertEqual(a.returncode, 1)
        self.assertIn("unreachable", a.stdout)

    def test_secret_fixture(self):
        root = self._fresh("secret")
        ev = self._first_event(root)
        with open(ev, "a", encoding="utf-8") as fh:
            fh.write("\n" + ph.SECRET_CONTROL.split()[0] + "\n")
        p = self._validate(root, ["--no-render-check"])
        self.assertEqual(p.returncode, 1)
        self.assertIn("possible secret", p.stdout)

    def test_backfill_dates(self):
        root = self._fresh("dates")
        ev = self._first_event(root)
        with open(ev, encoding="utf-8") as fh:
            text = fh.read()
        import re
        text = re.sub(r"recorded_at: \S+", "recorded_at: 1999-01-01", text, count=1)
        with open(ev, "w", encoding="utf-8") as fh:
            fh.write(text)
        p = self._validate(root, ["--no-render-check"])
        self.assertEqual(p.returncode, 1)
        self.assertIn("recorded_at earlier than occurred_at", p.stdout)

    def test_state_count_mismatch(self):
        root = self._fresh("count")
        path = os.path.join(root, ".project-history", "state.yml")
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        import re
        text = re.sub(r"reachable_commit_count: \d+", "reachable_commit_count: 999999", text)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        p = self._validate(root, ["--no-render-check"])
        self.assertEqual(p.returncode, 1)
        self.assertIn("reachable_commit_count", p.stdout)


if __name__ == "__main__":
    unittest.main()
