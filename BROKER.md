# Broker notes

## Current: Alpaca (paper only)

Bull trades through Alpaca via [`scripts/alpaca.py`](scripts/alpaca.py), with
`ALPACA_PAPER=true`. **This is simulated money.**

## Canada limitation — read before ever going live

The account owner is a **Canadian resident**. As of July 2026, Alpaca offers
**paper trading globally** (Canada included) but **does not permit live,
real-money trading for Canadian residents**. Paper works fine; live does not.

This is not a blocker today — `memory/strategy.md` requires paper-only operation
for at least 1–3 months regardless. It only matters if a human later decides to
trade real money.

### What "going live" would require

Flipping `ALPACA_PAPER=false` will **not** work from Canada. Going live means
switching to a broker that (a) accepts Canadian residents and (b) exposes a
trading API. Options that meet both, as of writing:

- **Interactive Brokers (IBKR)** — supports Canada, mature API, has its own
  paper environment.
- **Questrade** — Canadian, has an API.
- **Wealthsimple** — Canadian, but no official public trading API.

Swapping brokers is a **contained** job: rewrite `scripts/alpaca.py` to speak
the new broker's API. `scripts/guardrails.py`, the routines, and the memory
files do not need to change — they don't know or care which broker is underneath.

This is a **human decision**, not something a routine may do on its own. None of
this is financial or brokerage advice.
