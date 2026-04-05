from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.models.schemas import HealthResponse, TaskRequest, TaskResponse
from app.services.agent import AgentService
from app.services.tool_registry import ToolRegistry

router = APIRouter()
settings = get_settings()
agent_service = AgentService(ToolRegistry())


@router.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(status="ok", app=settings.app_name, env=settings.app_env)


@router.get("/readyz", response_model=HealthResponse)
def readyz() -> HealthResponse:
    return HealthResponse(status="ready", app=settings.app_name, env=settings.app_env)


@router.get("/api/v1/tools")
def list_tools() -> dict:
    return {"tools": ToolRegistry().list_tools()}


@router.post("/api/v1/tasks/run", response_model=TaskResponse)
def run_task(request: TaskRequest) -> TaskResponse:
    if len(request.text) > settings.max_input_chars:
        raise HTTPException(status_code=413, detail="Input text exceeds configured max size.")

    result = agent_service.run(request)
    return TaskResponse(task=request.task, **result)
