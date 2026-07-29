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

### 2026-07-29 — Perplexity synthesis is not a substitute for reading the filing
- **What happened:** First-ever run. Account was empty (no positions, no
  watchlist), so I tried to bootstrap the watchlist by asking Perplexity for
  large-cap tech/growth candidates with a thesis, catalyst, and valuation vs.
  5-year range.
- **What I believed at the time:** That a well-scoped Perplexity prompt asking
  for primary-source grounding would return citable facts I could use to
  write a real thesis.
- **What was actually true:** The response had the shape of rigor (specific
  8-K/10-K tags like `[MSFT-8K-Q3FY26]`) but no real links to those filings,
  no actual reported numbers, and hedged qualitative language ("toward the
  upper half of its range") standing in for a number I could verify. The
  citation list returned by the API was generic finance-content sites, not
  SEC EDGAR or IR pages. This is exactly the failure mode `strategy.md`
  already warns about: Perplexity is for finding sources, not for
  substituting its own summary for one.
- **What changes:** Do not add a watchlist candidate on a Perplexity
  narrative alone. Either pull the actual filing (EDGAR, company IR page) and
  read the real numbers, or don't write the thesis yet. If Perplexity's
  citations aren't primary sources (EDGAR, IR, official press release), treat
  the answer as a lead to verify, not a fact to log.
