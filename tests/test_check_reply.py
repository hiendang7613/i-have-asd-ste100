import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_reply import check  # noqa: E402

FULL = """- **Fix:** `verifyToken` now reads the `Authorization` header.
- **Tests:** 214 ran and 213 pass.

**Conclusion:** Login is fixed; one payment test still fails, cause not checked.

**0.Done:** Login fix merged.

**1.InProgress:** CI reruns the full suite.

**2.Questions:**
  - **Q1.** Approve: deploy to production?
    - `<a>` After CI passes.
    - (b) Now.

**3.Todos:** Check `payment.spec.ts:88`.

**4.Pending:** Review from the other agent.

**5.Backlog:** Update `jsonwebtoken` in a separate change.
"""


class ShapeTests(unittest.TestCase):
    def test_full_shape_passes(self):
        report = check(FULL)
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["stats"]["sections"], [0, 1, 2, 3, 4, 5])

    def test_shipped_examples_pass_and_the_old_style_fails(self):
        for name in ("after-en.md", "after-vi.md", "after-zh.md", "after-ja.md", "after-es.md", "compare/3-i-have-asd-ste100.md"):
            with self.subTest(name=name):
                self.assertTrue(check((ROOT / "examples" / name).read_text())["ok"])
        before = check((ROOT / "examples/before.md").read_text())
        self.assertFalse(before["ok"])
        self.assertTrue(any("No conclusion part" in v for v in before["violations"]))

    def test_conclusion_line_alone_is_allowed_and_small_answers_need_nothing(self):
        self.assertTrue(check("I renamed the file.\n\n**Conclusion:** The file is renamed.\n")["ok"])
        self.assertTrue(check("102.")["ok"])
        self.assertTrue(check('```json\n{"status": "ok", "count": 3}\n```')["ok"])

    def test_sections_out_of_order_repeated_or_out_of_range_fail(self):
        swapped = FULL.replace("**4.Pending:** Review from the other agent.\n\n", "").replace(
            "**1.InProgress:** CI reruns the full suite.\n", "**4.Pending:** Review from the other agent.\n")
        self.assertNotEqual(swapped, FULL)
        self.assertFalse(check(swapped)["ok"])
        self.assertFalse(check(FULL.replace("**5.Backlog:**", "**6.Backlog:**"))["ok"])
        self.assertFalse(check(FULL.replace("**1.InProgress:**", "**0.InProgress:**"))["ok"])

    def test_empty_sections_must_be_left_out(self):
        report = check(FULL.replace("**4.Pending:** Review from the other agent.", "**4.Pending:**"))
        self.assertTrue(any("Section 4" in v and "empty" in v for v in report["violations"]))

    def test_each_question_with_options_marks_exactly_one_recommended(self):
        none = FULL.replace("`<a>` After CI passes.", "(a) After CI passes.")
        two = FULL.replace("(b) Now.", "`<a>` Now.")
        for text in (none, two):
            with self.subTest(text=text[-200:-150]):
                self.assertNotEqual(text, FULL)
                self.assertTrue(any("options marked" in v for v in check(text)["violations"]))

    def test_sections_need_a_blank_line_before_them_unless_bulleted(self):
        packed = FULL.replace("    - (b) Now.\n\n**3.Todos:**", "    - (b) Now.\n**3.Todos:**")
        self.assertNotEqual(packed, FULL)
        self.assertTrue(any("blank line before each section" in v for v in check(packed)["violations"]))
        bulleted = FULL
        for n in range(6):
            bulleted = bulleted.replace("\n\n**%d." % n, "\n- **%d." % n)
        self.assertNotEqual(bulleted, FULL)
        self.assertTrue(check(bulleted)["ok"], check(bulleted))

    def test_conclusion_line_length(self):
        long_line = FULL.replace("Login is fixed; one payment test still fails, cause not checked.", " ".join(["word"] * 26) + ".")
        self.assertTrue(any("Conclusion line has 27" in v or "Conclusion line has 26" in v for v in check(long_line)["violations"]))


class StyleTests(unittest.TestCase):
    def test_emoji_and_square_brackets_fail_but_code_spans_may_hold_anything(self):
        self.assertFalse(check(FULL.replace("**0.Done:**", "**0.Done:** ✅"))["ok"])
        self.assertFalse(check(FULL.replace("**Conclusion:**", "\U0001F3AF **Conclusion:**"))["ok"])
        self.assertFalse(check(FULL.replace("**0.Done:**", "**[0.Done]:**"))["ok"])
        bracket_body = FULL.replace("- **Fix:**", "- **[Fix]:**")
        self.assertNotEqual(bracket_body, FULL)
        self.assertTrue(any("square brackets" in v for v in check(bracket_body)["violations"]))
        self.assertTrue(check(FULL.replace("Check `payment.spec.ts:88`.", "Check `arr[0]` in `payment.spec.ts:88`."))["ok"])

    def test_conclusion_wrapped_in_a_code_block_fails(self):
        wrapped = "Here is the status.\n\n```markdown\n" + FULL + "```\n\n**Conclusion:** See above.\n"
        self.assertTrue(any("inside a code block" in v for v in check(wrapped)["violations"]))

    def test_openers_closers_and_long_sentences(self):
        self.assertTrue(any("opener" in v for v in check("Great question! " + FULL)["violations"]))
        closer = FULL.replace("- **Tests:** 214 ran and 213 pass.", "- **Tests:** 214 ran and 213 pass. Hope this helps.")
        self.assertTrue(any("pleasantry" in v for v in check(closer)["violations"]))
        long_body = FULL.replace("- **Tests:** 214 ran and 213 pass.", "- " + " ".join(["word"] * 30) + ".")
        report = check(long_body)
        self.assertTrue(report["ok"])
        self.assertTrue(any("Long sentence (30 words)" in w for w in report["warnings"]))

    def test_code_blocks_do_not_count_as_sentences(self):
        code = "```\n" + " ".join(["token"] * 60) + "\n```\n\n" + FULL
        self.assertEqual(check(code)["warnings"], [])
        odd_backtick = "```sh\necho `date\n" + " ".join(["word"] * 40) + "\n```\n\n" + FULL
        self.assertEqual(check(odd_backtick)["warnings"], [])


class MultilingualTests(unittest.TestCase):
    def test_labels_in_any_language_are_found_by_structure(self):
        swahili = ("- **Kurekebisha:** Kuingia kumerekebishwa.\n\n**Hitimisho:** Jaribio moja la malipo bado linashindwa.\n\n"
                   "**0.Imekamilika:** Kuingia kumerekebishwa.\n\n**2.Maswali:**\n  - **Q1.** Niangalie sasa?\n"
                   "    - `<a>` Ndiyo.\n    - (b) Baadaye.\n\n**4.Yaliyobaki:** Kusasisha jsonwebtoken.\n")
        report = check(swahili)
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["stats"]["sections"], [0, 2, 4])

    def test_length_counts_characters_in_scripts_without_spaces(self):
        long_ja = "- **説明：** " + "これはとても長い説明の文で" * 6 + "す。\n\n**結論：** 完了しました。\n"
        self.assertTrue(any(w.startswith("Long sentence") for w in check(long_ja)["warnings"]))
        two = ("- **测试：** 测试已经在预发布环境中全部运行完毕并且全部通过了没有问题。"
               "支付模块的一个测试仍然失败但是它的原因到现在还没有检查过。\n\n**结论：** 完成。\n")
        self.assertEqual(check(two)["warnings"], [])

    def test_fullwidth_colon_labels_and_section_numbers(self):
        report = check((ROOT / "examples/after-zh.md").read_text())
        self.assertEqual(report["stats"]["sections"], [0, 2, 3, 5])


if __name__ == "__main__":
    unittest.main()
