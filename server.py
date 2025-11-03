from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from agents.task_agent import process_message
from db.database import (
    init_db, get_all_tasks, delete_task, 
    update_task, snooze_task
)
from utils.logger import log
from scheduler import start_scheduler, stop_scheduler
from datetime import datetime
from typing import List
import uvicorn
import atexit
import os
import json

app = FastAPI(
    title="🤖 Task Reminder Agent API",
    description="""
    An intelligent AI-powered task reminder assistant with natural language processing.
    
    ## Features
    * 💬 Natural language understanding ("remind me at 5pm to study")
    * ⏰ Automated reminders via background scheduler
    * 🗄️ Persistent SQLite database
    * 🔄 Full CRUD operations for task management
    * 🤖 Telex A2A protocol integration
    
    ## Example Usage
    Send a POST request to `/a2a/agent/taskAgent`:
    ```json
    {
        "message": "remind me tomorrow at 3pm to call mom",
        "user": "john_doe"
    }
    ```
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Victor Kalanza",
        "url": "https://github.com/Kalanza/telex-task-agent",
    },
    license_info={
        "name": "MIT",
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        log(f"WebSocket connected. Total connections: {len(self.active_connections)}", "info")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        log(f"WebSocket disconnected. Total connections: {len(self.active_connections)}", "info")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

# Initialize DB when server starts
init_db()
log("Database initialized successfully", "info")

# Start the reminder scheduler
start_scheduler()

# Register cleanup handler to stop scheduler on shutdown
atexit.register(stop_scheduler)

@app.get("/", response_class=HTMLResponse)
def home():
    """Landing page with interactive UI"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🤖 Task Reminder Agent</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 800px;
                width: 100%;
                padding: 40px;
            }
            h1 {
                color: #667eea;
                font-size: 2.5em;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 15px;
            }
            .subtitle {
                color: #666;
                font-size: 1.1em;
                margin-bottom: 30px;
            }
            .status {
                background: #d4edda;
                color: #155724;
                padding: 15px 20px;
                border-radius: 10px;
                margin-bottom: 30px;
                border-left: 4px solid #28a745;
                font-weight: 500;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .feature {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                transition: transform 0.3s;
            }
            .feature:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .feature-icon {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .feature-title {
                font-weight: 600;
                color: #333;
                margin-bottom: 5px;
            }
            .feature-desc {
                font-size: 0.9em;
                color: #666;
            }
            .buttons {
                display: flex;
                gap: 15px;
                margin-top: 30px;
                flex-wrap: wrap;
            }
            .btn {
                padding: 15px 30px;
                border: none;
                border-radius: 10px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .btn-secondary {
                background: #f8f9fa;
                color: #333;
                border: 2px solid #667eea;
            }
            .example {
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 20px;
                border-radius: 10px;
                margin: 30px 0;
            }
            .example-title {
                font-weight: 600;
                color: #856404;
                margin-bottom: 10px;
            }
            code {
                background: #f8f9fa;
                padding: 2px 6px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                color: #e83e8c;
            }
            .endpoint {
                background: #d1ecf1;
                border-left: 4px solid #17a2b8;
                padding: 15px;
                border-radius: 10px;
                margin-top: 20px;
                font-family: 'Courier New', monospace;
                font-size: 0.95em;
            }
            .stats {
                display: flex;
                gap: 20px;
                margin: 20px 0;
            }
            .stat {
                flex: 1;
                background: #e7f3ff;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
            }
            .stat-value {
                font-size: 1.8em;
                font-weight: 700;
                color: #667eea;
            }
            .stat-label {
                font-size: 0.9em;
                color: #666;
                margin-top: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>
                <span>🤖</span>
                <span>Task Reminder Agent</span>
            </h1>
            <p class="subtitle">AI-powered task management with natural language understanding</p>
            
            <div class="status">
                ✅ System Online | Scheduler Active | Database Connected
            </div>

            <div class="features">
                <div class="feature">
                    <div class="feature-icon">💬</div>
                    <div class="feature-title">Natural Language</div>
                    <div class="feature-desc">Just say "remind me at 5pm"</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">⏰</div>
                    <div class="feature-title">Auto Reminders</div>
                    <div class="feature-desc">Delivered right on time</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🗄️</div>
                    <div class="feature-title">Persistent Storage</div>
                    <div class="feature-desc">Never lose a task</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🔄</div>
                    <div class="feature-title">Full CRUD API</div>
                    <div class="feature-desc">Complete task control</div>
                </div>
            </div>

            <div class="example">
                <div class="example-title">💡 Example Usage</div>
                <p><strong>You:</strong> <code>remind me tomorrow at 3pm to call mom</code></p>
                <p><strong>Agent:</strong> <code>✅ Saved task #1: 'call mom' for November 04 at 03:00 PM</code></p>
            </div>

            <div class="endpoint">
                <strong>A2A Endpoint:</strong><br>
                POST https://task-reminder-agent-hng-c5d935d03667.herokuapp.com/a2a/agent/taskAgent
            </div>

            <div class="buttons">
                <a href="/static/login.html" class="btn btn-primary">🔐 Login / Dashboard</a>
                <a href="/static/test.html" class="btn btn-primary">🧪 Try it Now!</a>
                <a href="/docs" class="btn btn-primary">📚 API Documentation</a>
                <a href="/redoc" class="btn btn-secondary">📖 ReDoc</a>
                <a href="/tasks" class="btn btn-secondary">📋 View Tasks</a>
                <a href="https://github.com/Kalanza/telex-task-agent" target="_blank" class="btn btn-secondary">
                    💻 GitHub Repo
                </a>
            </div>

            <div style="margin-top: 40px; text-align: center; color: #666; font-size: 0.9em;">
                <p>Built with ❤️ using FastAPI, Python & Telex A2A Protocol</p>
                <p style="margin-top: 5px;">© 2025 Victor Kalanza | HNG Internship Stage 3</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/trigger-reminders")
def trigger_reminders():
    """Manual endpoint to trigger reminder check (for testing)"""
    from scheduler import reminder_job
    log("Manual reminder check triggered", "info")
    reminder_job()
    return {"status": "Reminder check executed"}


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint for real-time task updates and reminders.
    
    Connect to: ws://your-domain/ws/your_username
    
    Receives:
    - Real-time task reminders
    - Task updates
    - System notifications
    """
    await manager.connect(websocket)
    try:
        # Send welcome message
        await manager.send_personal_message(
            json.dumps({
                "type": "connected",
                "message": f"✅ Connected to Task Reminder Agent",
                "user": user_id,
                "timestamp": datetime.now().isoformat()
            }),
            websocket
        )
        
        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Handle different message types
            if message_data.get("type") == "ping":
                await manager.send_personal_message(
                    json.dumps({"type": "pong", "timestamp": datetime.now().isoformat()}),
                    websocket
                )
            elif message_data.get("type") == "task_query":
                # Send task updates
                tasks = get_all_tasks(user=user_id)
                await manager.send_personal_message(
                    json.dumps({
                        "type": "task_list",
                        "tasks": tasks,
                        "count": len(tasks)
                    }),
                    websocket
                )
            else:
                # Echo back for testing
                await manager.send_personal_message(
                    json.dumps({
                        "type": "echo",
                        "received": message_data,
                        "timestamp": datetime.now().isoformat()
                    }),
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        log(f"User {user_id} disconnected from WebSocket", "info")
    except Exception as e:
        log(f"WebSocket error for user {user_id}: {e}", "error")
        manager.disconnect(websocket)


# Helper function to send WebSocket notifications (can be called from scheduler)
async def send_websocket_reminder(user: str, task_text: str, task_id: int):
    """Send reminder via WebSocket to connected clients"""
    message = json.dumps({
        "type": "reminder",
        "task_id": task_id,
        "task": task_text,
        "message": f"⏰ Reminder: {task_text}",
        "timestamp": datetime.now().isoformat()
    })
    await manager.broadcast(message)
    log(f"WebSocket reminder sent for task #{task_id}", "info")
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


@app.post("/a2a/agent/taskAgent")
async def a2a_agent(request: Request):
    """
    A2A Protocol endpoint for Telex integration.
    This endpoint follows the Agent-to-Agent protocol specification.
    """
    try:
        payload = await request.json()
        log(f"A2A Request received: {payload}", "debug")
        
        # Extract message from A2A protocol payload
        # A2A protocol typically sends: {"message": "...", "user": "...", "context": {...}}
        message = payload.get("message", "")
        user = payload.get("user", payload.get("sender", "unknown-user"))
        
        if not message:
            return {
                "success": False,
                "error": "No message provided",
                "response": "❓ No message received"
            }
        
        # Process through your agent
        reply = process_message(user, message)
        log(f"A2A Reply to {user}: {reply}", "info")
        
        # Return A2A protocol response
        return {
            "success": True,
            "response": reply,
            "agent": "taskAgent",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        log(f"A2A Error: {e}", "error")
        return {
            "success": False,
            "error": str(e),
            "response": "❌ An error occurred processing your request"
        }


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 9000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
