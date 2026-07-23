"""
Hard risk limits. These are enforced in code, not in prompts.

Every order goes through check_order() before it reaches Alpaca. If a rule
fails, the order is rejected and the reason is printed. The agent cannot
talk its way past this file — it can only report that it was blocked.

Edit the LIMITS dict to change policy. Treat changes here the way you'd
treat changes to a live production config: deliberately, and not at 3pm
on a red day.
"""

import json
import os
from datetime import datetime, timezone

LIMITS = {
    # No single position may exceed this share of total equity.
    "max_position_pct": 0.05,

    # Refuse all new buys once the portfolio is down this much on the day.
    # This is the circuit breaker. It exists to stop a bad day from
    # becoming a bad week.
    "daily_loss_halt_pct": 0.03,

    # Maximum number of distinct holdings at once.
    "max_open_positions": 15,

    # Maximum NEW positions opened per calendar week.
    "max_new_positions_per_week": 3,

    # Minimum cash buffer, as a share of equity, that must remain after
    # any buy. Prevents the agent from going fully invested.
    "min_cash_reserve_pct": 0.10,

    # Hard cap on any single order's notional value, in account currency.
    "max_order_notional": 2000,

    # Never trade these. Leveraged and inverse ETFs decay and are not
    # appropriate for a hold-and-review cadence.
    "symbol_blocklist": [
        "TQQQ", "SQQQ", "UVXY", "SVXY", "SPXL", "SPXS", "SOXL", "SOXS",
        "TNA", "TZA", "UPRO", "SPXU", "LABU", "LABD", "YANG", "YINN",
        "VIX", "VXX", "UGAZ", "DGAZ", "NUGT", "DUST",
    ],

    # Order types the agent is permitted to submit.
    "allowed_order_types": ["market", "limit"],

    # Asset classes permitted. Options and crypto are off.
    "allowed_asset_classes": ["us_equity"],
}

STATE_PATH = os.path.join(os.path.dirname(__file__), "..", "memory", ".risk_state.json")


class Rejected(Exception):
    """Raised when an order violates a hard limit."""


def _load_state():
    try:
        with open(STATE_PATH) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"week": None, "new_positions_this_week": 0}


def _save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def _current_week():
    now = datetime.now(timezone.utc)
    return f"{now.isocalendar().year}-W{now.isocalendar().week:02d}"


def record_new_position():
    """Call after a buy that opens a position the account did not hold."""
    state = _load_state()
    week = _current_week()
    if state.get("week") != week:
        state = {"week": week, "new_positions_this_week": 0}
    state["new_positions_this_week"] += 1
    _save_state(state)


def new_positions_this_week():
    state = _load_state()
    if state.get("week") != _current_week():
        return 0
    return state.get("new_positions_this_week", 0)


def check_order(*, symbol, side, notional, order_type, account, positions):
    """
    Validate an order against every hard limit.

    account:   dict from Alpaca GET /v2/account
    positions: list from Alpaca GET /v2/positions

    Raises Rejected with a human-readable reason, or returns a list of
    non-fatal warnings.
    """
    symbol = symbol.upper()
    side = side.lower()
    warnings = []

    equity = float(account["equity"])
    last_equity = float(account.get("last_equity") or equity)
    cash = float(account["cash"])
    held = {p["symbol"].upper(): p for p in positions}

    if order_type not in LIMITS["allowed_order_types"]:
        raise Rejected(f"order type '{order_type}' is not permitted")

    if symbol in LIMITS["symbol_blocklist"]:
        raise Rejected(f"{symbol} is on the blocklist (leveraged/inverse/volatility product)")

    if account.get("trading_blocked") or account.get("account_blocked"):
        raise Rejected("Alpaca reports the account is blocked from trading")

    # --- Sells: only ever to close or trim an existing long. No shorting. ---
    if side == "sell":
        if symbol not in held:
            raise Rejected(f"cannot sell {symbol}: no open position (shorting is disabled)")
        held_value = abs(float(held[symbol]["market_value"]))
        if notional > held_value * 1.01:
            raise Rejected(
                f"sell notional {notional:.2f} exceeds position value {held_value:.2f}"
            )
        return warnings

    if side != "buy":
        raise Rejected(f"unrecognized side '{side}'")

    # --- Buys ---
    daily_pl_pct = (equity - last_equity) / last_equity if last_equity else 0.0
    if daily_pl_pct <= -LIMITS["daily_loss_halt_pct"]:
        raise Rejected(
            f"daily loss circuit breaker: portfolio is {daily_pl_pct:.2%} on the day, "
            f"limit is -{LIMITS['daily_loss_halt_pct']:.0%}. No new buys today."
        )

    if notional > LIMITS["max_order_notional"]:
        raise Rejected(
            f"order notional {notional:.2f} exceeds per-order cap "
            f"{LIMITS['max_order_notional']:.2f}"
        )

    existing_value = abs(float(held[symbol]["market_value"])) if symbol in held else 0.0
    resulting_pct = (existing_value + notional) / equity
    if resulting_pct > LIMITS["max_position_pct"]:
        raise Rejected(
            f"{symbol} would become {resulting_pct:.2%} of equity, "
            f"limit is {LIMITS['max_position_pct']:.0%}"
        )

    is_new = symbol not in held
    if is_new and len(held) >= LIMITS["max_open_positions"]:
        raise Rejected(
            f"already holding {len(held)} positions, limit is {LIMITS['max_open_positions']}"
        )

    if is_new and new_positions_this_week() >= LIMITS["max_new_positions_per_week"]:
        raise Rejected(
            f"already opened {new_positions_this_week()} new positions this week, "
            f"limit is {LIMITS['max_new_positions_per_week']}"
        )

    remaining_cash = cash - notional
    if remaining_cash < equity * LIMITS["min_cash_reserve_pct"]:
        raise Rejected(
            f"order would leave {remaining_cash:.2f} cash, below the "
            f"{LIMITS['min_cash_reserve_pct']:.0%} reserve ({equity * LIMITS['min_cash_reserve_pct']:.2f})"
        )

    if daily_pl_pct <= -LIMITS["daily_loss_halt_pct"] / 2:
        warnings.append(
            f"portfolio is {daily_pl_pct:.2%} on the day — halfway to the circuit breaker"
        )

    return warnings


if __name__ == "__main__":
    print(json.dumps(LIMITS, indent=2))
    print(f"\nnew positions this week: {new_positions_this_week()}")
