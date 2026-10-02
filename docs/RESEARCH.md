# Research basis

What the rules rest on, and how strong each part is. Sources were read on 2026-10-02.

## What we read

| Source | What it is | What we took | Evidence it offers |
|---|---|---|---|
| [i-have-adhd](https://github.com/ayghri/i-have-adhd) | Reply rules for ADHD readers, Claude Code plugin | Plugin layout, opt-in hook pattern, pre-send check, "a rule fights the task" exceptions | Blind LLM-judge A/B, 14 cases x 3 trials, weighted 4.045 to 4.473 (moderate: same model judges) |
| [caveman](https://github.com/juliusbrussee/caveman) | Token-saving reply style with levels | Never compress code, paths, errors, warnings or negations; clarity exceptions | 86 tasks, 8.5% fewer output tokens, quality unchanged (moderate, tokens only) |
| [SimpleEnglish](https://github.com/AminBlg/SimpleEnglish) | STE-based reply and document rules | First sentence carries the answer; no openers or closers; word-count self-check | LLM-counted "defects" 218 to 11 on 8 questions (weak: counts rule hits) |
| [asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill) | STE rewrite skill and linter | Keep real hedges; never drop a safety condition to shorten | None on readers |
| [asd-ste100-writer-skill](https://github.com/blagoySimandov/asd-ste100-writer-skill) | STE rewrite skill | If a rule conflicts with accuracy, keep accuracy and say so | None published |
| [directive](https://github.com/deftai/directive) | Governance rules for coding agents | Fail-loud summaries: never read as success after an anomaly | None |
| STE gists ([L1nefeed](https://gist.github.com/L1nefeed/4164ecaaf77879e76dca3c06f142f1c2), [toppa](https://gist.github.com/toppa/bf7ff49d6fc44fd4fc3337248f8f2a7e), [starise](https://gist.github.com/starise/470f53dbd16149dcd168fa45bff17d1f)) | Output styles for Claude Code | One idea per sentence; one term per concept; split instead of delete | Anecdotes only |
| [woosal1337 ep01](https://github.com/woosal1337/blog/tree/main/videos/ep01-the-cure-for-ai-slop) | STE kit with hooks and a linter | Per-turn reminders against drift | Self-made linter scores, circular (weak) |
| [rtk](https://github.com/rtk-ai/rtk), [headroom](https://github.com/headroomlabs-ai/headroom), [pxpipe](https://github.com/teamchong/pxpipe), [ponytail](https://github.com/dietrichgebert/ponytail) | Tool-output or input compression; less code | Not reply style. Idea kept: failures first, full detail recoverable | Token counts |

## Any language: what the evidence says

| Finding | Source | Strength |
|---|---|---|
| Plain-language principles (relevant, findable, understandable, usable) apply to most written languages; no numeric sentence limit | [ISO 24495-1:2023](https://www.iso.org/standard/78907.html) | Moderate (consensus standard) |
| One idea per sentence; same word for the same thing; lists for three or more items | Inclusion Europe *Information for all*; W3C COGA *Making Content Usable* (2021); Japanese *yasashii nihongo* guideline (2020) | Moderate |
| Numeric caps differ by guide: 20 words on average (EU *How to write clearly*), 8 to 12 words (German and French easy-read guides), 50 to 60 characters as a check point (Japanese official writing, 2022) | EU DG Translation; Kanton Zürich; insieme; Agency for Cultural Affairs (Japan) | Weak: conventions, not tested limits |
| Reading time across languages follows how many words a language needs for the same message (Korean 692, German 975, Chinese 980, French 1062 per 1,000 English words) | Brysbaert, *Journal of Memory and Language* (2019), 190 studies | Moderate |
| About 1.5 Chinese characters carry one English word, so 20 English words are about 30 characters | Cao, Yang and Zhu, Google Research (2007); our derivation | Weak for any single ratio |
| Short labels expand most in translation (up to 200 to 300 percent); use one word per concept; test with native readers | W3C Internationalization; Microsoft Style Guide (2023) | Moderate |

So the rules say "one idea per sentence" for every language and give word targets only for languages with spaces.
The checker converts characters to word equivalents (1.5 for Chinese and Japanese; an unverified 4 for Thai, Lao, Myanmar and Khmer).

## Conclusion first or last?

Web, document and chat research says put the conclusion first: NN/g on scanning (1997) and the inverted pyramid (2018),
GOV.UK, BLUF, Japanese official writing (2022) and NN/g's chatbot study (2026, nine users).
Terminal guidance says the opposite: the CLI Guidelines put the most important information at the end, where the eye rests.
No study compares the two in a chat or terminal reply. This plugin puts the block last, because coding agents run in terminals
and its first user asked for a final conclusion. Saying "conclusion first" moves the block to the top for the session.

## Format choices made with the first user (v0.4)

- **Numbered sections instead of icons.** Numbers are read the same in every language and every terminal, and a reader can answer "2, Q1". Icons were dropped at the user's request; words carry the status.
- **`<a>` in a code span for the recommended option.** A bare `<a>` or `<b>` is parsed as an HTML tag and deleted by Markdown renderers (checked with the GitHub Markdown API on 2026-10-02); a code span shows it exactly and highlights it.
- **Every section is a top-level list item.** Bold labels written as plain lines after a nested list are merged into the previous item by CommonMark's lazy continuation rule (checked with the GitHub Markdown API).

## What we did not take, and why

- **Controlled dictionaries.** They strip the user's own terms, and the ASD-STE100 dictionary is copyrighted.
- **Modal bans** ("never may, might, should"). They hide real uncertainty.
- **Prose only, no lists.** It conflicts with a fixed, scannable block.
- **Telegraphic fragments and dropped articles.** They save tokens but lose the cause and the evidence.
- **Hard word counters enforced by code.** They invite choppy cutting; the limits here are guides.

## Honest limits

- No source measured human comprehension. Every number above is tokens, rule hits or an LLM judge.
- The STE sources are English-only. The language-general rules are our design and need native-speaker review.
- This plugin's own eval suite has not run yet.

ASD-STE100 is a trademark and specification of ASD. This project is not affiliated with ASD and contains no specification text.
