---
description: 'Nine review findings: at most five visible items, highest severity first, the rest grouped.'
tags: [shape, en, review]
runs: 3
max_turns: 2
timeout_seconds: 180
allowed_tools: []
---

Report these review findings to me:
high: SQL injection in api/search.py:41; high: missing auth check in api/admin.py:12; medium: N+1 query in views/list.py:88;
medium: no timeout on http client in sync.py:20; medium: broad except in worker.py:65; low: unused import in utils.py:3;
low: typo in README.md:10; low: long function in report.py:120; low: magic number in config.py:7.
