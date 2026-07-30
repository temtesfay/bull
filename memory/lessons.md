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

### 2026-07-30 — SEC EDGAR is unreachable from this environment; go to the company's own IR site instead
- **What happened:** Tried to apply yesterday's lesson by going straight to a
  primary source instead of trusting Perplexity's summary. Both the web
  fetch tool and a direct `curl` (with a proper `User-Agent`) to
  `www.sec.gov` and `data.sec.gov` failed — the fetch tool got HTTP 403 from
  SEC's own server, and `curl` never even reached SEC because the
  environment's outbound network policy rejected the CONNECT to
  `data.sec.gov:443` before it left the container.
- **What I believed at the time:** That EDGAR would be the most reliable
  primary source since it's the regulator's own filing archive.
- **What was actually true:** EDGAR is not reachable from this environment,
  full stop, for either tool. It's not a rate limit or a bad URL problem —
  it's blocked at the network layer for `curl` and returns 403 for the fetch
  tool. Company IR sites (e.g. `microsoft.com/en-us/investor/...`) worked
  fine and are still a legitimate primary source under the research diet
  rule (it's the company's own press release, not sell-side commentary).
- **What changes:** Stop trying EDGAR first. Go directly to the company's
  own investor-relations site for earnings releases and filings indexes.
  Only reach for EDGAR mirrors/aggregators as a last resort, and treat them
  as leads to verify (per the 2026-07-29 lesson), not as the source itself.

### 2026-07-30 — `alpaca.py quote` was silently broken since day one
- **What happened:** Tried to pull a current price for MSFT to check
  valuation. `python3 scripts/alpaca.py quote MSFT` returned `{}` — looked
  like no data was available (plausible pre-market).
- **What I believed at the time:** That the empty result meant Alpaca's data
  feed had nothing for that symbol at that time of day, or that this run's
  paper account had a data-plan limitation.
- **What was actually true:** Calling the underlying snapshots function
  directly showed Alpaca returns the requested symbols at the top level of
  the JSON response with no `snapshots` wrapper key. The CLI's `quote`
  command did `get_snapshots(args.symbols).get("snapshots", {})`, which
  always evaluated to `{}` — a code bug, not a data problem. This means
  every past and hypothetical use of `quote` would have silently returned
  nothing and could have been misread as "no data available" rather than
  "the parser is wrong."
- **What changes:** Fixed `scripts/alpaca.py` (`quote` now falls back to the
  raw response when there's no `snapshots` wrapper) and verified it returns
  real prices. General takeaway: when a script returns suspiciously empty
  output, check the raw API response before concluding the data doesn't
  exist — an empty result and a parsing bug look identical from the output
  alone.

### 2026-07-30 — Three straight runs have landed on a branch, not `main`
- **What happened:** `CLAUDE.md` and every file in `routines/` are explicit:
  work must land on `main` because midday/close/weekly-review start from a
  fresh checkout of `main`, and `SETUP.md` says the environment "must have
  'push to `main`' enabled." This run (and, per `git log`, the two before
  it — bootstrap and the MSFT research run) instead ran inside a session
  whose harness-level instructions designated a fixed working branch
  (`claude/magical-rubin-e1byxh`) and explicitly forbade pushing anywhere
  else without permission. `origin/main` is still sitting at `1af572d`
  ("SETUP.md" doc commit) — none of the actual trading memory (bootstrap,
  MSFT watchlist entry, this run's skip) has ever reached it.
- **What I believed at the time:** That committing and pushing to the
  branch I was placed on satisfied "land on main," since the prior two runs
  in this same chain did the same thing and I could still read their memory
  updates on wake.
- **What was actually true:** I could read the prior runs' memory only
  because I started from the *same persistent branch*, not from `main`. If
  a routine (e.g. the midday or close check) is ever scheduled to start from
  a fresh `main` checkout as the docs describe, it would see none of this —
  no positions history, no watchlist, no lessons past `1af572d`. The
  handoff between routines is currently working by accident (same branch
  reused) rather than by design (main advancing).
- **What changes:** Flagging this to the human via notification rather than
  trying to force a push to `main` against the explicit session-level branch
  restriction — that restriction is a harder constraint than `CLAUDE.md`'s
  general guidance and isn't mine to override. Future runs: if you find
  yourself pinned to a non-`main` branch again, check `git log origin/main`
  vs. your branch before assuming continuity is intact, and say so if they've
  diverged. This needs a human fix (either enable direct main pushes per
  `SETUP.md`, or point the scheduler at `main` instead of a fixed branch).
