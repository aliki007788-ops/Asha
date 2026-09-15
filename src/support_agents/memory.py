# ==========================================
# memory.py
# Version: 1.0.0
# Last Change: Full Memory module (2026-09-14)
# Impact Set (v1.0.0): support layer
# Caller Audit: agents / orchestrator
# Adapter Audit: N/A
# ==========================================

from __future__ import annotations

from typing import Any, Optional


class MemoryStore:
    """حافظه ساده کلید-مقدار برای ایجنت‌ها (in-memory)."""

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._store.get(key, default)

    def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False

    def clear(self) -> None:
        self._store.clear()

    def keys(self) -> list[str]:
        return list(self._store.keys())
