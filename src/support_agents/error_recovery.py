# ==========================================
# error_recovery.py
# Version: 1.0.0
# Last Change: Error recovery helpers (2026-09-14)
# Impact Set (v1.0.0): support layer
# Caller Audit: orchestrator
# Adapter Audit: N/A
# ==========================================

from __future__ import annotations

import asyncio
from typing import Callable, Awaitable, TypeVar, Any

T = TypeVar("T")


async def retry_async(
    fn: Callable[[], Awaitable[T]],
    max_attempts: int = 3,
    delay_sec: float = 0.1,
) -> T:
    last_exc: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return await fn()
        except Exception as exc:
            last_exc = exc
            if attempt < max_attempts:
                await asyncio.sleep(delay_sec * attempt)
    assert last_exc is not None
    raise last_exc
