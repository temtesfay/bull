# Watchlist

Candidates with a thesis forming but no position yet. Promotion to a position
requires the buy criteria in `strategy.md`.

Retire anything that has sat here more than 60 days without a catalyst. A
stale watchlist is worse than an empty one because it invites lazy buying.

## Format

### TICKER
- **Thesis forming:** what you think might be true
- **What you're waiting for:** the specific trigger
- **Added:** date
- **Review by:** date

---

*(No open candidates. MSFT was researched here 2026-07-30/31, cleared buy
criteria, and was promoted to a position on 2026-07-31 — see `portfolio.md`
and `trade-log.md` for the live thesis. Full research trail for that
promotion is preserved in git history rather than repeated here.)*

---

## Plan for today — 2026-08-10

Ground truth via Alpaca: equity $100,094.36, cash $99,000.00, day change
-0.0% ($-0.42), `trading_blocked: false`. `clock` shows `is_open: false`
pre-open (checked ~08:41 ET), `next_open`/`next_close` both today
(2026-08-10, Monday) — not a holiday, normal session. No discrepancy
against `portfolio.md`/last known state (MSFT qty 2.189599299, avg entry
$456.70, matches exactly).

**Position thesis check (MSFT, the only open position):** queried
Perplexity, restricted to SEC filings / official Microsoft IR / official
corporate statements, for anything dated 2026-08-07 through today touching
Azure guidance, commercial RPO, or AI capex. Result: no new 8-K, no new IR
release, no new guidance — most recent primary-source item remains the
2026-07-29 FY26 Q4 print (Microsoft Cloud revenue $59.3B +27% YoY, Azure
+43% YoY, commercial RPO $678B +84% YoY). **Thesis intact, unchanged.**

**Overnight/weekend price check:** `quote MSFT` shows `prev_close` $500.035
-> `last` $499.875, essentially flat (-0.03%) — no gap. `positions` shows
current $499.80 vs $456.70 entry, +9.4% unrealized, nowhere near the
-7%/-15% sell triggers. Position is ~1.09% of equity.

**Trailing stop:** `orders --status open` confirms the 10% trailing stop
(`cee441de-48ae-4e48-9cc2-d6482a4c3b0a`) still live: status `new`, hwm
$505.18, stop price $454.662 — unchanged since 2026-08-07. No action
needed.

**Watchlist candidates:** none open. Re-ran the reachability probe on five
previously-blocked primary-source domains (`ir.aboutamazon.com`,
`investor.atmeta.com`, `investor.nvidia.com`, `abc.xyz`, `sec.gov`) — all
five still fail to connect (`curl` HTTP code `000`). The network-policy
block identified in the 2026-08-05/08-06 lessons has not changed. Did not
pursue Perplexity research on a new satellite name this run for the same
reason as every prior run: no primary source reachable to verify one
against besides Microsoft.

**Core ETF sleeve — new finding, first run since the 2026-08-08 strategy
clarification:** `strategy.md`'s change log (2026-08-08) now says the core
sleeve (10–40%, target ~25%, SPY/VTI/similar) should be "funded promptly
and independently of satellite sourcing" and is exempt from the satellite
buy criteria. No run has acted on this yet — the last portfolio update
(2026-08-07) predates the clarification, and the account is still 0% core,
~99% cash outside the one MSFT position. Before drafting a size, checked
`scripts/guardrails.py`: `max_position_pct` is a flat 5% cap applied
identically to every symbol, with no carve-out for core index ETFs, and
`max_order_notional` caps any single order at $2,000. **A single ticker
cannot reach the ~25% target under the current code-enforced guardrail** —
5% of equity (~$5,000 today) is the hard ceiling for SPY or VTI alone, and
even that would take three $2,000-ish orders across separate weeks (the
$2,000 per-order cap and 3-new-positions-per-week cap both bind). Reaching
25% at all would require diversifying across multiple broad-market index
tickers (e.g. SPY + VTI + IVV + ITOT + SCHB), several of which are
near-duplicate S&P 500 exposure — not a decision this run should make
unilaterally, since it's a policy/config question in the same category
`CLAUDE.md` reserves for the human on `strategy.md` itself. See
`lessons.md` for the full writeup.

**Draft proposal for the market-open routine (NOT executed by this run —
this is a research routine only):**

- **Ticker:** SPY
- **Direction:** BUY (core index sleeve, first tranche)
- **Size:** $2,000 (~2.0% of equity — sized to the per-order cap, not a
  view on timing)
- **Reasoning:** `strategy.md`'s 2026-08-08 clarification makes core ETF
  buys exempt from thesis/catalyst criteria and says to fund the sleeve
  promptly; this is a first, guardrail-clean step (new-position count 0/3
  this week, resulting position ~2% of equity, well under the 5% cap,
  cash reserve stays well above the 10% floor) that moves the account off
  9+ trading days of near-total cash without waiting on the multi-ETF
  diversification question above to be resolved. It does **not** by itself
  close the gap to 25% — that requires either repeated tranches over
  several weeks or human guidance on spreading the sleeve across more than
  one ticker.
- **Guardrails for the market-open routine specifically:** do not buy in
  the first 15 minutes after the open. Re-pull the quote before acting —
  if SPY has moved meaningfully from $773.16 (Friday's close) by market
  open, that's still fine for an allocation-driven index buy (no
  valuation math to invalidate, unlike a satellite thesis), but confirm
  the resulting position stays under 5% of equity at the executed price.

This is a plan, not an order. The market-open routine should re-verify
ground truth per its own instructions before acting.

**No trade executed today; no thesis broken, no gap, no data-source
failure on required checks — not notifying, per this routine's scope.**

---

## Market-open execution check — 2026-08-10

Ran the market-open routine. `clock` confirms `is_open: true` (`next_close`
today 16:00 ET, checked ~09:54 ET, well past the first-15-minute no-trade
window). Today's plan (above, dated 2026-08-10) is dated today, so it's not
stale, and it did contain a drafted buy this time — the SPY core-sleeve
tranche.

Re-verified ground truth via Alpaca: equity $100,108.42, cash $99,000.00
(pre-trade), MSFT +10.84% unrealized ($506.22 vs $456.70 entry), matches
`portfolio.md`, no discrepancy. Re-pulled `quote SPY`: `last` $773.20 vs the
plan's $773.16 reference — 0.01% move, nowhere near the 3% threshold that
would have invalidated the setup.

**Executed:** `alpaca.py buy SPY --notional 2000` — filled immediately,
$773.10 avg, qty 2.586974518, no guardrail rejection (new-position count
was 0/3 this week, resulting position ~2.0% of equity, cash reserve stays
at ~97% of equity, all well inside limits). Full reasoning in
`trade-log.md`. No trailing stop set — `strategy.md` exempts core
index-ETF holdings from stops. Post-trade checklist: trade logged
(`trade-log.md`), `portfolio.md` updated with new position and cash
balance, no stop required (exempt), commit/push pending as the last step
of this run.

No orders rejected. MSFT untouched — no sell trigger fired (up 10.84%,
nowhere near -7%/-15%, ~1.1% of equity).

**Notifying:** per the scheduled task's own instruction ("what was placed,
what was rejected and why, and the resulting cash position"), since a
trade was placed this run.

---

## Plan for today — 2026-08-05

Ground truth via Alpaca: equity $100,087.14, cash $99,000.00, day change
+0.01%, `trading_blocked: false`. `clock` shows `is_open: false` pre-open
(checked ~08:37 ET), `next_open`/`next_close` both today — not a holiday,
normal Wednesday session.

**Position thesis check (MSFT, the only open position):** queried
Perplexity, restricted to SEC filings / official Microsoft IR / official
corporate statements, for anything dated 2026-08-04 through today touching
Azure guidance, commercial RPO, or AI capex. Result: no new 8-K, no new IR
release, no new guidance — the only new primary-source item found in the
window is an old Reid Hoffman board-departure 8-K (not standing for
re-election, dated June 2026, no disagreement stated), which is unrelated
to the thesis. Most recent thesis-relevant filing is still the 2026-07-29
FY26 Q4 print. **Thesis intact, unchanged.**

**Overnight price check:** Alpaca `positions` shows MSFT `current` $496.50
vs yesterday's $495.17, +8.71% unrealized from the $456.70 entry — a small
continuation move, not a gap. Well under the 5% overnight-gap notification
threshold and nowhere near the -7%/-15% sell triggers.

**Watchlist candidates:** none open, so no trigger checks applied.

**New-candidate sourcing (bonus effort, not required by this run's scope):**
Given the account has sat ~99% cash for a week (flagged in several prior
daily entries), spent part of this routine trying to source a second name.
Perplexity flagged Alphabet (Google Cloud revenue acceleration) as a lead,
but gave internally inconsistent growth figures across sources (+32% vs
+82% for the same metric) — the exact "synthesis, not a substitute"
failure the 2026-07-29 lesson warns about. Tried to verify directly against
Alphabet's own IR site and earnings release PDF; both `WebFetch` and a
direct `curl` to `abc.xyz` / `investor.google.com` failed with a
gateway-level `connect_rejected` (confirmed via the proxy status endpoint —
a network policy block, not a site-side issue, same pattern as the SEC
EDGAR block from 2026-07-30). See `lessons.md` for the full writeup.
**Did not add GOOGL to the watchlist** — an unverifiable number is not a
thesis, per existing policy. Amazon and Meta were named as other leads by
Perplexity but were not pursued this run (time-boxed to one name); either
is a reasonable next attempt for a future research run, ideally with a
cheap IR-domain reachability check done first.

**No action planned.** Nothing broken, nothing gapped, no thesis
invalidated, no watchlist trigger fired. Not notifying — data-source
failure was on bonus candidate-sourcing effort, not on required
thesis-integrity checks (MSFT's news source worked fine), so it doesn't
meet this routine's notify bar.

---

## Plan for today — 2026-07-30

Ground truth: $100,000 cash, 0 open positions, `trading_blocked: false`,
day change 0.0% (account untouched since inception). Market not a holiday —
`clock` shows `is_open: false` pre-open, `next_open` today 09:30 ET.

No open positions, so no thesis-break checks were possible or needed. No
prior watchlist candidates, so no trigger checks were possible or needed.

Spent the routine sourcing one real candidate from scratch, applying last
run's lesson: went straight to the company's own IR site for the actual
press release instead of trusting Perplexity's summary. SEC EDGAR itself
(sec.gov, data.sec.gov) returned HTTP 403 to this session's fetch tool and
to a direct `curl` (blocked upstream by the network policy before it even
reached SEC) — noted as a lesson below since it changes where to look first.
Microsoft's IR site worked and gave real, verifiable numbers (see MSFT entry
above). NVDA/GOOGL/AVGO/META were not researched this run — ran out of scope
for one routine to do more than one name properly rather than five names
shallowly.

Also found and fixed a real bug in `scripts/alpaca.py`: the `quote` command
was reading `response["snapshots"]`, but the Alpaca snapshots endpoint
returns symbols at the top level with no `snapshots` wrapper — so `quote`
was silently returning `{}` for every symbol, always, regardless of market
hours. Fixed to fall back to the raw response. Verified working: `quote MSFT
SPY` now returns real prices. This was previously a silent failure — the
prior run reading `quote` output as "no data" would have been wrong; it was
a code bug, not a data availability gap.

**No trade planned for market open.** MSFT is a watchlist candidate, not a
buy candidate yet — it already gapped up on the news before I could check
valuation, and I have exactly one quarter's Azure number, not a trend. Both
gaps need to close before it clears the buy criteria in `strategy.md`. Next
routine (market open) should re-check MSFT's price against its 5-year
multiple range now that `quote` actually works, and pull the FQ3 FY26 Azure
number for comparison, before considering a starter position.

---

## Plan for today — 2026-07-31

Ground truth (pre-market): equity $100,000, cash $100,000, 0 open
positions, `trading_blocked: false`, day change 0.0%. Market not a
holiday — `clock` shows `is_open: false` pre-open, `next_open` today
09:30 ET, `next_close` today 16:00 ET.

No open positions, so no thesis-break checks were needed or possible.
One watchlist candidate, MSFT — trigger check above. Both gating items
from yesterday (trend confirmation, valuation after the earnings pop)
are now resolved and MSFT clears the buy criteria in `strategy.md` (5 of
5, only 3 required).

**Draft proposal for the market-open routine (NOT executed by this
run — this is a research routine only):**

- **Ticker:** MSFT
- **Direction:** BUY (starter position)
- **Size:** $1,000 (1% of equity)
- **Reasoning:** Azure revenue growth accelerated 40% → 43% YoY across
  FQ3 and FQ4 FY26 (both confirmed from Microsoft's own IR site, not
  Perplexity's summary) — a real trend, not a one-quarter data point.
  Despite the stock already running +15.48% the day after earnings to
  $451.545, trailing P/E (~25.2x on FY26 GAAP diluted EPS of $17.95) is
  near the bottom of MSFT's own 5-year P/E range (~25.1x–37.8x): EPS
  growth is outrunning the price move, not the other way around.
- **Why a 1% starter and not the 3% standard size:** conviction alone
  (5/5 criteria, clean valuation math) would support a standard 3%
  entry. Sizing down one notch for two reasons the buy criteria don't
  capture: (a) it's a higher-beta growth name — `strategy.md` says size
  down a notch on those regardless — and (b) the stock already moved
  15% in a single session before this routine could act on it, which is
  chase risk even when the multiple still looks reasonable. A 1% starter
  earns the position without betting size on a single hot day.
- **Invalidation (write this down now, before any fill exists):** Azure
  YoY growth decelerates back below ~35% in the FQ1 FY27 print, or
  commercial RPO growth reverses meaningfully, or capex guidance is cut
  in a way that reads as AI-monetization doubt rather than discipline.
- **Guardrails for the market-open routine specifically:** do not buy in
  the first 15 minutes after the open (`strategy.md` rule). Re-pull the
  quote before acting — if MSFT has gapped meaningfully further from
  $451.545 by market open, that changes the valuation math above and the
  entry should be reconsidered, not assumed still valid. No earnings
  blackout applies (the print already happened).

This is a plan, not an order. The market-open routine should re-verify
ground truth and the price above before acting, per its own instructions.

---

## Intraday risk-reduction check — 2026-07-30 13:09 ET

This routine only reduces risk (no new positions permitted here regardless
of what looked attractive). Ground truth via Alpaca: equity $100,000, cash
$100,000, 0 open positions, day change 0.0%, `trading_blocked: false`,
`orders --status open` → none, market `is_open: true`. No circuit breaker
trip (day change well under 3%).

With zero open positions there was nothing for the sell rules (thesis-break,
-7%, -15%, >5% trim) or the trailing-stop check to act on — all four are
no-ops on an empty book. No action taken. MSFT remains the only watchlist
item, unchanged since this morning's pre-market run; still waiting on
post-open valuation check and the FQ3 FY26 Azure comparison before it can
clear buy criteria — that work belongs to a run that's allowed to open
positions, not this one.

## Intraday risk-reduction check — 2026-07-31 13:xx ET

Ground truth via Alpaca: equity $100,010.86, cash $99,000.01, day change
+0.01% (`trading_blocked: false`) — nowhere near the 3% circuit breaker.
**MSFT is no longer a watchlist candidate — the market-open routine bought
it** (filled 2026-07-31 13:46:11 UTC, $456.70 avg, $1,000 notional per the
plan drafted here yesterday). It's promoted to a position; full detail is
in `portfolio.md` and `trade-log.md`.

That trade had not been written to `trade-log.md`/`portfolio.md` or pushed
to `main` — this run found it only by checking Alpaca directly, exactly as
`CLAUDE.md` warns can happen. Backfilled both files this run; see
`lessons.md` for the process fix.

Sell-rule check on the one open position: MSFT is up 1.09% unrealized, well
inside normal noise, no thesis-break indication (checked general news —
FY26 Q4 beat on both lines, guidance raised, no red flags), position is
1.01% of equity (nowhere near the 5% trim trigger). No sell action taken.

Trailing-stop check: `orders --status open` was empty — MSFT had no stop.
Set a 10% trailing stop this run (`alpaca.py protect MSFT --trail-percent
10`), covering 2 of its 2.19 shares (fractional remainder can't carry a
broker-side trailing stop).

Watchlist is now empty. No new candidates sourced this run — this routine's
scope is risk reduction only, not origination; next candidate sourcing
belongs to a pre-market or research run.

---

## Plan for today — 2026-08-03

Ground truth via Alpaca: equity $100,039.44, cash $99,000.00, day change
+0.02%, `trading_blocked: false`. `clock` shows `is_open: false` pre-open,
`next_open` today 09:30 ET — not a holiday, normal Monday session.

**Position thesis check (MSFT, the only open position):** queried Perplexity,
restricted to SEC filings / official Microsoft IR / official corporate
statements, for anything dated between the 2026-07-29 FY26 Q4 print and
today (2026-08-03) touching Azure guidance, commercial RPO, or AI capex.
Result: no new 8-K, no new IR release, no new guidance of any kind in that
window — the only official filings on record are the 2026-07-29 10-K/8-K
that the thesis is already built on (SEC EDGAR filing index, accession
0001193125-26-323632, cross-checked against Microsoft's own IR SEC-filings
page). **Thesis intact, unchanged.** Price: $474.72 vs $456.70 entry, +3.94%
unrealized — a continuation of the post-earnings move, not an overnight gap,
and nowhere near the -7%/-15% sell triggers. No gap >5% overnight to flag.

**Watchlist candidates:** none open (see promoted-MSFT note above), so no
trigger checks were possible or needed. This routine's scope (per today's
instructions) was checking existing positions/candidates, not originating a
new one — no new name was sourced this run.

**No action planned.** Nothing broken, nothing gapped, no data source
failed, no trigger fired. Not notifying — routine, quiet day, exactly the
outcome `CLAUDE.md` says should be the default.

---

## Market-open execution check — 2026-08-03

Ran the market-open routine. `clock` confirms `is_open: true`. This plan
(above, dated 2026-08-03) contains no drafted buy — it explicitly says "No
action planned" — so there was nothing to re-verify against a 3% price-move
threshold and nothing to execute. Steps 3-5 of the market-open routine were
no-ops by design, not a skip.

Ground truth via Alpaca: equity $100,069.73, cash $99,000.00 (unchanged),
day change +0.05%, `trading_blocked: false`. Matches `portfolio.md`, no
discrepancy. MSFT is the only position, now +7.07% unrealized ($489.00 vs
$456.70 entry) — a continuation of the same post-earnings move noted in
this morning's pre-market check, not a new gap. Nowhere near the -7%/-15%
sell triggers and well under the 5%-of-equity trim threshold (~1.1% of
equity). Trailing stop (`cee441de-48ae-4e48-9cc2-d6482a4c3b0a`) confirmed
still live: status `new`, hwm marked up to $490.80, stop price $441.72.

No trades placed, no orders rejected, no memory drift found. Per the
routine's own instructions ("If nothing happened, send nothing"), no
notification sent.

---

## Intraday risk-reduction check — 2026-08-03 ~13:14 ET

This routine only reduces risk — no new positions permitted regardless of
what looks attractive. Ground truth via Alpaca: equity $100,068.85, cash
$99,000.00, day change +0.05% (`trading_blocked: false`), `clock` shows
`is_open: true`. Nowhere near the 3% circuit breaker — no halt, orders
proceed as normal (none needed).

**Sell-rule check on MSFT (only open position):** market value $1,068.79 vs
$100,068.85 equity = ~1.07% of equity, unrealized +6.88% ($488.12 vs $456.70
entry). Checked for thesis-breaking news via Perplexity (unrestricted query
this time, per the 2026-07-31 lesson that price/news sanity-checks don't
need the primary-source-only filter) covering today specifically: no new
8-K, no new IR release, no lawsuit, no regulatory action, no executive
change, no capex or guidance revision beyond what's already priced in from
the 2026-07-29 print. Today's coverage is recap of the known earnings beat,
not new information. Thesis intact.

None of the four sell triggers fire: not thesis-broken, not down 7%, not
down 15%, not above 5% of equity (it's ~1.07%). No trim, no exit.

**Trailing-stop check:** `orders --status open` shows the existing 10%
trailing stop (`cee441de-48ae-4e48-9cc2-d6482a4c3b0a`) still live — status
`new`, hwm marked up to $491.35 (from $490.80 at market-open check), stop
price $442.215. Covers 2 of 2.19 whole shares, as before (fractional
remainder still can't carry a broker-side stop). No action needed.

Watchlist remains empty — this routine's scope is risk reduction only, not
origination, so no new candidate was sourced. No trades placed, nothing to
log in `trade-log.md`. No notification sent (nothing broke, nothing
triggered, per `CLAUDE.md`'s "default to doing nothing").

---

## Plan for today — 2026-08-04

Ground truth via Alpaca: equity $100,047.24, cash $99,000.00, day change
-0.02%, `trading_blocked: false`. `clock` shows `is_open: false` pre-open
(checked ~08:37 ET), `next_open` today 09:30 ET, `next_close` today 16:00
ET — not a holiday, normal Tuesday session.

**Position thesis check (MSFT, the only open position):** queried
Perplexity, restricted to SEC filings / official Microsoft IR / official
corporate statements, for anything dated between 2026-08-03 and today
touching Azure guidance, commercial RPO, or AI capex. Result: no new 8-K,
no new IR release, no new guidance of any kind — the most recent filing on
record is still the 2026-07-29 8-K (accession 0001193125-26-323632) the
thesis is already built on. **Thesis intact, unchanged.**

**Overnight price check:** Alpaca's own position mark shows MSFT
`current_price` $478.19 vs `lastday_price` $487.65 (change_today -1.94%),
i.e. a pre-market dip of under 2% with no corresponding news — this is
noise, not a gap, and well short of the 5% overnight-gap notification
threshold. (Note for the next Bull: the free/IEX snapshot feed's
`latestTrade` was still showing Monday's 16:00 ET close, $487.575, with no
newer print — Alpaca's position `current_price` field is the more current
mark pre-market and is what was used for this check, consistent with
`CLAUDE.md`'s "the broker is authoritative.") Still up 4.72% unrealized
from the $456.70 entry, nowhere near the -7%/-15% sell triggers.

**Trailing stop:** `orders --status open` confirms the 10% trailing stop
(`cee441de-48ae-4e48-9cc2-d6482a4c3b0a`) still live: status `new`, hwm
$491.63, stop price $442.467. No action needed.

**Watchlist candidates:** none open — nothing to check triggers on. Per
today's routine scope (checking existing positions/candidates, not
originating new ones), no new name was sourced this run.

**No action planned.** Nothing broken, nothing gapped past threshold, no
data source failed, no thesis invalidated. Not notifying — routine, quiet
day, exactly the outcome `CLAUDE.md` says should be the default.

---

## Market-open execution check — 2026-08-04

Ran the market-open routine. `clock` confirms `is_open: true`. Today's plan
(above, dated 2026-08-04) contains no drafted buy — it explicitly says "No
action planned" — so there was nothing to re-verify against the 3%
price-move threshold and nothing to execute. Steps 3-5 of the market-open
routine were no-ops by design, not a skip.

Ground truth via Alpaca: equity $100,067.21, cash $99,000.00 (unchanged),
day change -0.0% (`trading_blocked: false`). Matches `portfolio.md`/this
file, no discrepancy — also cross-checked `origin/main` via an explicit
`git fetch origin main` (not a bare `git log origin/main`, per the
2026-07-31 lesson) and confirmed local HEAD matches `origin/main` exactly
at `e5b7563`, so no drift there either. MSFT is the only position, now
+6.69% unrealized ($487.27 vs $456.70 entry per `positions`; `quote MSFT`
agrees at $488.37) — a continuation of the same post-earnings move, not a
new gap. Nowhere near the -7%/-15% sell triggers and well under the
5%-of-equity trim threshold (~1.07% of equity). Trailing stop
(`cee441de-48ae-4e48-9cc2-d6482a4c3b0a`) confirmed still live: status
`new`, hwm marked up to $491.63, stop price $442.467 — unchanged from the
pre-market check.

No trades placed, no orders rejected, no memory drift found. Per the
routine's own instructions ("If nothing happened, send nothing"), no
notification sent.

---

## Intraday risk-reduction check — 2026-08-04 ~15:30 ET

This routine only reduces risk — no new positions permitted regardless of
what looks attractive. Ground truth via Alpaca: equity $100,084.07, cash
$99,000.00, day change +0.02% (`trading_blocked: false`). Nowhere near the
3% circuit breaker — no halt, sell rules proceed as normal.

**Sell-rule check on MSFT (only open position):** market value $1,084.22 vs
$100,084.07 equity = ~1.08% of equity, unrealized +8.42% ($495.17 vs
$456.70 entry). Checked for thesis-breaking news via Perplexity (restricted
to SEC filings / Microsoft IR / official corporate statements) covering
2026-08-03 through today: no new 8-K, no new IR release, no new guidance —
the most recent primary-source item is still the 2026-07-29 FY26 Q4 print
(43% Azure YoY growth, commercial RPO +84% to $678B) that the thesis is
already built on. Thesis intact, unchanged.

None of the four sell triggers fire: not thesis-broken, not down 7% (it's
up), not down 15%, not above 5% of equity (~1.08%). No trim, no exit.

**Trailing-stop check:** `orders --status open` shows the existing 10%
trailing stop (`cee441de-48ae-4e48-9cc2-d6482a4c3b0a`) still live — status
`new`, hwm marked up to $499.34 (from $491.63 at this morning's check),
stop price $449.406. Covers 2 of 2.19 whole shares, as before. No action
needed.

Watchlist remains empty — this routine's scope is risk reduction only, not
origination, so no new candidate was sourced even though nothing here
looked attractive enough to flag anyway. No trades placed, nothing to log
in `trade-log.md`. No notification sent (nothing broke, nothing triggered,
per `CLAUDE.md`'s "default to doing nothing").

---

## Market-open execution check — 2026-08-05

Ran the market-open routine. `clock` confirms `is_open: true`
(`next_close` today 16:00 ET). Today's plan (above, dated 2026-08-05) is
dated today, so it's not stale — but it contains no drafted buy, explicitly
stating "No action planned," so there was nothing to re-verify against the
3% price-move threshold and nothing to execute. Steps 3-5 of the
market-open routine were no-ops by design, not a skip.

Ground truth via Alpaca: equity $100,075.17, cash $99,000.00 (unchanged),
day change -0.0% (`trading_blocked: false`). Matches `portfolio.md`/this
file, no discrepancy. MSFT is the only position, now +7.51% unrealized
($491.01 vs $456.70 entry) — a small pullback from yesterday's +8.71%/8.42%
reads, still well inside normal noise and nowhere near the -7%/-15% sell
triggers or the 5%-of-equity trim threshold (~1.07% of equity). Trailing
stop (`cee441de-48ae-4e48-9cc2-d6482a4c3b0a`) confirmed still live: status
`new`, hwm $499.34, stop price $449.406 — unchanged from yesterday's
checks.

No trades placed, no orders rejected, no memory drift found. Per the
routine's own instructions ("If nothing happened, send nothing"), no
notification sent.

---

## Intraday risk-reduction check — 2026-08-05 ~13:13 ET

This routine only reduces risk — no new positions permitted regardless of
what looks attractive. Ground truth via Alpaca: equity $100,069.63, cash
$99,000.00, day change -0.01% (`trading_blocked: false`). Nowhere near the
3% circuit breaker — no halt, sell rules proceed as normal.

**Sell-rule check on MSFT (only open position):** market value $1,069.63 vs
$100,069.63 equity = ~1.07% of equity, unrealized +6.96% ($488.50 vs
$456.70 entry, per `positions`; `quote MSFT` agrees at $488.365). Checked
for thesis-breaking news via Perplexity (restricted to SEC filings /
Microsoft IR / official corporate statements) covering 2026-08-04 through
today: no new 8-K, no new IR release, no new guidance on Azure, commercial
RPO, or AI capex — the only executive-related item surfaced was an old
Form 144 (proposed insider sale notice, June 2026, not a departure
disclosure) for Takeshi Numoto, unrelated to the thesis. Most recent
thesis-relevant filing remains the 2026-07-29 FY26 Q4 print. Thesis intact,
unchanged.

None of the four sell triggers fire: not thesis-broken, not down 7% (it's
up), not down 15%, not above 5% of equity (~1.07%). No trim, no exit.

**Trailing-stop check:** `orders --status open` shows the existing 10%
trailing stop (`cee441de-48ae-4e48-9cc2-d6482a4c3b0a`) still live — status
`new`, hwm $499.34, stop price $449.406, unchanged since the 2026-08-04
~15:30 ET check (price has pulled back slightly from the high-water mark
since then, not set a new one). Covers 2 of 2.19 whole shares, as before.
No action needed.

Watchlist remains empty — this routine's scope is risk reduction only, not
origination, so no new candidate was sourced. No trades placed, nothing to
log in `trade-log.md`. No notification sent (nothing broke, nothing
triggered, per `CLAUDE.md`'s "default to doing nothing").

---

## Plan for today — 2026-08-06

Ground truth via Alpaca: equity $100,060.03, cash $99,000.00, day change
-0.01%, `trading_blocked: false`. `clock` shows `is_open: false` pre-open
(checked ~08:40 ET), `next_open`/`next_close` both today — not a holiday,
normal Thursday session.

**Position thesis check (MSFT, the only open position):** queried
Perplexity, restricted to SEC filings / official Microsoft IR / official
corporate statements, for anything dated 2026-08-05 through today touching
Azure guidance, commercial RPO, or AI capex. Result: no new 8-K, no new IR
release, no new guidance — Microsoft's own IR SEC-filings page and EDGAR
still show the 2026-07-29 10-K/8-K as the latest filing. **Thesis intact,
unchanged.**

**Overnight price check:** `alpaca.py quote MSFT` shows `prev_close`
$492.83 -> `last` $487.46, change -1.09%; `positions` shows `current`
$484.12 vs $456.70 entry, +6.0% unrealized. A small pullback, not a gap —
well under the 5% overnight-gap notification threshold and nowhere near
the -7%/-15% sell triggers. Position is ~1.06% of equity, nowhere near the
5% trim threshold.

**Trailing stop:** `orders --status open` confirms the 10% trailing stop
(`cee441de-48ae-4e48-9cc2-d6482a4c3b0a`) still live: status `new`, hwm
$499.34, stop price $449.406 — unchanged since 2026-08-04. No action
needed.

**Watchlist candidates:** none open, so no trigger checks applied.

**New-candidate sourcing (bonus effort, given today's routine is explicitly
research-scoped and the account has sat ~99% cash for eight trading days):**
Before spending Perplexity effort, ran the cheap IR-domain reachability
probe the 2026-08-05 lesson recommended, this time across five other
large-cap candidates: `ir.aboutamazon.com`, `investor.atmeta.com`,
`investor.nvidia.com`, `investors.broadcom.com`, `www.apple.com` — all five
returned connection failures. Checked the proxy status endpoint directly:
every one was `connect_rejected` / gateway-403 on the CONNECT tunnel (same
network-policy pattern as the SEC EDGAR and Alphabet blocks), not a
site-side issue. Widened the probe to confirm this isn't just an
"IR-subdomain" pattern: `ir.tesla.com`, `investor.visa.com`, and even the
general corporate domain `www.costco.com` were blocked too, while
`microsoft.com` remains reachable (confirmed again this run, HTTP 301).
This looks less like a per-company IR block and more like a narrow domain
allowlist that happens to include Microsoft and not much else in the
primary-source universe Bull needs. Given that, did not pursue Perplexity
research on any new name this run — per the 2026-07-29 and 2026-08-05
lessons, an unverifiable number is not a thesis, and there is no primary
source reachable to verify one against for any candidate other than
Microsoft right now. Logged as a lesson (see `lessons.md`) since this
changes the realistic scope of candidate origination until/unless the
network policy changes, and is worth flagging to the human rather than
just re-discovering it name by name.

**No action planned.** Nothing broken, nothing gapped, no thesis
invalidated, no watchlist trigger fired. Not notifying — the MSFT
thesis-integrity checks (the required part of this routine) all worked
fine; the network limitation only affects bonus candidate-sourcing effort,
which doesn't meet this routine's notify bar per the same reasoning as
2026-08-05.

---

## Market-open execution check — 2026-08-06

Ran the market-open routine. `clock` confirms `is_open: true` (`next_close`
today 16:00 ET). Today's plan (above, dated 2026-08-06) is dated today, so
it's not stale — but it contains no drafted buy, explicitly stating "No
action planned," so there was nothing to re-verify against the 3%
price-move threshold and nothing to execute. Steps 3-5 of the market-open
routine were no-ops by design, not a skip.

Ground truth via Alpaca: equity $100,076.89, cash $99,000.00 (unchanged),
day change +0.01% (`trading_blocked: false`). Matches `portfolio.md`/this
file, no discrepancy — also cross-checked `origin/main` via an explicit
`git fetch origin main`: local HEAD matches `origin/main` exactly at
`bfaa211`, so no drift there either. MSFT is the only position, now +7.69%
unrealized ($491.84 vs $456.70 entry) — a continuation of the same
post-earnings move, not a new gap. Nowhere near the -7%/-15% sell triggers
and well under the 5%-of-equity trim threshold (~1.08% of equity).
Trailing stop (`cee441de-48ae-4e48-9cc2-d6482a4c3b0a`) confirmed still
live: status `new`, hwm $499.34, stop price $449.406 — unchanged from
pre-market.

No trades placed, no orders rejected, no memory drift found. Per the
routine's own instructions ("If nothing happened, send nothing"), no
notification sent.

---

## Intraday risk-reduction check — 2026-08-06 ~13:xx ET

This routine only reduces risk — no new positions permitted regardless of
what looks attractive. Ground truth via Alpaca: equity $100,086.09, cash
$99,000.00, day change +0.02% (`trading_blocked: false`). Nowhere near the
3% circuit breaker — no halt, sell rules proceed as normal.

**Sell-rule check on MSFT (only open position):** market value $1,086.09 vs
$100,086.09 equity = ~1.09% of equity, unrealized +8.61% ($496.02 vs
$456.70 entry). Checked for thesis-breaking news via Perplexity (restricted
to SEC filings / Microsoft IR / official corporate statements) covering
2026-08-06: no new 8-K, no new IR release, no new guidance on Azure,
commercial RPO, or AI capex — the only items surfaced are the same ones
already on record (2026-07-29 FY26 Q4 print, Reid Hoffman's prior
not-standing-for-re-election disclosure). Thesis intact, unchanged.

None of the four sell triggers fire: not thesis-broken, not down 7% (it's
up), not down 15%, not above 5% of equity (~1.09%). No trim, no exit.

**Trailing-stop check:** `orders --status open` shows the existing 10%
trailing stop (`cee441de-48ae-4e48-9cc2-d6482a4c3b0a`) still live — status
`new`, hwm $499.34, stop price $449.406, unchanged since 2026-08-04 (price
is below the high-water mark, so no new hwm set). Covers 2 of 2.19 whole
shares, as before. No action needed.

Watchlist remains empty — this routine's scope is risk reduction only, not
origination, so no new candidate was sourced. No trades placed, nothing to
log in `trade-log.md`. No notification sent (nothing broke, nothing
triggered, per `CLAUDE.md`'s "default to doing nothing").

---

## Plan for today — 2026-08-07

Ground truth via Alpaca: equity $100,091.52, cash $99,000.00, day change
-0.0% (-$2.97), `trading_blocked: false`. `clock` shows `is_open: false`
pre-open (checked ~08:40 ET), `next_open`/`next_close` both today — not a
holiday, normal Friday session.

**Position thesis check (MSFT, the only open position):** queried
Perplexity, restricted to SEC filings / official Microsoft IR / official
corporate statements, for anything dated 2026-08-06 through today touching
Azure guidance, commercial RPO, or AI capex. Result: no new 8-K, no new IR
release, no new guidance — most recent primary-source item remains the
2026-07-29 FY26 Q4 print (Microsoft Cloud revenue $59.3B, commercial RPO
$678B, Azure annual revenue above $100B). **Thesis intact, unchanged.**

**Overnight price check:** `alpaca.py quote MSFT` shows `prev_close`
$487.46 -> `last` $500.035, change +2.58%; `positions` shows `current`
$498.50 vs $456.70 entry, +9.15% unrealized. A continuation of the
post-earnings uptrend, not a gap — well under the 5% overnight-gap
notification threshold and nowhere near the -7%/-15% sell triggers.
Position is ~1.09% of equity, nowhere near the 5% trim threshold.

**Trailing stop:** `orders --status open` confirms the 10% trailing stop
(`cee441de-48ae-4e48-9cc2-d6482a4c3b0a`) still live: status `new`, hwm
$501.55, stop price $451.395 — hwm advanced slightly from $499.34 as of
the 2026-08-06 check. No action needed.

**Watchlist candidates:** none open, so no trigger checks applied.

**New-candidate sourcing (bonus effort):** re-ran the cheap reachability
probe from the 2026-08-05/08-06 lessons against four previously-blocked IR
domains (`ir.aboutamazon.com`, `investor.atmeta.com`, `abc.xyz`,
`investor.nvidia.com`) before spending any Perplexity effort. All four
still fail to connect (`curl` returns HTTP 000 / connection failure) — the
network-policy block identified in those lessons has not changed. Per
existing policy, did not pursue Perplexity research on any new name this
run — no primary source is reachable to verify one against besides
Microsoft. No new lesson written since this just reconfirms the prior
finding rather than surfacing anything new.

**No action planned.** Nothing broken, nothing gapped, no thesis
invalidated, no watchlist trigger fired. Not notifying — the MSFT
thesis-integrity checks (the required part of this routine) all worked
fine; the network limitation only affects bonus candidate-sourcing effort,
already known and previously flagged to the human, so it doesn't meet
this routine's notify bar again today.

---

## Market-open execution check — 2026-08-07

Ran the market-open routine. `clock` confirms `is_open: true` (`next_close`
today 16:00 ET). Today's plan (above, dated 2026-08-07) is dated today, so
it's not stale — but it contains no drafted buy, explicitly stating "No
action planned," so there was nothing to re-verify against the 3%
price-move threshold and nothing to execute. Re-pulled `quote MSFT` anyway
per the routine's own instructions: `last` $504.295 vs the plan's $498.50
mark, +1.16% since the plan was written — nowhere near the 3% threshold
that would have invalidated a setup, moot anyway since no entry was
planned. Steps 3-5 of the market-open routine were no-ops by design, not a
skip.

Ground truth via Alpaca: equity $100,104.16, cash $99,000.00 (unchanged),
day change +0.01% (`trading_blocked: false`). Matches `portfolio.md`/this
file, no discrepancy — also cross-checked `origin/main` via an explicit
`git fetch origin main`: local HEAD matches `origin/main` exactly at
`6b7862b` (today's pre-market commit), so no drift there either. MSFT is
the only position, now +10.42% unrealized ($504.27 vs $456.70 entry) — a
continuation of the same post-earnings uptrend, not a new gap. Nowhere
near the -7%/-15% sell triggers and well under the 5%-of-equity trim
threshold (~1.10% of equity). Trailing stop
(`cee441de-48ae-4e48-9cc2-d6482a4c3b0a`) confirmed still live: status
`new`, hwm advanced to $504.97 (from $501.55 pre-market), stop price
$454.473 — moving up automatically with the price, as designed.

No trades placed, no orders rejected, no memory drift found. Per the
routine's own instructions ("If nothing happened, send nothing"), no
notification sent.

---

## Intraday risk-reduction check — 2026-08-07 ~13:13 ET

This routine only reduces risk — no new positions permitted regardless of
what looks attractive. Ground truth via Alpaca: equity $100,095.66, cash
$99,000.00, day change +$1.17 / 0.0% (`trading_blocked: false`), `clock`
shows `is_open: true`. Nowhere near the 3% circuit breaker — no halt, sell
rules proceed as normal.

**Sell-rule check on MSFT (only open position):** market value $1,095.66 vs
$100,095.66 equity = ~1.09% of equity, unrealized +9.57% ($500.39 vs
$456.70 entry). Checked for thesis-breaking news via Perplexity (restricted
to SEC filings / Microsoft IR / official corporate statements) covering
2026-08-06 through today: no new 8-K, no new IR release, no new guidance on
Azure, commercial RPO, or AI capex — the most recent primary-source item
remains the 2026-07-29 FY26 Q4 print. Thesis intact, unchanged.

None of the four sell triggers fire: not thesis-broken, not down 7% (it's
up), not down 15%, not above 5% of equity (~1.09%). No trim, no exit.

**Trailing-stop check:** `orders --status open` shows the existing 10%
trailing stop (`cee441de-48ae-4e48-9cc2-d6482a4c3b0a`) still live — status
`new`, hwm advanced to $505.18 (from $504.97 at this morning's market-open
check), stop price $454.662. Covers 2 of 2.19 whole shares, as before. No
action needed.

Watchlist remains empty — this routine's scope is risk reduction only, not
origination, so no new candidate was sourced. No trades placed, nothing to
log in `trade-log.md`. No notification sent (nothing broke, nothing
triggered, per `CLAUDE.md`'s "default to doing nothing").
