import logging
import time
<<<<<<< HEAD
from typing import Any, Dict

from app.core.metrics import TASK_DURATION_SECONDS, TASK_REQUESTS_TOTAL
from app.models.schemas import AgentDecision, TaskRequest
=======
from typing import Any, Dict, List

from app.core.config import get_settings
from app.core.metrics import TASK_DURATION_SECONDS, TASK_REQUESTS_TOTAL, TOOL_ATTEMPTS_TOTAL
from app.models.schemas import AgentDecision, TaskRequest, ToolExecutionAttempt
>>>>>>> 4be58da (add day 2: retrieval and agent flow improvements)
from app.services.tool_registry import ToolRegistry

logger = logging.getLogger(__name__)


class AgentService:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry
<<<<<<< HEAD
=======
        self.settings = get_settings()
>>>>>>> 4be58da (add day 2: retrieval and agent flow improvements)

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
<<<<<<< HEAD
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
=======
        elif any(word in task_lower for word in ["retrieve", "context", "lookup", "search"]):
            selected_tool = "retrieve_context"
            rationale = "Task suggests context retrieval."
        elif any(word in task_lower for word in ["answer", "explain", "what is", "how does"]) or any(
            word in text_lower for word in ["rag", "grounded", "knowledge base"]
        ):
            selected_tool = "answer_with_context"
            rationale = "Task suggests grounded answering with retrieval."
        elif any(word in task_lower for word in ["classify", "categorize", "label"]):
            selected_tool = "classify"
            rationale = "Task suggests classification."
        else:
            selected_tool = self.settings.default_fallback_tool
            rationale = f"Defaulted to configured fallback tool: {self.settings.default_fallback_tool}."

        fallback_tool = None
        if not self.registry.exists(selected_tool):
            fallback_tool = self.registry.list_tools()[0]
            return AgentDecision(
                selected_tool=fallback_tool,
                rationale=f"Selected tool was unavailable, fell back to {fallback_tool}.",
                fallback_tool=fallback_tool,
            )

        return AgentDecision(selected_tool=selected_tool, rationale=rationale, fallback_tool=fallback_tool)

    def run(self, request: TaskRequest) -> Dict[str, Any]:
        decision = self.decide(request)
        attempts: List[ToolExecutionAttempt] = []
        tool_name = decision.selected_tool
        tool = self.registry.get(tool_name)

        for attempt_number in range(1, self.settings.retry_attempts + 1):
            start = time.perf_counter()
            try:
                result = tool.run(request)
                elapsed = time.perf_counter() - start
                TASK_REQUESTS_TOTAL.labels(tool=tool_name, status="success").inc()
                TASK_DURATION_SECONDS.labels(tool=tool_name).observe(elapsed)
                TOOL_ATTEMPTS_TOTAL.labels(tool=tool_name, status="success").inc()
                attempts.append(
                    ToolExecutionAttempt(
                        tool=tool_name,
                        status="success",
                        duration_ms=round(elapsed * 1000, 2),
                        detail=f"Execution succeeded on attempt {attempt_number}.",
                    )
                )
                logger.info(
                    "task_executed",
                    extra={
                        "tool": tool_name,
                        "status": "success",
                        "duration_ms": round(elapsed * 1000, 2),
                        "attempt": attempt_number,
                    },
                )
                return {
                    "status": "success",
                    "selected_tool": tool_name,
                    "rationale": decision.rationale,
                    "output": result,
                    "attempts": [attempt.model_dump() for attempt in attempts],
                }
            except Exception as exc:  # pragma: no cover
                elapsed = time.perf_counter() - start
                TOOL_ATTEMPTS_TOTAL.labels(tool=tool_name, status="error").inc()
                attempts.append(
                    ToolExecutionAttempt(
                        tool=tool_name,
                        status="error",
                        duration_ms=round(elapsed * 1000, 2),
                        detail=f"Attempt {attempt_number} failed: {exc}",
                    )
                )
                logger.exception(
                    "task_failed_attempt",
                    extra={
                        "tool": tool_name,
                        "status": "error",
                        "duration_ms": round(elapsed * 1000, 2),
                        "attempt": attempt_number,
                    },
                )
                if attempt_number >= self.settings.retry_attempts or not tool.should_retry(exc):
                    TASK_REQUESTS_TOTAL.labels(tool=tool_name, status="error").inc()
                    TASK_DURATION_SECONDS.labels(tool=tool_name).observe(elapsed)
                    raise exc

        raise RuntimeError("Agent execution ended unexpectedly.")
>>>>>>> 4be58da (add day 2: retrieval and agent flow improvements)
