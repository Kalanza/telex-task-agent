# 🤖 Task Reminder Agent

> A modern, AI-powered task management system that transforms natural language into actionable reminders. Never forget important tasks again with intelligent scheduling, real-time notifications, and beautiful analytics.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![WebSocket](https://img.shields.io/badge/WebSocket-Enabled-brightgreen.svg)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
[![Heroku](https://img.shields.io/badge/deployed-Heroku-purple.svg)](https://task-reminder-agent-hng-c5d935d03667.herokuapp.com/)

## 🌟 Overview

**Task Reminder Agent** is a sophisticated task management application that understands how humans naturally communicate. Built with cutting-edge technologies, it combines the power of natural language processing, real-time WebSocket communication, and automated scheduling to create a seamless task management experience.

**What makes it special?**
- 🧠 **Smart NLP**: Just tell it "remind me tomorrow at 3pm to call mom" - no complex forms or date pickers
- ⚡ **Real-time Everything**: WebSocket-powered live updates, instant notifications, zero page refreshes needed
- 📊 **Insightful Analytics**: Visualize your productivity patterns with interactive charts and metrics
- 🎨 **Beautiful UI**: Modern, responsive interface with dark mode and smooth animations
- 🤖 **A2A Integration**: Seamlessly integrates with Telex messaging platform for agent-to-agent communication
- 🔔 **Never Miss Deadlines**: Automated background scheduler checks every 30 seconds and delivers timely reminders

Whether you're managing personal tasks, team projects, or building an AI agent ecosystem, Task Reminder Agent provides the robust infrastructure you need with an interface so beautiful, you'll actually want to use it.

## 🚀 Live Demo

🌐 **Production App**: [https://task-reminder-agent-hng-c5d935d03667.herokuapp.com/](https://task-reminder-agent-hng-c5d935d03667.herokuapp.com/)

**Try it now:**
- 📱 [Main Dashboard](https://task-reminder-agent-hng-c5d935d03667.herokuapp.com/) - View and manage all your tasks
- 🎯 [Tasks Page](https://task-reminder-agent-hng-c5d935d03667.herokuapp.com/tasks) - Advanced filtering and statistics
- 🔬 [Interactive Tester](https://task-reminder-agent-hng-c5d935d03667.herokuapp.com/static/test.html) - Test the API in real-time
- 📚 [API Documentation](https://task-reminder-agent-hng-c5d935d03667.herokuapp.com/docs) - Full API reference

**Quick API Test:**
```bash
curl -X POST https://task-reminder-agent-hng-c5d935d03667.herokuapp.com/a2a/agent/taskAgent \
  -H "Content-Type: application/json" \
  -d '{"message": "remind me at 5pm to check emails", "user": "demo-user"}'
```

## ✨ Features

### Core Features
- 💬 **Natural Language Processing**: Speak naturally - "remind me at 5pm to study", "tomorrow at 3pm call mom"
- ⏰ **Automated Reminders**: Background scheduler monitors tasks 24/7, sends reminders at exact times
- 🔄 **Webhook Integration**: Seamless Telex platform integration via HTTP webhooks
- 📅 **Smart Time Parsing**: Understands diverse formats - relative (tomorrow, next week) and absolute (5pm, 17:00)
- 🗂️ **Comprehensive API**: Full CRUD operations - create, read, update, delete, snooze tasks
- 💾 **Persistent Storage**: SQLite database with ACID compliance and migration support
- 🌐 **RESTful Architecture**: Clean API design following REST best practices

### Advanced UI Features
- 🎨 **Modern Dashboard**: Sleek, intuitive interface with card-based task visualization
- 📊 **Analytics & Insights**: Interactive charts, completion rates, productivity streaks, response times
- 📅 **Calendar Integration**: Visual calendar with task highlighting and date navigation
- 🌙 **Dark Mode**: Eye-friendly theme with seamless switching and preference persistence
- 🔐 **User Authentication**: Secure login system with session management and guest access
- ⚡ **Real-time WebSocket**: Instant updates, live notifications, no manual refresh required
- 🔔 **Smart Notifications**: Browser push notifications with audio alerts and customization
- 📱 **Fully Responsive**: Perfect experience on desktop, tablet, and mobile devices
- 🎭 **Beautiful Animations**: Smooth transitions, hover effects, and loading states
- 🎨 **Modern Color Scheme**: Professional blue-teal gradient design

### Technical Excellence
- 📝 **Production Logging**: Comprehensive file and console logging with multiple log levels
- 🧪 **Test Coverage**: Unit tests, integration tests, and mock infrastructure
- 🚀 **Production Ready**: Error handling, graceful shutdown, health checks, CORS configuration
- 🔗 **A2A Protocol**: Agent-to-Agent communication for building AI agent ecosystems
- 🔒 **Security**: Input validation, SQL injection prevention, XSS protection
- ⚙️ **Configurable**: Environment variables, adjustable scheduler intervals, flexible limits
- 📖 **Documentation**: Auto-generated Swagger UI and ReDoc API documentation
- 🐳 **Deployment Ready**: Heroku/Railway/Render compatible with Procfile configuration

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                    Client Layer                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Dashboard   │  │   Calendar   │  │  Analytics   │        │
│  │  (React-UI)  │  │    View      │  │   Charts     │        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │
│         │                  │                  │                 │
│         └──────────────────┴──────────────────┘                 │
│                            │                                     │
│                  WebSocket & REST API                           │
└────────────────────────────┼───────────────────────────────────┘
                             │
┌────────────────────────────┼───────────────────────────────────┐
│                            ▼                                     │
│              FastAPI Application Server                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  server.py - HTTP + WebSocket Endpoints                  │  │
│  │  • REST API (/tasks, /a2a/agent/taskAgent)              │  │
│  │  • WebSocket Manager (Real-time connections)             │  │
│  │  • Static File Serving                                   │  │
│  │  • CORS Middleware                                       │  │
│  └─────────────┬────────────────────────┬───────────────────┘  │
│                │                         │                       │
│         ┌──────▼────────┐        ┌──────▼───────┐              │
│         │  Task Agent   │        │  Scheduler   │              │
│         │  (NLP Logic)  │        │ (APScheduler)│              │
│         └───────┬───────┘        └──────┬───────┘              │
│                 │                        │                       │
│         ┌───────▼────────┐       ┌──────▼───────┐              │
│         │   NLP Parser   │       │ Reminder Job │              │
│         │  (dateparser)  │       │ (Every 30s)  │              │
│         └────────────────┘       └──────┬───────┘              │
│                                          │                       │
│                                  ┌───────▼────────┐             │
│                                  │  Telex/Webhook │             │
│                                  │  Notification  │             │
│                                  └────────────────┘             │
└────────────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────▼───────────────────────────────────┐
│                    Data Layer                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  SQLite Database (tasks.db)                              │  │
│  │  • tasks table (CRUD operations)                         │  │
│  │  • Auto-incrementing IDs                                 │  │
│  │  • Indexed queries                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Logging System (logs/app.log)                           │  │
│  │  • Structured logging                                    │  │
│  │  • Multi-level (INFO, WARNING, ERROR, DEBUG)            │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│              External Integrations                              │
│  ┌──────────────────────┐    ┌──────────────────────┐         │
│  │  Telex Platform      │    │  Browser WebSocket   │         │
│  │  (A2A Protocol)      │    │  (Real-time Client)  │         │
│  └──────────────────────┘    └──────────────────────┘         │
└────────────────────────────────────────────────────────────────┘
```

**Data Flow:**
1. **Input**: User sends natural language message via Telex webhook or Dashboard UI
2. **Processing**: NLP parser extracts task description and reminder time
3. **Storage**: Task saved to SQLite database with metadata
4. **Scheduling**: Background scheduler monitors database every 30 seconds
5. **Reminder**: At scheduled time, reminder sent via Telex webhook + WebSocket
6. **Real-time Update**: Connected clients receive instant notification via WebSocket

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
- **Python 3.11+** (Python 3.8+ supported but 3.11+ recommended)
- **pip** package manager
- **Git** for cloning the repository

### Installation

```bash
# Clone the repository
git clone https://github.com/Kalanza/telex-task-agent.git
cd telex-task-agent

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database (automatic on first run)
# Database file will be created at: db/tasks.db
```

### Running Locally

```bash
# Start the server
python server.py

# Server will start on http://localhost:9000
# Watch for the startup message:
# "✅ Reminder scheduler started"
# "Uvicorn running on http://0.0.0.0:9000"
```

### Access the Application

Once running, open your browser and visit:

- **🏠 Main Dashboard**: [http://localhost:9000/](http://localhost:9000/)
- **📋 All Tasks**: [http://localhost:9000/tasks](http://localhost:9000/tasks)
- **🔐 Login Page**: [http://localhost:9000/static/login.html](http://localhost:9000/static/login.html)
- **🧪 API Tester**: [http://localhost:9000/static/test.html](http://localhost:9000/static/test.html)
- **📚 API Docs**: [http://localhost:9000/docs](http://localhost:9000/docs) (Swagger UI)
- **📖 ReDoc**: [http://localhost:9000/redoc](http://localhost:9000/redoc) (Alternative docs)

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

The application supports configuration via environment variables. Create a `.env` file in the root directory (this file is automatically ignored by `.gitignore` for security):

```bash
# Optional: Telex webhook URL for sending reminders
# If not set, reminders will only be logged and sent via WebSocket
TELEX_WEBHOOK_URL=https://your-telex-instance.com/api/webhook

# Optional: Server configuration
PORT=9000
HOST=0.0.0.0

# Optional: Database path (default: db/tasks.db)
DATABASE_PATH=db/tasks.db
```

**Important Security Notes:**
- ⚠️ **Never commit `.env` files to version control**
- ⚠️ **Never hardcode API keys or secrets in your code**
- ✅ Always use environment variables for sensitive configuration
- ✅ The `.gitignore` file already protects `.env`, `.env.local`, and database files

### Scheduler Settings

To adjust the reminder check interval, edit `scheduler.py`:

```python
# Default: Check every 30 seconds
scheduler.add_job(
    reminder_job,
    'interval',
    seconds=30  # Adjust this value (minimum: 10 seconds recommended)
)
```

**Performance Considerations:**
- Lower interval (e.g., 10s) = More responsive, higher CPU usage
- Higher interval (e.g., 60s) = Less responsive, lower CPU usage
- Recommended: 30 seconds for optimal balance

## 🔒 Security Best Practices

This application follows security best practices to protect your data:

### Built-in Security Features
- ✅ **SQL Injection Prevention**: Parameterized queries throughout
- ✅ **XSS Protection**: HTML escaping in frontend rendering
- ✅ **CORS Configuration**: Controlled cross-origin requests
- ✅ **Input Validation**: FastAPI Pydantic models validate all inputs
- ✅ **Sensitive Data Protection**: `.gitignore` prevents accidental commits of:
  - Environment variables (`.env`, `.env.local`)
  - Database files (`*.db`, `*.sqlite`)
  - Log files (`*.log`, `logs/`)
  - Virtual environments (`venv/`, `env/`)
  - IDE configurations (`.vscode/`, `.idea/`)
  - Python cache files (`__pycache__/`, `*.pyc`)

### What's Safe to Commit
✅ Source code (`.py` files)  
✅ Static assets (`static/` folder)  
✅ Configuration templates  
✅ Documentation (`.md` files)  
✅ Requirements file (`requirements.txt`)  
✅ `.gitignore` file  

### What's Protected (Never Committed)
❌ Environment variables (`.env`)  
❌ Database files (`.db`, `.sqlite`)  
❌ Log files (`.log`)  
❌ API keys, tokens, secrets  
❌ User credentials  
❌ Virtual environment folders  

### Deployment Security
When deploying to production:
1. Use environment variables for all sensitive configuration
2. Enable HTTPS/TLS encryption
3. Set strong authentication if exposing publicly
4. Regularly update dependencies: `pip install --upgrade -r requirements.txt`
5. Monitor logs for suspicious activity
6. Use secure database connections if using external databases

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

Core production dependencies with their purposes:

| Package | Version | Purpose |
|---------|---------|---------|
| **FastAPI** | 0.104+ | Modern async web framework with automatic API docs |
| **Uvicorn** | 0.24+ | Lightning-fast ASGI server for production |
| **WebSockets** | 12.0+ | Real-time bidirectional communication protocol |
| **APScheduler** | 3.10+ | Background job scheduling for automated reminders |
| **dateparser** | 1.2+ | Natural language date/time parsing |
| **requests** | 2.31+ | HTTP client for external webhook calls |
| **sqlite-utils** | 3.38+ | SQLite database utilities and helpers |
| **Pydantic** | 2.0+ | Data validation using Python type hints |

Development dependencies:

| Package | Version | Purpose |
|---------|---------|---------|
| **pytest** | Latest | Testing framework for unit and integration tests |
| **pytest-cov** | Latest | Code coverage reporting |
| **httpx** | Latest | Async HTTP client for testing |

**Total Size**: ~40MB installed (lightweight and efficient)

**Installation:**
```bash
# Production dependencies only
pip install -r requirements.txt

# With development dependencies
pip install -r requirements.txt pytest pytest-cov httpx
```

## 🚢 Deployment

### Heroku Deployment

This project is production-ready and deployed on Heroku. Follow these steps to deploy your own instance:

```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name

# Add Python buildpack (automatic detection)
heroku buildpacks:set heroku/python

# Set environment variables (if needed)
heroku config:set TELEX_WEBHOOK_URL=https://your-webhook-url

# Deploy
git push heroku master

# Open your app
heroku open

# View logs
heroku logs --tail
```

**Heroku Configuration Files:**
- `Procfile`: Defines the web process command
- `runtime.txt`: Specifies Python version (can be replaced with `.python-version`)
- `requirements.txt`: Lists all Python dependencies

### Railway Deployment

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Set environment variables
railway variables set TELEX_WEBHOOK_URL=https://your-webhook-url
```

### Render Deployment

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set the following:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
   - **Environment**: Python 3.11
4. Add environment variables in the dashboard
5. Deploy!

### Docker Deployment (Optional)

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 9000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:9000/')"

# Run the application
CMD ["python", "server.py"]
```

**Build and run:**
```bash
docker build -t task-reminder-agent .
docker run -p 9000:9000 -e TELEX_WEBHOOK_URL=your-url task-reminder-agent
```

### Environment Variables for Production

Set these in your hosting platform's dashboard:

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `TELEX_WEBHOOK_URL` | Optional | Webhook URL for Telex notifications | `https://telex.example.com/webhook` |
| `PORT` | Auto-set | Port number (usually set by platform) | `9000` |
| `DATABASE_PATH` | Optional | Custom database location | `db/tasks.db` |

## 🤝 Contributing

Contributions are welcome and appreciated! Here's how you can help:

### Ways to Contribute
- 🐛 Report bugs and issues
- 💡 Suggest new features or enhancements
- 📝 Improve documentation
- 🧪 Add tests or improve test coverage
- 🎨 Enhance UI/UX design
- 🔧 Submit bug fixes or new features

### Contribution Process
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/telex-task-agent.git
cd telex-task-agent

# Add upstream remote
git remote add upstream https://github.com/Kalanza/telex-task-agent.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run with auto-reload for development
uvicorn server:app --reload --port 9000
```

### Code Style
- Follow PEP 8 Python style guide
- Use type hints where appropriate
- Add docstrings for functions and classes
- Keep functions focused and concise
- Write meaningful commit messages

## 🎯 Use Cases

This application is perfect for:

- **Personal Productivity**: Manage daily tasks and reminders
- **Team Collaboration**: Share task management across teams
- **AI Agent Ecosystems**: Integrate with Telex A2A protocol for multi-agent systems
- **Educational Projects**: Learn FastAPI, WebSockets, and async programming
- **Prototyping**: Quick foundation for task management features
- **API Development**: Reference implementation for REST + WebSocket architecture

## 🛣️ Roadmap

Future enhancements planned:

- [ ] Multi-user authentication with JWT tokens
- [ ] Email/SMS notification options
- [ ] Recurring tasks (daily, weekly, monthly)
- [ ] Task categories and tags
- [ ] Priority levels (high, medium, low)
- [ ] Task sharing and collaboration
- [ ] Mobile app (React Native)
- [ ] Export tasks (CSV, JSON, iCal)
- [ ] Integration with Google Calendar, Outlook
- [ ] Voice input support
- [ ] Task templates
- [ ] Advanced analytics and reporting
- [ ] Machine learning for smart scheduling suggestions

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

**You are free to:**
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Use privately

**Conditions:**
- 📝 Include copyright notice
- 📝 Include license text

## 🙏 Acknowledgments

Built with love using these amazing open-source projects:

- **FastAPI** - For the incredible web framework
- **dateparser** - For natural language date parsing
- **APScheduler** - For reliable background job scheduling
- **Telex Platform** - For A2A protocol integration
- **Heroku** - For seamless deployment platform
- **Python Community** - For the amazing ecosystem

## 📞 Contact & Support

**Developer**: Victor Kalanza  
**GitHub**: [@Kalanza](https://github.com/Kalanza)  
**Repository**: [telex-task-agent](https://github.com/Kalanza/telex-task-agent)  
**Live Demo**: [task-reminder-agent-hng-c5d935d03667.herokuapp.com](https://task-reminder-agent-hng-c5d935d03667.herokuapp.com/)

### Getting Help
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/Kalanza/telex-task-agent/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Kalanza/telex-task-agent/discussions)
- 📖 **Documentation**: [GitHub Wiki](https://github.com/Kalanza/telex-task-agent/wiki)
- ⭐ **Star the repo** if you find it useful!

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/Kalanza/telex-task-agent?style=social)
![GitHub forks](https://img.shields.io/github/forks/Kalanza/telex-task-agent?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/Kalanza/telex-task-agent?style=social)
![GitHub repo size](https://img.shields.io/github/repo-size/Kalanza/telex-task-agent)
![GitHub language count](https://img.shields.io/github/languages/count/Kalanza/telex-task-agent)
![GitHub top language](https://img.shields.io/github/languages/top/Kalanza/telex-task-agent)
![GitHub last commit](https://img.shields.io/github/last-commit/Kalanza/telex-task-agent)

---

<div align="center">

**Built with ❤️ by [Kalanza](https://github.com/Kalanza)**

*If this project helped you, please consider giving it a ⭐ star!*

[Live Demo](https://task-reminder-agent-hng-c5d935d03667.herokuapp.com/) • [Report Bug](https://github.com/Kalanza/telex-task-agent/issues) • [Request Feature](https://github.com/Kalanza/telex-task-agent/issues)

</div>
