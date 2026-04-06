from typing import Any, Dict

<<<<<<< HEAD
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
=======
from app.core.config import get_settings
from app.models.schemas import TaskRequest
from app.services.vector_store import InMemoryVectorStore
from app.tools.base import Tool


class RetrieveContextTool(Tool):
    name = "retrieve_context"
    description = "Retrieve context snippets from an in-memory vector store."

    def __init__(self, vector_store: InMemoryVectorStore, top_k: int | None = None) -> None:
        settings = get_settings()
        self.vector_store = vector_store
        self.top_k = top_k or settings.retrieve_top_k

    def run(self, request: TaskRequest) -> Dict[str, Any]:
        results = self.vector_store.search(f"{request.task} {request.text}", top_k=self.top_k)
        contexts = [
            {
                "id": item["id"],
                "topic": item["topic"],
                "snippet": item["text"],
                "score": item["score"],
            }
            for item in results
        ]
        return {
            "contexts": contexts,
            "context_count": len(contexts),
            "retrieval_backend": "in_memory_vector_store",
>>>>>>> 4be58da (add day 2: retrieval and agent flow improvements)
        }
