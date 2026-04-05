from abc import ABC, abstractmethod
from typing import Any, Dict

from app.models.schemas import TaskRequest


class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, request: TaskRequest) -> Dict[str, Any]:
        raise NotImplementedError
