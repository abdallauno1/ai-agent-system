import logging
import time
from typing import Any, Dict

from app.core.metrics import TASK_DURATION_SECONDS, TASK_REQUESTS_TOTAL
from app.models.schemas import AgentDecision, TaskRequest
from app.services.tool_registry import ToolRegistry

logger = logging.getLogger(__name__)


class AgentService:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def decide(self, request: TaskRequest) -> AgentDecision:
        if request.preferred_tool and self.registry.exists(request.preferred_tool):
            return AgentDecision(
                selected_tool=request.preferred_tool,
                rationale="Client provided a preferred tool and it is enabled.",
            )

        task_lower = request.task.lower()
        text_lower = request.text.lower()

        if any(word in task_lower for word in ["summarize", "summary"]) or len(request.text) > 500:
            selected_tool = "summarize"
            rationale = "Task suggests summarization or input is long."
        elif any(word in task_lower for word in ["classify", "categorize", "label"]):
            selected_tool = "classify"
            rationale = "Task suggests classification."
        elif any(word in task_lower for word in ["retrieve", "context", "lookup"]) or any(
            keyword in text_lower for keyword in ["kubernetes", "gitops", "observability", "agent"]
        ):
            selected_tool = "retrieve_context"
            rationale = "Task suggests context retrieval."
        else:
            selected_tool = "classify"
            rationale = "Defaulted to classify for short general requests."

        if not self.registry.exists(selected_tool):
            fallback = self.registry.list_tools()[0]
            return AgentDecision(
                selected_tool=fallback,
                rationale=f"Selected tool was unavailable, fell back to {fallback}.",
            )

        return AgentDecision(selected_tool=selected_tool, rationale=rationale)

    def run(self, request: TaskRequest) -> Dict[str, Any]:
        decision = self.decide(request)
        start = time.perf_counter()
        try:
            result = self.registry.get(decision.selected_tool).run(request)
            elapsed = time.perf_counter() - start
            TASK_REQUESTS_TOTAL.labels(tool=decision.selected_tool, status="success").inc()
            TASK_DURATION_SECONDS.labels(tool=decision.selected_tool).observe(elapsed)
            logger.info(
                "task_executed",
                extra={
                    "tool": decision.selected_tool,
                    "status": "success",
                    "duration_ms": round(elapsed * 1000, 2),
                },
            )
            return {
                "status": "success",
                "selected_tool": decision.selected_tool,
                "rationale": decision.rationale,
                "output": result,
            }
        except Exception as exc:  # pragma: no cover
            elapsed = time.perf_counter() - start
            TASK_REQUESTS_TOTAL.labels(tool=decision.selected_tool, status="error").inc()
            TASK_DURATION_SECONDS.labels(tool=decision.selected_tool).observe(elapsed)
            logger.exception(
                "task_failed",
                extra={
                    "tool": decision.selected_tool,
                    "status": "error",
                    "duration_ms": round(elapsed * 1000, 2),
                },
            )
            raise exc
