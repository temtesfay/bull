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

### 2026-08-11 09:54 ET — BUY SPY
- Size: $2,000 notional (~2.0% of equity at fill)
- Fill: $772.92 avg, qty 2.58757698 (fractional, notional order), resulting
  position 5.174551498 sh @ $773.01 avg, ~4.0% of equity
- Reason: second tranche of the core ETF sleeve per `strategy.md`'s
  2026-08-08 clarification (allocation decision, exempt from satellite
  buy criteria). Drafted in yesterday's pre-market plan
  (`watchlist.md` 2026-08-11). Re-verified `quote SPY` before executing:
  $773.065 last vs the plan's ~$773-774 reference, well under the 3%
  invalidation threshold. Adding to an existing position does not consume
  `new_positions_this_week` (confirmed against `guardrails.py` in
  yesterday's research run) — still 1/3 used. Resulting position (~4.0% of
  equity) stays under the 5%-per-symbol cap; cash reserve after the buy is
  ~95% of equity, far above the 10% floor.
- Thesis / invalidation: none — core sleeve, no thesis to invalidate; only
  trimmed if the sleeve drifts outside the 10-40% band or the human changes
  strategy.
- Confidence: n/a (allocation buy, not a conviction call)
- Source: `alpaca.py quote SPY` at time of trade; `strategy.md` core-sleeve
  policy; `guardrails.py` read directly for the new-position-count logic.
- No trailing stop set — `strategy.md` exempts index-ETF core holdings from
  stops.

### 2026-08-12 09:46 ET — BUY SPY
- Size: $900 notional (~0.9% of equity at fill)
- Fill: $772.476 avg, qty 1.165071795 (fractional, notional order),
  resulting position 6.339623293 sh @ $772.91 avg, ~4.89% of equity
- Reason: third tranche of the core ETF sleeve per `strategy.md`'s
  2026-08-08 clarification (allocation decision, exempt from satellite
  buy criteria). Drafted in this morning's pre-market plan
  (`watchlist.md` 2026-08-12), sized to $900 specifically because the
  prior two $2,000 tranches had brought SPY to ~4.00% of equity, leaving
  only ~$1,000 of headroom to the code-enforced 5%-per-symbol cap before
  `guardrails.py` would reject a further order outright — $900 was chosen
  to fit inside that room with a buffer for intraday price movement.
  Re-verified `quote SPY` before executing: $772.75 last vs the plan's
  $773.95 pre-market reference, -0.15% move, well under the 3%
  invalidation threshold. Adding to an existing position does not consume
  `new_positions_this_week` (still 1/3 used, confirmed via `account`
  before and after the order). Resulting position (~4.89% of equity)
  stays just under the 5%-per-symbol cap; cash reserve after the buy is
  ~94.0% of equity, far above the 10% floor.
- Thesis / invalidation: none — core sleeve, no thesis to invalidate; only
  trimmed if the sleeve drifts outside the 10-40% band or the human changes
  strategy.
- Confidence: n/a (allocation buy, not a conviction call)
- Source: `alpaca.py quote SPY` at time of trade; `strategy.md` core-sleeve
  policy; `watchlist.md` 2026-08-12 pre-market headroom calculation.
- No trailing stop set — `strategy.md` exempts index-ETF core holdings from
  stops.
- **Note:** this exhausts SPY's own headroom to the 5% cap (~4.89% now,
  ~$108 of room left at today's equity). Per the standing open question in
  `lessons.md` (2026-08-07, 2026-08-10), reaching anywhere near the ~25%
  core target from here requires either a distinct second index ticker
  (VTI, IVV, etc.) or explicit human guidance — not something this run
  decides unilaterally. No further SPY core buy should be attempted until
  that's resolved.

## 2026-09-29 risk-only check
- No trades. Day -0.02%, no sell rule triggered (SPY -1.34%, MSFT +11.22%), MSFT trailing stop confirmed live (qty 2, 10%, stop $467.46). Broker matches portfolio.md.

## 2026-09-30 risk-only check
- No trades. Day +0.05%, no sell rule triggered (SPY -0.60%, MSFT +13.46%, SPY ~4.87% <5%). MSFT trailing stop live (qty 2, 10%, stop $467.85). Broker matches portfolio.md.

## 2026-10-02 execution check
- No trades. Plan dated 2026-10-02 reads "No action planned"; nothing to execute.

## 2026-10-05 risk-only check
- No trades. Day +0.04%, no sell rule triggered (SPY +0.13% vs entry at 4.90% of equity, under 5% cap; MSFT +15.02%, ~1.15%). MSFT trailing stop live (qty 2, 10%, stop $479.115). Broker matches portfolio.md. Sleeve is ~94% cash; no new positions allowed in this routine.

## 2026-10-06 risk-only check
- No trades. Day +0.05%, no sell rule triggered (SPY +0.90% vs entry at 4.93% of equity, under 5% cap; MSFT +16.56%, ~1.16%). MSFT trailing stop live (qty 2, 10%, stop $482.121). Broker matches portfolio.md. No new positions allowed in this routine.

## 2026-10-07 risk-only check
- No trades. Day -0.02%, no sell rule triggered (SPY +0.51% vs entry at 4.92% of equity, under 5% cap; MSFT +15.63%, ~1.15%). MSFT trailing stop live (qty 2, 10%, stop $482.121, hwm $535.69). Broker matches portfolio.md. No new positions allowed in this routine.

## 2026-10-08 execution check
- No trades. Plan dated 2026-10-08 reads "No action planned"; nothing to execute.

## 2026-10-09 risk-only check
- No trades. Day +0.05% (equity $100,205.05), no sell rule triggered (SPY +0.70% vs entry at 4.92% of equity, under 5% cap; MSFT +17.07%, ~1.17%). MSFT trailing stop live (qty 2, 10%, stop $482.121, hwm $535.69, expires 2026-10-29, verified via orders --status open). Broker matches portfolio.md. Price-only check, no news pull (Perplexity out of credits); no thesis-break evidence. No new positions allowed in this routine.

## 2026-10-12 risk-only check
No orders. Equity $100,211.64 (day 0.00%), well inside the 3% breaker. SPY +0.62% vs entry, 4.92% of equity (under 5% cap). MSFT +18.15%, 1.18% of equity, trailing stop 10% live on 2 sh (stop $488.45). No position down 7%+, no thesis break evidence. Research tool (Perplexity) unavailable, so no fresh news check; uncertain only in that respect.

## 2026-10-13 execution check
- No trades. Plan dated 2026-10-13 reads "No action planned"; nothing to execute.

## 2026-10-13 risk-only check
- No orders. Equity $100,221.52 (day +$3.76, 0.00%), breaker not tripped. SPY +0.55% vs entry, 4.92% of equity (under 5% cap). MSFT +19.47%, ~1.19% of equity; trailing stop 10% live on 2 sh (stop $496.035, hwm $551.15, expires 2026-10-29, verified via orders --status open). No position down 7%+; no thesis-break evidence in price. Price-only check, no news pull (Perplexity out of credits). No new positions allowed in this routine.

## 2026-10-14 execution check
- No trades. Plan dated 2026-10-14 reads "No action planned"; nothing to execute. Broker equity $100,206.03, cash $94,100.00, matches portfolio.md.

## 2026-10-14 risk-only check
- No orders. Equity $100,155.90 (day -$66.33, -0.07%), breaker not tripped. SPY -0.37% vs entry, 4.87% of equity (under 5% cap). MSFT +17.42%, ~1.17% of equity; trailing stop 10% live on 2 sh (stop $496.035, hwm $551.15, expires 2026-10-29, verified via orders --status open). No position down 7%+; no thesis-break evidence (price-only check, no news pull — Perplexity previously out of credits, not re-tested). No new positions allowed in this routine.

## 2026-10-15 risk-only check
- No orders. Equity $100,160.26 (day +$12.72, +0.01%), breaker not tripped. SPY -0.43% vs entry, 4.87% of equity (under 5% cap). MSFT +18.14%, ~1.18% of equity; trailing stop 10% live on 2 sh (stop $496.035, hwm $551.15, expires 2026-10-29, verified via orders --status open). No position down 7%+; no thesis-break evidence in price. Price-only check, no news pull. Note: stop GTC expires 2026-10-29 — renew before then.

## 2026-10-16 risk-only check
- No orders. Equity $100,106.22 (day -$67.80, -0.07%), breaker not tripped. SPY -0.99% vs entry, 4.85% of equity (under 5% cap). MSFT +15.45%, ~1.15% of equity; trailing stop 10% live on 2 sh (stop $496.035, hwm $551.15, expires 2026-10-29, verified via orders --status open). No position down 7%+; no thesis-break evidence in price. Price-only check, no news pull. Broker matches portfolio.md. Stop GTC expiry 2026-10-29 still needs renewal before then.

## 2026-10-19 premarket research
- No trades (research-only routine). Equity $100,119.38, broker matches portfolio.md, MSFT stop live (stop $496.035, expires 2026-10-29). Perplexity still out of credits (HTTP 401); no news check done, thesis status unverified. Plan: No action planned.

## 2026-10-19 execution check
- No trades. Plan dated 2026-10-19 reads "No action planned"; nothing to execute. Broker equity $100,125.60, cash $94,100.00, SPY/MSFT match portfolio.md; trading_blocked false.

## 2026-10-20 risk-only check
- No orders. Equity $100,141.16 (day +$13.77, +0.01%), cash $94,100.00, breaker not tripped. SPY 6.3396 sh $768.89, -0.52% vs entry, ~4.87% of equity (under 5% cap). MSFT 2.1896 sh $532.83, +16.67%, ~1.17% of equity; trailing stop 10% live on 2 sh (stop $496.035, hwm $551.15, expires 2026-10-29, verified via orders --status open). No position down 7%+; no sell rule triggered. Price-only check, no news pull. Broker matches portfolio.md. Reminder: MSFT stop GTC expires 2026-10-29 — needs re-protect before then.

## 2026-10-21 premarket research
- No trades (research-only). Equity $100,149.85, broker matches portfolio.md, MSFT stop live per last check. Perplexity still HTTP 401 quota; no news check done, thesis unverified. Plan: No action planned.

## 2026-10-21 risk-only check
- No orders. Equity $100,173.40 (day +$33.33, +0.03%), breaker not tripped. SPY +0.13% vs entry, 4.90% of equity (under 5% cap). MSFT +16.71%, ~1.17% of equity; trailing stop 10% live on 2 sh (stop $496.035, hwm $551.15, expires 2026-10-29, verified via orders --status open). No position down 7%+; no thesis-break evidence in price. Price-only check, no news pull (Perplexity out of quota); thesis unverified. Stop GTC expiry 2026-10-29 still needs renewal.

## 2026-10-22 risk-only check
- No orders. Equity $100,081.94 (day -$86.11, -0.09%), cash $94,100.00, breaker not tripped. SPY 6.3396 sh $762.55, -1.34% vs entry, ~4.83% of equity (under 5% cap). MSFT 2.1896 sh $524.14, +14.77%, ~1.15% of equity; trailing stop 10% live on 2 sh (stop $496.035, hwm $551.15, expires 2026-10-29, verified via orders --status open). No position down 7%+; no sell rule triggered. Price-only check, no news pull; thesis not independently verified. Broker matches portfolio.md. Stop GTC expiry 2026-10-29 still needs renewal (a full 2 sh covered; 0.19 sh remainder unprotected, immaterial).

## 2026-10-23 premarket research
- No trades (research-only). Equity $100,057.46, broker matches portfolio.md, MSFT stop live (stop $496.035, expires 2026-10-29). Perplexity still HTTP 401 quota; no news check done, thesis unverified. Plan: No action planned.

## 2026-10-23 risk-only check
- No orders. Equity $100,070.56 (day -$13.62, -0.01%), cash $94,100.00, breaker not tripped. SPY 6.3396 sh $760.54, -1.60% vs entry, ~4.82% of equity (under 5% cap). MSFT 2.1896 sh $524.75, +14.9%, ~1.15% of equity; trailing stop 10% live on 2 sh (stop $496.035, hwm $551.15, expires 2026-10-29, verified via orders --status open). No position down 7%+; no sell rule triggered. Price-only check, no news pull (Perplexity out of quota); thesis unverified. Broker matches portfolio.md. Stop GTC expiry 2026-10-29 still needs renewal.

## 2026-10-26 premarket research
- No trades (research-only). Equity $100,086.72, broker matches portfolio.md, MSFT stop live (stop $496.035, expires 2026-10-29). Perplexity still HTTP 401 quota; no news check done, thesis unverified. Plan: No action planned.

## 2026-10-26 risk-only check
- No orders. Equity $100,120.18 (day +$53.79, +0.05%), cash $94,100.00, breaker not tripped. SPY 6.3396 sh $766.21, -0.87% vs entry, ~4.85% of equity (under 5% cap). MSFT 2.1896 sh $531.01, +16.27%, ~1.16% of equity; trailing stop 10% live on 2 sh (stop $496.035, hwm $551.15, expires 2026-10-29, verified via orders --status open). No sell rule triggered. Price-only check, no news pull (Perplexity out of quota); thesis unverified. Broker matches portfolio.md. Stop GTC expiry 2026-10-29 (3 days) still needs renewal.

## 2026-10-26 daily close
- No trades, no rejections. Equity $100,116.51; broker matches portfolio.md. MSFT stop live, expires 2026-10-29.

## 2026-10-27 risk-only check
- No orders. Equity $100,144.01 (day +$25.67, +0.03%), cash $94,100.00, breaker not tripped. SPY 6.3396 sh $769.55, -0.43% vs entry, ~4.87% of equity (under 5% cap). MSFT 2.1896 sh $532.22, +16.54%, ~1.16%; trailing stop 10% live on 2 sh (stop $496.035, hwm $551.15, expires 2026-10-29, verified via orders --status open). No sell rule triggered. Price-only check, no news pull (Perplexity out of quota); thesis unverified. Broker matches portfolio.md. **Stop expires in 2 days; `alpaca.py` cannot cancel/replace, so a plain `protect` would be rejected while the old order holds the shares. Needs human action or a script change.**

## 2026-10-28 premarket research
- No trades (research-only). Equity $100,151.52, broker matches portfolio.md, MSFT stop live (stop $496.035, expires 2026-10-29 — tomorrow). Perplexity still HTTP 401; thesis unverified. Plan: No action planned.

## 2026-10-28 execution check
- No trades. Plan dated 2026-10-28 reads "No action planned"; nothing to execute. Broker equity $100,143.39, cash $94,100.00, SPY 6.3396 sh $770.32 (-0.34% vs entry), MSFT 2.1896 sh $529.62 (+15.97%) match portfolio.md; trading_blocked false. MSFT stop GTC expires 2026-10-29 (tomorrow) — alpaca.py cannot cancel/replace; needs human action or script change.

## 2026-10-28 risk-only check
- No orders. Equity $100,143.64 (day +$0.89, 0.00%), cash $94,100.00, breaker not tripped. SPY 6.3396 sh $771.27 (-0.21% vs entry, ~4.88%, under cap). MSFT 2.1896 sh $527.08 (+15.41%, ~1.15%); trailing stop live on 2 sh (stop $496.035, hwm $551.15, verified via orders --status open). No sell rule triggered; no news pull (Perplexity out of credits), thesis unverified but no price evidence of break. Broker matches portfolio.md. **MSFT stop expires 2026-10-29 20:00Z (tomorrow); no cancel/replace in alpaca.py — human action needed. Warn notification sent.**

## 2026-10-28 daily close
- No trades, no rejections. Equity $100,204.44 (day +$61.69, +0.06%) vs SPY +0.34% (quote, intraday); since inception +0.20% vs +5.85% (-5.65pp). Broker matches portfolio.md (SPY 6.3396 sh, MSFT 2.1896 sh, cash $94,100). No position >5% underwater. MSFT stop GTC (stop $496.035) expires 2026-10-29 20:00Z — unrenewed, MSFT goes unprotected tomorrow unless a human/process renews it (alpaca.py has no cancel/replace). Perplexity still 401; thesis unverified.

## 2026-10-29 premarket research
- No trades (research-only). Equity $100,158.25, broker matches portfolio.md. MSFT $540.00 (-2.4% vs prior close), stop live but expires today 20:00Z. Perplexity still 401 quota; thesis unverified. Plan: No action planned.

### 2026-10-29 — Execution check (no orders)
Market open (10:02 ET). Plan dated 2026-10-29 says "No action planned." Nothing placed, nothing rejected. MSFT 10% trailing stop (qty 2, stop $496.035) still live but its GTC expires today 20:00Z; alpaca.py has no cancel/replace, so renewal is a human action. Not attempted: a second protect order is not covered by strategy.md.

### 2026-10-30 — Execution (stop restored, no new positions)
Market open (09:46 ET). Plan dated 2026-10-30: no new buys; re-place MSFT 10% trailing stop if unprotected. `orders --status open` was `[]` (prior GTC stop lapsed 2026-10-29). Ran `alpaca.py protect MSFT --trail-percent 10` -> PROTECTED, order 27274a69-f0d3-4f19-91b5-29d8c50121e5, qty 2, stop $471.1365, hwm $523.485, expires 2027-01-28. Verified live via `orders --status open`. This restores existing protection (MSFT +14.6% vs $456.70 entry; thesis unverified, Perplexity 401), not a new position. No rejections. Equity $100,066.64, cash $94,100.00. Note: new stop is looser in dollars than the old one ($496.035) because the 10% trail restarted from today's price. Remember: GTC stops lapse after ~90 days; renew before 2027-01-28.

## 2026-10-30 risk-only check
- No orders. Equity $100,028.14 (day -$110.11, -0.11%), cash $94,100.00, breaker not tripped. SPY 6.3396 sh $755.11, -2.30% vs entry, ~4.79% (under 5% cap, core exempt from stops and thesis exits). MSFT 2.1896 sh $521.12, +14.1%, ~1.14%; trailing stop live on 2 sh (stop $472.608, hwm $525.12, verified via orders --status open). No sell rule triggered. No news pull (Perplexity out of credits); price-only, thesis unverified but no price evidence of a break. Nothing attractive found; watchlist unchanged.

## 2026-10-30 daily close
- No trades, no rejections. Equity $100,039.89 (day -0.10%) vs SPY -1.79% (quote); since inception +0.04% vs +3.58% (-3.54pp). Broker matches portfolio.md; MSFT stop (27274a69) live. No position >5% underwater.

## 2026-11-02 execution check
- No trades. Plan dated 2026-11-02 reads "No action planned"; nothing to execute, nothing rejected. Broker equity $100,072.57, cash $94,100.00, SPY 6.3396 sh $760.14 (-1.65% vs entry), MSFT 2.1896 sh $526.79 (+15.35%) match portfolio.md; trading_blocked false. MSFT 10% trailing stop live on 2 sh (27274a69, stop $475.632, hwm $528.48, expires 2027-01-28, verified via orders --status open).

## 2026-11-02 risk-only check
- No orders. Equity $100,043.14 (day +0.01
## 2026-11-02 risk-only check
- No orders. Equity $100,043.14 (day +0.01%), cash $94,100.00, breaker not tripped. SPY -1.98% vs entry, ~4.80% (core, under cap); MSFT +13.99%, ~1.14%, trailing stop 27274a69 live (stop $476.667, verified). No sell rule triggered. Broker matches portfolio.md.

## 2026-11-04 risk-only check
- No orders. Equity $100,185.78 (day +0.16%), cash $94,100.00, breaker not tripped. SPY -0.66% vs entry, ~4.86% (core); MSFT +21.79%, ~1.22%, trailing stop 27274a69 live (stop $502.245, hwm $558.05, verified). No sell rule triggered. News not checked (Perplexity out of credits). Broker matches portfolio.md.

## 2026-11-05 risk-only check
- No orders. Equity $99,977.93 (day -$200.34, -0.20%), cash $94,100.00, breaker not tripped. SPY -4.25% vs entry, ~4.69% (core, exempt from thesis/stop rules; not at -7%). MSFT +18.62%, ~1.19%, trailing stop 27274a69 live on 2 sh (stop $503.235, verified). No sell rule triggered. News not checked (Perplexity out of credits) — price move alone is not evidence of a broken thesis. Broker matches portfolio.md.

## 2026-11-06 risk-only check
- No orders. Equity $99,958.05 (day +$37.63, +0.04%), cash $94,100.00, breaker not tripped. SPY -4.35% vs entry, ~4.69% (core, no stop by design; not at -7%). MSFT +17.10%, ~1.17%, trailing stop 27274a69 live on 2 sh (stop $503.235, hwm $559.15, verified via orders --status open; 0.19 sh fractional remainder unprotected, not a full share). No sell rule triggered. News not checked (Perplexity out of credits). Broker matches portfolio.md.

## 2026-11-06 weekly review
- No trades. Review #15 written to lessons.md. Equity $99,936.95; broker matches portfolio.md.

## 2026-11-09 risk-only check
- No orders. Equity $100,056.66 (day +$133.38, +0.13%), cash $94,100.00, breaker not tripped. SPY -2.71% vs entry, ~4.76% (core, no stop by design; not at -7%). MSFT +18.95%, ~1.19%, trailing stop 27274a69 live on 2 sh (stop $503.235, hwm $559.15, verified via orders --status open). No sell rule triggered. News not checked (Perplexity 401). Broker matches portfolio.md.

## 2026-11-10 risk-only check
- No orders. Equity $100,026.46 (day -$39.04, -0.04%), cash $94,100.00, breaker not tripped, trading_blocked false. SPY -3.31% vs entry ($747.35 vs $772.91), ~4.74% (core, no stop by design; not at -7%, under 5% cap). MSFT +18.84% ($542.76 vs $456.70), ~1.19%, trailing stop 27274a69 live on 2 sh (stop $503.235, hwm $559.15, expires 2027-01-28, verified via orders --status open). Sell rules checked in order: no thesis-break evidence (news not checked — Perplexity 401 re-confirmed this run; a price move alone is not evidence), no position down 7% or 15%, no position above 5%. Broker matches portfolio.md. Watchlist unchanged.

## 2026-11-10 daily close
- No orders placed or rejected (markets-closed routine; clock actually showed is_open=true at 15:16 ET — no orders regardless). Equity $100,013.19 (day -$52.31, -0.05%), cash $94,100.00. SPY -3.12% vs entry, ~4.75% (core). MSFT +16.63%, ~1.17%, trailing stop 27274a69 live on 2 sh (stop $503.235, verified). Broker matches portfolio.md. Day vs SPY: -0.05% vs -0.51% (+0.46pp); since inception +0.01% vs +2.64% (-2.63pp).

## 2026-11-11 research routine
- No orders (research-only). Equity $100,067.48, cash $94,100.00; broker matches portfolio.md; MSFT stop 27274a69 verified live. Perplexity 401 insufficient_quota — news not checked. Plan: no action.

## 2026-11-11 risk-only check
- No orders. Equity $100,060.28 (day +$38.66, +0.04%), cash $94,100.00, breaker not tripped, trading_blocked false (12:12 ET). SPY -1.65% vs entry ($760.12 vs $772.91), ~4.82% (core, no stop by design; not at -7%, under 5% cap). MSFT +14.14% ($521.28 vs $456.70), ~1.14%, trailing stop 27274a69 live on 2 sh (stop $503.235, hwm $559.15, expires 2027-01-28, verified via orders --status open). Sell rules checked in order: no thesis-break evidence (news not checked — Perplexity 401 re-confirmed this run; MSFT's ~4% slide from yesterday's $544.94 premarket mark is unexplained, and a price move alone is not evidence), no position down 7% or 15%, no position above 5%. Broker matches portfolio.md. Watchlist unchanged.

## 2026-11-11 daily close
- No orders placed or rejected (markets-closed routine; clock showed is_open=true at 15:16 ET — no orders regardless). Equity $100,058.19 (day +$36.57, +0.04%), cash $94,100.00. SPY -1.62% vs entry, ~4.82% (core). MSFT +13.79%, ~1.14%, trailing stop 27274a69 live on 2 sh (stop $503.235, verified). Broker matches portfolio.md. Day vs SPY: +0.04% vs +1.38% (-1.34pp); since inception +0.06% vs +4.21% (-4.15pp).

## 2026-11-12 research routine
- No orders (research-only). Equity $100,036.94, cash $94,100.00; broker matches portfolio.md; MSFT stop 27274a69 verified live. Perplexity 401 insufficient_quota; MSFT FQ1 FY27 thesis checkpoint verified from Microsoft IR release directly: Azure +48% (vs 44-45% guide, ~35% floor), commercial RPO +73% to $677B — thesis intact. Plan: no action.

## 2026-11-12 risk-only check
- No orders. Equity $100,081.52 (day +$23.56, +0.02%), cash $94,100.00, breaker not tripped, trading_blocked false (12:12 ET). SPY -1.54% vs entry ($760.98 vs $772.91), ~4.82% (core, no stop by design; not at -7%, under 5% cap). MSFT +15.72% ($528.50 vs $456.70), ~1.16%, trailing stop 27274a69 live on 2 sh (stop $503.235, hwm $559.15, expires 2027-01-28, verified via orders --status open). Sell rules checked in order: no thesis break (MSFT FQ1 verified via IR this morning), nothing down 7% or 15%, nothing above 5%. Nothing to do; did nothing.

## 2026-11-12 daily close
- No orders placed or rejected (markets-closed routine; clock showed is_open=true at 15:16 ET — no orders regardless). Equity $100,041.53 (day -$16.43, -0.02%), cash $94,100.00. SPY -2.03% vs entry, ~4.80% (core). MSFT +14.09%, ~1.14%, trailing stop 27274a69 live on 2 sh (stop $503.235, verified). Broker matches portfolio.md. Day vs SPY: -0.02% vs -0.35% (+0.33pp); since inception +0.04% vs +3.78% (-3.74pp).

## 2026-11-13 research routine
- No orders (research-only). Equity $100,040.22, cash $94,100.00; broker matches portfolio.md; MSFT stop 27274a69 verified live. Perplexity 401 insufficient_quota; Microsoft IR checked directly — no new release since FQ1 results dated 2026-10-28; MSFT thesis intact. No gap >5%. Plan: no action.

## 2026-11-13 risk-only check
- No orders. Equity $100,012.00 (day -$33.02, -0.03%), cash $94,100.00, breaker not tripped, trading_blocked false (12:13 ET). SPY -2.77% vs entry ($751.46 vs $772.91), ~4.76% (core, no stop by design; not at -7%, under 5% cap). MSFT +14.80% ($524.31 vs $456.70), ~1.15%, trailing stop 27274a69 live on 2 sh (stop $503.235, hwm $559.15, expires 2027-01-28, verified via orders --status open). Sell rules checked in order: no thesis break (no MSFT IR release since FQ1 10-28, per this morning's research), nothing down 7% or 15%, nothing above 5%. Broker matches portfolio.md. Nothing to do; did nothing.

## 2026-11-13 daily close
- No orders placed or rejected (markets-closed routine; clock showed is_open=true at 15:16 ET — no orders regardless). Equity $100,024.73 (day -$20.29, -0.02%), cash $94,100.00. SPY -2.52% vs entry, ~4.78% (core). MSFT +14.85%, ~1.15%, trailing stop 27274a69 live on 2 sh (stop $503.235, verified). Broker matches portfolio.md. Day vs SPY: -0.02% vs -0.49% (+0.47pp); since inception +0.02% vs +3.28% (-3.25pp).

## 2026-11-13 weekly review
- No trades, no rejections. Review #16 written to lessons.md. Equity $100,018.15 (15:43 ET, market open); broker matches portfolio.md; MSFT stop 27274a69 verified live. Since inception +0.02% vs SPY +3.17% (-3.15pp); week +0.08% vs +2.12% (-2.03pp). Grade D+. Recommends the human decide whether to fix the research and core-sleeve blockers or pause the routines.

## 2026-11-16 research routine
- No orders (research-only). Equity $99,994.49, cash $94,100.00; broker matches portfolio.md; MSFT stop 27274a69 verified live. Perplexity 401 insufficient_quota; Microsoft IR checked directly — no new release since FQ1 results 2026-10-28; MSFT thesis intact. No gap >5% (SPY ~-0.6%, MSFT ~-0.2% vs Friday marks). Plan: no action.

## 2026-11-16 risk-only check
- No orders. Equity $99,965.99 (day -$63.52, -0.06%), cash $94,100.00, breaker not tripped, trading_blocked false (12:12 ET). SPY -3.69% vs entry ($744.41 vs $772.91), ~4.72% (core, no stop by design; not at -7%, under 5% cap). MSFT +14.67% ($523.71 vs $456.70), ~1.15%, trailing stop 27274a69 live on 2 sh (stop $503.235, hwm $559.15, expires 2027-01-28, verified via orders --status open); mark ~$20.5 (~3.9%) above stop. Sell rules checked in order: no thesis break (no MSFT IR release since FQ1 10-28, per this morning's research; no news check beyond that — Perplexity 401), nothing down 7% or 15%, nothing above 5%. SPY's ~-0.6% drift since premarket is index noise, not a reason to act. Broker matches portfolio.md. Did nothing.

## 2026-11-16 daily close
- No orders placed or rejected. Equity $99,917.56 (day -$111.95, -0.11%), cash $94,100.00. Broker matches portfolio.md. SPY $738.66 (-4.43% vs entry, core), MSFT $518.24 (+13.48%); MSFT stop 27274a69 live (stop $503.235, ~2.9% below mark). Day vs SPY -2.02% = +1.91pp (cash weight); since inception -0.08% vs +1.29% = -1.37pp. SPY drop cause unknown (no news source). Figures are 15:16 ET pre-bell marks.

## 2026-11-17 research routine
- No orders (research-only). Equity $99,919.70, cash $94,100.00. Broker matches portfolio.md. MSFT stop 27274a69 verified live (stop $503.235, mark ~2.5% above). Perplexity returned 401 insufficient_quota. Checked Microsoft IR directly: no release since the 2026-10-28 FQ1 results, so the MSFT thesis is intact. The IR calendar shows an Ignite investor Q&A with Nadella today after the close. No gap >5% (SPY +0.15%, MSFT -0.44% vs the 11-16 close marks). Plan: no action.

## 2026-11-17 risk-only check — MSFT trailing stop FILLED
- **Fill (broker-side, not placed by Bull):** MSFT 10% trailing stop `27274a69` sold 2 sh @ $503.03, 2026-11-17 10:40:48 ET (stop $503.235, hwm $559.15). Entry was $456.70 (2026-07-31) → realized ~+$92.66 / +10.1% on 2 sh. Cash $94,100.00 → $95,106.06.
- **Reasoning held:** The stop exists as overnight/intraday protection, not a thesis judgment. The thesis (Azure growth ≥35%, FQ1 FY27 Azure +48%, RPO +73%) was not contradicted by any primary source: Microsoft IR shows no release since 10-28. MSFT was -3.23% on the day (prev close $518.23, last $501.51) vs SPY -1.07%; I do not know why — Perplexity 401, no news source. The Ignite investor Q&A is after today's close, so it can't explain the move.
- **Residual:** 0.189599299 sh (~$95, ~0.10%) left. It is fractional so it can't be stopped, and no sell rule triggers (+9.79%, thesis intact). I did not sell it; selling to tidy up isn't a risk-reduction rule.
- **Other sell rules, in order:** no thesis break found; nothing down 7%+ (SPY core -5.24%, MSFT residual +9.79%); nothing above 5% (SPY ~4.65%). Day -0.08%, breaker not tripped, trading_blocked false. Open orders: none (correct; SPY core has no stop by design, and the MSFT fraction can't carry one).
- **No orders placed by this run.** Re-entry is not allowed here; MSFT is added to watchlist.md for pre-market review.

## 2026-11-18 research routine
- No orders (research-only). Equity $99,856.89, cash $95,106.02 (-$0.04 vs file; likely regulatory fees on the 11-17 MSFT sale). Holdings match portfolio.md; open orders none (correct). Perplexity 401 insufficient_quota. Microsoft IR: no release since FQ1 (10-28), and no Ignite Q&A material found, so the MSFT thesis is intact and the re-entry trigger has not fired. No gap >5% (SPY +0.7%, MSFT +0.1% vs 11-17 marks). Plan: no action.

## 2026-11-18 risk-only check (12:12 ET)
- **No orders placed.** Circuit breaker clear (day -$15.41 / -0.02%); trading_blocked false. Broker matches file: equity $99,829.99, cash $95,106.02, SPY 6.339623293 sh @ $730.26 (-5.52% vs entry, ~4.64%), MSFT residual 0.189599299 sh @ $502.31 (+9.99%, ~0.10%).
- **Sell rules, in order:** (1) Thesis break: none. MSFT IR showed nothing new this morning and I didn't re-check news (Perplexity 401). SPY is core with no thesis. (2) Down 7%: nothing. SPY -5.52% is closest; it's ~1.6% above the -7% line, and whether that rule applies to the core is still an open human question. (3) Down 15%: nothing. (4) Above 5%: nothing (SPY ~4.64%).
- **Stops:** open orders empty. That's correct: there's no full-share satellite (MSFT is a 0.19 sh fraction, and Alpaca won't stop fractions), and SPY core has no stop by design.

## 2026-11-18 daily close
- No orders placed or rejected. Equity $99,835.44 (day -$9.96, -0.01%), cash $95,106.02. Broker matches portfolio.md. SPY $730.83 (-5.45% vs entry, core, no stop by design), MSFT residual 0.19 sh $507.54 (+11.13%, fractional, no stop possible). Open orders: none (correct). Day vs SPY -0.21% = +0.20pp (cash weight); since inception -0.16% vs +0.18% = -0.34pp. Figures are 15:16 ET pre-bell marks.

## 2026-11-19 research routine
- No orders (research-only). Equity $99,886.48, cash $95,106.02 (matches file). Broker matches portfolio.md; open orders none (correct). Perplexity 401 insufficient_quota. Microsoft IR has no release since FQ1 (10-28) and no Ignite Q&A material, so the MSFT thesis is intact and the re-entry trigger has not fired. No gap >5% (SPY +1.1%, MSFT +1.4% vs 11-18 marks). Plan: no action.

## 2026-11-19 risk-only check (12:12 ET)
- **No orders placed.** Circuit breaker clear (day -$69.25 / -0.07%); trading_blocked false. Broker matches file: equity $99,762.33, cash $95,106.02, SPY 6.339623293 sh @ $719.36 (-6.93% vs entry, ~4.57%), MSFT residual 0.189599299 sh @ $505.48 (+10.68%, ~0.10%).
- **Sell rules, in order:** (1) Thesis break: none. MSFT IR had nothing new this morning; MSFT is -0.53% today, which isn't evidence of anything. SPY is core and has no thesis. (2) Down 7%: **not triggered, but only by $0.55.** SPY -6.93% at the position mark (quote $719.95 = -6.85%); the line is ~$718.81. SPY is -1.42% on the day (prev close $730.33). This morning's $738.67 was a pre-market mark, so the intraday drop looks bigger than it really is. I don't know the cause; Perplexity is 401 and I checked no news. Whether rule 2 even applies to the index core is still the open human question. Strategy says the core "doesn't get shaken out," and rule 2 is framed around a "thesis-consistent explanation" that an index fund can't have. I did not pre-empt it. Trimming a core ETF $0.55 before a line that may not apply would be the "doing something" mistake. If a later run finds SPY below the line, it should escalate rather than trim unilaterally (CLAUDE.md: not covered by strategy → urgent, no action), unless the human has answered by then. (3) Down 15%: nothing. (4) Above 5%: nothing (SPY ~4.57%).
- **Stops:** open orders empty. That's correct: there's no full-share satellite, and SPY core has no stop by design.
- **Notified human** (normal) that SPY is at the -7% line with the core-applicability question unresolved.

## 2026-11-19 daily close
- No orders placed or rejected (routine forbids orders). Equity $99,747.81 (day -$83.77, -0.08%), cash $95,106.02. Broker matches portfolio.md. Open orders: none (correct).
- **SPY crossed the -7% trim line:** $717.21 at the position mark, -7.21% vs $772.91 entry (line ~$718.81). Quote was $716.70, -1.87% on the day. Sell rule 2 says "trim half, reassess next wake," but nobody has answered whether it applies to the core index sleeve, which has no thesis and no stop by design. I didn't act. I escalated urgent to the human. **Recommendation for next Bull, with no human answer:** don't trim the core. It's an allocation holding, not a thesis position. Trimming ballast on an index drawdown contradicts the core's stated purpose. That's my reading, not a ruled decision, so re-check for a human reply first. If SPY reaches -15% (~$656.97), rule 3 is unambiguous in wording. Escalate again before acting.
- MSFT residual 0.19 sh $500.81 (+9.66%, fractional, no stop possible). Benchmark: day +1.79pp vs SPY (cash weight); since inception -0.25% vs SPY -1.76% = +1.51pp. That's a cash cushion in a falling market, not skill. Figures are 15:16 ET pre-bell marks.

## 2026-11-20 research routine
- No orders (research-only). Equity $99,700.84, cash $95,106.02 (matches file). Broker matches portfolio.md; open orders none (correct). Perplexity 401 insufficient_quota. Microsoft IR: no release since FQ1 (10-28), so the MSFT thesis is intact and the re-entry trigger has not fired. No gap >5% (SPY -1.0%, MSFT -2.4% vs 11-19 marks). **SPY core closed 11-19 below the -7% trim line** (last $715.84; pre-market $710.16, -8.12% vs entry). Core applicability of rule 2 is still unanswered. I re-escalated urgent and planned no trim. Plan: no action.

## 2026-11-20 risk-only check
- No orders (12:12 ET). Equity $99,651.35 (day -0.09%), cash $95,106.02 (matches file). Breaker not tripped. Broker matches portfolio.md. Open orders: none, which is correct because no satellite holds a full share.
- **SPY core is -9.13% vs entry** ($702.35 vs $772.91), below the -7% trim line for a second session. I did not trim. Whether sell rule 2 applies to the index core is still an open human question, and acting on an uncovered case is an escalation trigger, not something I decide alone. I did not invent a thesis-break story either: SPY has no thesis, and a broad market decline is exactly what ballast is supposed to sit through. Rule 3's -15% line is about $656.97. I re-notified the human.
- MSFT residual 0.19 sh (+7.05%). Thesis intact, no rule triggered. Nothing new for the watchlist.

## 2026-11-20 daily close
- No orders placed or rejected (routine forbids orders). Equity $99,598.48 (day -$140.36, -0.14%), cash $95,106.02. Broker matches portfolio.md. Open orders: none (correct). Figures are 15:16 ET pre-bell marks.
- **SPY core -10.19% vs entry** ($694.15 vs $772.91; quote -3.04% on the day). Below the -7% line for a third session. No trim — rule-2 applicability to the core is still unanswered. The -15% line (rule 3, ~$656.97) is now ~5.4% away; if a later run sees SPY there, escalate urgent before acting — do not exit the core unilaterally, and do not ignore it either.
- MSFT residual 0.19 sh $486.56 (+6.54%). Benchmark: day +2.90pp vs SPY (cash weight); since inception -0.40% vs SPY -4.87% = +4.47pp — cash cushion in a falling market, not skill.

## 2026-11-20 weekly review
- No orders placed or rejected by this run (review-only). Equity $99,572.70 (15:44 ET, market still open), cash $95,106.02. Broker matches portfolio.md. Open orders: none (correct). SPY $690.12 (-10.71% vs entry; below the -7% line, ~4.8% above the -15% line ~$656.97). MSFT residual 0.19 sh $483.04 (+5.77%). Week -0.45% vs SPY -8.31% (+7.87pp, cash). Since inception -0.43% vs SPY -5.41% (+4.98pp, cash, not skill). Grade D+. Review #17 is in lessons.md. Top ask: explicitly rule whether sell rules 2/3 apply to the core before SPY reaches ~$657.

## 2026-11-23 research routine
- No orders (research-only). Equity $99,681.40, cash $95,106.02. Broker matches portfolio.md. Open orders: none (correct). Pre-market marks.
- SPY core $706.79 (-8.55% vs entry). Still below the -7% line; no human ruling on whether rules 2/3 apply to the core, so no trim is planned. MSFT residual $498.96 (+9.25%); thesis intact per Microsoft IR (nothing new since 10-28). No >5% overnight gap. Perplexity is still 401, so no news was checked.

## 2026-11-23 risk-only check (12:12 ET)
- **No orders placed.** Circuit breaker clear (day +$214.03 / +0.21%); trading_blocked false. Broker matches file: equity $99,785.05, cash $95,106.02, SPY 6.339623293 sh @ $723.14, MSFT residual 0.189599299 sh @ $498.93.
- **Sell rules, in order:** (1) Thesis break: none. MSFT IR showed nothing new since 10-28 as of this morning, and MSFT is roughly flat on the day. SPY is the core and has no thesis. (2) Down 7%: **not triggered now.** SPY is -6.44% vs entry, back above the ~$718.81 line after a +4.68% day (prev close $690.68). I don't know why it rallied: Perplexity is 401 and I checked no news. The core-applicability question is still unanswered, but it is moot at today's mark. A next run that finds SPY back below the line should keep treating it as escalate-don't-trim. (3) Down 15%: no (~$656.97 line, ~9% below mark). (4) Above 5%: no (SPY ~4.59%, MSFT ~0.09%).
- **Stops:** open orders empty. That's correct: there's no full-share satellite (MSFT is 0.19 sh, fractional), and the SPY core has no stop by design.
- Nothing new for the watchlist. No notification sent: nothing triggered, and the open core question was already escalated (weekly review #17).

## 2026-11-23 daily close (15:16 ET, pre-bell)
- **No orders placed or rejected** (routine forbids orders). Equity $99,790.51 (day +$219.49 / +0.22%), cash $95,106.02. Broker matches portfolio.md. Open orders: none (correct). trading_blocked false.
- SPY core $724.02 (-6.33% vs entry $772.91), above the -7% line (~$718.81) by only ~0.7% after a +4.75% day (quote 723.455 vs prev close 690.68). I don't know what drove the rally: Perplexity is still 401 and no news was checked. A dip of under 1% puts it back below the line; core-applicability of rules 2/3 is still unanswered, so keep treating that as escalate-don't-trim.
- MSFT residual 0.19 sh $498.30 (+9.11%). Benchmark: day -4.53pp vs SPY (cash weight on an up day); since inception -0.21% vs SPY -0.84% = +0.63pp, down from +4.47pp on Friday. Cash cushion, not skill.

## 2026-11-24 research routine
- No orders (research-only). Equity $99,728.66, cash $95,106.02. Broker matches portfolio.md. Open orders: none (correct). Pre-market marks.
- SPY core $714.52 (-7.56% vs entry), back below the -7% line after closing just above it Monday; no human ruling on rules 2/3 for the core, so no trim planned. MSFT residual $489.75 (+7.24%); thesis intact per Microsoft IR (nothing new since 10-28). No >5% overnight gap (SPY -1.1%, MSFT -0.6% vs 11-23 last trade). Perplexity still 401; no news checked.

## 2026-11-24 risk-only check (12:12 ET)
- **No orders placed.** Circuit breaker clear (day -$21.83 / -0.02%); trading_blocked false. Broker matches file: equity $99,756.61, cash $95,106.02, SPY 6.339623293 sh @ $718.56, MSFT residual 0.189599299 sh @ $499.85.
- **Sell rules, in order:** (1) Thesis break: none. MSFT is +9.45% vs entry with no adverse price signal. I did not pull news (Perplexity 401 per this morning's research run). SPY is the core and has no thesis. (2) Down 7%: **SPY -7.03% vs entry**, about $0.25 below the ~$718.81 line. That's a hair under it, after it closed just above on 11-23. Not trimmed. Rule-2 applicability to the core is still unanswered by the human (escalated urgent 11-19, re-notified 11-20, top ask in weekly review #17). Treatment unchanged: escalate, don't trim. A trim here would be acting on a ~0.03% line crossing in a broad-index decline, which is the "feel like I'm doing something" trade. (3) Down 15%: no (line ~$656.97, ~8.6% below mark). (4) Above 5%: no (SPY ~4.57%, MSFT ~0.10%).
- **Stops:** open orders empty. That's correct: there's no full-share satellite (MSFT 0.19 sh is fractional), and the SPY core has no stop by design.
- Nothing new for the watchlist. No notification sent: nothing new triggered, and the open core question is already escalated.

## 2026-11-24 daily close (15:15 ET, pre-bell)
- **No orders placed or rejected** (routine forbids orders). Broker matches file: equity $99,745.20, cash $95,106.02, SPY 6.339623293 sh @ $717.01 (-7.23% vs entry, below the -7% line; core applicability of rule 2 still unanswered, not trimmed), MSFT residual 0.189599299 sh @ $493.71 (+8.11%). Open orders empty (correct). No new lesson.

## 2026-11-25 research routine
- No orders (research-only). Equity $99,669.70, cash $95,106.02. Broker matches portfolio.md. Open orders: none (correct). Pre-market marks.
- SPY core $705.52 (-8.72% vs entry), below the -7% line pre-market. The 11-24 last trade, $718.91 (unconfirmed as close), was ~$0.10 above it. No human ruling on rules 2/3 for the core, so no trim planned. MSFT residual $479.70 (+5.04%). Thesis intact per Microsoft IR (nothing new since 10-28). No >5% overnight gap (SPY -1.9%, MSFT -3.3% vs 11-24 last trade). Cause unknown: Perplexity still 401, no news checked.
- No notification sent. Perplexity has been 401 for ~9 weeks and is already escalated in the weekly reviews. No thesis broke and nothing gapped >5%.

## 2026-11-25 risk-only check (12:11 ET)
- **No orders placed.** Circuit breaker clear (day -$80.85 / -0.08%); trading_blocked false. Broker matches file: equity $99,676.03, cash $95,106.02, SPY 6.339623293 sh @ $706.34, MSFT residual 0.189599299 sh @ $485.66.
- **Sell rules, in order:** (1) Thesis break: none. MSFT is +6.34% vs entry. Microsoft IR has nothing new since 10-28 (per this morning's research run). No news pulled: Perplexity is still 401. SPY is the core and has no thesis. (2) Down 7%: **SPY -8.61% vs entry**, below the ~$718.81 line. Not trimmed: whether rule 2 applies to the core is still unanswered by the human (escalated urgent 11-19, re-asked in weekly review #17). Same treatment as every prior run. Trimming an index sleeve into a broad decline is the macro call strategy.md says Bull shouldn't make. (3) Down 15%: no. The line is ~$656.97, ~7.0% below the mark. (4) Above 5%: no (SPY ~4.49%, MSFT ~0.09%).
- **Stops:** open orders empty. That's correct: there's no full-share satellite, and the core has no stop by design.
- Nothing new for the watchlist. No notification sent: nothing new triggered, and the core question is already escalated.

## 2026-11-25 daily close (15:16 ET, pre-bell)
- **No orders placed or rejected** (routine forbids orders). Broker matches file: equity $99,739.43, cash $95,106.02, SPY 6.339623293 sh @ $716.25 (-7.33% vs entry, below the -7% line; core applicability of rule 2 still unanswered, not trimmed), MSFT residual 0.189599299 sh @ $489.69 (+7.22%). Open orders empty (correct). Market closed Thu 11-26 (Thanksgiving); next open Fri 11-27 09:30 ET (expected half-day). No new lesson.
