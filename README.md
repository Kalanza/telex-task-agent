# 🤖 Telex Task Agent

> An intelligent task reminder bot with natural language processing, real-time WebSocket updates, advanced analytics, and a beautiful modern UI.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![WebSocket](https://img.shields.io/badge/WebSocket-Enabled-brightgreen.svg)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)

## ✨ Features

### Core Features
- 💬 **Natural Language Processing**: Type tasks naturally like "remind me at 5pm to study"
- ⏰ **Automated Reminders**: Background scheduler checks every 30 seconds and sends reminders
- 🔄 **Webhook Integration**: Receives messages from Telex platform via HTTP webhooks
- 📅 **Smart Time Parsing**: Understands various time formats (5pm, 17:00, tomorrow at 3pm)
- 🗂️ **Task Management API**: List, update, delete, and snooze tasks via REST endpoints
- 💾 **SQLite Database**: Persistent storage with migration support and CRUD operations

### Advanced Features
- 🎨 **Modern Dashboard UI**: Beautiful, responsive task management interface
- 📊 **Analytics Dashboard**: Charts, graphs, and productivity metrics
- 📅 **Calendar View**: Visual task calendar with date highlighting
- 🌙 **Dark Mode**: Toggle between light and dark themes
- 🔐 **User Authentication**: Login system with guest mode support
- ⚡ **Real-time WebSocket**: Live task updates and notifications without refresh
- 🔔 **Desktop Notifications**: Browser notifications for task reminders
- 📱 **Mobile Responsive**: Works seamlessly on all devices

### Technical Features
- 📝 **Comprehensive Logging**: File and console logging for debugging
- 🧪 **Full Test Coverage**: Unit and integration tests with mock infrastructure
- 🚀 **Production Ready**: Error handling, graceful shutdown, and health checks
- 🔗 **A2A Protocol**: Agent-to-Agent communication support

## 🏗️ Architecture

```
┌─────────────────────────────────┐
│     Telex Messaging Platform    │
│   (Sends/Receives Messages)     │
└─────────┬───────────────────────┘
          │ HTTP POST
          ▼
┌─────────────────────────────────┐
│   FastAPI Server (server.py)    │
│      Port 9000 - Webhooks       │
└─────────┬───────────────────────┘
          │
          ├──► Task Agent (agents/)
          │    └─► NLP Processor (utils/nlp.py)
          │    └─► Database (db/database.py)
          │
          └──► Scheduler (scheduler.py)
               └─► Reminder Job (every 30s)
                   └─► Telex API (utils/telex.py)
```

## 📁 Project Structure

```
telex-task-agent/
├── agents/
│   └── task_agent.py       # Business logic for task processing
├── db/
│   ├── database.py         # SQLite operations & schema
│   └── tasks.db           # Database file (created at runtime)
├── logs/
│   └── app.log            # Application logs (auto-created)
├── static/
│   ├── dashboard.html     # Advanced task dashboard
│   ├── login.html         # User authentication page
│   └── test.html          # Interactive API tester
├── utils/
│   ├── nlp.py             # Natural language processing
│   ├── logger.py          # Logging utilities
│   └── telex.py           # Telex API integration
├── tests/
│   └── test_nlp.py        # Unit tests
├── scheduler.py           # APScheduler for reminders
├── server.py              # FastAPI webhook server + WebSocket
├── main.py                # CLI interface
├── requirements.txt       # Python dependencies
└── README.md             # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Kalanza/telex-task-agent.git
cd telex-task-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Server

```bash
python server.py
```

Server starts on `http://localhost:9000`

**Access the Application:**
- Landing Page: http://localhost:9000/
- Login/Dashboard: http://localhost:9000/static/login.html
- Interactive Tester: http://localhost:9000/static/test.html
- API Documentation: http://localhost:9000/docs
- ReDoc: http://localhost:9000/redoc

### Dashboard Features

#### 1. **Login System** (`/static/login.html`)
- Username/password authentication (demo mode)
- Guest access option
- Persistent session storage

#### 2. **Task Dashboard** (`/static/dashboard.html`)
- **Tasks Tab**: Visual task list with real-time updates
  - Statistics cards (total, pending, completed, due today)
  - Filter buttons (all, pending, completed, today)
  - Edit, delete, and snooze actions
  - Real-time WebSocket notifications
  
- **Calendar Tab**: Visual calendar view
  - Navigate months (previous, today, next)
  - Tasks highlighted on dates
  - Click dates to view tasks
  
- **Analytics Tab**: Productivity metrics
  - Task creation chart (last 7 days)
  - Completion rate
  - Average response time
  - Productivity streak
  - Productivity score

#### 3. **Dark Mode**
- Toggle between light and dark themes
- Preference saved to localStorage
- Smooth theme transitions

#### 4. **Real-time Updates (WebSocket)**
- Live task reminders
- Instant task list refresh
- Browser notifications
- Audio alerts
- Auto-reconnection on disconnect

### Quick Test

```bash
# Test health endpoint
curl http://localhost:9000/

# Test A2A endpoint (main Telex integration point)
curl -X POST http://localhost:9000/a2a/agent/taskAgent \
  -H "Content-Type: application/json" \
  -d '{"message": "remind me at 5pm to study", "user": "test-user"}'

# Expected response:
# {"success": true, "response": "✅ Saved task #1: 'study' for ...", "agent": "taskAgent", "timestamp": "..."}
```

## 💡 Usage Examples

### Create a Task via Webhook

```powershell
$body = @{
    sender = "alice"
    message = "remind me tomorrow at 3pm to call mom"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:9000/webhook/telex" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**Response:**
```json
{
  "response": "✅ Saved task #1: 'call mom' for November 04 at 03:00 PM"
}
```

### Automatic Reminder Delivery

When the scheduled time arrives (3pm tomorrow), the scheduler automatically sends:

```
⏰ Reminder: call mom (Task #1)
```

### CLI Mode

```bash
python main.py alice

You: remind me at 5pm to study
Agent: ✅ Saved task #1: 'study' for November 03 at 05:00 PM
```

## 🔌 API Endpoints

### `GET /`
Health check endpoint
```json
{"status": "Reminder Agent Online ✔️"}
```

### `POST /webhook/telex`
Receive messages from Telex platform

**Request:**
```json
{
  "sender": "alice",
  "message": "remind me at 5pm to study"
}
```

**Response:**
```json
{
  "response": "✅ Saved task #1: 'study' for November 03 at 05:00 PM"
}
```

### `POST /a2a/agent/taskAgent`
A2A Protocol endpoint for Telex integration (Agent-to-Agent communication)

**Request:**
```json
{
  "message": "remind me at 5pm to study",
  "user": "victor-kalanza"
}
```

**Response:**
```json
{
  "success": true,
  "response": "✅ Saved task #1: 'study' for November 03 at 05:00 PM",
  "agent": "taskAgent",
  "timestamp": "2025-11-03T14:30:00.000000"
}
```

### `GET /trigger-reminders`
Manually trigger reminder check (testing only)

### `GET /tasks`
List all tasks with optional filters

**Query Parameters:**
- `user` (optional): Filter by username
- `status` (optional): Filter by status (pending/completed)
- `limit` (optional): Maximum tasks to return (default: 100)

**Response:**
```json
{
  "tasks": [
    {
      "id": 1,
      "user": "alice",
      "task": "call mom",
      "time": "2024-11-04 15:00:00",
      "status": "pending",
      "sent": 0
    }
  ],
  "count": 1
}
```

### `DELETE /tasks/{task_id}`
Delete a specific task

**Response:**
```json
{
  "success": true,
  "message": "Task 1 deleted"
}
```

### `PATCH /tasks/{task_id}`
Update task details

**Request:**
```json
{
  "task": "call dad instead",
  "time": "2024-11-04 16:00:00",
  "status": "pending"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Task 1 updated"
}
```

### `POST /tasks/{task_id}/snooze`
Snooze a task for specified minutes

**Request:**
```json
{
  "minutes": 30
}
```

**Response:**
```json
{
  "success": true,
  "message": "Task 1 snoozed for 30 minutes",
  "new_time": "2024-11-04 15:30:00"
}
```

### `GET /docs`
Interactive API documentation (Swagger UI)

### `WS /ws/{user_id}`
WebSocket endpoint for real-time task updates

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:9000/ws/alice');

ws.onopen = () => {
  console.log('Connected');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

// Send ping to keep alive
ws.send(JSON.stringify({ type: 'ping' }));

// Query tasks
ws.send(JSON.stringify({ type: 'task_query' }));
```

**Message Types:**

**Received Messages:**
```json
// Connection confirmation
{"type": "connected", "message": "✅ Connected", "user": "alice"}

// Task reminder
{"type": "reminder", "task_id": 1, "task": "study", "message": "⏰ Reminder: study"}

// Task list response
{"type": "task_list", "tasks": [...], "count": 5}

// Ping response
{"type": "pong", "timestamp": "2025-11-03T..."}
```

**Send Messages:**
```json
// Keep connection alive
{"type": "ping"}

// Request task list
{"type": "task_query"}
```

## ⚙️ Configuration

### Environment Variables

```bash
# Telex webhook URL for sending reminders
export TELEX_WEBHOOK_URL="https://your-telex-instance.com/api/webhook"
```

### Scheduler Settings

Edit `scheduler.py` to change check interval:
```python
scheduler.add_job(
    reminder_job,
    'interval',
    seconds=30  # Check every 30 seconds
)
```

## 🗄️ Database Schema

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    task TEXT NOT NULL,
    time DATETIME NOT NULL,
    status TEXT DEFAULT 'pending',
    sent BOOLEAN DEFAULT 0
);
```

## 📊 Logging

Logs are written to:
- **Console**: Real-time output
- **File**: `logs/app.log`

**Log Levels:**
- `INFO`: Normal operations
- `WARNING`: Non-critical issues
- `ERROR`: Failures and exceptions
- `DEBUG`: Detailed debugging info

**Example Log:**
```
2025-11-03 14:30:00 - __main__ - INFO - Database initialized successfully
2025-11-03 14:30:00 - __main__ - INFO - ✅ Reminder scheduler started
2025-11-03 14:30:15 - __main__ - INFO - From alice: remind me at 5pm to study
2025-11-03 14:30:15 - __main__ - INFO - ✅ Reminder sent and marked: Task #1
```

## 🧪 Testing

Run tests:
```bash
pytest tests/
```

Manual reminder trigger:
```bash
curl http://localhost:9000/trigger-reminders
```

See [TESTING.md](TESTING.md) for detailed testing guide.

## 📦 Dependencies

- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **WebSockets**: Real-time bidirectional communication
- **APScheduler**: Background job scheduling
- **dateparser**: Natural language date parsing
- **requests**: HTTP client for Telex API
- **sqlite-utils**: Database utilities
- **pytest**: Testing framework

## 🚢 Deployment

### Railway / Render

1. Connect GitHub repository
2. Set environment variables:
   - `TELEX_WEBHOOK_URL`
3. Deploy command: `python server.py`
4. Port: 9000

### Docker (Optional)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "server.py"]
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and open a PR

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with FastAPI and APScheduler
- Natural language parsing powered by dateparser
- Integrated with Telex messaging platform

## 📞 Support

- Issues: [GitHub Issues](https://github.com/Kalanza/telex-task-agent/issues)
- Documentation: [GitHub Wiki](https://github.com/Kalanza/telex-task-agent/wiki)

---

Made with ❤️ by [Kalanza](https://github.com/Kalanza)
