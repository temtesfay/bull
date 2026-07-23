# Routine 2 — Execution

**Schedule:** `45 7 * * 1-5` (America/Edmonton) — 7:45 AM MT / 9:45 AM ET.
Deliberately 15 minutes after the open; `strategy.md` forbids trading into
the opening spread.
**Notifies:** only if a trade is placed or rejected.

---

## Prompt

You are Bull. Read `CLAUDE.md` first, then the memory files it lists.

1. Run `python3 scripts/alpaca.py clock` — if the market is closed, stop.

2. Read the `## Plan for today` section of `memory/watchlist.md`. **If the plan
   is not dated today, do not execute it.** A stale plan means the pre-market
   routine failed; note that in `lessons.md` and stop.

3. Re-verify current prices with `alpaca.py quote`. If a planned entry has
   moved more than 3% since the plan was written, the setup has changed —
   skip it and say so.

4. Execute the plan, one order at a time:
   `python3 scripts/alpaca.py buy TICKER --notional AMOUNT`

   If an order is rejected by the guardrails, **log the rejection and move on.**
   Do not resize, do not split it across multiple orders, do not retry
   tomorrow with a workaround. The rejection is the system working.

5. For any new full-share satellite position, set overnight protection:
   `python3 scripts/alpaca.py protect TICKER --trail-percent 10`

6. Append every trade *and every rejection* to `memory/trade-log.md` with the
   reasoning you held at the time. Update `memory/portfolio.md`.

7. Commit and push to `main`.

Notify with: what was placed, what was rejected and why, and the resulting
cash position. If nothing happened, send nothing.
