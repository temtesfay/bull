# Bull

An autonomous equity portfolio agent that runs on Claude Code routines.
Wakes on a schedule, reads its own files, decides, writes back, pushes.

**Starts in paper mode. Leave it there for a while.**

## Layout

```
CLAUDE.md              agent constitution — read first on every wake
memory/
  strategy.md          the rules. You write these. Bull doesn't touch them.
  portfolio.md         holdings + the reasoning the broker doesn't store
  trade-log.md         append-only ledger, with reasoning at decision time
  watchlist.md         candidates and the daily plan
  lessons.md           post-mortems — the only way this improves
scripts/
  guardrails.py        hard risk limits, enforced in code
  alpaca.py            the only path to the broker
  notify.py            webhook notifications
routines/              five prompts, one per scheduled run
```

## The design choice that matters

The risk limits are in **code**, not in the prompt. `alpaca.py` has no bypass
flag — every order calls `guardrails.check_order()` first, and a rejection is
final.

This is the difference between a system and a suggestion. A stateless agent
waking up four times a day will, eventually, on some volatile afternoon,
construct a very reasonable-sounding argument for why today is different and
the 5% cap shouldn't apply. Prompts lose that argument. Python doesn't.

Current limits: 5% max per position, 3% daily loss circuit breaker, 3 new
positions per week, 15 positions max, 10% cash reserve, $2000 per order,
long US equities only, leveraged and inverse ETFs blocklisted.

Change them by editing `LIMITS` in `guardrails.py` — deliberately, and not
on a red day.

## Setup

**1. Alpaca** — sign up at alpaca.markets, take the paper trading account.
Generate an API key and secret; the secret is shown once. Live accounts need
verification, which takes a few days, so start paper regardless.

**2. GitHub** — push this to a **private** repo. Remote routines clone the
repo into a fresh container, work, and destroy it. The repo *is* the agent's
memory. `.gitignore` already excludes `.env` and key files.

**3. Cloud environment** — in the Claude Code desktop app, Routines → New →
Remote → add a cloud environment. Give it network access and set:

```
ALPACA_API_KEY_ID
ALPACA_API_SECRET_KEY
ALPACA_PAPER            true
PERPLEXITY_API_KEY
NOTIFY_WEBHOOK_URL
NOTIFY_FORMAT           slack | discord | plain
```

Names must match **character for character**. A mismatched variable name is
the most common reason a first run dies, and it fails silently-ish — the
script exits with an auth error buried in a long transcript.

**4. Routines** — create five, one per file in `routines/`, pointed at this
repo and that environment. Crons are in the file headers, already set to
Mountain Time for Edmonton (the 7:45 AM open run is 15 minutes after the
bell on purpose).

In each routine's permissions, enable **allow unrestricted branch pushes**,
or Bull writes to a `claude/*` branch and the next run reads stale files.

**5. Test before scheduling.** Run each routine manually with "Run now" and
read the full transcript. Confirm specifically that the commit landed on
`main` — a routine that does perfect analysis and fails to push has done
nothing at all.

## Local smoke test

```bash
export ALPACA_API_KEY_ID=... ALPACA_API_SECRET_KEY=... ALPACA_PAPER=true
cd scripts
python3 alpaca.py account
python3 alpaca.py quote SPY AAPL
python3 guardrails.py            # prints active limits
python3 alpaca.py buy AAPL --notional 50000   # should be REJECTED
```

## Going live

Don't, yet. Before flipping `ALPACA_PAPER=false`:

- Run paper for at least a full quarter. Three months is still a small
  sample, but it's enough to catch the process failures — missed pushes,
  stale plans, auth expiry, reconciliation drift.
- Read every weekly review. If Bull graded its own process honestly and the
  grades were bad, that's the system working; fix it before adding money.
- Fund it with an amount whose total loss would change nothing about your
  life. Not "an amount I'd be annoyed to lose."

## What this is not

This is not a strategy with a demonstrated edge. It's a well-instrumented
harness for running one and finding out.

Thirty days of beating the index proves nothing — any portfolio more
volatile than the benchmark beats it roughly half the time over a month, and
you only ever hear about the halves that won. Meaningful separation of skill
from luck in equity returns takes years, not weeks. The weekly review prints
a sample-size warning for exactly this reason, and it will keep printing it
for six months.

The honest reason to build this is that the architecture — scheduled
stateless agents, file-based memory, code-enforced limits, self-auditing
review loops — is genuinely useful and transfers to a dozen other problems.
The portfolio is the excuse to learn it. Treat any returns as a rounding
error on the education.

Not investment advice. You are responsible for every order this places.
