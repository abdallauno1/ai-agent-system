from typing import Any, Dict

from app.models.schemas import TaskRequest
from app.tools.base import Tool


class SummarizeTool(Tool):
    name = "summarize"
    description = "Summarize the input text into a few concise sentences."

    def __init__(self, sentence_count: int = 2):
        self.sentence_count = sentence_count

    def run(self, request: TaskRequest) -> Dict[str, Any]:
        parts = [segment.strip() for segment in request.text.replace("\n", " ").split(".") if segment.strip()]
        summary = ". ".join(parts[: self.sentence_count])
        if summary and not summary.endswith("."):
            summary += "."
        return {
            "summary": summary or request.text[:300],
            "summary_sentences": min(len(parts), self.sentence_count),
            "input_length": len(request.text),
        }
