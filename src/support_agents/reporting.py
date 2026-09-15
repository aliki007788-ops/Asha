# ==========================================
# reporting.py
# Version: 1.0.0
# Last Change: Reporting helper (2026-09-14)
# Impact Set (v1.0.0): support layer
# Caller Audit: N/A
# Adapter Audit: N/A
# ==========================================

from __future__ import annotations

from typing import Any


class Reporter:
    def __init__(self) -> None:
        self._reports: list[dict[str, Any]] = []

    def add(self, title: str, data: dict[str, Any]) -> dict[str, Any]:
        report = {"title": title, "data": data}
        self._reports.append(report)
        return report

    def list_reports(self) -> list[dict[str, Any]]:
        return list(self._reports)
