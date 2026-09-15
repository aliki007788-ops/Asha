# ==========================================
# recruitment.py
# Version: 1.0.0
# Last Change: Full RecruitmentAgent implementation (2026-09-14)
# Impact Set (v1.0.0): base.py
# Caller Audit: orchestrator via registry
# Adapter Audit: N/A
# ==========================================

from __future__ import annotations

from typing import Any

from src.agents.base import BaseAgent


class RecruitmentAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            agent_id="recruitment",
            name="Recruitment",
            version="1.0.0",
            description="جذب نیرو و غربالگری اولیه رزومه",
        )

    async def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        job_title = payload.get("job_title", "موقعیت شغلی")
        required_skills = [s.lower() for s in payload.get("required_skills", [])]
        candidate = payload.get("candidate", {})
        resume_text = str(payload.get("resume_text", "")).lower()

        candidate_skills = [s.lower() for s in candidate.get("skills", [])]
        matched = [s for s in required_skills if s in candidate_skills or s in resume_text]
        score = (len(matched) / len(required_skills)) if required_skills else 0.5
        decision = "interview" if score >= 0.6 else "reject" if score < 0.3 else "review"

        return {
            "agent_id": self.agent_id,
            "status": "success",
            "job_title": job_title,
            "candidate_name": candidate.get("name", "نامشخص"),
            "matched_skills": matched,
            "score": round(score, 2),
            "decision": decision,
            "message": self._message(decision, candidate.get("name", "داوطلب"), job_title),
        }

    def _message(self, decision: str, name: str, job: str) -> str:
        if decision == "interview":
            return f"{name} عزیز، رزومه شما برای موقعیت {job} بررسی شد. لطفاً برای مصاحبه هماهنگ کنیم."
        if decision == "reject":
            return f"{name} عزیز، متأسفانه در این مرحله با پروفایل شما پیش نرفتیم. موفق باشید."
        return f"{name} عزیز، رزومه شما در حال بررسی تکمیلی برای {job} است."
