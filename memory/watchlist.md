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

## Market-open check — 2026-07-30 09:46 ET

Ran the market-open routine. `clock`: `is_open: true`. Ground truth
reconfirmed: $100,000 cash, 0 open positions, `trading_blocked: false`,
`day_change_pct: 0.0`. Plan above is dated today, so it applied.

Re-verified MSFT price per the routine's 3%-move rule: `quote` now shows
MSFT last $448.77 vs. prior close $391 (+14.77% same-day), and further above
the $426.41 extended-hours print noted in the pre-market plan (roughly
another +5.2% since that snapshot). This is far past the 3% threshold —
**skipped, no order placed.** A stock up ~15% on the day is exactly the kind
of move `strategy.md`'s "no reacting to noise" posture warns against buying
into, and it makes the still-open valuation gap (criterion 3) harder to
clear, not easier — the multiple has re-rated on the same news, not settled.
Did not pull the FQ3 FY26 Azure comparison number this run since the price
move alone was disqualifying; that research still needs doing before MSFT
can be reconsidered.

No other watchlist candidates existed to check. No open positions, so no
thesis-invalidation or stop checks applied. **No trades, no rejections, no
action taken this run** — cash remains $100,000, 0 positions.

**Review by 2026-08-13 stands.** Before re-considering MSFT: let the
post-earnings move settle for a few sessions, then check P/E against MSFT's
own 5-year range at whatever price it's trading, and pull FQ3 FY26 Azure
growth for a real two-quarter trend comparison.
