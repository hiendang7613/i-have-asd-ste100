---
type: llm
weight: 3
---

Pass if both high-severity findings (api/search.py:41 SQL injection and
api/admin.py:12 missing auth check) appear first with their locations, no visible list has more than five items, and the
remaining low or medium findings are grouped or summarised with their count rather than dropped silently.
