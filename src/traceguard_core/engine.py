"""Fail-closed action-name allowlist used by the MCP decision endpoint.

This module deliberately does not execute tools and does not validate argument-level
policy. The caller remains responsible for enforcing an ALLOW decision.
"""
from __future__ import annotations

import json
import os
from collections.abc import Iterable, Mapping
from typing import Any

ENV_ALLOWED_ACTIONS = "TRACEGUARD_ALLOWED_ACTIONS"


def parse_allowed_actions(value: str | None = None) -> frozenset[str]:
    """Parse a JSON list of exact action names; absent configuration denies all."""
    raw = os.environ.get(ENV_ALLOWED_ACTIONS) if value is None else value
    if raw is None or raw == "":
        return frozenset()
    try:
        parsed = json.loads(raw)
    except (TypeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{ENV_ALLOWED_ACTIONS} must be a JSON array of strings") from exc
    if type(parsed) is not list or any(type(item) is not str or not item for item in parsed):
        raise ValueError(f"{ENV_ALLOWED_ACTIONS} must be a JSON array of non-empty strings")
    return frozenset(parsed)


def evaluate_call(
    target_tool: Any,
    arguments: Any,
    allowed_actions: Iterable[str] | None = None,
) -> bool:
    """Return whether an exact tool name is allow-listed; malformed inputs deny.

    Arguments are checked for a JSON-object shape only. No argument-level policy
    is implied. An omitted allowlist uses TRACEGUARD_ALLOWED_ACTIONS and defaults
    to an empty set, so an unconfigured process denies every action.
    """
    if type(target_tool) is not str or not target_tool.strip():
        return False
    if type(arguments) is not dict or any(type(key) is not str for key in arguments):
        return False
    if allowed_actions is None:
        try:
            allowed = parse_allowed_actions()
        except ValueError:
            return False
    else:
        if isinstance(allowed_actions, (str, bytes, Mapping)):
            return False
        try:
            allowed = frozenset(allowed_actions)
        except TypeError:
            return False
        if any(type(item) is not str or not item for item in allowed):
            return False
    return target_tool in allowed
