# ==========================================
# registry.py
# Version: 0.1.0
# Last Change: Initial Agent Registry with Service Discovery (2026-09-14)
# Impact Set (v0.1.0): orchestrator.py, agents/base.py
# Caller Audit: N/A (bootstrap)
# Adapter Audit: N/A
# ==========================================

"""
ASHA Agent Registry

ثبت و کشف ایجنت‌ها (Service Discovery).
هر ایجنت جدید بدون تغییر در هسته قابل ثبت است.
"""

from __future__ import annotations

import logging
from typing import Optional

from src.agents.base import BaseAgent

logger = logging.getLogger("asha.core.registry")


class AgentRegistry:
    """ثبت‌کننده و کشف‌کننده ایجنت‌های آشا."""

    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        """
        ثبت یک ایجنت جدید.

        Args:
            agent: نمونه از BaseAgent یا زیرکلاس آن

        Raises:
            ValueError: اگر agent_id تکراری باشد
        """
        agent_id = agent.agent_id
        if agent_id in self._agents:
            raise ValueError(f"Agent '{agent_id}' is already registered")

        self._agents[agent_id] = agent
        logger.info("Registered agent: %s (version=%s)", agent_id, agent.version)

    def unregister(self, agent_id: str) -> None:
        """حذف ایجنت از رجیستری."""
        if agent_id not in self._agents:
            logger.warning("Attempted to unregister unknown agent: %s", agent_id)
            return
        del self._agents[agent_id]
        logger.info("Unregistered agent: %s", agent_id)

    def get(self, agent_id: str) -> Optional[BaseAgent]:
        """دریافت ایجنت بر اساس شناسه."""
        return self._agents.get(agent_id)

    def list_agents(self) -> list[str]:
        """فهرست تمام ایجنت‌های ثبت‌شده."""
        return list(self._agents.keys())

    def has(self, agent_id: str) -> bool:
        """بررسی وجود ایجنت."""
        return agent_id in self._agents

    def clear(self) -> None:
        """پاک کردن تمام ایجنت‌ها (فقط برای تست)."""
        self._agents.clear()
        logger.info("Registry cleared")

    def __len__(self) -> int:
        return len(self._agents)

    def __contains__(self, agent_id: str) -> bool:
        return agent_id in self._agents
