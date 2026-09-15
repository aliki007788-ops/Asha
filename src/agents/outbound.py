# ==========================================
# outbound.py
# Version: 1.0.0
# Last Change: Full OutboundAgent implementation (2026-09-14)
# Impact Set (v1.0.0): base.py
# Caller Audit: orchestrator via registry
# Adapter Audit: N/A
# ==========================================

"""
Outbound Agent

ایجنت پیام‌رسانی خروجی — ساخت و ارسال پیام‌های اولیه به لیدها.
"""

from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent


class OutboundAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="outbound",
            name="Outbound",
            version="1.0.0",
            description="پیام‌رسانی خروجی و جذب لید",
        )

    async def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        lead_name = payload.get("lead_name", "دوست عزیز")
        product = payload.get("product", "محصول ما")
        channel = payload.get("channel", "eitaa")
        template = payload.get("template", "intro")
        custom_note = payload.get("custom_note", "")

        message = self._build_message(lead_name, product, template, custom_note)

        return {
            "agent_id": self.agent_id,
            "status": "success",
            "channel": channel,
            "lead_name": lead_name,
            "message": message,
            "template_used": template,
            "ready_to_send": True,
        }

    def _build_message(
        self,
        lead_name: str,
        product: str,
        template: str,
        custom_note: str,
    ) -> str:
        templates = {
            "intro": (
                f"سلام {lead_name} عزیز 👋\n"
                f"من از تیم فروش هستم. می‌خواستم در مورد {product} باهاتون صحبت کنم. "
                f"اگر علاقه‌مندید، خوشحال می‌شم کمک کنم."
            ),
            "followup": (
                f"سلام {lead_name}،\n"
                f"چند روز پیش در مورد {product} پیام داده بودم. "
                f"اگر هنوز سوالی دارید در خدمتم."
            ),
            "value": (
                f"{lead_name} عزیز،\n"
                f"می‌دونستید با {product} می‌تونید فروش‌تون رو افزایش بدید؟ "
                f"بذارید براتون توضیح بدم چطور."
            ),
        }
        base = templates.get(template, templates["intro"])
        if custom_note:
            base = f"{base}\n\n{custom_note}"
        return base
