# ==========================================
# analytics.py
# Version: 1.0.0
# Last Change: Full Analytics module (2026-09-14)
# Impact Set (v1.0.0): support layer
# Caller Audit: N/A
# Adapter Audit: N/A
# ==========================================

from __future__ import annotations

from collections import defaultdict
from typing import Any


class Analytics:
    def __init__(self) -> None:
        self._counters: dict[str, int] = defaultdict(int)
        self._events: list[dict[str, Any]] = []

    def track(self, event_name: str, properties: dict[str, Any] | None = None) -> None:
        self._counters[event_name] += 1
        self._events.append({"event": event_name, "properties": properties or {}})

    def count(self, event_name: str) -> int:
        return self._counters.get(event_name, 0)

    def summary(self) -> dict[str, Any]:
        return {
            "counters": dict(self._counters),
            "total_events": len(self._events),
        }
