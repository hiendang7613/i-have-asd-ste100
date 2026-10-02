"""Offline check of one reply against the i-have-asd-ste100 shape. No model call, no network.

Usage:
  python3 scripts/check_reply.py REPLY.md            # human-readable report
  python3 scripts/check_reply.py REPLY.md --json     # machine-readable report
  cat reply.md | python3 scripts/check_reply.py -    # read standard input

Exit code 0 when there is no violation, 1 otherwise. Warnings never fail the check.
The check covers what can be counted (block shape, line and sentence length, openers, closers).
It cannot judge meaning, accuracy or tone; a passing reply can still be wrong.

Any language: the block is found by its structure (one or five trailing "label: text" lines), so labels in any
language work. Label order is checked only for label sets it knows. Length is counted in words for scripts that
separate words with spaces and in characters (converted to word equivalents) for scripts written without spaces.
"""

import json
import re
import sys

LABELS = [  # known label sets, used only to check the order; unknown labels still pass the structure check
    ("conclusion", ["Conclusion", "Chốt", "Kết luận", "结论", "結論", "결론", "Conclusión", "Fazit", "Conclusão", "Вывод"]),
    ("approve", ["Approve", "Cần duyệt", "需要批准", "承認", "승인", "Aprobar", "À approuver", "Freigabe", "Aprovar", "Утвердить"]),
    ("action", ["Your action", "Bạn cần làm", "Anh cần làm", "Chị cần làm", "你需要做", "あなたの作業", "할 일",
                "Tu acción", "Votre action", "Deine Aufgabe", "Sua ação", "Ваше действие"]),
    ("question", ["Question", "Câu hỏi", "问题", "質問", "질문", "Pregunta", "Frage", "Pergunta", "Вопрос"]),
    ("open", ["Open", "Việc còn mở", "Việc mở", "待办", "未完了", "남은 일", "Pendiente", "En cours", "Offen", "Pendente", "Открыто"]),
]
ICONS = {"🎯": "conclusion", "🔑": "approve", "👉": "action", "❓": "question", "📌": "open"}
NO_SPACE_SCRIPTS = [  # (regex, characters per English-word equivalent); see docs/RESEARCH.md
    # About 1.5 Chinese characters carry one English word (translation ratio, Google Research 2007).
    (re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]"), 1.5),   # Japanese kana, Chinese and Japanese kanji
    # No published ratio found for these scripts; 4 characters per word is an unverified placeholder.
    (re.compile(r"[\u0e00-\u0e7f\u0e80-\u0eff\u1000-\u109f\u1780-\u17ff]"), 4.0),   # Thai, Lao, Myanmar, Khmer
]
SENTENCE_END = r"(?<=[.!?。！？؟।])\s*"
GENERIC_LABEL = re.compile(r"^\s*(?:[-*•]\s*|\d+[.)]\s*)?(?:\*\*)?([^\s:：*][^:：*\n]{0,28}?)(?:\*\*)?\s*[:：]\s*(?:\*\*)?\s*(\S.*)$")
BLOCK_HEADINGS = {"conclusion", "chốt"}
MAX_LINE_WORDS = 20
MAX_SENTENCE_WORDS = 25
BODY_WORD_BUDGET = 250
SMALL_ANSWER_WORDS = 40
OPENERS = re.compile(r"^(great question|good question|sure[,!. ]|certainly|of course|let me |i'll |i will now|"
                     r"câu hỏi hay|tuyệt|để tôi |chắc chắn rồi)", re.I)
CLOSERS = re.compile(r"(hope this helps|let me know if|feel free to|happy to help|hy vọng (điều này|giúp)|"
                     r"cứ hỏi nếu|đừng ngần ngại)", re.I)
LINE_PREFIX = re.compile(r"^\s*(?:[-*•]\s*|\d+[.)]\s*)?(?:\*\*)?")
ICON_PREFIX = re.compile(r"^\s*(?:[-*•]\s*)?(" + "|".join(ICONS) + r")\s*")


def label_of(line):
    """Return (key, text) for a block line. key is a known role, or "?" for a label in an unknown language.
    A leading block icon fixes the role in any language."""
    icon = ICON_PREFIX.match(line)
    if icon:
        rest = line[icon.end():]
        match = re.match(r"(?:\*\*)?[^:：*\n]{1,30}?(?:\*\*)?\s*[:：]\s*(?:\*\*)?\s*(\S.*)$", rest)
        if match:
            return ICONS[icon.group(1)], match.group(1).strip()
    stripped = LINE_PREFIX.sub("", line, count=1)
    for key, names in LABELS:
        for name in names:
            match = re.match(re.escape(name) + r"\s*(?:\*\*)?\s*[:：]\s*(?:\*\*)?\s*(.*)$", stripped, re.I)
            if match:
                return key, match.group(1).strip()
    generic = GENERIC_LABEL.match(line)
    if generic and len(generic.group(1).split()) <= 4 and not re.search(r"[.!?。`/]", generic.group(1)):
        return "?", generic.group(2).strip()
    return None


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


def is_block_heading(line):
    text = re.sub(r"[#*_:：\s]+", " ", line).strip().lower()
    known = {name.lower() for name in LABELS[0][1]}
    return text in BLOCK_HEADINGS or text in known


def strip_code(text):
    return re.sub(r"```.*?```", " ", text, flags=re.S)


def sentences(text):
    plain = re.sub(r"`[^`]*`", "X", strip_code(text))
    plain = re.sub(r"(?m)^\s*(?:[-*•]|\d+[.)]|#+)\s+", "", plain)
    parts = re.split(SENTENCE_END + r"|\n+", plain)
    return [p.strip() for p in parts if units(p) >= 3]


def split_block(text):
    """Split the reply into body and the trailing conclusion block (a list of (key, text))."""
    lines = text.rstrip().splitlines()
    trailing, index = [], len(lines) - 1
    while index >= 0:
        if not lines[index].strip():
            index -= 1
            continue
        found = label_of(lines[index])
        if not found:
            break
        trailing.insert(0, (index, found))
        index -= 1
    known = [i for i, (_, (key, _)) in enumerate(trailing) if key == "conclusion"]
    if known:
        trailing = trailing[known[-1]:]
    elif len(trailing) > 5:
        trailing = trailing[-5:]
    cut = trailing[0][0] if trailing else len(lines)
    while cut > 0 and (not lines[cut - 1].strip() or is_block_heading(lines[cut - 1])):
        cut -= 1
    return "\n".join(lines[:cut]), [found for _, found in trailing]


def check(text):
    body, block = split_block(text)
    words = units(strip_code(text))
    violations, warnings = [], []
    order = [key for key, _ in LABELS]
    keys = [key for key, _ in block]

    if not block:
        if words > SMALL_ANSWER_WORDS:
            violations.append("No conclusion block at the end of a reply longer than %d words." % SMALL_ANSWER_WORDS)
    elif "?" in keys:
        if len(block) not in (1, 5):
            violations.append("The block must have one line or five lines; found %d." % len(block))
        warnings.append("Block labels not recognised (any language is fine); their order was not checked.")
    else:
        if keys[0] != "conclusion":
            violations.append("The block must start with the Conclusion line.")
        if keys not in (order[:1], order):
            violations.append("The block must have only the Conclusion line or all five lines in order; found: %s." % ", ".join(keys))
    for key, line in block:
        count = units(line)
        if count > MAX_LINE_WORDS:
            violations.append("Block line '%s' has %g words (limit %d)." % (key, count, MAX_LINE_WORDS))
        if not line:
            violations.append("Block line '%s' is empty; write None in the user's language." % key)

    body_sentences = sentences(body)
    for sentence in (s for s in body_sentences if units(s) > MAX_SENTENCE_WORDS):
        warnings.append("Long sentence (%g words): %s..." % (units(sentence), sentence[:60]))
    body_words = units(strip_code(body))
    if block and body_words > BODY_WORD_BUDGET:
        warnings.append("Body has %g words (target about %d); move detail to a file." % (body_words, BODY_WORD_BUDGET))
    first = next((line for line in strip_code(body).splitlines() if line.strip()), block[0][1] if block else "")
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
            "block_lines": keys,
            "block_line_words": [units(line) for _, line in block],
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
