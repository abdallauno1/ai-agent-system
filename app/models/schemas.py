from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    task: str = Field(..., min_length=3, max_length=200)
    text: str = Field(..., min_length=1)
    labels: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    preferred_tool: Optional[str] = None


class AgentDecision(BaseModel):
    selected_tool: str
    rationale: str
<<<<<<< HEAD
=======
    fallback_tool: Optional[str] = None


class ToolExecutionAttempt(BaseModel):
    tool: str
    status: Literal["success", "error", "skipped"]
    duration_ms: float
    detail: str
>>>>>>> 4be58da (add day 2: retrieval and agent flow improvements)


class TaskResponse(BaseModel):
    status: Literal["success", "error"]
    task: str
    selected_tool: str
    rationale: str
    output: Dict[str, Any]
<<<<<<< HEAD
=======
    attempts: List[ToolExecutionAttempt] = Field(default_factory=list)
>>>>>>> 4be58da (add day 2: retrieval and agent flow improvements)


class HealthResponse(BaseModel):
    status: str
    app: str
    env: str
