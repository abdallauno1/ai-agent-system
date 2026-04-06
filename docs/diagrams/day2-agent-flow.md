# Day 2 - Agent Flow, Retrieval, and Fallback Execution

**Author:** Abdalla Mady

```mermaid
sequenceDiagram
    participant C as Client
    participant A as FastAPI
    participant S as Agent Service
    participant R as Tool Router
    participant T as Selected Tool
    participant V as Vector Store

    C->>A: POST /api/v1/tasks/run
    A->>S: Validate request
    S->>R: Decide best tool
    R-->>S: summarize | classify | retrieve_context | answer_with_context
    alt grounded answer path
        S->>T: Execute answer_with_context
        T->>V: Retrieve top-k context
        V-->>T: Ranked documents
        T-->>S: Grounded answer + sources
    else direct tool path
        S->>T: Execute selected tool
        T-->>S: Tool output
    end
    S-->>A: Structured result + rationale + attempts
    A-->>C: JSON response
```

## Story

Day 2 extends the baseline service with:

- retrieval-backed execution
- vector store abstraction
- richer tool registry metadata
- retry-ready execution flow
- structured attempt history in responses
