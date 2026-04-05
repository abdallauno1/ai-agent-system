from typing import Any, Dict

from app.models.schemas import TaskRequest
from app.tools.base import Tool


class ClassifyTool(Tool):
    name = "classify"
    description = "Classify text into a coarse-grained category."

    def run(self, request: TaskRequest) -> Dict[str, Any]:
        text = request.text.lower()
        if any(token in text for token in ["incident", "latency", "error", "degradation"]):
            label = "operations_incident"
        elif any(token in text for token in ["policy", "governance", "compliance", "security"]):
            label = "governance_security"
        elif any(token in text for token in ["customer", "feature", "roadmap", "product"]):
            label = "product_business"
        else:
            label = "general"
        return {
            "classification": label,
            "matched_labels": request.labels,
            "input_length": len(request.text),
        }
