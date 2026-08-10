# Trade log

Append-only. Never edit or delete a past entry, including the embarrassing
ones — those are the entries with the most information in them.

Every entry records the reasoning at the time of the decision, not the
reasoning that looks best in hindsight.

## Format

```
### YYYY-MM-DD HH:MM — BUY/SELL TICKER
- Size: $X (Y% of equity)
- Fill: $Z
- Reason: why, in one or two sentences
- Thesis / invalidation: what would make this wrong
- Confidence: low / medium / high
- Source: what you actually read
```

Rejected orders get logged too, with the guardrail that fired. A pattern of
rejections is a signal the strategy and the limits are out of sync.

---

### 2026-07-31 09:46 ET — BUY MSFT
- Size: $1,000 notional (1.0% of equity at fill)
- Fill: $456.70 avg, qty 2.189599299 (fractional, notional order)
- Reason: Azure revenue growth accelerated 40% -> 43% YoY across FQ3 and FQ4
  FY26 (both confirmed directly from Microsoft's own IR site). Despite the
  stock already running +15.48% the session after earnings, trailing P/E
  (~25.2x on FY26 GAAP diluted EPS of $17.95) sits near the bottom of MSFT's
  own 5-year P/E range (~25.1x-37.8x) — EPS growth outrunning the price move.
  Sized as a 1% starter (not the 3% standard) to account for it being a
  higher-beta growth name and for chase risk on a name that had already
  moved 15% in a day before this plan could act on it.
- Thesis / invalidation: Azure YoY growth decelerates back below ~35% in the
  FQ1 FY27 print, or commercial RPO growth reverses meaningfully, or capex
  guidance is cut in a way that reads as AI-monetization doubt rather than
  discipline.
- Confidence: high (5 of 5 buy criteria met; only 3 required)
- Source: Microsoft's own FY26 Q4 and Q3 IR press releases (fetched
  directly, cross-checked), reasoning drafted in `watchlist.md` during the
  2026-07-31 pre-market run.
- **Note on this entry:** This trade was executed by the market-open routine
  (order filled 2026-07-31 13:46:11 UTC, per Alpaca) following the plan
  drafted in `watchlist.md`. It was never written to this log or to
  `portfolio.md`, and neither file's update was pushed to `main` — this
  entry is being backfilled by the 2026-07-31 intraday risk-reduction run,
  which found the position on the broker but not in memory. See
  `lessons.md` 2026-07-31 entry for the process failure this exposes.

### 2026-07-31 13:xx ET — PROTECT MSFT (trailing stop)
- Action: placed broker-side trailing stop, 10% trail, qty 2 whole shares
  (Alpaca does not accept trailing stops on the fractional remainder, per
  `scripts/alpaca.py`'s own guard) — order id
  `cee441de-48ae-4e48-9cc2-d6482a4c3b0a`.
- Reason: `strategy.md` requires every satellite position to carry a live
  10% trailing stop once it's a full-share position. Checked
  `orders --status open` at the start of this intraday run and found none
  — the market-open routine bought MSFT but never set the stop. Fixed
  immediately; this is the intraday routine's explicit job.
- Confidence: n/a (mechanical, not a thesis decision)

### 2026-08-10 09:54 ET — BUY SPY
- Size: $2,000 notional (~2.0% of equity at fill)
- Fill: $773.10 avg, qty 2.586974518 (fractional, notional order)
- Reason: Core index sleeve, first tranche. `strategy.md`'s 2026-08-08
  change-log clarification says the core ETF sleeve (target ~25%, 10-40%
  range) should be funded promptly and independently of satellite sourcing,
  and is exempt from the satellite buy criteria (thesis/catalyst/valuation)
  — it's an allocation decision, not a stock pick. This is the first core
  buy since inception (2026-07-29); the account had sat ~99% cash for 9+
  trading days while satellite candidate-sourcing stayed blocked by the
  network-policy issue logged 2026-08-05/06/07. Sized to the $2,000
  per-order guardrail cap (`max_order_notional`), not to any price-timing
  view — plan drafted pre-market today in `watchlist.md`, price re-verified
  immediately before the order ($773.20 last vs $773.16 plan reference,
  effectively unchanged) and the trade executed outside the first-15-minute
  window (market opened 09:30 ET, order placed ~09:54 ET).
- Thesis / invalidation: none required (core allocation buy, exempt per
  strategy.md). Not a thesis position — no catalyst or invalidation
  condition; it stays sized per the core-sleeve band, trimmed only if it
  drifts outside that band or the human changes the strategy.
- Confidence: n/a (allocation decision, not a stock thesis)
- Source: `strategy.md` 2026-08-08 change-log entry; price from
  `alpaca.py quote SPY` immediately pre-order.
- **Note on sizing:** this single $2,000 tranche is ~2% of equity — it does
  not by itself reach the 25% core target, and per the 2026-08-10
  `lessons.md` entry, a single ticker is hard-capped at 5% of equity by
  `guardrails.py` regardless of tranche count. Reaching 25% requires either
  many more tranches over time or the human resolving the multi-ticker
  question raised in that lesson. No trailing stop set — `strategy.md`'s
  "Overnight protection" section explicitly exempts index-ETF core holdings
  from stops.
