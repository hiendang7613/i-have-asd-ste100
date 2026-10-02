# Changelog

## 0.4.1 — 2026-10-02
- Sections start their own line with the number first (`**0.Done:**`), not as list items, with one blank line between sections. Without the blank line, Markdown merges a section into the list above it (checked with the GitHub Markdown API); the checker now reports that case.

## 0.4.0 — 2026-10-02
- New closing shape, designed with the first user: a one-sentence **Conclusion:** line, then numbered sections in a fixed order: 0.Done, 1.InProgress, 2.Questions, 3.Pending, 4.Backlog. Empty sections are left out; numbers never move.
- Questions hold everything that needs the user, including approvals ("Approve: ..."). The recommended option is `<a>` in a code span, because a bare `<a>` or `<b>` is an HTML tag that Markdown renderers delete (checked on GitHub); other options are (b), (c).
- No emoji and no square brackets anywhere in a reply; status is written in words. Section numbers replace icons as the same anchor in every language.
- The checker understands the new shape: section order and range, empty sections, exactly one `<a>` per question with options, emoji, square brackets, and replies wrapped in a code block.
- README, hero image, examples in five languages and social preview follow the new shape.

## 0.3.0 — 2026-10-02
- Format layer for fast reading: the five block lines carry fixed icons (🎯 🔑 👉 ❓ 📌) that mean the same in every language; status icons ✅ ❌ ⏳ always come with words; every bullet starts with its key; code spans only for exact strings; a bold budget; tables only for comparisons; no headings in normal replies.
- The block lines are list items, so Markdown renderers never merge them into one paragraph.
- All icons are single wide code points without variation selectors, so terminal columns stay aligned; a test enforces it.
- "no icons" removes the icons for a session.
- The checker reads a line's role from its icon in any language, so the order is checked even for unknown labels.
- README redesign: SVG before and after hero, format table, comparison table with measured word and sentence counts, FAQ; new social preview.

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
