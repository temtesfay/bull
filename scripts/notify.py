#!/usr/bin/env python3
"""
Send a notification to a webhook. Works with Slack, Discord, ClickUp, or any
endpoint that accepts a JSON POST.

    NOTIFY_WEBHOOK_URL   the endpoint
    NOTIFY_FORMAT        slack | discord | plain   (default: slack)

Usage:
    python3 notify.py "message body" --title "Market close" --urgency normal
    echo "body" | python3 notify.py --title "Weekly review"
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

PREFIX = {"normal": "", "warn": "[WARN] ", "urgent": "[URGENT] "}


def send(title, body, urgency="normal"):
    url = os.environ.get("NOTIFY_WEBHOOK_URL")
    if not url:
        print("NOTIFY_WEBHOOK_URL not set — printing instead:\n", file=sys.stderr)
        print(f"{PREFIX.get(urgency,'')}{title}\n{body}")
        return

    text = f"{PREFIX.get(urgency, '')}*{title}*\n{body}"
    fmt = os.environ.get("NOTIFY_FORMAT", "slack").lower()
    payload = {"content": text} if fmt == "discord" else {"text": text}
    if fmt == "plain":
        payload = {"title": title, "body": body, "urgency": urgency}

    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (compatible; BullBot/1.0)",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print(f"notified ({r.status})")
    except urllib.error.HTTPError as e:
        print(f"ERROR: webhook returned {e.code}: {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERROR: webhook unreachable: {e.reason}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("body", nargs="?", default=None)
    ap.add_argument("--title", default="Bull")
    ap.add_argument("--urgency", default="normal", choices=["normal", "warn", "urgent"])
    a = ap.parse_args()
    send(a.title, a.body if a.body is not None else sys.stdin.read(), a.urgency)
