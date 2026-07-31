# Portfolio

Last updated: 2026-07-31 (intraday risk-reduction routine) — reconciled
against Alpaca, which showed a MSFT position this file did not have on
record. See `lessons.md` 2026-07-31 entry for why.

**Alpaca is the source of truth.** This file is a human-readable mirror with
the reasoning attached, which the broker does not store. If they disagree,
trust Alpaca, fix this file, and log why they drifted.

## Snapshot

| Field | Value |
|-------|-------|
| Mode | PAPER |
| Equity | $100,010.86 |
| Cash | $99,000.01 |
| Open positions | 1 |
| New positions this week | 0 (per Alpaca `new_positions_this_week`; MSFT buy filled 2026-07-31, same week) |

## Holdings

### MSFT — 1.01% of equity
- **Entry:** 2026-07-31, $456.70 avg, $1,000 notional (2.189599299 sh)
- **Thesis:** Azure/cloud revenue growth is accelerating (40% -> 43% YoY,
  FQ3 -> FQ4 FY26) on real reported numbers, not capex narrative; EPS
  growth (FY26 GAAP diluted EPS $17.95) is outrunning the post-earnings
  price move, so the ~25.2x trailing P/E is near the bottom of MSFT's own
  5-year range despite the stock being up double digits post-print.
- **Invalidation:** Azure YoY growth decelerates back below ~35% in the
  FQ1 FY27 print, commercial RPO growth reverses meaningfully, or capex
  guidance is cut in a way that reads as AI-monetization doubt rather than
  discipline.
- **Catalyst:** already happened (FY26 Q4 earnings, reported 2026-07-29);
  next checkpoint is the FQ1 FY27 print.
- **Stop:** 10% trailing stop live as of 2026-07-31 intraday run (covers 2
  of 2.19 whole shares; Alpaca does not accept trailing stops on the
  fractional remainder). Order id `cee441de-48ae-4e48-9cc2-d6482a4c3b0a`.
- **Status:** on track — up 1.09% unrealized, no news since entry that
  challenges the thesis (FY26 Q4 beat on both EPS and revenue, guidance
  raised; see trade-log for sourcing).

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
