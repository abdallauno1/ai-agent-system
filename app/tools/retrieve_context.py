from typing import Any, Dict

from app.models.schemas import TaskRequest
from app.tools.base import Tool


MOCK_KNOWLEDGE_BASE = {
    "kubernetes": "Kubernetes orchestrates containerized applications and supports declarative deployment models.",
    "gitops": "GitOps uses Git as the source of truth for infrastructure and application deployment workflows.",
    "observability": "Observability combines metrics, logs, and traces to understand system behavior and failures.",
    "agent": "AI agents can select tools, execute actions, and return structured results for a given task.",
}


class RetrieveContextTool(Tool):
    name = "retrieve_context"
    description = "Retrieve context snippets from a mock knowledge base."

    def run(self, request: TaskRequest) -> Dict[str, Any]:
        lowered = request.text.lower()
        hits = []
        for key, value in MOCK_KNOWLEDGE_BASE.items():
            if key in lowered or key in request.task.lower():
                hits.append({"topic": key, "snippet": value})
        return {
            "contexts": hits,
            "context_count": len(hits),
        }
