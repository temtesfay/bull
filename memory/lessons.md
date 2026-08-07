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

### 2026-07-31 — First weekly review: the failures are operational, not analytical, and self-discipline alone won't catch the next one
- **What happened:** First-ever weekly review (routine 5). Account is 2
  calendar days old (funded 2026-07-29), so "this week" and "since inception"
  are almost the same number — see the full review sent via notify for the
  numbers. Process audit turned up that in those 2 days, three separate
  silent failures occurred and were each caught only by a *later* run
  stumbling onto the discrepancy by chance, not by any check designed to
  catch it: `alpaca.py quote` silently returned `{}` from a parsing bug,
  `notify.py` was silently dropped by a Cloudflare bot filter, and — most
  seriously — the market-open run that placed the account's only real trade
  (MSFT buy) never wrote it to `trade-log.md`/`portfolio.md`, never pushed to
  `main`, and never set the required trailing stop, leaving a live,
  unprotected position invisible to memory for hours until an intraday run
  happened to check the broker directly.
- **What I believed at the time:** That "read this first, write this last"
  plus each run's own diligence would be enough discipline to keep memory
  and the broker in sync, since every run *intends* to complete the
  write-commit-push sequence.
- **What was actually true:** Intent isn't a control. Each of these three
  failures happened inside a run that believed it was following the rules
  correctly; the gap was only visible from the *next* run's outside view.
  A stateless agent that reasons well on any single wake but has no
  cross-run enforcement will keep having exactly this failure mode — good
  decisions with silently-lost side effects — no matter how carefully any
  one run's reasoning is graded.
- **What changes:** Proposing (not implementing — this is a tooling/process
  change, not a `strategy.md` rule, but flagging it here since it's the one
  concrete lever this review found): add a mechanical check, not a reminder,
  that a run cannot end "successfully" after placing an order unless (a) a
  matching `trade-log.md` entry exists, (b) `portfolio.md` reflects the new
  position, (c) a required trailing stop order exists on the broker for any
  full-share satellite position, and (d) the commit actually landed on
  `main` (fetch-and-compare, not a local assumption) — e.g. a `scripts/`
  post-trade verification step that fails loudly instead of trusting the
  next run to notice. Until something enforces this mechanically, treat
  every "the trade went fine" self-report with skepticism and keep
  re-verifying against the broker directly, per `CLAUDE.md`'s own framing.

### 2026-08-05 — Alphabet's own IR/investor domains are blocked at the network layer, same pattern as SEC EDGAR
- **What happened:** Tried to source a second watchlist candidate. Perplexity
  surfaced a Google Cloud growth-acceleration lead (GOOGL) but gave
  internally inconsistent numbers across snippets (+32% in one place, +82%
  in another, for the same metric) — exactly the synthesis-not-substitute
  problem from the 2026-07-29 lesson, so it needed primary-source
  verification before going anywhere near the watchlist. Both `WebFetch`
  (`abc.xyz/investor/`, `abc.xyz/assets/investor/.../2026Q2_alphabet_earnings_release.pdf`)
  and a direct `curl` with a normal User-Agent to `abc.xyz`,
  `investor.google.com`, and `www.investor.google.com` all failed. The
  proxy status endpoint (`$HTTPS_PROXY/__agentproxy/status`) confirmed these
  were `connect_rejected` / gateway-403 on the CONNECT tunnel, not a
  site-side block — i.e. the environment's outbound network policy, not
  Alphabet's server.
- **What I believed at the time:** That since Microsoft's IR site (a
  comparable large-cap company site) worked fine, any company's own IR
  domain would be reachable, and a 403 here would mean the same thing it
  meant for `notify.py` — a fixable bot-filter issue.
- **What was actually true:** This is a network-policy allowlist/denylist
  issue like the 2026-07-30 SEC EDGAR finding, not a per-site quirk to work
  around with headers. Some primary-source domains are reachable
  (`microsoft.com`), others are not (`abc.xyz`, `google.com`
  investor subdomains, `sec.gov`), and there's no way to know which without
  trying. This is out of Bull's control to fix — it's an environment
  network policy, not a code bug.
- **What changes:** Before spending real effort building a thesis on a
  company, do one cheap reachability probe of its IR domain first (a quick
  `curl -o /dev/null -w "%{http_code}"`) rather than discovering the block
  after Perplexity research is already done. When a primary source is
  network-blocked, don't fall back to Perplexity's synthesis as a
  substitute — per the 2026-07-29 lesson, an unverifiable number is not a
  thesis; the candidate stays unwritten until it can be verified, even if
  that means the watchlist stays empty longer than would be ideal.

### 2026-08-04 — `alpaca.py quote`'s snapshot feed lags pre-market; `positions[].current_price` is the fresher mark
- **What happened:** Pre-market research routine. `alpaca.py quote MSFT`
  showed `last: 487.575` (a Monday 2026-08-03 16:00 ET close print, per the
  raw snapshot's `latestTrade.t`), which would have implied MSFT hadn't
  moved at all overnight. But `alpaca.py positions` reported
  `current_price: 478.19` against `lastday_price: 487.65` — a real ~2%
  pre-market move the `quote` command's snapshot data didn't reflect at all.
- **What I believed at the time:** That `quote` and `positions` would agree
  on "current price" since both ultimately come from Alpaca, and that a
  flat `quote` reading meant nothing had moved pre-market.
- **What was actually true:** `quote`'s snapshot endpoint (IEX/free feed)
  simply had no newer trade to report pre-market — its `latestTrade` and
  `latestQuote` were both still timestamped at Monday's regular-session
  close. Alpaca's own position `current_price` field, used for
  `unrealized_pl`, is marked more currently (evidently from a feed that
  does see pre-market activity) and is the one that actually moved. Using
  `quote` alone pre-market would have under-reported an overnight move —
  in this case a small, non-thesis-breaking dip, but the same gap could
  hide a real gap-down on a day it mattered.
- **What changes:** For overnight-gap checks specifically (not general spot
  quotes), prefer `positions[].current_price` vs `lastday_price` over
  `quote`'s snapshot fields when checking pre-market — it's the field that
  actually updates before the open. If `quote` and `positions` disagree,
  treat `positions` (closer to the broker's own P&L calc) as the more
  current one, consistent with `CLAUDE.md`'s "the broker is authoritative."

### 2026-08-06 — PRs were closing without merging into `main`; two trading days of memory writes were invisible to `main` until this run caught it
- **What happened:** Daily-close routine. Before writing this run's entry,
  fetched `origin/main` explicitly and cross-checked open/closed PRs via
  the GitHub API (per the 2026-07-31 lesson's own instruction not to trust
  an unfetched ref). `main` was sitting at PR #12 — the 2026-08-04 daily
  close. Everything since (2026-08-05's full day of routines, plus today's
  pre-market and market-open runs) existed only on the feature branch
  `claude/nice-sagan-0ur9ie`. PRs #13, #14, #15 had all been opened
  correctly with `base: main`, but the GitHub API shows each one as
  `state: closed`, `merged: false` — closed without ever being merged.
  Meanwhile the local branch history shows merge commits for those same
  PRs, but merged into the *next feature branch*, not into `main`. Every
  affected run's own commit message said things like "reconciled clean" or
  "confirmed still live" and believed the write-commit-push sequence had
  succeeded, because from inside that run it had — the branch push
  worked. The failure was one layer up: PR→main never happened.
- **What I believed at the time:** Nothing to believe yet — this is the
  run that found it. But it's worth noting every run in the affected
  window (five of them) had no way to detect this from inside its own
  scope; each one's local checkout was seeded from the previous unmerged
  branch, so `git log` looked internally consistent even though none of
  it had reached `main`.
- **What was actually true:** Merging a PR by running `git merge` locally
  and pushing the result to the *next* feature branch satisfies nothing —
  GitHub only marks a PR merged when the merge lands on the PR's actual
  base branch via a tracked commit (or the merge API). Whatever process
  produced those local merge commits (likely a prior run doing `git merge
  <branch>` while checked out on its own new feature branch, instead of
  merging into `main` and pushing there, or using the merge API) closed
  the PR as a side effect without merging it. This is the 2026-07-31
  lesson's exact failure mode ("intent isn't a control") recurring at the
  branch/PR level instead of the trade-log level — a mechanical check
  would have caught it; narrative self-report from each run did not.
- **What changes:** (1) This run merges the accumulated branch into `main`
  using the GitHub merge API directly (`merge_pull_request`), not a local
  `git merge`, specifically because a local merge is what silently caused
  this. (2) Every future run should verify the merge actually landed by
  re-fetching `origin/main` afterward and confirming the SHA matches what
  was just merged — not just checking that `gh pr merge`/the API call
  returned success. (3) Flagging this to the human in today's notification
  rather than treating it as routine, since it's a process failure that
  recurred across multiple runs in exactly the way a prior lesson already
  warned about — worth knowing whether the branch-then-PR workflow itself
  needs to change (e.g. direct push to `main` if permissions allow) rather
  than relying on each run to re-derive the fix.

### 2026-08-07 — Second weekly review: the core ETF sleeve has never been funded, and that gap is not explained by the network block
- **What happened:** Second weekly review (first was 2026-07-31). Sat down to
  grade process, not P&L. This week: portfolio +0.07% vs SPY +5.24% (07-31
  close to today); since inception (2026-07-29): portfolio +0.09% vs SPY
  +5.97%, delta -5.88%. Zero trades, zero guardrail rejections, zero
  watchlist candidates added this week — the book is unchanged from a week
  ago: one MSFT position (~1.1% of equity), ~99% cash. Went looking for a
  process failure to name honestly (per this routine's own instruction not
  to grade every week "fine") and found one that isn't just "network policy
  blocked candidate sourcing again": `strategy.md` calls for a **10–40% core
  in broad index ETFs** (SPY, VTI, or similar), independent of the satellite
  circle-of-competence sourcing that's been network-blocked since
  2026-08-05. Buying SPY or VTI needs no company-specific primary-source
  filing at all — it needs a price, which Alpaca (the broker, already
  authoritative per `CLAUDE.md`) provides directly. Nine trading days in,
  no run has ever evaluated or attempted a core ETF buy. Every daily entry
  frames the ~99% cash position purely as "cash-drag from the satellite
  side being blocked," which is true but incomplete — it quietly excuses a
  sleeve of the strategy that was never blocked in the first place.
- **What I believed at the time (implicit, across every daily run this
  week):** That "no watchlist candidates, network policy blocks sourcing"
  fully accounts for the account sitting almost entirely in cash.
- **What was actually true:** The satellite-sourcing block and the
  core-ETF gap are two different problems with two different causes. One is
  an environment constraint outside Bull's control. The other is a plan
  that was never executed — no run treated "build the core sleeve" as a
  task with its own criteria to check, so it fell through by default rather
  than by decision. A strategy with a 10–40% core target and a 12-month
  horizon that reaches day 9 at 0% core is not "cautious," it's an
  unexecuted allocation.
- **What changes:** Proposing to the human (not editing `strategy.md`
  myself): (1) clarify whether the core ETF sleeve is meant to be
  established promptly and independently of satellite timing — if so, a
  future pre-market or market-open run should treat "is the core funded to
  at least its 10% floor" as an explicit check alongside the existing
  thesis/trigger checks, the same way the trailing-stop check is a standing
  item every run. (2) The buy criteria in `strategy.md` (falsifiable
  thesis, catalyst, valuation-vs-range, no macro call, liquidity) read as
  written for satellite stock-picks; it's not clear they're meant to gate a
  core index buy at all, and no run has ever tried to apply them to one.
  Worth the human saying explicitly whether core ETF buys are exempt from
  those five criteria (a broad index isn't a stock thesis) or whether a
  different, simpler bar applies. Until that's answered, this stays a
  proposal, not a trade — no core position was opened by this review.
  Sample size: 2 weekly reviews completed since inception (2026-07-29);
  under any read of "week," this is nowhere near the 26-week bar for
  distinguishing process from luck, and neither is the MSFT position's
  9.48% vs. SPY's 5.24% over the same holding window (a single name, five
  trading days) — noted as a data point, not evidence of stock-picking
  skill.

### 2026-08-06 — the network block on non-Microsoft primary sources is broad, not per-IR-page: it looks like a narrow domain allowlist
- **What happened:** Building on the 2026-08-05 finding that Alphabet's IR
  domains were blocked, today's research routine ran a cheap reachability
  probe (per that lesson's own recommendation) across five other candidate
  IR domains before spending any Perplexity effort: `ir.aboutamazon.com`,
  `investor.atmeta.com`, `investor.nvidia.com`, `investors.broadcom.com`,
  `www.apple.com`. All five failed to connect. Widened the probe further to
  test whether this was specific to "investor relations" subdomains —
  `ir.tesla.com`, `investor.visa.com`, and even a plain general corporate
  site, `www.costco.com`, were blocked too. `microsoft.com` remained
  reachable throughout (confirmed via `curl`, HTTP 301).
- **What I believed at the time:** That the 2026-08-05 block was specific
  to Alphabet's domains, or maybe to "investor relations" subdomains as a
  category, and that other companies' IR pages would likely work like
  Microsoft's did.
- **What was actually true:** The proxy status endpoint
  (`$HTTPS_PROXY/__agentproxy/status`) confirmed every one of these was a
  `connect_rejected` / gateway-403 on the CONNECT tunnel — a network-policy
  denial, identical in kind to the SEC EDGAR and Alphabet blocks, not a
  site-specific quirk. With eight domains now tested across very different
  companies and even a non-IR general site (Costco) also blocked, this
  reads like a narrow outbound allowlist that happens to include
  `microsoft.com` rather than a blocklist targeting specific "problem"
  sites. In practice, MSFT may currently be the only name in the circle of
  competence whose primary sources are reachable at all from this
  environment.
- **What changes:** Stop treating each new company's IR block as a
  one-off surprise to rediscover — assume, until told otherwise, that only
  `microsoft.com` (and whatever else has been separately confirmed
  reachable, e.g. `sec.gov` is confirmed *unreachable*) is available for
  primary-source verification. This makes new-candidate origination via
  the required "read the real filing, not Perplexity's summary" process
  effectively blocked for now — not a Bull process failure, an environment
  constraint outside Bull's control to fix. Worth surfacing to the human
  directly (this is exactly the kind of thing `CLAUDE.md`'s escalation
  list doesn't explicitly cover but should probably know about) rather
  than quietly absorbing it as "no candidate sourced again today." Do not
  spend a full Perplexity research pass on a new name before confirming
  its primary-source domain is reachable first — the reachability probe
  costs one `curl` call; a full research pass that turns out unverifiable
  costs much more and still can't be written down per existing policy.
