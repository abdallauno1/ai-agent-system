from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_tools():
    response = client.get("/api/v1/tools")
    assert response.status_code == 200

    assert "summarize" in response.json()["tools"]

    tools = response.json()["tools"]
    assert "summarize" in tools
    assert "answer_with_context" in tools


def test_tool_details():
    response = client.get("/api/v1/tools/details")
    assert response.status_code == 200
    details = response.json()["tools"]
    assert any(item["name"] == "retrieve_context" for item in details)


def test_run_task_summarize():
    payload = {
        "task": "Summarize this incident",
        "text": "A latency spike affected checkout. The team scaled replicas. Service recovered in 10 minutes.",
        "labels": ["incident"],
    }
    response = client.post("/api/v1/tasks/run", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["selected_tool"] == "summarize"



def test_run_task_classify():
    payload = {
        "task": "Classify this note",
        "text": "Security policy update for container image scanning.",
    }
    response = client.post("/api/v1/tasks/run", json=payload)
    assert response.status_code == 200
    assert response.json()["selected_tool"] == "classify"

    assert body["attempts"][0]["status"] == "success"


def test_run_task_grounded_answer():
    payload = {
        "task": "Explain how RAG helps AI agents",
        "text": "I want a grounded answer with retrieval context for agent systems.",
    }
    response = client.post("/api/v1/tasks/run", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["selected_tool"] == "answer_with_context"
    assert body["output"]["source_count"] >= 1


def test_run_task_retrieve_context():
    payload = {
        "task": "Retrieve context about observability",
        "text": "Need context on observability and Kubernetes for platform teams.",
    }
    response = client.post("/api/v1/tasks/run", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["selected_tool"] == "retrieve_context"
    assert body["output"]["context_count"] >= 1
