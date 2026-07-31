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

### MSFT
- **Thesis forming:** Cloud/AI capacity buildout is translating into real
  revenue acceleration, not just capex narrative. FQ4 FY26 (quarter ended
  2026-06-30, reported 2026-07-29): total revenue $90.0B (+18% YoY, +17% cc),
  Microsoft Cloud revenue $59.3B (+27% YoY), Azure and other cloud services
  +43% YoY, operating margin 45.1%, commercial RPO $678B (+84% YoY). Source:
  Microsoft's own IR press release,
  https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast
  — headline "Microsoft Cloud and AI Strength Fuels Fourth Quarter Results,"
  fetched twice independently and cross-checked for consistency (numbers and
  headline matched both times).
- **What you're waiting for:** Two things before this clears buy criteria.
  (1) Valuation: the stock already moved on this news before I could check
  it — prevDailyBar close (2026-07-28) $393.44 vs latest extended-hours trade
  $426.41 as of 2026-07-30 08:34 ET, roughly +8.4%. Need to see where it
  settles after the open and check P/E against MSFT's own 5-year range before
  claiming valuation is defensible (criterion 3) — did not have this data
  during this research-only run. (2) Trend confirmation: I only pulled this
  one quarter's Azure number (43% YoY). Before calling this "acceleration" I
  need to pull the FQ3 FY26 Azure growth number for comparison — one data
  point is not a trend.
- **Update, 2026-07-31 (pre-market research):** Both gaps are now closed.
  (1) Trend: Microsoft's own FQ3 FY26 metrics page
  (microsoft.com/en-us/investor/earnings/fy-2026-q3/metrics, confirmed
  directly via fetch, not just Perplexity's summary) shows Azure and other
  cloud services revenue growth of 40% YoY (39% cc) for the quarter ended
  2026-03-31. 40% → 43% across two consecutive quarters is a real
  acceleration, not a one-point read. (2) Valuation: Alpaca's own daily bar
  shows MSFT closed 2026-07-30 at $451.545 (dailyBar), up from a
  prevDailyBar close of $391.00 on 2026-07-29 — a +15.48% one-day move,
  which I did not take at face value given the size (verified against
  general news search before trusting it; see lessons.md 2026-07-31 entry).
  Microsoft's own FY26 Q4 release (fetched directly) gives full-year GAAP
  diluted EPS of $17.95. At $451.545, that's a trailing P/E of ~25.2x.
  MSFT's own 5-year TTM P/E range (per Perplexity, cross-referenced across
  VCPScanner/Macrotrends/TradingView — not a primary-source figure since
  P/E history isn't published in a filing, but a computed ratio using
  Microsoft's own reported EPS) is roughly 25.1x–37.8x. So despite the
  stock being up ~15% post-earnings, it is sitting near the *bottom* of its
  own historical multiple range — EPS grew faster than price. Valuation is
  defensible, not stretched.
- **Buy criteria check:** (1) falsifiable thesis — yes, cloud/AI revenue
  acceleration, stated above. (2) catalyst — already happened and is
  confirmed with real numbers (FQ4 print). (3) valuation vs 5-year range —
  defensible, see above. (4) not a macro call — yes, company-specific. (5)
  liquidity — mega-cap, trivial. That's 5 of 5; criteria only require 3.
  The one thing criteria don't capture: the stock already ran +15% in a
  single day, which is chase risk regardless of how cheap the multiple
  looks on paper. See the plan below for how that's handled in sizing.
- **Added:** 2026-07-30
- **Review by:** 2026-08-13

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

---

## Market-open execution — 2026-07-31 09:46 ET

Plan was dated today (2026-07-31), so it was current — executed. Re-verified
MSFT's quote before acting: $456.21, vs $451.545 referenced in the plan,
+1.03% — under the 3% skip threshold, so the setup was unchanged. Traded 16
minutes after the 09:30 ET open (past the first-15-minutes rule).

**Executed:** BUY MSFT, $1,000 notional (1% starter), filled 2.1896 shares at
$456.70 avg. Full reasoning in `trade-log.md`. MSFT is promoted from
watchlist candidate to an open position — see `portfolio.md`. No overnight
protection set (fractional share count, below Alpaca's 1-share minimum for a
trailing stop); revisit if/when this position is added to.

No other candidates were on the watchlist, so nothing else to execute or
skip this run.
