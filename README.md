# 🤖 Task Reminder Agent

> AI-powered task management that understands natural language. Just say "remind me tomorrow at 3pm to call mom" and let the agent handle the rest.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

🌐 **Live Demo**: [https://task-reminder-agent-hng-c5d935d03667.herokuapp.com/](https://task-reminder-agent-hng-c5d935d03667.herokuapp.com/)

## Features

- 💬 **Natural Language Processing**: "remind me tomorrow at 3pm to call mom"
- ⏰ **Automated Reminders**: Background scheduler sends notifications at scheduled times
- ⚡ **Real-time Updates**: WebSocket-powered live notifications
- 📊 **Analytics Dashboard**: Track productivity with interactive charts
- 🌙 **Dark Mode**: Modern, responsive UI with theme switching
- 🔄 **RESTful API**: Full CRUD operations with Swagger documentation

## Project Structure

```
telex-task-agent/
├── agents/          # Task processing logic
├── db/              # SQLite database
├── static/          # Web UI (dashboard, login, test pages)
├── utils/           # NLP, logging, Telex integration
├── tests/           # Unit tests
├── scheduler.py     # APScheduler for reminders
├── server.py        # FastAPI server + WebSocket
└── main.py          # CLI interface
```

## Quick Start

### Installation

```bash
# Clone and setup
git clone https://github.com/Kalanza/telex-task-agent.git
cd telex-task-agent
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Run

```bash
python server.py
# Access at http://localhost:9000
```

## API Examples

### Create Task
```bash
curl -X POST http://localhost:9000/a2a/agent/taskAgent \
  -H "Content-Type: application/json" \
  -d '{"message": "remind me at 5pm to study", "user": "test-user"}'
```

### List Tasks
```bash
curl http://localhost:9000/tasks
```

## Key Endpoints

- `POST /a2a/agent/taskAgent` - Create task with natural language
- `GET /tasks` - List all tasks (filter by `?user=name&status=pending`)
- `PATCH /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task
- `POST /tasks/{id}/snooze` - Snooze task
- `WS /ws/{user_id}` - WebSocket for real-time updates
- `GET /docs` - Interactive API documentation

## Configuration

Optional environment variables:
```bash
TELEX_WEBHOOK_URL=https://your-telex-instance.com/api/webhook
PORT=9000
DATABASE_PATH=db/tasks.db
```

## Deployment

**Heroku:**
```bash
heroku create your-app-name
git push heroku master
```

**Docker:**
```bash
docker build -t task-agent .
docker run -p 9000:9000 task-agent
```

## License

MIT License - see [LICENSE](LICENSE) file.

## Contact

**Developer**: Victor Kalanza  
**Repository**: [telex-task-agent](https://github.com/Kalanza/telex-task-agent)  
**Live Demo**: [task-reminder-agent-hng-c5d935d03667.herokuapp.com](https://task-reminder-agent-hng-c5d935d03667.herokuapp.com/)

---

Built with ❤️ by [Kalanza](https://github.com/Kalanza)
