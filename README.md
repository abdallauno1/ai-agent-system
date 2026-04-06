# AI Agent System

Production-ready AI Agent System built with **Python + FastAPI**, featuring:

- Tool-based agent execution
- Structured JSON logging
- Prometheus metrics
- Docker packaging
- Kubernetes manifests
- GitHub Actions CI
- Day 1 / Day 2 / Day 3 architecture docs for GitHub storytelling

## What this project does

The service exposes an API where a client submits a task. The agent:

1. inspects the request
2. selects the most appropriate tool
<<<<<<< HEAD
3. executes the tool
4. returns the result with observability metadata

Initial built-in tools:
=======
3. executes the tool with retries
4. retrieves context when needed
5. returns the result with observability metadata

Built-in tools:
>>>>>>> 4be58da (add day 2: retrieval and agent flow improvements)

- `summarize`
- `classify`
- `retrieve_context`
<<<<<<< HEAD

This repository is intentionally self-contained so it can be pushed directly to GitHub and extended later with a real LLM, vector database, tracing, auth, and policy controls.

=======
- `answer_with_context`

This repository is intentionally self-contained so it can be pushed directly to GitHub and extended later with a real LLM, vector database, tracing, auth, and policy controls.

## Day 2 additions

Day 2 turns the baseline service into a more realistic agent runtime:

- in-memory vector store abstraction
- retrieval-backed answering tool
- richer tool registry with descriptions
- execution attempts in the response contract
- retry-ready agent flow

>>>>>>> 4be58da (add day 2: retrieval and agent flow improvements)
## Architecture

See:

- `docs/diagrams/day1-architecture.md`
- `docs/diagrams/day2-agent-flow.md`
- `docs/diagrams/day3-observability-governance.md`

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- API docs: `http://localhost:8000/docs`
- health: `http://localhost:8000/healthz`
- metrics: `http://localhost:8000/metrics`

<<<<<<< HEAD
## Example request
=======
## Example requests

### Summarization
>>>>>>> 4be58da (add day 2: retrieval and agent flow improvements)

```bash
curl -X POST http://localhost:8000/api/v1/tasks/run \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Summarize the following incident update",
    "text": "The payment service experienced intermittent latency between 09:10 and 09:24 UTC. Mitigation included scaling replicas from 2 to 6.",
    "labels": ["incident", "ops"]
  }'
```

<<<<<<< HEAD
=======
### Grounded answer

```bash
curl -X POST http://localhost:8000/api/v1/tasks/run \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Explain how RAG helps AI agents",
    "text": "I want a grounded answer with context about retrieval and agents."
  }'
```

>>>>>>> 4be58da (add day 2: retrieval and agent flow improvements)
## Environment variables

| Variable | Default | Description |
|---|---:|---|
| `APP_NAME` | `ai-agent-system` | Service name |
| `APP_ENV` | `dev` | Runtime environment |
| `LOG_LEVEL` | `INFO` | Logging level |
| `HOST` | `0.0.0.0` | Bind host |
| `PORT` | `8000` | Bind port |
<<<<<<< HEAD
| `ALLOWED_TOOLS` | `summarize,classify,retrieve_context` | Enabled tools |
| `MAX_INPUT_CHARS` | `12000` | Max accepted text length |
| `DEFAULT_SUMMARY_SENTENCES` | `2` | Summary sentence count |
=======
| `ALLOWED_TOOLS` | `summarize,classify,retrieve_context,answer_with_context` | Enabled tools |
| `MAX_INPUT_CHARS` | `12000` | Max accepted text length |
| `DEFAULT_SUMMARY_SENTENCES` | `2` | Summary sentence count |
| `DEFAULT_FALLBACK_TOOL` | `classify` | Default routing fallback |
| `RETRY_ATTEMPTS` | `2` | Max execution attempts |
| `RETRIEVE_TOP_K` | `3` | Number of retrieved documents |
>>>>>>> 4be58da (add day 2: retrieval and agent flow improvements)

## Docker

```bash
docker build -t ai-agent-system:latest .
docker run -p 8000:8000 ai-agent-system:latest
```

## Kubernetes

Apply the manifests:

```bash
kubectl apply -f k8s/
```

## Tests

```bash
pytest -q
```

## Roadmap

### Day 1
- Core FastAPI service
- Tool routing
- Logging
- Metrics
- Docker + Kubernetes baseline

### Day 2
<<<<<<< HEAD
- Add RAG integration
- Add external vector store abstraction
- Add tool registry improvements
- Add retry / fallback logic

### Day 3
- Add governance and security controls
- Add tracing / dashboards
- Add rate limits / policy checks
- Add multi-agent workflow orchestration
=======
- Retrieval-backed answering
- Vector store abstraction
- Tool registry improvements
- Retry / fallback-ready flow

### Day 3
- Governance and security controls
- Tracing / dashboards
- Rate limits / policy checks
- Multi-agent workflow orchestration
>>>>>>> 4be58da (add day 2: retrieval and agent flow improvements)

---

**Author label for diagrams/posts:** Abdalla Mady
