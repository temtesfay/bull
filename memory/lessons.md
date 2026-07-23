# Lessons

Append-only. Things that went wrong and what changed as a result.

This file is the only mechanism by which Bull actually improves. A run that
produces no trades but one honest lesson has done more for long-run
performance than a run that produces three trades and no reflection.

Write a lesson when:
- A thesis was wrong, and you can name why
- A process failed (bad data, missed push, auth error, stale file)
- You noticed yourself reasoning badly (anchoring on entry price,
  rationalizing a loser, trading to look busy)

Do NOT write a lesson for: a position that went down for reasons your thesis
already anticipated. That is not a lesson, that is variance.

## Format

```
### YYYY-MM-DD — short title
- **What happened:**
- **What I believed at the time:**
- **What was actually true:**
- **What changes:** a concrete behavior change, or "nothing — this was variance"
```

---

_Empty._
