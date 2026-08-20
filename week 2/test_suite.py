import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    client.post("/reset")

def test_read_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "endpoints" in resp.json()

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_get_all_tasks():
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert len(resp.json()) == 3

def test_create_task():
    resp = client.post("/tasks", json={"title": "Test new task"})
    assert resp.status_code == 201
    assert resp.json()["title"] == "Test new task"
    assert resp.json()["done"] is False

def test_get_single_task():
    resp = client.get("/tasks/1")
    assert resp.status_code == 200
    assert resp.json()["id"] == 1

def test_update_task_put_and_patch():
    resp_put = client.put("/tasks/1", json={"done": True, "title": "Updated Task 1"})
    assert resp_put.status_code == 200
    assert resp_put.json()["done"] is True

    resp_patch = client.patch("/tasks/1", json={"done": False})
    assert resp_patch.status_code == 200
    assert resp_patch.json()["done"] is False

def test_delete_task():
    resp = client.delete("/tasks/1")
    assert resp.status_code in [200, 204]
    get_resp = client.get("/tasks/1")
    assert get_resp.status_code == 404

def test_stats():
    resp = client.get("/stats")
    assert resp.status_code == 200
    assert "total" in resp.json()
    assert "done" in resp.json()
