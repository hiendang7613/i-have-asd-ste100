# Changelog

## 0.2.0 — 2026-10-02
- Language-neutral rules: the labels are written in the user's language; the injected rules name no language and use only ASCII, because a named language pulls replies toward it.
- Sentence length for scripts without spaces is measured in characters; the checker finds the block by structure, knows label sets in ten languages, and splits sentences on CJK punctuation.
- Scope: the block goes only in the final message of a turn and only in text a person reads, never in agent messages, commits or files.
- Errors: state the cause only when checked; otherwise "cause not known" plus the check that would find it.
- Abbreviations are spelled out at first use; no telegraphic style; the five-item cap applies to lists the reader must act on.
- "stop ste mode" now works anywhere in a prompt, except inside quotes or code; the per-session state moved from the temp directory to the Claude config directory.
- Examples in Chinese, Japanese and Spanish; README with a direct comparison to i-have-adhd.

## 0.1.1 — 2026-10-02
- On by default after install: the SessionStart hook injects the rules and a one-line reminder is added to each prompt.
- Opt out everywhere with `.i-have-asd-ste100-off` in `~/.claude` or `$CODEX_HOME`, or per process with `I_HAVE_ASD_STE100=off`.

## 0.1.0 — 2026-10-02
- First version: skill, opt-in hooks, offline reply checker, ten eval cases, Claude Code and Codex manifests.
