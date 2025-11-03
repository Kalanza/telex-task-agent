import pytest
from fastapi.testclient import TestClient
from server import app
from db.database import init_db, save_task
from datetime import datetime, timedelta
import tempfile
import os


@pytest.fixture
def client(monkeypatch):
    """Create test client with temporary database"""
    # Create temporary database
    temp_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(temp_dir, "test_tasks.db")
    
    # Patch database path
    monkeypatch.setattr('db.database.DB_NAME', test_db_path)
    
    # Initialize database
    init_db()
    
    # Create test client
    client = TestClient(app)
    
    yield client
    
    # Cleanup
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Reminder Agent Online ✔️"


def test_webhook_telex_success(client):
    """Test successful task creation via webhook"""
    payload = {
        "sender": "alice",
        "message": "remind me tomorrow at 5pm to call mom"
    }
    
    response = client.post("/webhook/telex", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "response" in data
    assert "✅" in data["response"]  # Success emoji


def test_webhook_telex_no_message(client):
    """Test webhook with missing message"""
    payload = {
        "sender": "bob"
    }
    
    response = client.post("/webhook/telex", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "❓" in data["response"]  # Error emoji


def test_webhook_telex_no_time(client):
    """Test webhook with message but no time detected"""
    payload = {
        "sender": "carol",
        "message": "remind me to buy milk"
    }
    
    response = client.post("/webhook/telex", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "🕒" in data["response"]  # Clock emoji


def test_list_tasks_empty(client):
    """Test listing tasks when database is empty"""
    response = client.get("/tasks")
    assert response.status_code == 200
    
    data = response.json()
    assert data["count"] == 0
    assert data["tasks"] == []


def test_list_tasks_with_data(client):
    """Test listing tasks with existing data"""
    # Create some tasks directly
    save_task("alice", "task 1", datetime.now())
    save_task("bob", "task 2", datetime.now())
    
    response = client.get("/tasks")
    assert response.status_code == 200
    
    data = response.json()
    assert data["count"] == 2
    assert len(data["tasks"]) == 2


def test_list_tasks_filter_by_user(client):
    """Test filtering tasks by user"""
    save_task("alice", "alice's task", datetime.now())
    save_task("bob", "bob's task", datetime.now())
    
    response = client.get("/tasks?user=alice")
    assert response.status_code == 200
    
    data = response.json()
    assert data["count"] == 1
    assert data["tasks"][0]["user"] == "alice"


def test_list_tasks_filter_by_status(client):
    """Test filtering tasks by status"""
    task_id = save_task("carol", "pending task", datetime.now())
    
    # Get pending tasks
    response = client.get("/tasks?status=pending")
    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_delete_task_success(client):
    """Test deleting an existing task"""
    task_id = save_task("dave", "task to delete", datetime.now())
    
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "deleted"
    assert data["task_id"] == task_id
    
    # Verify task is deleted
    list_response = client.get("/tasks")
    assert list_response.json()["count"] == 0


def test_delete_task_not_found(client):
    """Test deleting a non-existent task"""
    response = client.delete("/tasks/99999")
    assert response.status_code == 404


def test_update_task_success(client):
    """Test updating a task"""
    task_id = save_task("eve", "old task", datetime.now())
    
    update_data = {
        "task": "updated task",
        "status": "completed"
    }
    
    response = client.patch(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "updated"


def test_update_task_not_found(client):
    """Test updating a non-existent task"""
    update_data = {"task": "new task"}
    
    response = client.patch("/tasks/99999", json=update_data)
    assert response.status_code == 404


def test_snooze_task_success(client):
    """Test snoozing a task"""
    task_id = save_task("frank", "snoozable task", datetime.now())
    
    snooze_data = {"minutes": 30}
    
    response = client.post(f"/tasks/{task_id}/snooze", json=snooze_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "snoozed"
    assert data["minutes"] == 30


def test_snooze_task_default_minutes(client):
    """Test snoozing with default minutes"""
    task_id = save_task("grace", "task", datetime.now())
    
    response = client.post(f"/tasks/{task_id}/snooze", json={})
    assert response.status_code == 200
    
    data = response.json()
    assert data["minutes"] == 10  # Default


def test_snooze_task_invalid_minutes(client):
    """Test snoozing with invalid minutes"""
    task_id = save_task("henry", "task", datetime.now())
    
    response = client.post(f"/tasks/{task_id}/snooze", json={"minutes": -5})
    assert response.status_code == 400


def test_trigger_reminders_endpoint(client):
    """Test manual reminder trigger"""
    response = client.get("/trigger-reminders")
    assert response.status_code == 200
    assert response.json()["status"] == "Reminder check executed"
