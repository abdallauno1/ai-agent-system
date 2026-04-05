from typing import Dict

from app.core.config import get_settings
from app.tools.base import Tool
from app.tools.classify import ClassifyTool
from app.tools.retrieve_context import RetrieveContextTool
from app.tools.summarize import SummarizeTool


class ToolRegistry:
    def __init__(self) -> None:
        settings = get_settings()
        available = {
            "summarize": SummarizeTool(sentence_count=settings.default_summary_sentences),
            "classify": ClassifyTool(),
            "retrieve_context": RetrieveContextTool(),
        }
        self.tools: Dict[str, Tool] = {
            name: tool for name, tool in available.items() if name in settings.allowed_tools
        }

    def get(self, name: str) -> Tool:
        return self.tools[name]

    def exists(self, name: str) -> bool:
        return name in self.tools

    def list_tools(self) -> list[str]:
        return list(self.tools.keys())
