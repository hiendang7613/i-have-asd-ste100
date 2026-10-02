"""Offline check of one reply against the i-have-asd-ste100 shape. No model call, no network.

Usage:
  python3 scripts/check_reply.py REPLY.md            # human-readable report
  python3 scripts/check_reply.py REPLY.md --json     # machine-readable report
  cat reply.md | python3 scripts/check_reply.py -    # read standard input

Exit code 0 when there is no violation, 1 otherwise. Warnings never fail the check.
The check covers what can be checked mechanically: the conclusion part, exact English labels, section numbers
and order, label-only section lines with bold-key sub-items, option markers, emoji and square brackets, sentence
length, openers and closers.
It cannot judge meaning, accuracy or tone; a passing reply can still be wrong.

Any language: the body can use any language. The conclusion and section labels stay in English.
Length is counted in words for scripts with spaces and in characters (converted to word equivalents)
for scripts written without spaces.
"""

import json
import re
import sys

SECTIONS = {0: "Done", 1: "InProgress", 2: "Pending", 3: "Questions", 4: "Todos", 5: "Backlog"}
QUESTIONS = 3
ALWAYS_SHOWN = (0, 1, 2, 3, 4, 5)  # every section is shown; an empty one shows only its label
MAX_CONCLUSION_WORDS = 25
MAX_SENTENCE_WORDS = 25
BODY_WORD_BUDGET = 250
SMALL_ANSWER_WORDS = 40
NO_SPACE_SCRIPTS = [  # (regex, characters per English-word equivalent); see docs/RESEARCH.md
    # About 1.5 Chinese characters carry one English word (translation ratio, Google Research 2007).
    (re.compile(r"[぀-ヿ㐀-䶿一-鿿豈-﫿]"), 1.5),   # Japanese kana, Chinese and Japanese kanji
    # No published ratio found for these scripts; 4 characters per word is an unverified placeholder.
    (re.compile(r"[฀-๿຀-໿က-႟ក-៿]"), 4.0),   # Thai, Lao, Myanmar, Khmer
]
EMOJI = re.compile(r"[☀-➿⬀-⯿⌀-⏿\U0001F000-\U0001FAFF️]")
SENTENCE_END = r"(?<=[.!?。！？؟।])\s*"
CONCLUSION_LINE = re.compile(r"^\*\*([^*:：\n]{1,30})[:：]\*\*\s*(\S.*)$")
SECTION_LINE = re.compile(r"^(\d)\.\s+\*\*([^*:：\n]{1,30})[:：]\*\*\s*(.*)$")
SUB_ITEM = re.compile(r"^\s{2,}[-*]\s+(.*)$")
BOLD_KEY = re.compile(r"^\*\*[^*\n]{1,40}[:：]\*\*(\s|$)")
QUESTION_KEY = re.compile(r"^\*\*Q\d+\.\*\*\s")
RECOMMENDED = "`<a>`"
OPENERS = re.compile(r"^(great question|good question|sure[,!. ]|certainly|of course|let me |i'll |i will now|"
                     r"câu hỏi hay|tuyệt|để tôi |chắc chắn rồi)", re.I)
CLOSERS = re.compile(r"(hope this helps|let me know if|feel free to|happy to help|hy vọng (điều này|giúp)|"
                     r"cứ hỏi nếu|đừng ngần ngại)", re.I)


def units(text):
    """Length in word equivalents: words for spaced scripts, characters divided by a ratio for unspaced scripts."""
    count = 0.0
    for token in text.split():
        for pattern, ratio in NO_SPACE_SCRIPTS:
            chars = len(pattern.findall(token))
            if chars:
                count += chars / ratio
                token = pattern.sub("", token)
        if re.search(r"\w", token):
            count += 1
    return round(count, 1)


def strip_code(text):
    return re.sub(r"```.*?```", " ", text, flags=re.S)


def sentences(text):
    plain = re.sub(r"`[^`]*`", "X", strip_code(text))
    plain = re.sub(r"(?m)^\s*(?:[-*•]|\d+[.)]|#+)\s+", "", plain)
    parts = re.split(SENTENCE_END + r"|\n+", plain)
    return [p.strip() for p in parts if units(p) >= 3]


def split_reply(text):
    """Return (body, conclusion_label, conclusion_text, sections, layout_problems). sections is a list of
    (number, label, text, sub_items). The conclusion part is the last bold-label line, one blank line,
    then a numbered list whose items start with a bold label. When the user asked for the conclusion
    first, the Conclusion line opens the reply and the numbered list still ends it."""
    lines = text.rstrip().splitlines()
    index = len(lines) - 1
    tail = []
    while index >= 0 and (not lines[index].strip() or SECTION_LINE.match(lines[index])
                          or SUB_ITEM.match(lines[index])):
        tail.insert(0, lines[index])
        index -= 1
    conclusion = CONCLUSION_LINE.match(lines[index].strip()) if index >= 0 else None
    has_sections = any(SECTION_LINE.match(line) for line in tail)
    body_lines = lines[:index]
    top = next((i for i, line in enumerate(lines[:index]) if line.strip()), None)
    if not conclusion and has_sections and top is not None and CONCLUSION_LINE.match(lines[top].strip()):
        conclusion = CONCLUSION_LINE.match(lines[top].strip())
        body_lines = lines[top + 1:index + 1]
    if not conclusion or (any(line.strip() for line in tail) and not has_sections):
        return text, None, None, [], []
    problems = []
    if not tail or tail[0].strip():
        problems.append("Put one blank line between the Conclusion line and the list, or the list merges into it.")
    items = [line for line in tail[1:]]
    first = next((i for i, line in enumerate(items) if line.strip()), None)
    if first is not None and any(not line.strip() for line in items[first:]):
        problems.append("Write the sections without blank lines between them.")
    sections = []
    for line in tail:
        match = SECTION_LINE.match(line)
        if match:
            sections.append((int(match.group(1)), match.group(2).strip(), match.group(3).strip(), []))
        elif SUB_ITEM.match(line) and sections:
            sections[-1][3].append(line)
    return "\n".join(body_lines), conclusion.group(1).strip(), conclusion.group(2).strip(), sections, problems


def item_problems(number, sub_items):
    """Each top-level item in a section starts with a bold key; in Questions the key is **Q1.**, **Q2.** and so on."""
    key = QUESTION_KEY if number == QUESTIONS else BOLD_KEY
    shown = "**Q1.**" if number == QUESTIONS else "**Key:**"
    return ["Section %d item must start with %s: %s..." % (number, shown, item[:30])
            for item in (SUB_ITEM.match(line).group(1) for line in sub_items
                         if len(line) - len(line.lstrip()) <= 3) if not key.match(item)]


def question_problems(sub_items):
    """Each question with two or more options needs exactly one recommended option."""
    problems = []
    groups = []
    for line in sub_items:
        indent = len(line) - len(line.lstrip())
        item = SUB_ITEM.match(line).group(1)
        if indent <= 3:
            groups.append((item, []))
        elif groups:
            groups[-1][1].append(item)
    for question, options in groups:
        if len(options) >= 2:
            marked = sum(RECOMMENDED in option for option in options)
            if marked != 1:
                problems.append("Question '%s' has %d options marked `<a>` (need exactly 1)." % (question[:30], marked))
    return problems


def check(text):
    body, conclusion_label, conclusion, sections, layout = split_reply(text)
    words = units(strip_code(text))
    violations, warnings = [], []

    if conclusion is None:
        if words > SMALL_ANSWER_WORDS:
            violations.append("No conclusion part at the end of a reply longer than %d words." % SMALL_ANSWER_WORDS)
    else:
        if conclusion_label != "Conclusion":
            violations.append("The conclusion label must be exactly 'Conclusion'; found '%s'." % conclusion_label)
        if units(conclusion) > MAX_CONCLUSION_WORDS:
            violations.append("The Conclusion line has %g words (limit %d)." % (units(conclusion), MAX_CONCLUSION_WORDS))
        numbers = [number for number, _, _, _ in sections]
        missing = [n for n in ALWAYS_SHOWN if n not in numbers]
        if missing:
            violations.append("Sections %s must be shown; an empty one shows only its label." % ", ".join(str(n) for n in missing))
        if numbers != sorted(set(numbers)) or any(n not in SECTIONS for n in numbers):
            violations.append("Sections must be numbered 0 to 5, in order, each once; found %s." % numbers)
        violations.extend(layout)
        for number, label, line, subs in sections:
            if number in SECTIONS and label != SECTIONS[number]:
                violations.append("Section %d label must be '%s'; found '%s'." % (number, SECTIONS[number], label))
            if line.strip():
                violations.append("Section %d must show its label only on its line; write each item below it as a "
                                  "sub-item that starts with a bold key." % number)
            violations.extend(item_problems(number, subs))
            if number == QUESTIONS:
                violations.extend(question_problems(subs))

    outside_code = re.sub(r"`[^`]*`", "", strip_code(text))
    if EMOJI.search(outside_code):
        violations.append("The reply contains emoji; write status in words.")
    if re.search(r"\*\*\[|^[-*]\s+\[[^\]]+\]", outside_code, re.M):
        violations.append("Labels use square brackets; write bold labels without them.")
    if re.search(r"```[^\n]*\n(?:(?!```).)*\n\d\.\s+\*\*[^*]+:\*\*", text, re.S):
        violations.append("The conclusion part is inside a code block; the reader would see raw markers.")

    body_sentences = sentences(body)
    for sentence in (s for s in body_sentences if units(s) > MAX_SENTENCE_WORDS):
        warnings.append("Long sentence (%g words): %s..." % (units(sentence), sentence[:60]))
    body_words = units(strip_code(body))
    if conclusion is not None and body_words > BODY_WORD_BUDGET:
        warnings.append("Body has %g words (target about %d); trim optional detail, keep every needed fact."
                        % (body_words, BODY_WORD_BUDGET))
    first = next((line for line in strip_code(body).splitlines() if line.strip()), conclusion or "")
    if OPENERS.match(re.sub(r"^[#*\s-]+", "", first)):
        violations.append("The reply opens with a filler opener: %s..." % first[:40])
    if body_sentences and CLOSERS.search(body_sentences[-1]):
        violations.append("The body ends with a closing pleasantry: %s..." % body_sentences[-1][:40])

    return {
        "ok": not violations,
        "violations": violations,
        "warnings": warnings,
        "stats": {
            "words": words,
            "body_words": body_words,
            "conclusion_words": units(conclusion) if conclusion else 0,
            "sections": [number for number, _, _, _ in sections],
            "longest_sentence": max((units(s) for s in body_sentences), default=0),
        },
    }


def main(argv):
    if len(argv) < 2 or argv[1] in {"-h", "--help"}:
        print(__doc__.strip())
        return 2
    text = sys.stdin.read() if argv[1] == "-" else open(argv[1], encoding="utf-8").read()
    report = check(text)
    if "--json" in argv:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("OK" if report["ok"] else "FAIL")
        for item in report["violations"]:
            print("violation:", item)
        for item in report["warnings"]:
            print("warning:", item)
        print("stats:", json.dumps(report["stats"], ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
