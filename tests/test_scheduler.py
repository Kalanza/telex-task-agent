import pytest
from datetime import datetime, timedelta
from scheduler import reminder_job
from db.database import init_db, save_task, get_due_tasks, mark_task_sent
import tempfile
import os


@pytest.fixture
def test_db(monkeypatch):
    """Create a temporary test database"""
    # Create temporary database
    temp_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(temp_dir, "test_tasks.db")
    
    # Patch the database path
    monkeypatch.setattr('db.database.DB_NAME', test_db_path)
    
    # Initialize database
    init_db()
    
    yield test_db_path
    
    # Cleanup
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


def test_get_due_tasks_empty(test_db):
    """Test get_due_tasks when no tasks are due"""
    # Save a future task
    future_time = datetime.now() + timedelta(hours=2)
    save_task("alice", "future task", future_time)
    
    # Should return empty list
    due_tasks = get_due_tasks()
    assert len(due_tasks) == 0


def test_get_due_tasks_with_past_task(test_db):
    """Test get_due_tasks with a past task"""
    # Save a past task
    past_time = datetime.now() - timedelta(hours=1)
    task_id = save_task("bob", "past task", past_time)
    
    # Should return the task
    due_tasks = get_due_tasks()
    assert len(due_tasks) == 1
    assert due_tasks[0][0] == task_id
    assert due_tasks[0][1] == "bob"
    assert due_tasks[0][2] == "past task"


def test_mark_task_sent(test_db):
    """Test marking a task as sent"""
    # Create a past task
    past_time = datetime.now() - timedelta(minutes=30)
    task_id = save_task("carol", "test task", past_time)
    
    # Mark as sent
    success = mark_task_sent(task_id)
    assert success is True
    
    # Should not appear in due tasks anymore
    due_tasks = get_due_tasks()
    assert len(due_tasks) == 0


def test_reminder_job_no_tasks(test_db, caplog):
    """Test reminder job when no tasks are due"""
    # Create only future tasks
    future_time = datetime.now() + timedelta(hours=5)
    save_task("dave", "future task", future_time)
    
    # Run reminder job
    reminder_job()
    
    # Check log message
    assert "No due tasks found" in caplog.text


def test_multiple_due_tasks(test_db):
    """Test handling multiple due tasks"""
    # Create multiple past tasks
    past_time_1 = datetime.now() - timedelta(hours=2)
    past_time_2 = datetime.now() - timedelta(minutes=30)
    
    save_task("user1", "task 1", past_time_1)
    save_task("user2", "task 2", past_time_2)
    
    due_tasks = get_due_tasks()
    assert len(due_tasks) == 2


def test_task_not_sent_twice(test_db):
    """Test that sent tasks are not returned as due"""
    # Create past task
    past_time = datetime.now() - timedelta(hours=1)
    task_id = save_task("eve", "one-time task", past_time)
    
    # First check - should be due
    due_tasks_1 = get_due_tasks()
    assert len(due_tasks_1) == 1
    
    # Mark as sent
    mark_task_sent(task_id)
    
    # Second check - should not be due
    due_tasks_2 = get_due_tasks()
    assert len(due_tasks_2) == 0
