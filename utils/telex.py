import requests
import os
from utils.logger import log
from typing import Optional

# Telex webhook URL (can be configured via environment variable)
TELEX_WEBHOOK_URL = os.getenv("TELEX_WEBHOOK_URL", "http://localhost:9000/webhook/telex")


def send_telex_message(user: str, text: str) -> bool:
    """
    Send a message back to the user via Telex webhook.
    
    Args:
        user: Username/identifier to send message to
        text: Message text to send
        
    Returns:
        True if message sent successfully, False otherwise
    """
    try:
        payload = {
            "sender": user,
            "message": text,
            "type": "reminder"  # Mark as system-generated reminder
        }
        
        response = requests.post(
            TELEX_WEBHOOK_URL,
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            log(f"Reminder sent to {user}: {text}", "info")
            return True
        else:
            log(f"Failed to send reminder to {user}. Status: {response.status_code}", "error")
            return False
            
    except requests.RequestException as e:
        log(f"Error sending reminder to {user}: {e}", "error")
        return False


def send_reminder(user: str, task_text: str, task_id: int) -> bool:
    """
    Send a reminder notification to the user.
    
    Args:
        user: Username to send reminder to
        task_text: The task description
        task_id: ID of the task being reminded about
        
    Returns:
        True if reminder sent successfully
    """
    message = f"⏰ Reminder: {task_text} (Task #{task_id})"
    return send_telex_message(user, message)
