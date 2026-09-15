# ==========================================
# queue.py
# Version: 1.0.0
# Last Change: Simple in-memory task queue (2026-09-14)
# Impact Set (v1.0.0): support layer
# Caller Audit: orchestrator
# Adapter Audit: N/A
# ==========================================

from __future__ import annotations

import asyncio
from typing import Any
from collections import deque


class TaskQueue:
    def __init__(self) -> None:
        self._queue: deque[dict[str, Any]] = deque()
        self._lock = asyncio.Lock()

    async def enqueue(self, item: dict[str, Any]) -> None:
        async with self._lock:
            self._queue.append(item)

    async def dequeue(self) -> dict[str, Any] | None:
        async with self._lock:
            if self._queue:
                return self._queue.popleft()
            return None

    def size(self) -> int:
        return len(self._queue)
