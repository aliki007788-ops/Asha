# ==========================================
# sequencer.py
# Version: 1.0.0
# Last Change: Full SequencerAgent implementation (2026-09-14)
# Impact Set (v1.0.0): base.py
# Caller Audit: orchestrator via registry
# Adapter Audit: N/A
# ==========================================

"""
Sequencer Agent

ایجنت توالی پیام — طراحی و مدیریت sequenceهای چندمرحله‌ای فروش.
"""

from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent


class SequencerAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="sequencer",
            name="Sequencer",
            version="1.0.0",
            description="طراحی و مدیریت توالی پیام‌های فروش",
        )

    async def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        sequence_name = payload.get("sequence_name", "default_nurture")
        lead_stage = payload.get("lead_stage", "new")
        days_since_contact = int(payload.get("days_since_contact", 0))
        product = payload.get("product", "محصول")

        steps = self._build_sequence(sequence_name, product)
        current_step = self._resolve_current_step(steps, lead_stage, days_since_contact)

        return {
            "agent_id": self.agent_id,
            "status": "success",
            "sequence_name": sequence_name,
            "total_steps": len(steps),
            "current_step": current_step,
            "steps": steps,
            "next_message": current_step.get("message") if current_step else None,
            "next_delay_hours": current_step.get("delay_hours") if current_step else None,
        }

    def _build_sequence(self, name: str, product: str) -> list[dict[str, Any]]:
        if name == "aggressive_close":
            return [
                {"step": 1, "delay_hours": 0, "message": f"سلام! در مورد {product} سوالی دارید؟"},
                {"step": 2, "delay_hours": 24, "message": f"هنوز فرصت دارید از پیشنهاد ویژه {product} استفاده کنید."},
                {"step": 3, "delay_hours": 48, "message": "آخرین فرصت — تخفیف تا پایان امروز معتبر است."},
            ]
        return [
            {"step": 1, "delay_hours": 0, "message": f"سلام، ممنون از علاقه‌تون به {product}."},
            {"step": 2, "delay_hours": 48, "message": f"چند نکته مهم در مورد {product} که شاید براتون مفید باشه."},
            {"step": 3, "delay_hours": 96, "message": "اگر آماده‌اید، می‌تونیم سفارشتون رو نهایی کنیم."},
            {"step": 4, "delay_hours": 168, "message": "فقط یک یادآوری دوستانه — هنوز در خدمتم."},
        ]

    def _resolve_current_step(
        self,
        steps: list[dict[str, Any]],
        lead_stage: str,
        days_since_contact: int,
    ) -> dict[str, Any] | None:
        if lead_stage == "closed" or lead_stage == "lost":
            return None
        hours = days_since_contact * 24
        eligible = [s for s in steps if s["delay_hours"] <= hours]
        return eligible[-1] if eligible else steps[0]
