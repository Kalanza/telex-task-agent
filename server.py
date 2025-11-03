from fastapi import FastAPI, Request
from agents.task_agent import process_message
from db.database import init_db
from utils.logger import log
import uvicorn

app = FastAPI()

# Initialize DB when server starts
init_db()
log("Database initialized successfully", "info")

@app.get("/")
def home():
    return {"status": "Reminder Agent Online ✔️"}

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
