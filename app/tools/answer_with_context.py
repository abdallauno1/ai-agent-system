from typing import Any, Dict

from app.models.schemas import TaskRequest
from app.tools.base import Tool
from app.tools.retrieve_context import RetrieveContextTool


class AnswerWithContextTool(Tool):
    name = "answer_with_context"
    description = "Generate a grounded answer by retrieving relevant context first."

    def __init__(self, retriever: RetrieveContextTool) -> None:
        self.retriever = retriever

    def run(self, request: TaskRequest) -> Dict[str, Any]:
        retrieval = self.retriever.run(request)
        contexts = retrieval.get("contexts", [])
        if contexts:
            context_text = " ".join(item["snippet"] for item in contexts)
            answer = (
                f"Grounded answer: {request.task}. "
                f"Based on retrieved context, {context_text}"
            )
        else:
            answer = (
                f"Grounded answer: {request.task}. "
                "No highly relevant context was retrieved, so the response is based on the request text only."
            )
        return {
            "answer": answer,
            "sources": [{"id": item["id"], "topic": item["topic"], "score": item["score"]} for item in contexts],
            "source_count": len(contexts),
        }
