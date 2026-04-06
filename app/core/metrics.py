from prometheus_client import Counter, Histogram

TASK_REQUESTS_TOTAL = Counter(
    "ai_agent_task_requests_total",
    "Total task execution requests",
    ["tool", "status"],
)

TASK_DURATION_SECONDS = Histogram(
    "ai_agent_task_duration_seconds",
    "Task execution duration in seconds",
    ["tool"],
)

TOOL_ATTEMPTS_TOTAL = Counter(
    "ai_agent_tool_attempts_total",
    "Total tool execution attempts",
    ["tool", "status"],
)
