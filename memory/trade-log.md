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

### 2026-07-31 09:46 — BUY MSFT
- Size: $1,000 notional (1.00% of equity), filled 2.1896 shares
- Fill: $456.70 avg entry
- Reason: Executing the pre-market plan from `watchlist.md` (dated 2026-07-31,
  same day — plan was current). Re-verified price before acting: quote showed
  MSFT at $456.21 vs the plan's reference price of $451.545 (2026-07-30
  close), a +1.03% move — well under the 3% re-check threshold, so the setup
  was unchanged. Traded 16 minutes after the 09:30 ET open, clearing the
  first-15-minutes rule.
- Thesis / invalidation: Azure revenue growth accelerated 40% -> 43% YoY
  across FQ3/FQ4 FY26 (Microsoft's own IR site, not a summary) — real trend.
  Trailing P/E ~25.2x sits near the bottom of MSFT's own 5-year P/E range
  (~25.1x-37.8x) despite the post-earnings pop, so EPS growth is outrunning
  price. Invalidated if Azure YoY growth decelerates back below ~35% in the
  FQ1 FY27 print, commercial RPO growth reverses meaningfully, or capex
  guidance is cut in a way that reads as AI-monetization doubt rather than
  discipline.
- Confidence: medium-high (5 of 5 buy criteria met, only 3 required) — sized
  as a 1% starter rather than the 3% standard because it's a higher-beta
  growth name (size down a notch per `strategy.md`) and because the stock
  already ran +15% in the prior session before this routine could act,
  which is chase risk even with a defensible multiple.
- Source: Microsoft FY26 Q4 IR press release (fetched directly), Microsoft
  FY26 Q3 metrics page (fetched directly), Alpaca `quote`/`positions` for
  live price and fill.
- Overnight protection: NOT set. Position is 2.1896 fractional shares;
  `alpaca.py protect` requires >=1 whole share (Alpaca does not accept
  trailing stops on fractional quantities) and `CLAUDE.md` only requires
  protection on full-share satellite positions. Revisit protection once/if
  this position is added to and crosses into a whole share.
