# ==========================================
# content_calendar.py
# Version: 1.0.0
# Last Change: Full ContentCalendarAgent implementation (2026-09-14)
# Impact Set (v1.0.0): base.py
# Caller Audit: orchestrator via registry
# Adapter Audit: N/A
# ==========================================

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from src.agents.base import BaseAgent


class ContentCalendarAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="content_calendar",
            name="Content Calendar",
            version="1.0.0",
            description="برنامه‌ریزی تقویم محتوا",
        )

    async def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        start = payload.get("start_date")
        days = int(payload.get("days", 7))
        themes = payload.get("themes", ["معرفی محصول", "آموزشی", "نظر مشتری", "پشت صحنه", "پیشنهاد ویژه"])
        channels = payload.get("channels", ["instagram", "eitaa"])

        try:
            start_date = date.fromisoformat(start) if start else date.today()
        except ValueError:
            start_date = date.today()

        calendar = []
        for i in range(days):
            d = start_date + timedelta(days=i)
            theme = themes[i % len(themes)]
            channel = channels[i % len(channels)]
            calendar.append({
                "date": d.isoformat(),
                "theme": theme,
                "channel": channel,
                "title": f"{theme} — روز {i + 1}",
                "status": "planned",
            })

        return {
            "agent_id": self.agent_id,
            "status": "success",
            "start_date": start_date.isoformat(),
            "days": days,
            "calendar": calendar,
        }
