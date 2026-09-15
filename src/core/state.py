# ==========================================
# state.py
# Version: 0.1.0
# Last Change: Initial System State manager (2026-09-14)
# Impact Set (v0.1.0): orchestrator.py
# Caller Audit: N/A (bootstrap)
# Adapter Audit: N/A
# ==========================================

"""
ASHA System State

مدیریت وضعیت کلی سیستم و وظایف در حال اجرا.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskRecord:
    task_id: str
    agent_id: str
    payload: dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class SystemState:
    """مدیریت وضعیت سیستم و وظایف."""

    def __init__(self) -> None:
        self._status: str = "initialized"
        self._tasks: dict[str, TaskRecord] = {}

    def set_status(self, status: str) -> None:
        self._status = status

    @property
    def status(self) -> str:
        return self._status

    def create_task(self, agent_id: str, payload: dict[str, Any]) -> str:
        """ایجاد وظیفه جدید و بازگرداندن task_id."""
        task_id = str(uuid.uuid4())
        record = TaskRecord(
            task_id=task_id,
            agent_id=agent_id,
            payload=payload,
        )
        self._tasks[task_id] = record
        return task_id

    def mark_task_running(self, task_id: str) -> None:
        task = self._tasks.get(task_id)
        if task:
            task.status = TaskStatus.RUNNING
            task.updated_at = datetime.now(timezone.utc)

    def mark_task_completed(self, task_id: str, result: Any = None) -> None:
        task = self._tasks.get(task_id)
        if task:
            task.status = TaskStatus.COMPLETED
            task.result = result
            task.updated_at = datetime.now(timezone.utc)

    def mark_task_failed(self, task_id: str, reason: str = "") -> None:
        task = self._tasks.get(task_id)
        if task:
            task.status = TaskStatus.FAILED
            task.error = reason
            task.updated_at = datetime.now(timezone.utc)

    def get_task(self, task_id: str) -> Optional[TaskRecord]:
        return self._tasks.get(task_id)

    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        agent_id: Optional[str] = None,
    ) -> list[TaskRecord]:
        tasks = list(self._tasks.values())
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        if agent_id is not None:
            tasks = [t for t in tasks if t.agent_id == agent_id]
        return tasks

    def clear_completed(self) -> int:
        """پاک کردن وظایف تکمیل‌شده. تعداد حذف‌شده را برمی‌گرداند."""
        to_remove = [
            tid for tid, t in self._tasks.items()
            if t.status in (TaskStatus.COMPLETED, TaskStatus.CANCELLED)
        ]
        for tid in to_remove:
            del self._tasks[tid]
        return len(to_remove)
