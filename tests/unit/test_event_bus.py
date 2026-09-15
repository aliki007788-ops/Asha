# ==========================================
# test_event_bus.py
# Version: 1.0.0
# ==========================================

import pytest
from src.core.event_bus import EventBus


@pytest.mark.asyncio
async def test_publish_subscribe():
    bus = EventBus()
    received = []

    async def handler(event):
        received.append(event)

    await bus.subscribe("test.topic", handler)
    await bus.publish("test.topic", {"msg": "hello"})
    assert len(received) == 1
    assert received[0]["msg"] == "hello"

    await bus.unsubscribe_all()
    await bus.publish("test.topic", {"msg": "ignored"})
    assert len(received) == 1
