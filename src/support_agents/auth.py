# ==========================================
# auth.py
# Version: 1.0.0
# Last Change: Simple Auth helper (2026-09-14)
# Impact Set (v1.0.0): support layer, API
# Caller Audit: API middleware
# Adapter Audit: N/A
# ==========================================

from __future__ import annotations

import hashlib
import secrets
from typing import Optional


class AuthService:
    def __init__(self) -> None:
        self._tokens: dict[str, str] = {}  # token -> user_id

    def create_token(self, user_id: str) -> str:
        token = secrets.token_urlsafe(32)
        self._tokens[token] = user_id
        return token

    def validate_token(self, token: str) -> Optional[str]:
        return self._tokens.get(token)

    def revoke_token(self, token: str) -> bool:
        if token in self._tokens:
            del self._tokens[token]
            return True
        return False

    @staticmethod
    def hash_password(password: str, salt: str = "asha") -> str:
        return hashlib.sha256(f"{salt}:{password}".encode()).hexdigest()
