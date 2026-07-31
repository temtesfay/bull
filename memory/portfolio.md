# Portfolio

Last updated: 2026-07-31 (market-open execution routine, ground truth via
Alpaca after the MSFT fill: $100,000.22 equity, $99,000.01 cash, 1 open
position)

**Alpaca is the source of truth.** This file is a human-readable mirror with
the reasoning attached, which the broker does not store. If they disagree,
trust Alpaca, fix this file, and log why they drifted.

## Snapshot

| Field | Value |
|-------|-------|
| Mode | PAPER |
| Equity | $100,000.22 |
| Cash | $99,000.01 |
| Open positions | 1 |
| New positions this week | 1 |

## Holdings

### MSFT — 1.00% of equity
- **Entry:** 2026-07-31, avg $456.70, 2.1896 shares ($1,000 notional)
- **Thesis:** Azure revenue growth accelerated 40% -> 43% YoY across FQ3/FQ4
  FY26 (Microsoft's own IR site), and trailing P/E (~25.2x) sits near the
  bottom of MSFT's own 5-year range (~25.1x-37.8x) despite the post-earnings
  pop — EPS growth is outrunning price.
- **Invalidation:** Azure YoY growth decelerates back below ~35% in the FQ1
  FY27 print, commercial RPO growth reverses meaningfully, or capex guidance
  is cut in a way that reads as AI-monetization doubt rather than discipline.
- **Catalyst:** already happened (FQ4 FY26 earnings, 2026-07-29); next check
  point is the FQ1 FY27 print.
- **Stop:** none — position is 2.1896 fractional shares, below the 1-whole-
  share minimum Alpaca requires for a trailing stop. Set `protect` once/if
  this crosses into a full share.
- **Status:** on track (1% starter; earn size before adding)

Format for each position, one block:

### TICKER — 0.0% of equity
- **Entry:** date, avg price, size
- **Thesis:** one sentence, falsifiable
- **Invalidation:** the specific thing that would make this wrong
- **Catalyst:** what and roughly when
- **Stop:** trailing % if set
- **Status:** on track / watching / trimming

## Benchmark

| Date | Portfolio | SPY | Delta |
|------|-----------|-----|-------|
| 2026-07-30 | 0.00% | +1.65% | -1.65% |

Since-inception delta (2026-07-29 close baseline, when the account was first
funded at $100,000 with 0 positions): portfolio +0.00%, SPY +1.65%, delta
-1.65%. Identical to today's row because the account has never traded — only
one trading day has elapsed since inception, so "today" and "since inception"
are the same figure right now. They will diverge once either a trade happens
or another day passes. SPY figures come from `alpaca.py quote SPY`
(`prev_close` 729.57 → `last` 741.63); no SPY baseline price was captured on
day one itself, so this table starts today rather than retroactively.
