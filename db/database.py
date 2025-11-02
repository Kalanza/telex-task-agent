import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager
from typing import Optional, List, Tuple

# Use absolute path for database
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(DB_DIR, "tasks.db")

@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_NAME)
    try:
        yield conn
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db() -> None:
    """Initialize the database schema."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                task TEXT NOT NULL,
                time DATETIME NOT NULL,
                status TEXT DEFAULT 'pending'
            )
        """)
        conn.commit()

def save_task(user: str, task: str, time: datetime) -> int:
    """
    Save a new task to the database.
    
    Args:
        user: Username or identifier
        task: Task description
        time: Scheduled/created datetime
    
    Returns:
        The ID of the newly created task
    
    Raises:
        ValueError: If parameters are invalid
        sqlite3.Error: If database operation fails
    """
    if not user or not task:
        raise ValueError("User and task cannot be empty")
    
    time_str = time.isoformat() if isinstance(time, datetime) else str(time)
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (user, task, time) VALUES (?, ?, ?)",
            (user, task, time_str)
        )
        conn.commit()
        return cursor.lastrowid

def get_tasks(user: Optional[str] = None, status: Optional[str] = None) -> List[Tuple]:
    """Retrieve tasks, optionally filtered by user and/or status."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        
        if user:
            query += " AND user = ?"
            params.append(user)
        if status:
            query += " AND status = ?"
            params.append(status)
        
        cursor.execute(query, params)
        return cursor.fetchall()

def update_task_status(task_id: int, status: str) -> bool:
    """Update the status of a task."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET status = ? WHERE id = ?",
            (status, task_id)
        )
        conn.commit()
        return cursor.rowcount > 0
