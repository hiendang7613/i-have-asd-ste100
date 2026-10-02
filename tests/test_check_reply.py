import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_reply import check  # noqa: E402

FULL = """- **Fix:** `verifyToken` now reads the `Authorization` header.
- **Tests:** 214 ran and 213 pass.

**Conclusion:** Login is fixed; one payment test still fails, cause not checked.

0. **Done:**
   - **Login fix:** merged.
1. **InProgress:**
   - **CI:** reruns the full suite.
2. **Pending:**
   - **Review:** waiting for the other agent.
3. **Questions:**
   - **Q1.** Approve: deploy to production?
     - `<a>` After CI passes.
     - (b) Now.
4. **Todos:**
   - **Payment test:** check `payment.spec.ts:88`.
5. **Backlog:**
   - **Docs:** update the login guide later.
6. **Risks:**
   - **R1.** `jsonwebtoken` 8.5.1 is older than the 9.0.0 security release.
     - `<a>` update it in a separate change | (b) skip | (c) later
7. **AIIdeas:**
   - **I1.** Add a test for the `Authorization` header.
     - `<a>` plan it | (b) skip | (c) later
"""


class ShapeTests(unittest.TestCase):
    def test_full_shape_passes(self):
        report = check(FULL)
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["stats"]["sections"], list(range(8)))

    def test_shipped_examples_pass_and_the_old_style_fails(self):
        for name in ("after-en.md", "after-vi.md", "after-zh.md", "after-ja.md", "after-es.md", "compare/3-i-have-asd-ste100.md"):
            with self.subTest(name=name):
                self.assertTrue(check((ROOT / "examples" / name).read_text())["ok"])
        before = check((ROOT / "examples/before.md").read_text())
        self.assertFalse(before["ok"])
        self.assertTrue(any("No conclusion part" in v for v in before["violations"]))

    def test_all_six_sections_are_always_shown_and_empty_ones_show_only_the_label(self):
        alone = "I renamed the file.\n\n**Conclusion:** The file is renamed.\n"
        self.assertTrue(any("must be shown" in v for v in check(alone)["violations"]))
        labels = ["Done", "InProgress", "Pending", "Questions", "Todos", "Backlog", "Risks", "AIIdeas"]
        minimal = alone + "\n" + "\n".join("%d. **%s:**" % (n, label) for n, label in enumerate(labels)) + "\n"
        self.assertTrue(check(minimal)["ok"], check(minimal))
        no_pending = FULL.replace("2. **Pending:**\n   - **Review:** waiting for the other agent.\n", "")
        self.assertNotEqual(no_pending, FULL)
        self.assertTrue(any("2 must be shown" in v for v in check(no_pending)["violations"]))
        empty = FULL.replace("1. **InProgress:**\n   - **CI:** reruns the full suite.", "1. **InProgress:**")
        self.assertNotEqual(empty, FULL)
        self.assertTrue(check(empty)["ok"], check(empty))
        filler = empty.replace("1. **InProgress:**", "1. **InProgress:** None")
        self.assertTrue(any("show its label only" in v for v in check(filler)["violations"]))

    def test_items_are_sub_items_that_start_with_a_bold_key(self):
        inline = FULL.replace("0. **Done:**\n   - **Login fix:** merged.", "0. **Done:** Login fix merged.")
        self.assertNotEqual(inline, FULL)
        self.assertTrue(any("Section 0 must show its label only" in v for v in check(inline)["violations"]))
        plain = FULL.replace("   - **Payment test:** check", "   - Check")
        self.assertNotEqual(plain, FULL)
        self.assertTrue(any("Section 4 item must start with **Key:**" in v for v in check(plain)["violations"]))
        unnumbered = FULL.replace("   - **Q1.** Approve:", "   - Approve:")
        self.assertNotEqual(unnumbered, FULL)
        self.assertTrue(any("Section 3 item must start with **Q1.**" in v for v in check(unnumbered)["violations"]))
        detail = FULL.replace("   - **CI:** reruns the full suite.", "   - **CI:** reruns the full suite.\n     - job 812, about 9 minutes left")
        self.assertNotEqual(detail, FULL)
        self.assertTrue(check(detail)["ok"], check(detail))

    def test_small_answers_need_nothing(self):
        self.assertTrue(check("102.")["ok"])
        self.assertTrue(check('```json\n{"status": "ok", "count": 3}\n```')["ok"])

    def test_sections_out_of_order_repeated_or_out_of_range_fail(self):
        swapped = FULL.replace("3. **Questions:**", "9. **Questions:**").replace("2. **Pending:**", "3. **Pending:**").replace("9. **Questions:**", "2. **Questions:**")
        self.assertNotEqual(swapped, FULL)
        self.assertFalse(check(swapped)["ok"])
        self.assertFalse(check(FULL.replace("7. **AIIdeas:**", "8. **AIIdeas:**"))["ok"])
        self.assertFalse(check(FULL.replace("1. **InProgress:**", "0. **InProgress:**"))["ok"])

    def test_one_blank_line_after_the_conclusion_and_none_between_sections(self):
        glued = FULL.replace("cause not checked.\n\n0.", "cause not checked.\n0.")
        self.assertNotEqual(glued, FULL)
        self.assertTrue(any("blank line between the Conclusion line" in v for v in check(glued)["violations"]))
        loose = FULL.replace("\n4. **Todos:**", "\n\n4. **Todos:**")
        self.assertNotEqual(loose, FULL)
        self.assertTrue(any("without blank lines" in v for v in check(loose)["violations"]))

    def test_each_question_with_options_marks_exactly_one_recommended(self):
        none = FULL.replace("`<a>` After CI passes.", "(a) After CI passes.")
        two = FULL.replace("(b) Now.", "`<a>` Now.")
        for text in (none, two):
            with self.subTest(text=text[-260:-200]):
                self.assertNotEqual(text, FULL)
                self.assertTrue(any("options marked" in v for v in check(text)["violations"]))

    def test_conclusion_first_on_request_still_parses(self):
        body, rest = FULL.split("\n\n**Conclusion:**", 1)
        line, sections = rest.split("\n\n", 1)
        first = "**Conclusion:**" + line + "\n\n" + body + "\n\n" + sections
        report = check(first)
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["stats"]["sections"], list(range(8)))
        self.assertEqual(report["stats"]["body_words"], check(FULL)["stats"]["body_words"])
        glued = first.replace("213 pass.\n\n0.", "213 pass.\n0.")
        self.assertNotEqual(glued, first)
        self.assertTrue(any("blank line" in v for v in check(glued)["violations"]))
        self.assertTrue(any("No conclusion part" in v for v in check(body + "\n\n" + sections)["violations"]))

    def test_long_body_warning_does_not_ask_for_a_file(self):
        long_body = FULL.replace("- **Tests:** 214 ran and 213 pass.", "- **Tests:** " + "word " * 260 + "end.")
        warnings = check(long_body)["warnings"]
        self.assertTrue(any(w.startswith("Body has") for w in warnings), warnings)
        self.assertFalse(any("file" in w for w in warnings), warnings)

    def test_risks_and_ideas_are_numbered_and_offer_one_line_choices(self):
        for letter, section in (("R", 6), ("I", 7)):
            with self.subTest(letter=letter):
                wrong = FULL.replace("   - **%s1.**" % letter, "   - **Item:**")
                self.assertNotEqual(wrong, FULL)
                self.assertTrue(any("Section %d item must start with **%s1.**" % (section, letter) in v
                                    for v in check(wrong)["violations"]))
        for line in ("     - `<a>` plan it | (b) skip | (c) later\n", "     - `<a>` update it in a separate change | (b) skip | (c) later\n"):
            with self.subTest(removed=line[9:20]):
                no_choice = FULL.replace(line, "")
                self.assertNotEqual(no_choice, FULL)
                self.assertTrue(any("needs a choice line" in v for v in check(no_choice)["violations"]))
        single = FULL.replace("`<a>` plan it | (b) skip | (c) later", "`<a>` plan it")
        self.assertNotEqual(single, FULL)
        self.assertTrue(any("needs a choice line" in v for v in check(single)["violations"]))
        unmarked = FULL.replace("`<a>` plan it | (b) skip", "(a) plan it | (b) skip")
        self.assertNotEqual(unmarked, FULL)
        self.assertTrue(any("0 options marked" in v for v in check(unmarked)["violations"]))
        twice = FULL.replace("| (b) skip | (c) later\n7.", "| `<a>` skip | (c) later\n7.")
        self.assertNotEqual(twice, FULL)
        self.assertTrue(any("2 options marked" in v for v in check(twice)["violations"]))
        nested = FULL.replace("     - `<a>` plan it | (b) skip | (c) later", "     - `<a>` plan it\n     - (b) skip")
        self.assertNotEqual(nested, FULL)
        self.assertTrue(check(nested)["ok"], check(nested))
        one_line_question = FULL.replace("     - `<a>` After CI passes.\n     - (b) Now.", "     - `<a>` after CI passes | (b) now")
        self.assertNotEqual(one_line_question, FULL)
        self.assertTrue(check(one_line_question)["ok"], check(one_line_question))
        open_question = FULL.replace("     - `<a>` After CI passes.\n     - (b) Now.\n", "")
        self.assertNotEqual(open_question, FULL)
        self.assertTrue(check(open_question)["ok"], check(open_question))

    def test_conclusion_line_length(self):
        long_line = FULL.replace("Login is fixed; one payment test still fails, cause not checked.", " ".join(["word"] * 26) + ".")
        self.assertTrue(any("Conclusion line has 26" in v for v in check(long_line)["violations"]))


class StyleTests(unittest.TestCase):
    def test_emoji_and_square_brackets_fail_but_code_spans_may_hold_anything(self):
        self.assertFalse(check(FULL.replace("**Login fix:** merged.", "**Login fix:** merged ✅"))["ok"])
        self.assertFalse(check(FULL.replace("**Conclusion:**", "\U0001F3AF **Conclusion:**"))["ok"])
        self.assertFalse(check(FULL.replace("0. **Done:**", "0. **[Done]:**"))["ok"])
        bracket_body = FULL.replace("- **Fix:**", "- **[Fix]:**")
        self.assertNotEqual(bracket_body, FULL)
        self.assertTrue(any("square brackets" in v for v in check(bracket_body)["violations"]))
        self.assertTrue(check(FULL.replace("check `payment.spec.ts:88`.", "check `arr[0]` in `payment.spec.ts:88`."))["ok"])

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
    def test_body_can_be_multilingual_but_labels_stay_english(self):
        swahili = ("- **Kurekebisha:** Kuingia kumerekebishwa.\n\n**Hitimisho:** Jaribio moja la malipo bado linashindwa.\n\n"
                   "0. **Imekamilika:**\n   - **Kuingia:** kumerekebishwa.\n1. **Inaendelea:**\n2. **Inasubiri:**\n3. **Maswali:**\n"
                   "   - **Q1.** Niangalie sasa?\n     - `<a>` Ndiyo.\n     - (b) Baadaye.\n"
                   "4. **Kazi zijazo:**\n5. **Yaliyobaki:**\n   - **jsonwebtoken:** kusasisha.\n6. **Hatari:**\n7. **Mawazo:**\n")
        report = check(swahili)
        self.assertFalse(report["ok"], report)
        self.assertTrue(any("conclusion label must be exactly" in v for v in report["violations"]))
        self.assertTrue(any("Section 0 label must be" in v for v in report["violations"]))
        self.assertEqual(report["stats"]["sections"], list(range(8)))

    def test_length_counts_characters_in_scripts_without_spaces(self):
        long_ja = "- **説明：** " + "これはとても長い説明の文で" * 6 + "す。\n\n**Conclusion：** 完了しました。\n"
        self.assertTrue(any(w.startswith("Long sentence") for w in check(long_ja)["warnings"]))
        two = ("- **测试：** 测试已经在预发布环境中全部运行完毕并且全部通过了没有问题。"
               "支付模块的一个测试仍然失败但是它的原因到现在还没有检查过。\n\n**Conclusion：** 完成。\n")
        self.assertEqual(check(two)["warnings"], [])

    def test_fullwidth_colon_labels(self):
        wide = FULL.replace("**Conclusion:**", "**Conclusion：**").replace("**Done:**", "**Done：**").replace("**Login fix:**", "**登录修复：**")
        self.assertNotEqual(wide, FULL)
        report = check(wide)
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["stats"]["sections"], list(range(8)))


if __name__ == "__main__":
    unittest.main()
