"""Codex's plugin manifest must expose the shared skill and hook entry points."""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CodexAdapterTests(unittest.TestCase):
    def test_manifest_resolves_shared_skill_and_hook_configuration(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        skills_dir = ROOT / manifest["skills"]
        hooks_file = ROOT / manifest["hooks"]

        self.assertTrue((skills_dir / "ihav-asd-ste100/SKILL.md").is_file())
        self.assertTrue(hooks_file.is_file())

        hooks = json.loads(hooks_file.read_text())["hooks"]
        self.assertIn("SessionStart", hooks)
        self.assertIn("UserPromptSubmit", hooks)

    def test_codex_install_docs_explain_hook_trust_before_default_behavior(self):
        install = (ROOT / "INSTALL.md").read_text()
        codex = install.split("## Codex", 1)[1].split("## Uninstall", 1)[0]

        self.assertIn("/hooks", codex)
        self.assertIn("trust", codex.lower())
        self.assertIn("Without hook trust", codex)
        self.assertNotIn("do not run plugin hooks", codex)


if __name__ == "__main__":
    unittest.main()
