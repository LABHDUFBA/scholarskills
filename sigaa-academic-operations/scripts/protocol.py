#!/usr/bin/env python3
"""Offline validation for a SIGAA operation request.

This checker never contacts a portal. It validates scope and exposes the approval
and side-effect status that a browser workflow must present to the account holder.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PERSISTENT_ACTIONS = {
    "save", "update", "publish", "submit", "finalize", "approve",
    "homologate", "create", "delete", "grade", "attendance",
    "update_topic", "publish_notice", "submit_proposal",
}
REQUIRED = {"operation", "target", "institution", "term"}


def validate(request: dict) -> list[str]:
    errors = []
    missing = sorted(REQUIRED - request.keys())
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))
    for field in ("operation", "target", "institution", "term"):
        if field in request and not isinstance(request[field], str):
            errors.append(f"{field} must be a string")
        elif field in request and not request[field].strip():
            errors.append(f"{field} must not be empty")
    if "approval" in request and not isinstance(request["approval"], bool):
        errors.append("approval must be boolean when present")
    if "notify_email" in request and not isinstance(request["notify_email"], bool):
        errors.append("notify_email must be boolean when present")
    if request.get("operation") in {"submit_proposal", "submit", "finalize"}:
        if not request.get("call"):
            errors.append("formal submission requires a named call")
        if request.get("approval") is not True:
            errors.append("formal submission requires explicit approval")
    return errors


def summary(request: dict) -> dict:
    errors = validate(request)
    operation = request.get("operation", "")
    persistent = operation in PERSISTENT_ACTIONS or request.get("persistent_action") is True
    side_effects = list(request.get("side_effects", []))
    if request.get("notify_email") is True:
        side_effects.append("notification_email")
    if request.get("operation") in {"submit_proposal", "submit", "finalize"}:
        side_effects.append("formal_submission")
    return {
        "ready": not errors,
        "errors": errors,
        "target": request.get("target"),
        "action": operation,
        "persistent_action": persistent,
        "approval_required": persistent,
        "approval_received": request.get("approval") is True,
        "side_effects": sorted(set(side_effects)),
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} REQUEST.json", file=sys.stderr)
        return 2
    try:
        request = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read request: {exc}", file=sys.stderr)
        return 2
    result = summary(request)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
