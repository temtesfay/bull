# Setup — how Bull is wired

The live configuration, recorded so it can be rebuilt without guesswork.
Everything below lives in **Claude Routines**, not in this repo — the repo holds
only code, strategy, and memory. Secrets never live here.

## Cloud environment: `Trading`

- **Network access:** custom allowlist (not the default "Trusted" preset — that
  blocks Alpaca).
- **Environment variables:**
  | Name | Value | Needed by |
  |---|---|---|
  | `ALPACA_API_KEY_ID` | *(paper key)* | all |
  | `ALPACA_API_SECRET_KEY` | *(paper secret)* | all |
  | `ALPACA_PAPER` | `true` | all — **keep true** |
  | `PERPLEXITY_API_KEY` | *(key)* | routine 1 (research) |
  | `NOTIFY_WEBHOOK_URL` | *(Discord webhook)* | routines 4, 5, escalations |
  | `NOTIFY_FORMAT` | `discord` | notifications |
- **Network allowlist domains:**
  - `paper-api.alpaca.markets` — account, orders, clock
  - `data.alpaca.markets` — quotes
  - `api.alpaca.markets` — live endpoint (unused while paper)
  - `api.perplexity.ai` — news research
  - `discord.com` — notification webhook

## The five routines

All share repo `temtesfay/bull` + environment `Trading`, timezone
**America/Edmonton (Mountain)**, and **must have "push to `main`" enabled** in the
Behavior tab (or memory never saves). Instructions = the `## Prompt` section of
each file.

| # | Name | Local time | Cron | Source |
|---|---|---|---|---|
| 1 | Bull — Premarket | Mon–Fri 6:30 AM | `30 6 * * 1-5` | `routines/01-premarket.md` |
| 2 | Bull — Execution | Mon–Fri 7:45 AM | `45 7 * * 1-5` | `routines/02-open.md` |
| 3 | Bull — Risk check | Mon–Fri 11:00 AM | `0 11 * * 1-5` | `routines/03-midday.md` |
| 4 | Bull — Close | Mon–Fri 2:15 PM | `15 14 * * 1-5` | `routines/04-close.md` |
| 5 | Bull — Weekly | Fri 2:30 PM | `30 14 * * 5` | `routines/05-weekly-review.md` |

## Verified working (2026-07-24)

Read-only connection test passed: paper account $100,000, no positions, clock
correct. Discord webhook test delivered.

## Live rules of the road

- **Stay on paper** for at least 1–3 months (`strategy.md`). Going live from
  Canada requires a broker swap — see `BROKER.md`.
- Routine 2 (Execution) is the only one that places trades. Everything else
  reads, journals, or reduces risk.
- Optional first-week de-risking: leave routine 2 **disabled** so Premarket
  plans and Close journals without any trade actually executing; enable it once
  the reasoning has earned trust.
