# ==========================================
# main.py
# Version: 1.0.0
# Last Change: FastAPI application entrypoint (2026-09-14)
# Impact Set (v1.0.0): routes, bootstrap
# Caller Audit: uvicorn
# Adapter Audit: N/A
# ==========================================

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.bootstrap import create_system

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("asha.api")

system: dict[str, Any] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    global system
    system = create_system()
    await system["orchestrator"].start()
    logger.info("ASHA system started with %d agents", len(system["registry"]))
    yield
    await system["orchestrator"].stop()
    logger.info("ASHA system stopped")


app = FastAPI(
    title="ASHA — Multi-Platform Agent Factory",
    version="1.0.0",
    description="کارخانه ایجنت چندپلتفرمی آشا",
    lifespan=lifespan,
)


class TaskRequest(BaseModel):
    agent_id: str
    payload: dict[str, Any] = Field(default_factory=dict)
    priority: int = 5


class TaskResponse(BaseModel):
    task_id: str
    status: str


@app.get("/health")
async def health():
    orch = system.get("orchestrator")
    return {
        "status": "ok",
        "orchestrator_running": orch.is_running if orch else False,
        "agents": system["registry"].list_agents() if system else [],
        "adapters": list(system["adapters"].keys()) if system else [],
    }


@app.get("/agents")
async def list_agents():
    return {"agents": system["registry"].list_agents()}


@app.post("/tasks", response_model=TaskResponse)
async def submit_task(req: TaskRequest):
    if not system["registry"].has(req.agent_id):
        raise HTTPException(status_code=404, detail=f"Agent '{req.agent_id}' not found")
    task_id = await system["orchestrator"].submit_task(
        agent_id=req.agent_id,
        payload=req.payload,
        priority=req.priority,
    )
    return TaskResponse(task_id=task_id, status="submitted")


@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task = system["state"].get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "task_id": task.task_id,
        "agent_id": task.agent_id,
        "status": task.status.value,
        "result": task.result,
        "error": task.error,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }


@app.get("/adapters/{platform}/health")
async def adapter_health(platform: str):
    adapter = system["adapters"].get(platform)
    if not adapter:
        raise HTTPException(status_code=404, detail=f"Adapter '{platform}' not found")
    return await adapter.health_check()


@app.post("/adapters/{platform}/send")
async def adapter_send(platform: str, body: dict[str, Any]):
    adapter = system["adapters"].get(platform)
    if not adapter:
        raise HTTPException(status_code=404, detail=f"Adapter '{platform}' not found")
    chat_id = body.get("chat_id", "")
    text = body.get("text", "")
    ok = await adapter.send_message(chat_id, text)
    return {"ok": ok, "platform": platform}
