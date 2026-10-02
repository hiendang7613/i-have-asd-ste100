# Eval suite

Ten cases for `claude plugin eval` (native format: `prompt.md` plus `graders/*.md`). Running them calls paid models.

| Case | What it tests |
| --- | --- |
| status-report-en / status-report-vi | Full block, failure and pending approval kept, English and Vietnamese labels |
| decision-request-vi | One question, three options, recommended default |
| bad-news-first-en | The Conclusion line names the skipped step |
| one-fact-answer | No block for a one-fact answer |
| exact-output-json | Only JSON, no block |
| explain-detail-en | Full explanation allowed, still ends with the block |
| destructive-action-vi | Confirmation and warning before any step |
| negation-and-condition-en | Negations and conditions survive a summary |
| many-findings-en | At most five visible items, high severity first, the rest grouped |

Graders: `regex` graders are free (block lines present or absent, no filler, exact answer). `llm` graders are paid and judge
meaning (must-keep facts, weight 3) and readability (weight 2).

Activation: the hooks are on by default, so the with-plugin arm gets the rules and the no-plugin arm is the baseline.
Check the regex "conclusion-line" result of the with-plugin arm before trusting any score, and make sure no opt-out file
(`~/.claude/.i-have-asd-ste100-off`) exists on the machine that runs the suite.

Suggested first run (about ten cases, one run each, two arms; owner approval needed):

```bash
claude plugin eval . --model haiku --runs 1 --max-cost-usd 2 --no-publish
```
