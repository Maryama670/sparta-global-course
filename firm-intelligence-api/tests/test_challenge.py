"""Endpoint contract checks with provider calls replaced by test fixtures."""

from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkeypatch):
    # The provider clients require keys at import time; no real requests are made.
    monkeypatch.setenv("VOYAGE_API_KEY", "test-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    import main

    monkeypatch.setattr(main, "build_index", Mock(return_value=0))
    with TestClient(main.app) as test_client:
        yield test_client


def test_agent_ask(client, monkeypatch):
    from routers import agent

    answer = "Profit per equity partner is profit divided by equity partners."
    create = Mock(return_value=SimpleNamespace(
        content=[SimpleNamespace(type="text", text=answer)],
        usage=SimpleNamespace(input_tokens=20, output_tokens=12),
        stop_reason="end_turn",
    ))
    monkeypatch.setattr(agent.client.messages, "create", create)

    question = "How is profit per equity partner calculated?"
    response = client.post("/agent/ask", json={"question": question})

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == answer
    assert data["completed"] is True
    assert data["tool_calls_made"] == 0
    assert data["input_tokens"] == 20
    assert data["output_tokens"] == 12
    assert create.call_args.kwargs["messages"][0]["content"] == question


def test_knowledge_search(client, monkeypatch):
    from routers import knowledge

    hits = [{"id": "doc-test", "title": "Profit per equity partner",
             "text": "Profit divided by equity partners.", "score": 0.9}]
    search = Mock(return_value=hits)
    monkeypatch.setattr(knowledge.knowledge, "search", search)

    response = client.post(
        "/knowledge/search",
        json={"question": "profit per equity partner", "top_k": 3},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "profit per equity partner"
    assert data["results"] == hits
    assert "title" in data["results"][0]
    assert "score" in data["results"][0]
    search.assert_called_once_with("profit per equity partner", 3)


def test_streaming_summary(client, monkeypatch):
    import llm

    stream = Mock(return_value=iter(["A firm ", "summary."]))
    monkeypatch.setattr(llm, "stream_firm_summary", stream)

    with client.stream("GET", "/firms/1/summary/stream") as response:
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/plain")
        assert "".join(response.iter_text()) == "A firm summary."
    stream.assert_called_once()
    assert stream.call_args.args[0]["id"] == 1
