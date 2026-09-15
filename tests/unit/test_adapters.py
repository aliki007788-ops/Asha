# ==========================================
# test_adapters.py
# Version: 1.0.0
# ==========================================

import pytest
from src.adapters.eitaa_adapter import EitaaAdapter
from src.adapters.bale_adapter import BaleAdapter
from src.adapters.rubika_adapter import RubikaAdapter
from src.adapters.divar_adapter import DivarAdapter
from src.adapters.torob_adapter import TorobAdapter
from src.adapters.emalls_adapter import EmallsAdapter
from src.adapters.telegram_bridge import TelegramBridge
from src.adapters.instagram_bridge import InstagramBridge
from src.adapters.base import Message


ADAPTERS = [
    EitaaAdapter(),
    BaleAdapter(),
    RubikaAdapter(),
    DivarAdapter(),
    TorobAdapter(),
    EmallsAdapter(),
    TelegramBridge(),
    InstagramBridge(),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("adapter", ADAPTERS, ids=lambda a: a.platform_name)
async def test_adapter_contract(adapter):
    ok = await adapter.send_message("chat-1", "سلام تست")
    assert ok is True
    ok_empty = await adapter.send_message("", "")
    assert ok_empty is False

    file_ok = await adapter.send_file("chat-1", "/tmp/test.pdf")
    assert file_ok is True

    msgs = await adapter.receive_messages()
    assert isinstance(msgs, list)

    health = await adapter.health_check()
    assert health["platform"] == adapter.platform_name
    assert health["status"] == "healthy"


@pytest.mark.asyncio
async def test_eitaa_inject_incoming():
    adapter = EitaaAdapter()
    adapter.inject_incoming(Message(chat_id="c1", text="سلام"))
    msgs = await adapter.receive_messages()
    assert len(msgs) == 1
    assert msgs[0].text == "سلام"
    assert await adapter.receive_messages() == []
