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

### 2026-07-30 — `notify.py` was silently blocked by the webhook host's bot filter
- **What happened:** End-of-day routine. `python3 scripts/notify.py` (with
  `NOTIFY_WEBHOOK_URL` set) failed with `ERROR: webhook returned 403: error
  code: 1010`.
- **What I believed at the time:** That this might be another instance of
  the network policy blocking the request outright (like the SEC EDGAR
  case), or a genuinely dead/misconfigured webhook URL — either way, an
  unfixable environment problem to report and move past.
- **What was actually true:** Error code 1010 is Cloudflare's bot-signature
  block, and the specific, well-known trigger is Python's default
  `urllib` User-Agent header (`Python-urllib/3.x`), which many Cloudflare
  configs flag as a bot regardless of the request's legitimacy. The script
  sent no `User-Agent` at all. Adding a normal browser-like one
  (`Mozilla/5.0 (compatible; BullBot/1.0)`) fixed it immediately — verified
  with a real test notification that returned 204.
- **What changes:** Fixed `scripts/notify.py` to send a `User-Agent` header
  on every request. General takeaway: a 403 from a webhook/API host is not
  automatically "environment network policy" or "dead URL" — check the
  response body for a specific error code (Cloudflare 1010, 1015, etc.)
  before concluding it's unfixable. This one was a one-line fix, and without
  it, notifications — including future `urgent` escalations — would have
  been silently failing every single run.

### 2026-07-31 — An anomalous price move from Alpaca needs a plain news search to sanity-check, not a demand for a "primary source"
- **What happened:** `alpaca.py quote MSFT` showed a +15.48% one-day move
  (prevDailyBar close $391.00 on 2026-07-29 → dailyBar close $451.545 on
  2026-07-30). That's a very large move for a mega-cap, so before writing
  it into the watchlist as fact I tried to verify it the way the research
  diet rule says to verify everything: primary sources only. I asked
  Perplexity, restricted to SEC filings/IR pages, to confirm MSFT's
  closing prices for 07-28/29/30. It correctly refused — company IR sites
  and SEC filings do not publish daily closing stock prices, so there was
  no primary source to cite, and it said so instead of fabricating one.
- **What I believed at the time:** That the "primary sources only" rule
  from `strategy.md` applied to this too, and that if I couldn't get a
  primary-source citation for the price I should treat it as unverified.
- **What was actually true:** The research-diet rule is about *thesis*
  claims — revenue, growth rates, guidance — where sell-side spin and
  aggregator errors are the risk. Raw price ticks are a different kind of
  fact: Alpaca (the broker) is the authoritative source for those per
  `CLAUDE.md` ("the broker is authoritative"), not a filing. The right way
  to sanity-check an anomalous *price move* is a plain, unrestricted news
  search for the market reaction (which is exactly what surfaced that the
  move was plausible: MSFT was ~19-20% off its highs going into a strong
  beat, after-hours was already +2-8% right after the release, and the
  move could plausibly extend through the following regular session) —
  not to route it through the same primary-source filter used for
  fundamentals.
- **What changes:** When a broker-reported price move looks too large to
  be true, verify it with a general news search for the market reaction,
  not by asking a primary-source-restricted query that can only ever come
  back empty. Keep the primary-source-only rule for thesis facts (revenue,
  growth, guidance); don't apply it to raw market data, which the broker
  already authoritatively provides.

### 2026-07-31 — A run that trades must be the run that logs, updates memory, and pushes, in the same run
- **What happened:** This intraday risk-reduction run started with
  `portfolio.md` saying 0 positions and `trade-log.md` saying no trades
  ever, per `main` as of commit `5aba839`. `alpaca.py positions` showed a
  real MSFT position (filled 2026-07-31 13:46:11 UTC, $456.70 avg, $1,000
  notional) that matched the plan drafted in yesterday's `watchlist.md`
  entry almost exactly. The position also had no trailing stop, which
  `strategy.md` requires for every satellite position once it's a full-share
  size.
- **What I believed at the time:** Given `CLAUDE.md`'s framing ("if
  portfolio.md disagrees with Alpaca, Alpaca is right"), this looked like it
  could be ordinary drift. But the size of the gap — an entire trade with no
  trace anywhere in memory, plus a missing required trailing stop — points
  to something more specific than normal lag.
- **What was actually true:** The market-open routine executed the buy (the
  order exists on the broker, filled correctly) but its run either never
  reached the "write memory / commit / push" step, or reached it and the
  write/commit/push silently failed. Either way, the state that should have
  landed on `main` — the trade-log entry, the portfolio update, and the
  trailing stop — never did. Only the order itself, placed directly against
  the broker, survived. This is the specific failure mode `CLAUDE.md`
  describes generically ("a drift means something failed silently") but
  this is the first time it's actually happened with a real trade attached,
  not just a stale reconciliation of an empty book.
- **What changes:** Two things. (1) When ground truth shows a position or
  order that isn't in memory, don't just reconcile the numbers — check
  `orders --status all` for the fill details and backfill a full trade-log
  entry with real reasoning (recovered from the watchlist plan that
  presumably drove it), not just an updated snapshot number. A position
  with no logged thesis is unmanageable by the next Bull. (2) Every routine
  that can place orders should treat "commit and push landed on `main`" as
  part of the trade itself, not a cleanup step that can be skipped if the
  run ends early — an order that fills but is never logged or protected
  with a stop is a worse outcome than not trading at all, because it's
  invisible until a later run stumbles onto it by chance.

### 2026-07-31 — a bare `git log origin/main` can read a stale ref; always `git fetch` first when checking whether main actually advanced
- **What happened:** At the start of this daily-close routine, `git log
  origin/main` (no prior fetch this session) showed `main` four commits
  *behind* the local checked-out branch — as if a prior PR had merged into
  the feature branch instead of into `main`. That would have been a serious
  process failure worth an urgent flag. Before writing it down, checked the
  GitHub API directly (`list_branches`) and it showed `main` at the exact
  same commit as local HEAD. An explicit `git fetch origin main` then
  updated the local remote-tracking ref and `git log origin/main` matched
  reality.
- **What I believed at the time:** That `git log origin/main` without an
  explicit fetch reflects current remote state, since the working tree had
  just been freshly checked out for this run.
- **What was actually true:** The local `origin/main` ref can be stale
  relative to the actual remote even at the start of a fresh session-scoped
  checkout, apparently because the initial clone/checkout only fetches the
  branch being worked on, not `main`. Reading it without fetching first
  produces a plausible-looking but wrong diff.
- **What changes:** Before drawing any conclusion about whether `main` has
  advanced, diverged, or received a prior run's push (the check `CLAUDE.md`
  explicitly asks for), always run `git fetch origin main` first, or
  cross-check against the GitHub API. Do not trust a same-session
  `git log origin/main` that hasn't been preceded by an explicit fetch of
  `main` specifically.
