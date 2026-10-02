# Research basis

What the rules rest on, and how strong each part is. Sources were read on 2026-10-02.

## What we read

| Source | What it is | What we took | Evidence it offers |
|---|---|---|---|
| [i-have-adhd](https://github.com/ayghri/i-have-adhd) | Reply rules for ADHD readers, Claude Code plugin | Next action, persistent state, concrete progress, and explicit exceptions when a rule fights the task | Blind LLM-judge A/B, 14 cases x 3 trials, weighted 4.045 to 4.473; same model judges. Its release gate still fails, one case is impossible with the runner's disabled tools, and partial-success has a plausible accuracy regression. |
| [caveman](https://github.com/juliusbrussee/caveman) | Token-saving reply style with levels | Keep code, paths, errors, warnings and negations exact; use full words when fragments save no tokens; stop compression when it risks clarity | A cited JetBrains paired test on 86 coding tasks reports 8.5% fewer output tokens and no detectable quality difference (sign test p=.82). This is not a human readability test or proof of equality. |
| [SimpleEnglish](https://github.com/AminBlg/SimpleEnglish) | STE-inspired reply and document rules | Separate chat rules from document rules; state the result first; preserve exact content and allow task-specific exceptions | A corrected report uses 8 reply questions in two runs and a blind same-model judge. Its v2.0.1 replies win 7/8 pairs in each run against v2.0.0. Structural counts fall from 218 to 11, but count formatting features, not comprehension. One generation per cell and same-family judging limit confidence. |
| [asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill), [ste-writing-style](https://github.com/dandye/ste-writing-style), [writing-styles](https://github.com/cfcosta/writing-styles), [sdsheeks-ste100-skill](https://github.com/sdsheeks/ste100-skill), [asd-ste100-writer-skill](https://github.com/blagoySimandov/asd-ste100-writer-skill) | STE-focused rewrite and documentation skills | Borrow one idea per sentence, stable terms, direct verbs, and accuracy before simplification. Keep strict vocabulary and grammar modes scoped to technical documents. | No shared human comprehension test. These repos repeat related rules; they are not independent outcome replications. |
| [directive](https://github.com/deftai/directive) | Governance framework for coding agents | Rule precedence and lazy-loaded detail are relevant to keeping this style subordinate to exact user, harness, and project instructions. | Not a user-reply study. |
| STE gists ([L1nefeed](https://gist.github.com/L1nefeed/4164ecaaf77879e76dca3c06f142f1c2), [toppa](https://gist.github.com/toppa/bf7ff49d6fc44fd4fc3337248f8f2a7e), [starise](https://gist.github.com/starise/470f53dbd16149dcd168fa45bff17d1f)) | Output-style prompts for Claude Code | Preserve a precedence rule and allow accurate technical terms. Do not treat the gists as independent evaluations: starise is a fork of L1nefeed. | Anecdotes only; no controlled outcome data. |
| [woosal1337 ep01](https://github.com/woosal1337/blog/tree/main/videos/ep01-the-cure-for-ai-slop) | STE-inspired skill, hook reminders, and linter | A brief reminder can help keep a rule visible; a checker can count only a narrow, declared set of features. | Its self-made linter scores do not establish readability. |
| [rtk](https://github.com/rtk-ai/rtk) | Shell-output compression | Keep compression in the tool-output layer, separate from prose style. | It measures intercepted shell output; its byte/4 token values are estimates, not total-bill savings. |
| [headroom](https://github.com/headroomlabs-ai/headroom) | Reversible context compression, retrieval, and optional output-token shaping | Its optional verbosity note can reduce output tokens, but it does not define a reply structure. Keep token reduction separate from accuracy and required format. | README reports seeded offline and model-eval results. Output savings are estimated counterfactually unless a 10% unshaped holdout is enabled; neither measures reader comprehension. |
| [pxpipe](https://github.com/teamchong/pxpipe) | Image-based compression of model input | Input compression is a separate layer. A final-output format check still matters. | README reports exact-retrieval checks, but also describes a run that needed a nudge to follow a one-line output request. |
| [ponytail](https://github.com/dietrichgebert/ponytail) | Coding-agent minimalism | Keep the instruction file compact; overlong explanations of skipped work can erase token savings. | Its 5-task comparison has n=1 per task/config and measures coding deliverables, not reader response quality. |

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

## Independent source pass, 2026-10-02

The supplied GitHub references were shallow-cloned under `ref_repos/` and read at these local commit pins. They are ignored by Git and stay as research copies. No repository code, checker, proxy, benchmark runner, or install script was executed.

| Reference | Local commit | Relevance to this skill |
|---|---|---|
| `ponytail` | `e3ba2aa6f1e6` | The author reports that long explanations of skipped work erased savings; later versions shortened the skill itself. Small n and coding-only tasks limit transfer. |
| `i-have-adhd` | `839872f9d1cd` | Useful task-first and progress patterns; its full eval has an impossible no-tools case and a possible unsupported-cause regression. |
| `caveman` | `b39c90862855` | Good exactness and clarity exceptions. Aggressive fragment modes are unsuitable as a default for admin-facing prose. |
| `pxpipe` | `75668a4a8075` | Input token compression only; its own README separates retrieval success from final one-line format adherence. |
| `headroom` | `d5318ac23559` | Input compression, retrieval, and optional output verbosity shaping; reported output-token savings need a holdout to become measured. |
| `rtk` | `ff9bd8e6d06c` | Compresses selected shell output; token estimates use bytes divided by four. |
| `ste-writing-style` | `9a855963b645` | Documentation workflow and vocabulary extensions, not general chat. |
| `directive` | `be9f25dcdb0f` | Coding policy and precedence, not a reply-style evaluation. |
| `asd-ste100-skill` | `7d4a135a199a` | Separates strict and STE-flavored technical-writing modes. |
| `woosal-blog` | `5a0f04774bc9` | Adds reminders and a checker, but its own rule counts do not establish comprehension. |
| `writing-styles` | `182698ed9705` | Another STE-style skill; no user-response outcome data found in the reviewed entrypoint. |
| `sdsheeks-ste100-skill` | `269ddec7fd17` | Strict dictionary and format rules target technical documentation. |
| `asd-ste100-checker` | `e193ecdd66b0` | A more elaborate checker exists, but the clone includes extracted dictionary data. We did not read or run that data. |
| `asd-ste100-writer-skill` | `858eab440e03` | States that technical accuracy outranks language rules. |
| `SimpleEnglish` | `32ea2d3f4404` | Has separate chat/document rules and a corrected, limited blind-judge comparison. |

The [official ASD-STE100 downloads and AI white paper page](https://www.asd-ste100.org/STE_downloads.html) describes the standard as technical documentation with writing rules and a controlled dictionary. Its AI white paper warns that fluent AI text can still misapply the standard and requires informed human oversight. Use the principles as inspiration only; do not claim compliance, copy dictionary content, or imply endorsement. The official standard is free by request. We did not request or download it.

The linked [Hacker News discussion](https://news.ycombinator.com/item?id=49114639) is useful counterevidence, not a study: some readers report benefit from one-line prompts, while others warn that large skills become prescriptive, drift, or damage meaning when bans are applied mechanically. Several comments show the same key failure mode: a shorter rewrite can become less precise. Use this as a reason to keep the skill short, keep exceptions visible, and test task completion rather than linter compliance.

The linked [Reddit workflow entry](https://www.reddit.com/r/ClaudeWorkflows/comments/1vbw6xp/workflow_claude_skill_simplify_technical/) is an automatically generated workflow-card summary for simplifying technical documents. It recommends reviewing and iterating on rewrites, but gives no measured evidence for chat reply format. Treat it as discovery metadata, not a result.

### Resulting edits to the skill

- Keep the admin-selected eight-section format introduced in 0.8.0 and exact-output exceptions. These are product requirements, not deductions from STE or competitor results.
- Keep English labels, section digits, structural colons and Q/R/I IDs in ASCII. This supports predictable parsing; ordinary punctuation in multilingual prose stays local to the language.
- Use the five-item target for routine scan lists, not requested exhaustive findings. Keep every failure and material finding; the many-findings eval checks all nine supplied defects and locations.
- Make brevity and item counts targets. Do not omit required evidence, and do not create an unrequested file only to keep a reply short.
- Put the useful result in the first body line. Place the one-sentence Conclusion after the body and before the fixed status list. Call this the “Conclusion after the body” so “last” cannot be read as the final output line.
- Make the pre-send check conditional on the full format. A one-fact or exact-output reply must not be forced into a footer.
- Keep token reduction, technical-document standards, and reader-facing answer quality distinct. Headroom can steer terse output, but its output-token measure does not test comprehension or the required reply layout.

These changes do not establish improved comprehension. A human or independent, blinded evaluation is still needed before claiming a user-readability gain.
