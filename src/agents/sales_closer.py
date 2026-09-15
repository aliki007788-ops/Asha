# ==========================================
# sales_closer.py
# Version: 1.0.0
# Last Change: Full SalesCloserAgent implementation (2026-09-14)
# Impact Set (v1.0.0): base.py, registry
# Caller Audit: orchestrator via registry
# Adapter Audit: N/A
# ==========================================

"""
Sales Closer Agent

ایجنت بستن فروش — تحلیل مکالمه، تشخیص قصد خرید و پیشنهاد اقدام بستن.
"""

from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent


class SalesCloserAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="sales_closer",
            name="Sales Closer",
            version="1.0.0",
            description="تحلیل مکالمه و بستن فروش",
        )

    async def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        conversation = payload.get("conversation", [])
        customer_name = payload.get("customer_name", "مشتری")
        product = payload.get("product", "محصول")
        price = payload.get("price")

        intent_score = self._analyze_intent(conversation)
        objections = self._detect_objections(conversation)
        next_action = self._decide_next_action(intent_score, objections)

        closing_message = self._craft_closing_message(
            customer_name=customer_name,
            product=product,
            price=price,
            intent_score=intent_score,
            objections=objections,
        )

        return {
            "agent_id": self.agent_id,
            "status": "success",
            "intent_score": intent_score,
            "objections": objections,
            "next_action": next_action,
            "closing_message": closing_message,
            "recommended_discount": self._suggest_discount(intent_score, objections),
        }

    def _analyze_intent(self, conversation: list) -> float:
        if not conversation:
            return 0.3
        positive_keywords = ["می‌خرم", "قیمت", "موجود", "سفارش", "پرداخت", "بله", "موافقم"]
        text = " ".join(str(m.get("text", m) if isinstance(m, dict) else m) for m in conversation).lower()
        hits = sum(1 for k in positive_keywords if k in text)
        return min(0.95, 0.2 + hits * 0.15)

    def _detect_objections(self, conversation: list) -> list[str]:
        objections = []
        text = " ".join(str(m.get("text", m) if isinstance(m, dict) else m) for m in conversation).lower()
        if "گران" in text or "قیمت بالا" in text:
            objections.append("price")
        if "فکر" in text or "بعداً" in text:
            objections.append("delay")
        if "رقیب" in text or "جای دیگه" in text:
            objections.append("competitor")
        return objections

    def _decide_next_action(self, intent_score: float, objections: list[str]) -> str:
        if intent_score >= 0.7 and not objections:
            return "close_now"
        if "price" in objections:
            return "offer_discount_or_value"
        if "delay" in objections:
            return "create_urgency"
        return "nurture"

    def _craft_closing_message(
        self,
        customer_name: str,
        product: str,
        price: Any,
        intent_score: float,
        objections: list[str],
    ) -> str:
        if intent_score >= 0.7:
            price_part = f" با قیمت {price}" if price else ""
            return (
                f"{customer_name} عزیز، خوشحالم که {product} مورد توجه شماست"
                f"{price_part}. اگر موافقید همین الان سفارشتون رو نهایی کنیم؟"
            )
        if "price" in objections:
            return (
                f"{customer_name} عزیز، می‌فهمم که قیمت براتون مهمه. "
                f"بذارید یک پیشنهاد ویژه براتون آماده کنم تا ارزش واقعی {product} رو ببینید."
            )
        return (
            f"{customer_name} عزیز، اگر سوالی در مورد {product} دارید خوشحال می‌شم پاسخ بدم. "
            "آماده کمک هستم."
        )

    def _suggest_discount(self, intent_score: float, objections: list[str]) -> int | None:
        if "price" in objections and intent_score >= 0.5:
            return 10
        return None
