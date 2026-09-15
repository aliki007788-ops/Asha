# ==========================================
# seo_content.py
# Version: 1.0.0
# Last Change: Full SeoContentAgent implementation (2026-09-14)
# Impact Set (v1.0.0): base.py
# Caller Audit: orchestrator via registry
# Adapter Audit: N/A
# ==========================================

from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent


class SeoContentAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="seo_content",
            name="SEO Content",
            version="1.0.0",
            description="تولید محتوای بهینه‌شده برای موتورهای جستجو",
        )

    async def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        topic = payload.get("topic", "محصول")
        keywords = payload.get("keywords", [])
        tone = payload.get("tone", "حرفه‌ای")
        word_count = int(payload.get("word_count", 300))

        title = f"{topic} | راهنمای کامل و خرید"
        meta = f"همه چیز درباره {topic}. نکات مهم، مزایا و راهنمای انتخاب."
        body = self._generate_body(topic, keywords, tone, word_count)

        return {
            "agent_id": self.agent_id,
            "status": "success",
            "title": title,
            "meta_description": meta,
            "keywords": keywords or [topic],
            "body": body,
            "word_count_estimate": len(body.split()),
        }

    def _generate_body(self, topic: str, keywords: list, tone: str, word_count: int) -> str:
        kw_text = "، ".join(keywords) if keywords else topic
        paragraphs = [
            f"در این مطلب به بررسی جامع {topic} می‌پردازیم.",
            f"کلمات کلیدی مرتبط: {kw_text}.",
            f"با لحن {tone}، نکات کاربردی برای انتخاب و استفاده از {topic} ارائه شده است.",
            f"اگر به دنبال بهترین گزینه در حوزه {topic} هستید، این راهنما به شما کمک می‌کند.",
        ]
        body = "\n\n".join(paragraphs)
        while len(body.split()) < word_count:
            body += f"\n\nهمچنین توجه به کیفیت و پشتیبانی پس از فروش در انتخاب {topic} اهمیت بالایی دارد."
        return body
