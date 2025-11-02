from utils.nlp import extract_task_and_time
from db.database import save_task
import sqlite3

def process_message(user: str, text: str) -> str:
    """
    Process a user message and create a task.
    
    Args:
        user: Username or identifier
        text: Natural language task description with time
        
    Returns:
        Success or error message string
    """
    # Extract task information
    data = extract_task_and_time(text)

    # Validate time was detected
    if not data["time"]:
        return "🕒 I didn't detect a time. Try like: 'remind me at 5pm to study'"
    
    # Validate task description exists
    if not data["task"] or not data["task"].strip():
        return "❌ I couldn't understand the task. Please be more specific."

    # Save to database with error handling
    try:
        task_id = save_task(user, data["task"], data["time"])
        time_str = data["time"].strftime('%B %d at %I:%M %p')
        return f"✅ Saved task #{task_id}: '{data['task']}' for {time_str}"
    except ValueError as e:
        return f"❌ Invalid input: {e}"
    except sqlite3.Error as e:
        return f"❌ Database error: Could not save task. Please try again."
    except Exception as e:
        return f"❌ Unexpected error: {e}"
