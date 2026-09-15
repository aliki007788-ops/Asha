# ==========================================
# test_state.py
# Version: 1.0.0
# ==========================================

from src.core.state import SystemState, TaskStatus


def test_task_lifecycle():
    state = SystemState()
    state.set_status("running")
    assert state.status == "running"

    tid = state.create_task("sales_closer", {"x": 1})
    task = state.get_task(tid)
    assert task is not None
    assert task.status == TaskStatus.PENDING

    state.mark_task_running(tid)
    assert state.get_task(tid).status == TaskStatus.RUNNING

    state.mark_task_completed(tid, result={"ok": True})
    assert state.get_task(tid).status == TaskStatus.COMPLETED
    assert state.get_task(tid).result == {"ok": True}


def test_task_failed_and_list():
    state = SystemState()
    tid = state.create_task("support", {})
    state.mark_task_failed(tid, reason="timeout")
    assert state.get_task(tid).status == TaskStatus.FAILED
    assert state.get_task(tid).error == "timeout"
    assert len(state.list_tasks(status=TaskStatus.FAILED)) == 1
