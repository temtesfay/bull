#!/usr/bin/env python3
"""
Thin Alpaca client. Standard library only — no pip install needed, which
matters because remote routines run in a fresh container every time.

Every order goes through guardrails.check_order() first. There is no
bypass flag. If you need to place an order the guardrails reject, do it
by hand in the Alpaca web UI, where you have to think about it.

Credentials come from environment variables, never from a file:
    ALPACA_API_KEY_ID
    ALPACA_API_SECRET_KEY
    ALPACA_PAPER          "true" (default) or "false"

Usage:
    python3 alpaca.py account
    python3 alpaca.py positions
    python3 alpaca.py clock
    python3 alpaca.py quote AAPL MSFT
    python3 alpaca.py buy AAPL --notional 500
    python3 alpaca.py sell AAPL --notional 500
    python3 alpaca.py close AAPL
    python3 alpaca.py orders --status all --limit 20
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

import guardrails

PAPER = os.environ.get("ALPACA_PAPER", "true").lower() != "false"
TRADE_HOST = "https://paper-api.alpaca.markets" if PAPER else "https://api.alpaca.markets"
DATA_HOST = "https://data.alpaca.markets"


def _headers():
    key = os.environ.get("ALPACA_API_KEY_ID")
    secret = os.environ.get("ALPACA_API_SECRET_KEY")
    if not key or not secret:
        sys.exit(
            "ERROR: ALPACA_API_KEY_ID and ALPACA_API_SECRET_KEY must be set as "
            "environment variables. In a remote routine, set them on the cloud "
            "environment. Names must match exactly, character for character."
        )
    return {
        "APCA-API-KEY-ID": key,
        "APCA-API-SECRET-KEY": secret,
        "Content-Type": "application/json",
    }


def _request(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=_headers(), method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode()
        sys.exit(f"ERROR: Alpaca returned {e.code} for {method} {url}\n{detail}")
    except urllib.error.URLError as e:
        sys.exit(f"ERROR: could not reach Alpaca ({e.reason}). Check network access.")


def get_account():
    return _request("GET", f"{TRADE_HOST}/v2/account")


def get_positions():
    return _request("GET", f"{TRADE_HOST}/v2/positions")


def get_clock():
    return _request("GET", f"{TRADE_HOST}/v2/clock")


def get_snapshots(symbols):
    q = urllib.parse.urlencode({"symbols": ",".join(s.upper() for s in symbols)})
    return _request("GET", f"{DATA_HOST}/v2/stocks/snapshots?{q}")


def get_orders(status="all", limit=20):
    q = urllib.parse.urlencode({"status": status, "limit": limit, "direction": "desc"})
    return _request("GET", f"{TRADE_HOST}/v2/orders?{q}")


def place_order(symbol, side, notional, order_type="market", limit_price=None):
    symbol = symbol.upper()
    account = get_account()
    positions = get_positions()

    try:
        warnings = guardrails.check_order(
            symbol=symbol,
            side=side,
            notional=float(notional),
            order_type=order_type,
            account=account,
            positions=positions,
        )
    except guardrails.Rejected as e:
        print(json.dumps({"status": "REJECTED", "symbol": symbol, "reason": str(e)}, indent=2))
        sys.exit(2)

    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)

    held_before = {p["symbol"].upper() for p in positions}

    payload = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "time_in_force": "day",
        "notional": str(round(float(notional), 2)),
    }
    if order_type == "limit":
        if limit_price is None:
            sys.exit("ERROR: limit orders require --limit-price")
        payload["limit_price"] = str(limit_price)
        # Alpaca requires qty (not notional) for limit orders.
        snap = get_snapshots([symbol]).get("snapshots", {}).get(symbol, {})
        price = float(limit_price)
        payload.pop("notional")
        payload["qty"] = str(max(1, int(float(notional) / price)))
        del snap

    result = _request("POST", f"{TRADE_HOST}/v2/orders", payload)

    if side.lower() == "buy" and symbol not in held_before:
        guardrails.record_new_position()

    print(json.dumps({
        "status": "SUBMITTED",
        "mode": "PAPER" if PAPER else "LIVE",
        "id": result.get("id"),
        "symbol": result.get("symbol"),
        "side": result.get("side"),
        "notional": result.get("notional"),
        "qty": result.get("qty"),
        "type": result.get("order_type"),
        "warnings": warnings,
    }, indent=2))
    return result


def protect(symbol, trail_percent):
    """
    Place a broker-side trailing stop on an existing long.

    This is the only order that survives while every routine is asleep.
    It can only ever reduce exposure, so it bypasses the buy-side limits,
    but it still requires an open position.
    """
    symbol = symbol.upper()
    positions = {p["symbol"].upper(): p for p in get_positions()}
    if symbol not in positions:
        sys.exit(f"ERROR: no open position in {symbol}, nothing to protect")

    qty = abs(float(positions[symbol]["qty"]))
    if qty < 1:
        sys.exit(f"ERROR: {symbol} is a fractional position ({qty}); Alpaca "
                 "does not accept trailing stops on fractional shares")

    result = _request("POST", f"{TRADE_HOST}/v2/orders", {
        "symbol": symbol,
        "side": "sell",
        "type": "trailing_stop",
        "time_in_force": "gtc",
        "qty": str(int(qty)),
        "trail_percent": str(trail_percent),
    })
    print(json.dumps({
        "status": "PROTECTED",
        "symbol": symbol,
        "qty": int(qty),
        "trail_percent": trail_percent,
        "order_id": result.get("id"),
    }, indent=2))
    return result


def close_position(symbol):
    symbol = symbol.upper()
    positions = {p["symbol"].upper() for p in get_positions()}
    if symbol not in positions:
        sys.exit(f"ERROR: no open position in {symbol}")
    result = _request("DELETE", f"{TRADE_HOST}/v2/positions/{symbol}")
    print(json.dumps({"status": "CLOSING", "symbol": symbol, "order_id": result.get("id")}, indent=2))
    return result


def summarize_account():
    a = get_account()
    equity = float(a["equity"])
    last = float(a.get("last_equity") or equity)
    return {
        "mode": "PAPER" if PAPER else "LIVE",
        "equity": round(equity, 2),
        "cash": round(float(a["cash"]), 2),
        "day_change": round(equity - last, 2),
        "day_change_pct": round((equity - last) / last * 100, 2) if last else 0.0,
        "buying_power": round(float(a["buying_power"]), 2),
        "trading_blocked": a.get("trading_blocked"),
        "new_positions_this_week": guardrails.new_positions_this_week(),
    }


def summarize_positions():
    out = []
    for p in get_positions():
        out.append({
            "symbol": p["symbol"],
            "qty": p["qty"],
            "avg_entry": round(float(p["avg_entry_price"]), 2),
            "current": round(float(p["current_price"]), 2),
            "market_value": round(float(p["market_value"]), 2),
            "unrealized_pl": round(float(p["unrealized_pl"]), 2),
            "unrealized_pl_pct": round(float(p["unrealized_plpc"]) * 100, 2),
        })
    return sorted(out, key=lambda x: x["unrealized_pl_pct"])


def main():
    ap = argparse.ArgumentParser(description="Alpaca client with enforced risk limits")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("account")
    sub.add_parser("positions")
    sub.add_parser("clock")

    q = sub.add_parser("quote")
    q.add_argument("symbols", nargs="+")

    o = sub.add_parser("orders")
    o.add_argument("--status", default="all")
    o.add_argument("--limit", type=int, default=20)

    for side in ("buy", "sell"):
        s = sub.add_parser(side)
        s.add_argument("symbol")
        s.add_argument("--notional", type=float, required=True)
        s.add_argument("--type", dest="order_type", default="market")
        s.add_argument("--limit-price", type=float, default=None)

    c = sub.add_parser("close")
    c.add_argument("symbol")

    p = sub.add_parser("protect")
    p.add_argument("symbol")
    p.add_argument("--trail-percent", type=float, default=10.0)

    args = ap.parse_args()

    if args.cmd == "account":
        print(json.dumps(summarize_account(), indent=2))
    elif args.cmd == "positions":
        print(json.dumps(summarize_positions(), indent=2))
    elif args.cmd == "clock":
        print(json.dumps(get_clock(), indent=2))
    elif args.cmd == "quote":
        snaps = get_snapshots(args.symbols).get("snapshots", {})
        out = {}
        for sym, s in snaps.items():
            bar = s.get("dailyBar") or {}
            prev = s.get("prevDailyBar") or {}
            close, prev_close = bar.get("c"), prev.get("c")
            out[sym] = {
                "last": close,
                "prev_close": prev_close,
                "change_pct": round((close - prev_close) / prev_close * 100, 2)
                if close and prev_close else None,
                "volume": bar.get("v"),
            }
        print(json.dumps(out, indent=2))
    elif args.cmd == "orders":
        print(json.dumps(get_orders(args.status, args.limit), indent=2, default=str))
    elif args.cmd in ("buy", "sell"):
        place_order(args.symbol, args.cmd, args.notional, args.order_type, args.limit_price)
    elif args.cmd == "close":
        close_position(args.symbol)
    elif args.cmd == "protect":
        protect(args.symbol, args.trail_percent)


if __name__ == "__main__":
    main()
