import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_openrouter_endpoint():
    response = client.post("/openrouter", json={"prompt": "What is the capital of France?"})
    assert response.status_code == 200
    data = response.json()
    assert "capital" in data["response"].lower()

def test_search_memory_endpoint():
    response = client.post("/search-memory", json={"query": "France", "n_results": 2})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["memories"], list)

def test_clear_memory_endpoint():
    response = client.delete("/memory/clear")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "All memory cleared."