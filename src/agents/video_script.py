# ==========================================
# video_script.py
# Version: 1.0.0
# Last Change: Full VideoScriptAgent implementation (2026-09-14)
# Impact Set (v1.0.0): base.py
# Caller Audit: orchestrator via registry
# Adapter Audit: N/A
# ==========================================

from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent


class VideoScriptAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="video_script",
            name="Video Script",
            version="1.0.0",
            description="نوشتن اسکریپت ویدیو تبلیغاتی و آموزشی",
        )

    async def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        product = payload.get("product", "محصول")
        duration_sec = int(payload.get("duration_sec", 60))
        style = payload.get("style", "promotional")
        cta = payload.get("cta", "همین حالا سفارش دهید")

        scenes = self._build_scenes(product, duration_sec, style, cta)

        return {
            "agent_id": self.agent_id,
            "status": "success",
            "product": product,
            "duration_sec": duration_sec,
            "style": style,
            "scenes": scenes,
            "full_script": "\n\n".join(
                f"[صحنه {s['scene']}] ({s['duration']}ثانیه)\n{s['narration']}" for s in scenes
            ),
        }

    def _build_scenes(self, product: str, duration: int, style: str, cta: str) -> list[dict]:
        if style == "educational":
            return [
                {"scene": 1, "duration": 10, "narration": f"آیا می‌دانید {product} چه کمکی به شما می‌کند؟"},
                {"scene": 2, "duration": duration - 25, "narration": f"در این ویدیو سه نکته کلیدی درباره {product} را بررسی می‌کنیم."},
                {"scene": 3, "duration": 15, "narration": f"{cta}. لینک در توضیحات."},
            ]
        return [
            {"scene": 1, "duration": 8, "narration": f"معرفی {product} — راه‌حل جدید شما."},
            {"scene": 2, "duration": duration - 20, "narration": f"مزایای {product}: کیفیت، قیمت مناسب و پشتیبانی."},
            {"scene": 3, "duration": 12, "narration": f"{cta}!"},
        ]
