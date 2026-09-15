# ==========================================
# orchestrator.py
# Version: 0.1.0
# Last Change: Initial skeleton for ASHA Orchestrator (2026-09-14)
# Impact Set (v0.1.0): registry.py, event_bus.py, state.py, config.py
# Caller Audit: N/A (bootstrap)
# Adapter Audit: N/A
# ==========================================

"""
ASHA Core Orchestrator

مسئول هماهنگی بین ایجنت‌ها، تخصیص وظیفه و تصمیم‌گیری سطح بالا.
هر ایجنت از طریق Registry کشف و از طریق Event Bus ارتباط برقرار می‌کند.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Optional

from src.core.registry import AgentRegistry
from src.core.event_bus import EventBus
from src.core.state import SystemState
from src.core.config import AshaConfig

logger = logging.getLogger("asha.core.orchestrator")


class Orchestrator:
    """هماهنگ‌کننده اصلی سیستم آشا."""

    def __init__(
        self,
        registry: AgentRegistry,
        event_bus: EventBus,
        state: SystemState,
        config: AshaConfig,
    ) -> None:
        self.registry = registry
        self.event_bus = event_bus
        self.state = state
        self.config = config
        self._running = False

    async def start(self) -> None:
        """راه‌اندازی Orchestrator و شروع گوش دادن به Event Bus."""
        if self._running:
            logger.warning("Orchestrator already running")
            return

        logger.info("Starting ASHA Orchestrator...")
        self._running = True
        self.state.set_status("running")

        # ثبت handler برای رویدادهای سیستمی
        await self.event_bus.subscribe("system.task", self._handle_task)
        await self.event_bus.subscribe("system.shutdown", self._handle_shutdown)

        logger.info("ASHA Orchestrator started successfully")

    async def stop(self) -> None:
        """توقف امن Orchestrator."""
        if not self._running:
            return

        logger.info("Stopping ASHA Orchestrator...")
        self._running = False
        self.state.set_status("stopped")
        await self.event_bus.unsubscribe_all()
        logger.info("ASHA Orchestrator stopped")

    async def submit_task(
        self,
        agent_id: str,
        payload: dict[str, Any],
        priority: int = 5,
    ) -> str:
        """
        ارسال وظیفه به یک ایجنت خاص از طریق Event Bus.

        Returns:
            task_id: شناسه یکتای وظیفه
        """
        agent = self.registry.get(agent_id)
        if agent is None:
            raise ValueError(f"Agent '{agent_id}' not found in registry")

        task_id = self.state.create_task(agent_id=agent_id, payload=payload)
        event = {
            "type": "system.task",
            "task_id": task_id,
            "agent_id": agent_id,
            "payload": payload,
            "priority": priority,
        }
        await self.event_bus.publish("system.task", event)
        logger.info("Task %s submitted to agent %s", task_id, agent_id)
        return task_id

    async def _handle_task(self, event: dict[str, Any]) -> None:
        """پردازش رویداد وظیفه و ارجاع به ایجنت مربوطه."""
        agent_id = event.get("agent_id")
        task_id = event.get("task_id")
        payload = event.get("payload", {})

        agent = self.registry.get(agent_id)
        if agent is None:
            logger.error("Agent %s not found for task %s", agent_id, task_id)
            self.state.mark_task_failed(task_id, reason="agent_not_found")
            return

        try:
            self.state.mark_task_running(task_id)
            result = await agent.execute(payload)
            self.state.mark_task_completed(task_id, result=result)
            logger.info("Task %s completed by agent %s", task_id, agent_id)
        except Exception as exc:
            logger.exception("Task %s failed on agent %s: %s", task_id, agent_id, exc)
            self.state.mark_task_failed(task_id, reason=str(exc))

    async def _handle_shutdown(self, event: dict[str, Any]) -> None:
        """مدیریت درخواست خاموشی سیستم."""
        logger.info("Shutdown event received: %s", event)
        await self.stop()

    @property
    def is_running(self) -> bool:
        return self._running
