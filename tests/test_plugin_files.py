"""Manifests agree, the skill is the single source of truth, and no specification text is shipped."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/i-have-asd-ste100/SKILL.md"


def shipped_files():
    for path in ROOT.rglob("*"):
        parts = path.relative_to(ROOT).parts
        if path.is_file() and parts[0] not in {"ref_repos", ".git"} and "results" not in parts and "__pycache__" not in parts:
            yield path


class ManifestTests(unittest.TestCase):
    def test_manifests_share_name_version_and_licence(self):
        claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        codex = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        self.assertEqual(claude["name"], "i-have-asd-ste100")
        self.assertEqual((codex["name"], codex["version"], codex["license"]), (claude["name"], claude["version"], claude["license"]))
        self.assertEqual(market["plugins"][0]["name"], claude["name"])
        self.assertTrue((ROOT / codex["skills"] / "i-have-asd-ste100/SKILL.md").is_file())
        self.assertRegex(claude["version"], r"^\d+\.\d+\.\d+$")

    def test_licence_and_third_party_notice_exist(self):
        self.assertIn("Copyright (c) 2026 hiendang7613", (ROOT / "LICENSE").read_text())
        self.assertIn("Ayoub Ghriss", (ROOT / "licenses/i-have-adhd-LICENSE.txt").read_text())
        notice = (ROOT / "licenses/NOTICE.md").read_text()
        self.assertIn("no specification text and no dictionary", notice)
        self.assertIn("not affiliated", notice)


class SkillTests(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text()
        self.front = self.text.split("---")[1]

    def test_frontmatter_matches_the_directory_and_stays_manual(self):
        self.assertIn("name: i-have-asd-ste100", self.front)
        self.assertIn("disable-model-invocation: true", self.front)

    def test_skill_stays_small_because_always_on_injects_it_every_session(self):
        self.assertLessEqual(len(self.text.encode()), 6500)

    def test_required_sections_and_language_neutral_labels(self):
        for heading in ("## Persistence", "## The shape", "## Sentences", "## Protect meaning", "## Tone",
                        "## When to break the rules", "## Pre-send check"):
            self.assertIn(heading, self.text)
        for label in ("**Conclusion:**", "**Approve:**", "**Your action:**", "**Question:**", "**Open:**"):
            self.assertIn(label, self.text)
        self.assertIn("Write the labels in the user's language", self.text)
        self.assertIn('"stop ste mode"', self.text)

    def test_injected_rules_name_no_human_language_and_use_only_ascii(self):
        """A language named in always-on rules pulls replies into that language (caveman's finding)."""
        body = self.text.split("---", 2)[2]
        names = r"\b(English|Vietnamese|Chinese|Japanese|Korean|Spanish|French|German|Portuguese|Arabic|Russian|Thai|Hindi)\b"
        self.assertNotRegex(body, names)
        self.assertTrue(body.isascii(), [c for c in body if not c.isascii()][:10])

    def test_public_skill_does_not_hard_code_one_users_form_of_address(self):
        self.assertNotRegex(self.text, r"\bAnh cần làm\b|\banh\b")

    def test_no_specification_text_or_dictionary_is_shipped(self):
        rule_ids = re.compile(r"\b(?:Rule|RULE)\s+\d+\.\d+\b")
        for path in shipped_files():
            if path.suffix not in {".md", ".json", ".mjs", ".py", ".txt"} or path.name.startswith("test_"):
                continue
            text = path.read_text(errors="ignore")
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertIsNone(rule_ids.search(text))
                self.assertNotIn("approved word", text.lower())
        self.assertIn("claim no compliance", self.text)


if __name__ == "__main__":
    unittest.main()


class EvalSuiteTests(unittest.TestCase):
    """The eval suite is only written, never run here (running it calls paid models); it must at least load."""

    def front(self, path):
        return path.read_text().split("---")[1]

    def test_every_case_has_a_prompt_and_graders(self):
        cases = [p for p in (ROOT / "evals").iterdir() if p.is_dir() and p.name != "results"]
        self.assertGreaterEqual(len(cases), 10)
        for case in cases:
            with self.subTest(case=case.name):
                front = self.front(case / "prompt.md")
                self.assertNotIn("EVAL_I_HAVE_ASD_STE100", front)  # on by default since 0.1.1
                self.assertIn("allowed_tools: []", front)
                self.assertTrue(list((case / "graders").glob("*.md")))

    def test_regex_graders_compile_and_yaml_loads_when_available(self):
        try:
            import yaml
        except ImportError:
            yaml = None
        for grader in (ROOT / "evals").rglob("graders/*.md"):
            front = self.front(grader)
            with self.subTest(grader=str(grader.relative_to(ROOT))):
                data = yaml.safe_load(front) if yaml else dict(
                    line.split(": ", 1) for line in front.strip().splitlines())
                self.assertIn(str(data["type"]).strip("'\""), {"regex", "llm"})
                if str(data["type"]).strip("'\"") == "regex":
                    re.compile(str(data["pattern"]).strip("'"))
