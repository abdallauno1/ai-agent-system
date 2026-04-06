from typing import Any, Dict

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
        }
