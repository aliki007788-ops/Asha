# ==========================================
# support.py
# Version: 1.0.0
# Last Change: Full SupportAgent implementation (2026-09-14)
# Impact Set (v1.0.0): base.py
# Caller Audit: orchestrator via registry
# Adapter Audit: N/A
# ==========================================

"""
Support Agent

ایجنت پشتیبانی مشتری — پاسخ به سوالات متداول و ارجاع.
"""

from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent


class SupportAgent(BaseAgent):
    FAQ = {
        "ارسال": "سفارش‌ها معمولاً طی ۲ تا ۵ روز کاری ارسال می‌شوند.",
        "مرجوعی": "تا ۷ روز پس از دریافت امکان مرجوعی با شرایط سالم بودن کالا وجود دارد.",
        "پرداخت": "پرداخت آنلاین، کارت به کارت و در محل (برای برخی شهرها) پشتیبانی می‌شود.",
        "گارانتی": "تمام محصولات دارای گارانتی اصالت و سلامت فیزیکی هستند.",
        "پیگیری": "با کد پیگیری سفارش می‌توانید وضعیت را از بخش پیگیری سایت ببینید.",
    }

    def __init__(self) -> None:
        super().__init__(
            agent_id="support",
            name="Support",
            version="1.0.0",
            description="پشتیبانی مشتری و پاسخ به FAQ",
        )

    async def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        question = str(payload.get("question", "")).strip()
        customer_name = payload.get("customer_name", "مشتری")
        order_id = payload.get("order_id")

        answer, category, confidence = self._answer(question)
        needs_human = confidence < 0.5

        return {
            "agent_id": self.agent_id,
            "status": "success",
            "question": question,
            "answer": answer,
            "category": category,
            "confidence": confidence,
            "needs_human": needs_human,
            "order_id": order_id,
            "reply": f"{customer_name} عزیز، {answer}",
        }

    def _answer(self, question: str) -> tuple[str, str, float]:
        q = question.lower()
        for key, answer in self.FAQ.items():
            if key in q:
                return answer, key, 0.9
        if not question:
            return "لطفاً سوال خود را مطرح کنید تا بهتر راهنمایی کنم.", "empty", 0.3
        return (
            "سوال شما ثبت شد. در اسرع وقت همکاران پشتیبانی پاسخ می‌دهند.",
            "unknown",
            0.4,
        )
