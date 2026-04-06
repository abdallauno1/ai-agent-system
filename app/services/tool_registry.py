from typing import Dict, List

from app.core.config import get_settings
from app.services.vector_store import InMemoryVectorStore
from app.tools.answer_with_context import AnswerWithContextTool
from app.tools.base import Tool
from app.tools.classify import ClassifyTool
from app.tools.retrieve_context import RetrieveContextTool
from app.tools.summarize import SummarizeTool


class ToolRegistry:
    def __init__(self) -> None:
        settings = get_settings()
        vector_store = InMemoryVectorStore()
        retriever = RetrieveContextTool(vector_store=vector_store, top_k=settings.retrieve_top_k)
        available = {
            "summarize": SummarizeTool(sentence_count=settings.default_summary_sentences),
            "classify": ClassifyTool(),
            "retrieve_context": retriever,
            "answer_with_context": AnswerWithContextTool(retriever=retriever),
        }
        self.tools: Dict[str, Tool] = {
            name: tool for name, tool in available.items() if name in settings.allowed_tools
        }

    def get(self, name: str) -> Tool:
        return self.tools[name]

    def exists(self, name: str) -> bool:
        return name in self.tools

    def list_tools(self) -> List[str]:
        return list(self.tools.keys())

    def describe_tools(self) -> List[Dict[str, str]]:
        return [
            {"name": name, "description": tool.description}
            for name, tool in self.tools.items()
        ]
