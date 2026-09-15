# ==========================================
# base.py
# Version: 0.1.0
# Last Change: Initial BaseAgent abstract class (2026-09-14)
# Impact Set (v0.1.0): registry.py, all future agents
# Caller Audit: N/A (bootstrap)
# Adapter Audit: N/A
# ==========================================

"""
ASHA Base Agent

کلاس پایه برای تمام ایجنت‌های آشا.
هر ایجنت باید این کلاس را ارث‌بری کند و متد execute را پیاده‌سازی کند.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseAgent(ABC):
    """کلاس پایه ایجنت‌های آشا."""

    def __init__(
        self,
        agent_id: str,
        name: str,
        version: str = "0.1.0",
        description: str = "",
    ) -> None:
        self.agent_id = agent_id
        self.name = name
        self.version = version
        self.description = description

    @abstractmethod
    async def execute(self, payload: dict[str, Any]) -> Any:
        """
        اجرای وظیفه اصلی ایجنت.

        Args:
            payload: داده‌های ورودی وظیفه

        Returns:
            نتیجه اجرای وظیفه
        """
        ...

    async def health_check(self) -> dict[str, Any]:
        """بررسی سلامت ایجنت."""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "version": self.version,
            "status": "healthy",
        }

    def __repr__(self) -> str:
        return f"<Agent {self.agent_id} v{self.version}>"
