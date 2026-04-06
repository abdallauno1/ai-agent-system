from abc import ABC, abstractmethod
from typing import Any, Dict

from app.models.schemas import TaskRequest


class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, request: TaskRequest) -> Dict[str, Any]:
        raise NotImplementedError
<<<<<<< HEAD
=======

    def should_retry(self, exception: Exception) -> bool:
        return False
>>>>>>> 4be58da (add day 2: retrieval and agent flow improvements)
