#!/usr/bin/env bash
#
# Run once, from inside the bull/ directory, after extracting.
#   ./setup.sh
#
set -euo pipefail

cd "$(dirname "$0")"
echo "Bull setup"
echo "=========="

# --- 1. Python ---
if ! command -v python3 >/dev/null 2>&1; then
  echo "FAIL: python3 not found. Install it before continuing."
  exit 1
fi
echo "  python3        $(python3 --version 2>&1 | cut -d' ' -f2)"

if ! python3 -m py_compile scripts/*.py 2>/dev/null; then
  echo "FAIL: scripts did not compile. The extraction may be incomplete."
  exit 1
fi
echo "  scripts        compile clean"

# --- 2. Structure ---
missing=0
for f in CLAUDE.md README.md .gitignore \
         memory/strategy.md memory/portfolio.md memory/trade-log.md \
         memory/watchlist.md memory/lessons.md \
         scripts/guardrails.py scripts/alpaca.py scripts/notify.py \
         routines/01-premarket.md routines/02-open.md routines/03-midday.md \
         routines/04-close.md routines/05-weekly-review.md; do
  [ -f "$f" ] || { echo "  MISSING: $f"; missing=1; }
done
[ "$missing" -eq 0 ] && echo "  structure      all 16 files present"

# --- 3. Guardrail self-test (no network, no credentials needed) ---
python3 - <<'PY'
import sys
sys.path.insert(0, "scripts")
import guardrails as g

acct = {"equity": "10000", "last_equity": "10000", "cash": "10000",
        "trading_blocked": False, "account_blocked": False}
checks = [
    ("normal buy allowed",   dict(symbol="AAPL", side="buy",  notional=400, order_type="market"), True),
    ("oversized rejected",   dict(symbol="AAPL", side="buy",  notional=900, order_type="market"), False),
    ("blocklist rejected",   dict(symbol="TQQQ", side="buy",  notional=100, order_type="market"), False),
    ("short rejected",       dict(symbol="AAPL", side="sell", notional=100, order_type="market"), False),
    ("bad type rejected",    dict(symbol="AAPL", side="buy",  notional=100, order_type="stop"),   False),
]
ok = True
for name, kw, should_pass in checks:
    try:
        g.check_order(account=acct, positions=[], **kw)
        passed = True
    except g.Rejected:
        passed = False
    status = "ok" if passed == should_pass else "FAIL"
    if status == "FAIL":
        ok = False
    print(f"  guardrail      {status:4} {name}")

breaker = dict(acct); breaker["equity"] = "9600"
try:
    g.check_order(symbol="AAPL", side="buy", notional=100, order_type="market",
                  account=breaker, positions=[])
    print("  guardrail      FAIL circuit breaker did not fire"); ok = False
except g.Rejected:
    print("  guardrail      ok   circuit breaker fires at -3%")

sys.exit(0 if ok else 1)
PY

# --- 4. Git ---
if [ ! -d .git ]; then
  git init -q
  git add -A
  git -c user.email=bull@localhost -c user.name=Bull \
      commit -qm "Bull: initial scaffold" || true
  echo "  git            initialized, first commit made"
else
  echo "  git            already initialized"
fi

cat <<'NEXT'

Setup passed. Remaining steps, in order:

  1. Rewrite memory/strategy.md. It ships with a placeholder strategy that
     is not yours. This file is the actual product.

  2. Create a PRIVATE GitHub repo and push:
       gh repo create bull --private --source=. --push
     (or ask Claude Code to do it — it handles the auth flow)

  3. Claude Code desktop -> Routines -> New -> Remote -> add a cloud
     environment. Set these variables, names matching exactly:
       ALPACA_API_KEY_ID
       ALPACA_API_SECRET_KEY
       ALPACA_PAPER=true
       PERPLEXITY_API_KEY
       NOTIFY_WEBHOOK_URL
       NOTIFY_FORMAT

  4. Create five routines from the files in routines/. Crons are in each
     file header (Mountain Time). Enable "allow unrestricted branch
     pushes" on each, or Bull writes to a branch nobody reads.

  5. Run each one manually before scheduling. Confirm the commit landed
     on main — that is the step that silently fails.

Local smoke test once you have Alpaca keys:
  export ALPACA_API_KEY_ID=... ALPACA_API_SECRET_KEY=... ALPACA_PAPER=true
  python3 scripts/alpaca.py account
  python3 scripts/alpaca.py buy AAPL --notional 50000   # must be REJECTED

NEXT
