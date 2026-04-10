
from typing import List

ALLOWED_TOOLS = ["summarize", "classify", "retrieve_context", "answer_with_context"]
MAX_TEXT_LENGTH = 5000

def validate_request(tool: str, text: str):
    if tool not in ALLOWED_TOOLS:
        raise ValueError(f"Tool {tool} not allowed")
    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError("Input too large")
