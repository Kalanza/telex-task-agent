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
                status TEXT DEFAULT 'pending',
                sent BOOLEAN DEFAULT 0
            )
        """)
        
        # Add sent column to existing tables (migration)
        try:
            cursor.execute("ALTER TABLE tasks ADD COLUMN sent BOOLEAN DEFAULT 0")
        except sqlite3.OperationalError:
            # Column already exists
            pass
        
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


def get_due_tasks() -> List[Tuple]:
    """
    Get all tasks that are due (time <= now) and haven't been sent yet.
    
    Returns:
        List of tuples: (id, user, task, time, status, sent)
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute("""
            SELECT * FROM tasks 
            WHERE time <= ? 
            AND sent = 0 
            AND status = 'pending'
            ORDER BY time ASC
        """, (now,))
        return cursor.fetchall()


def mark_task_sent(task_id: int) -> bool:
    """
    Mark a task as sent (reminder delivered).
    
    Args:
        task_id: ID of the task to mark as sent
        
    Returns:
        True if task was updated, False otherwise
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET sent = 1, status = 'sent' WHERE id = ?",
            (task_id,)
        )
        conn.commit()
        return cursor.rowcount > 0


def get_all_tasks(user: Optional[str] = None, status: Optional[str] = None, limit: int = 100) -> List[dict]:
    """
    Get all tasks with optional filtering.
    
    Args:
        user: Filter by username (optional)
        status: Filter by status (optional)
        limit: Maximum number of results
        
    Returns:
        List of task dictionaries with all fields
    """
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row  # Enable column access by name
        cursor = conn.cursor()
        
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        
        if user:
            query += " AND user = ?"
            params.append(user)
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY time DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Convert rows to dictionaries
        return [dict(row) for row in rows]


def delete_task(task_id: int) -> bool:
    """
    Delete a task by ID.
    
    Args:
        task_id: ID of the task to delete
        
    Returns:
        True if task was deleted, False if not found
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        return cursor.rowcount > 0


def update_task(task_id: int, task_text: Optional[str] = None, 
                time: Optional[datetime] = None, status: Optional[str] = None) -> bool:
    """
    Update a task's details.
    
    Args:
        task_id: ID of the task to update
        task_text: New task description (optional)
        time: New scheduled time (optional)
        status: New status (optional)
        
    Returns:
        True if task was updated, False if not found
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if task_text is not None:
            updates.append("task = ?")
            params.append(task_text)
        if time is not None:
            updates.append("time = ?")
            time_str = time.isoformat() if isinstance(time, datetime) else str(time)
            params.append(time_str)
        if status is not None:
            updates.append("status = ?")
            params.append(status)
        
        if not updates:
            return False  # Nothing to update
        
        params.append(task_id)
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0


def snooze_task(task_id: int, minutes: int) -> bool:
    """
    Snooze a task by adding minutes to its scheduled time.
    
    Args:
        task_id: ID of the task to snooze
        minutes: Number of minutes to snooze
        
    Returns:
        True if task was snoozed, False if not found
    """
    from datetime import timedelta
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get current task time
        cursor.execute("SELECT time, sent FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        
        if not row:
            return False
        
        current_time_str, sent = row
        current_time = datetime.fromisoformat(current_time_str)
        
        # Add snooze time
        new_time = current_time + timedelta(minutes=minutes)
        
        # Update task with new time and reset sent flag
        cursor.execute(
            "UPDATE tasks SET time = ?, sent = 0, status = 'pending' WHERE id = ?",
            (new_time.isoformat(), task_id)
        )
        conn.commit()
        return cursor.rowcount > 0
