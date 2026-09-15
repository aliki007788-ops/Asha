# ==========================================
# test_orchestrator.py
# Version: 1.0.0
# ==========================================

import asyncio
import pytest
from src.bootstrap import create_system
from src.core.state import TaskStatus


@pytest.mark.asyncio
async def test_full_task_flow():
    sys = create_system()
    orch = sys["orchestrator"]
    await orch.start()
    assert orch.is_running

    task_id = await orch.submit_task(
        agent_id="sales_closer",
        payload={
            "conversation": [{"text": "می‌خرم"}],
            "customer_name": "تست",
            "product": "محصول",
        },
    )
    assert task_id

    # اجازه پردازش رویداد
    await asyncio.sleep(0.05)

    task = sys["state"].get_task(task_id)
    assert task is not None
    assert task.status in (TaskStatus.COMPLETED, TaskStatus.RUNNING, TaskStatus.PENDING)
    if task.status == TaskStatus.COMPLETED:
        assert task.result is not None
        assert task.result["status"] == "success"

    await orch.stop()
    assert not orch.is_running


@pytest.mark.asyncio
async def test_unknown_agent_raises():
    sys = create_system()
    orch = sys["orchestrator"]
    await orch.start()
    with pytest.raises(ValueError):
        await orch.submit_task("nonexistent_agent", {})
    await orch.stop()


@pytest.mark.asyncio
async def test_all_agents_via_orchestrator():
    sys = create_system()
    orch = sys["orchestrator"]
    await orch.start()
    agent_ids = sys["registry"].list_agents()
    assert len(agent_ids) == 15

    for agent_id in agent_ids:
        tid = await orch.submit_task(agent_id, {})
        assert tid
    await asyncio.sleep(0.1)
    completed = sys["state"].list_tasks(status=TaskStatus.COMPLETED)
    assert len(completed) >= 10  # اکثر باید تمام شده باشند
    await orch.stop()
