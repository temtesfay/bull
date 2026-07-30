# Portfolio

Last updated: 2026-07-30 (end-of-day close, ground truth reconfirmed via Alpaca — no change)

**Alpaca is the source of truth.** This file is a human-readable mirror with
the reasoning attached, which the broker does not store. If they disagree,
trust Alpaca, fix this file, and log why they drifted.

## Snapshot

| Field | Value |
|-------|-------|
| Mode | PAPER |
| Equity | $100,000.00 |
| Cash | $100,000.00 |
| Open positions | 0 |
| New positions this week | 0 |

## Holdings

_None yet._

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
