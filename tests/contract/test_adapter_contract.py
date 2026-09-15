# ==========================================
# test_adapter_contract.py
# Version: 1.0.0
# ==========================================

"""Contract tests: همه Adapterها باید اینترفیس BaseAdapter را رعایت کنند."""

import pytest
from src.adapters import (
    EitaaAdapter, BaleAdapter, RubikaAdapter, DivarAdapter,
    TorobAdapter, EmallsAdapter, TelegramBridge, InstagramBridge,
)
from src.adapters.base import BaseAdapter


ALL = [
    EitaaAdapter, BaleAdapter, RubikaAdapter, DivarAdapter,
    TorobAdapter, EmallsAdapter, TelegramBridge, InstagramBridge,
]


@pytest.mark.parametrize("cls", ALL, ids=lambda c: c.__name__)
def test_is_base_adapter(cls):
    inst = cls()
    assert isinstance(inst, BaseAdapter)
    assert hasattr(inst, "send_message")
    assert hasattr(inst, "receive_messages")
    assert hasattr(inst, "send_file")
    assert hasattr(inst, "health_check")


@pytest.mark.asyncio
@pytest.mark.parametrize("cls", ALL, ids=lambda c: c.__name__)
async def test_send_receive_contract(cls):
    inst = cls()
    assert await inst.send_message("id", "text") is True
    assert isinstance(await inst.receive_messages(), list)
    health = await inst.health_check()
    assert "platform" in health
    assert "status" in health
