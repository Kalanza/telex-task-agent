from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from agents.task_agent import process_message
from db.database import (
    init_db, get_all_tasks, delete_task, 
    update_task, snooze_task
)
from utils.logger import log
from scheduler import start_scheduler, stop_scheduler
from datetime import datetime
import uvicorn
import atexit

app = FastAPI()

# Initialize DB when server starts
init_db()
log("Database initialized successfully", "info")

# Start the reminder scheduler
start_scheduler()

# Register cleanup handler to stop scheduler on shutdown
atexit.register(stop_scheduler)

@app.get("/")
def home():
    return {"status": "Reminder Agent Online ✔️"}

@app.get("/trigger-reminders")
def trigger_reminders():
    """Manual endpoint to trigger reminder check (for testing)"""
    from scheduler import reminder_job
    log("Manual reminder check triggered", "info")
    reminder_job()
    return {"status": "Reminder check executed"}


@app.get("/tasks")
def list_tasks(user: str = None, status: str = None, limit: int = 100):
    """
    Get all tasks with optional filtering.
    
    Query Parameters:
        - user: Filter by username (optional)
        - status: Filter by status (optional)
        - limit: Maximum results (default: 100)
    """
    try:
        tasks = get_all_tasks(user=user, status=status, limit=limit)
        log(f"Retrieved {len(tasks)} tasks (user={user}, status={status})", "info")
        return {"tasks": tasks, "count": len(tasks)}
    except Exception as e:
        log(f"Error retrieving tasks: {e}", "error")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/tasks/{task_id}")
def delete_task_endpoint(task_id: int):
    """Delete a task by ID"""
    try:
        success = delete_task(task_id)
        if success:
            log(f"Task #{task_id} deleted", "info")
            return {"status": "deleted", "task_id": task_id}
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except HTTPException:
        raise
    except Exception as e:
        log(f"Error deleting task #{task_id}: {e}", "error")
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/tasks/{task_id}")
async def update_task_endpoint(task_id: int, request: Request):
    """
    Update a task's details.
    
    Request body can include:
        - task: New task description
        - time: New scheduled time (ISO format)
        - status: New status
    """
    try:
        data = await request.json()
        
        task_text = data.get("task")
        time_str = data.get("time")
        status = data.get("status")
        
        # Parse time if provided
        time_obj = None
        if time_str:
            try:
                time_obj = datetime.fromisoformat(time_str)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid time format. Use ISO format.")
        
        success = update_task(task_id, task_text=task_text, time=time_obj, status=status)
        
        if success:
            log(f"Task #{task_id} updated", "info")
            return {"status": "updated", "task_id": task_id}
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except HTTPException:
        raise
    except Exception as e:
        log(f"Error updating task #{task_id}: {e}", "error")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tasks/{task_id}/snooze")
async def snooze_task_endpoint(task_id: int, request: Request):
    """
    Snooze a task by adding minutes to its scheduled time.
    
    Request body:
        - minutes: Number of minutes to snooze (default: 10)
    """
    try:
        data = await request.json()
        minutes = data.get("minutes", 10)
        
        if not isinstance(minutes, int) or minutes <= 0:
            raise HTTPException(status_code=400, detail="Minutes must be a positive integer")
        
        success = snooze_task(task_id, minutes)
        
        if success:
            log(f"Task #{task_id} snoozed for {minutes} minutes", "info")
            return {
                "status": "snoozed",
                "task_id": task_id,
                "minutes": minutes,
                "message": f"Task snoozed for {minutes} minutes"
            }
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except HTTPException:
        raise
    except Exception as e:
        log(f"Error snoozing task #{task_id}: {e}", "error")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhook/telex")
async def telex_webhook(request: Request):
    payload = await request.json()

    # Extract incoming data from Telex payload
    user = payload.get("sender", "unknown-user")
    message = payload.get("message")
    
    # Log incoming message
    log(f"From {user}: {message}")

    if not message:
        log("Empty message received", "warning")
        return {"response": "❓ No message received"}

    # Process the text through your agent
    reply = process_message(user, message)
    log(f"Reply to {user}: {reply}", "debug")

    return {
        "response": reply  # Telex displays this message
    }


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=9000, reload=True)
