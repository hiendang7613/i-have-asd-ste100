import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_reply import check  # noqa: E402

FULL_EN = """- The build passed.
- I ran 214 tests. 213 pass.

Conclusion: The build passed; one test still fails.
Approve: None.
Your action: None.
Question: Should I fix the failing test now (recommended) or later?
Open: The failing test, owned by me.
"""


class CheckReplyTests(unittest.TestCase):
    def test_examples_shipped_with_the_plugin(self):
        self.assertTrue(check((ROOT / "examples/after-en.md").read_text())["ok"])
        self.assertTrue(check((ROOT / "examples/after-vi.md").read_text())["ok"])
        before = check((ROOT / "examples/before.md").read_text())
        self.assertFalse(before["ok"])
        self.assertTrue(any("No conclusion block" in item for item in before["violations"]))

    def test_full_block_and_bold_list_and_heading_forms(self):
        self.assertTrue(check(FULL_EN)["ok"])
        bold = "Body line one is here.\n\n## Chốt\n- **Chốt:** Xong.\n- **Cần duyệt:** Không có.\n- **Anh cần làm:** Không có.\n- **Câu hỏi:** Không có.\n- **Việc còn mở:** Không có.\n"
        report = check(bold)
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["stats"]["block_lines"], ["conclusion", "approve", "action", "question", "open"])

    def test_conclusion_line_alone_is_allowed(self):
        self.assertTrue(check("I renamed the file.\n\nConclusion: The file is renamed; nothing else is open.\n")["ok"])

    def test_wrong_order_partial_block_and_long_line_fail(self):
        swapped = FULL_EN.replace("Approve: None.\nYour action: None.", "Your action: None.\nApprove: None.")
        self.assertFalse(check(swapped)["ok"])
        partial = FULL_EN.replace("Question: Should I fix the failing test now (recommended) or later?\n", "")
        self.assertFalse(check(partial)["ok"])
        long_line = FULL_EN.replace("The build passed; one test still fails.", " ".join(["word"] * 21) + ".")
        self.assertTrue(any("has 21 words" in v for v in check(long_line)["violations"]))

    def test_small_answers_and_exact_output_need_no_block(self):
        self.assertTrue(check("102.")["ok"])
        self.assertTrue(check('```json\n{"status": "ok", "count": 3}\n```')["ok"])

    def test_openers_closers_and_long_sentences(self):
        opener = "Great question! " + FULL_EN
        self.assertTrue(any("opener" in v for v in check(opener)["violations"]))
        closer = FULL_EN.replace("- I ran 214 tests. 213 pass.", "- I ran 214 tests. 213 pass. Hope this helps.")
        self.assertTrue(any("pleasantry" in v for v in check(closer)["violations"]))
        long_sentence = FULL_EN.replace("- The build passed.", "- " + " ".join(["word"] * 30) + ".")
        report = check(long_sentence)
        self.assertTrue(report["ok"])
        self.assertTrue(any("Long sentence (30 words)" in w for w in report["warnings"]))

    def test_code_blocks_do_not_count_as_sentences(self):
        code = "```\n" + " ".join(["token"] * 60) + "\n```\n\n" + FULL_EN
        self.assertEqual(check(code)["warnings"], [])
        odd_backtick = "```sh\necho `date\n" + " ".join(["word"] * 40) + "\n```\n\n" + FULL_EN
        self.assertEqual(check(odd_backtick)["warnings"], [])


class MultilingualTests(unittest.TestCase):
    def test_examples_in_other_languages_pass_and_find_the_block(self):
        for name in ("after-zh.md", "after-es.md", "after-ja.md"):
            with self.subTest(name=name):
                report = check((ROOT / "examples" / name).read_text())
                self.assertTrue(report["ok"], report)
                self.assertEqual(report["stats"]["block_lines"], ["conclusion", "approve", "action", "question", "open"])

    def test_body_lines_shaped_like_labels_are_not_taken_into_the_block(self):
        labelled_body = ("- 原因：请求头错误。\n- 测试：214 个测试运行，213 个通过。\n\n"
                         "结论：已修复。\n需要批准：无。\n你需要做：无。\n问题：无。\n待办：无。\n")
        report = check(labelled_body)
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["stats"]["block_lines"], ["conclusion", "approve", "action", "question", "open"])

    def test_cjk_full_stops_split_sentences_on_one_line(self):
        two = ("- 测试已经在预发布环境中全部运行完毕并且全部通过了没有问题。"
               "支付模块的一个测试仍然失败但是它的原因到现在还没有检查过。\n\n结论：完成。\n")
        self.assertEqual(check(two)["warnings"], [])

    def test_unknown_language_labels_pass_by_structure_with_a_warning(self):
        swahili = ("Nimerekebisha jaribio la kuingia na kulituma kwenye staging.\n\n"
                   "Hitimisho: Kuingia kumerekebishwa; jaribio moja la malipo bado linashindwa.\n"
                   "Idhinisha: Hakuna.\nKazi yako: Hakuna.\nSwali: Niangalie jaribio la malipo sasa?\n"
                   "Yaliyobaki: Kusasisha jsonwebtoken baadaye.\n")
        report = check(swahili)
        self.assertTrue(report["ok"], report)
        self.assertTrue(any("not recognised" in w for w in report["warnings"]))
        three = "\n".join(swahili.splitlines()[:5]) + "\n"
        self.assertFalse(check(three)["ok"])

    def test_known_labels_in_wrong_order_fail_in_any_language(self):
        original = (ROOT / "examples/after-es.md").read_text()
        approve = next(line for line in original.splitlines() if "**Aprobar:**" in line)
        action = next(line for line in original.splitlines() if "**Tu acción:**" in line)
        swapped = original.replace(approve + "\n" + action, action + "\n" + approve)
        self.assertNotEqual(swapped, original)
        self.assertFalse(check(swapped)["ok"])
        unlabelled = swapped.replace("🔑 ", "").replace("👉 ", "")
        self.assertNotEqual(unlabelled, swapped)
        self.assertFalse(check(unlabelled)["ok"])  # known Spanish labels still fix the order without icons

    def test_length_counts_characters_in_scripts_without_spaces(self):
        long_ja = "- " + "これはとても長い説明の文で" * 6 + "す。\n\n結論：完了しました。\n"
        report = check(long_ja)
        self.assertTrue(any(w.startswith("Long sentence") for w in report["warnings"]), report)
        short_zh = "- 测试全部通过。\n\n结论：完成。\n"
        self.assertEqual(check(short_zh)["warnings"], [])


class IconTests(unittest.TestCase):
    BLOCK = ("- ✅ **Tests:** 214 ran, 213 pass.\n- ❌ `payment.spec.ts:88` fails; cause not checked.\n\n"
             "🎯 **{0}:** Login is fixed; one payment test still fails.\n🔑 **{1}:** Deploy to production.\n"
             "👉 **{2}:** None.\n❓ **{3}:** Check the payment test first (recommended)?\n📌 **{4}:** Update jsonwebtoken later.\n")

    def test_icons_fix_the_roles_in_any_language(self):
        for labels in (("Conclusion", "Approve", "Your action", "Question", "Open"),
                       ("Hitimisho", "Idhinisha", "Kazi yako", "Swali", "Yaliyobaki")):
            with self.subTest(labels=labels[0]):
                report = check(self.BLOCK.format(*labels))
                self.assertTrue(report["ok"], report)
                self.assertEqual(report["stats"]["block_lines"], ["conclusion", "approve", "action", "question", "open"])
                self.assertEqual(report["warnings"], [])

    def test_icon_order_is_checked_even_for_unknown_labels(self):
        text = self.BLOCK.format("Hitimisho", "Idhinisha", "Kazi yako", "Swali", "Yaliyobaki")
        swapped = text.replace("🔑 **Idhinisha:** Deploy to production.\n👉 **Kazi yako:** None.",
                               "👉 **Kazi yako:** None.\n🔑 **Idhinisha:** Deploy to production.")
        self.assertFalse(check(swapped)["ok"])

    def test_status_icon_bullets_are_body_lines_not_block_lines(self):
        report = check(self.BLOCK.format("Conclusion", "Approve", "Your action", "Question", "Open"))
        self.assertEqual(len(report["stats"]["block_lines"]), 5)


if __name__ == "__main__":
    unittest.main()
