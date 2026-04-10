# Day 3 - Observability and Governance

**Author:** Abdalla Mady

```mermaid
flowchart TB
    subgraph Runtime
        api[FastAPI Service]
        agent[Agent Execution]
        tools[Tool Layer]
    end

    api --> agent --> tools
    api --> logs[JSON Logs]
    api --> metrics[Prometheus Metrics]
    agent --> policy[Policy Controls]
    policy --> limits[Input / Tool Limits]
    policy --> allowed[Allowed Tool List]
    metrics --> dashboard[Grafana Dashboard]
    logs --> logstack[Central Log Backend]
```

## Story

Day 3 frames the service as an enterprise AI system:

- observability by default
- controlled tool execution
- runtime governance
- clear path to dashboards, alerts, and policies
