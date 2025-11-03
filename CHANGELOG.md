# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Task management API endpoints
- Comprehensive test suite
- Mock Telex server for testing

## [0.3.0] - 2025-11-03

### Added
- **Task Management API**
  - `GET /tasks` - List all tasks with filtering
  - `DELETE /tasks/{id}` - Delete tasks
  - `PATCH /tasks/{id}` - Update task details
  - `POST /tasks/{id}/snooze` - Snooze tasks
- **Testing Suite**
  - Scheduler tests (`test_scheduler.py`)
  - Integration tests (`test_integration.py`)
  - Mock Telex server for testing
- **Database Functions**
  - `get_all_tasks()` - Retrieve tasks with filters
  - `delete_task()` - Delete by ID
  - `update_task()` - Update task fields
  - `snooze_task()` - Delay task execution

### Changed
- Enhanced database module with full CRUD operations
- Improved error handling in API endpoints
- Better logging for task operations

## [0.2.0] - 2025-11-03

### Added
- **Automated Reminder System**
  - APScheduler background job
  - Checks for due tasks every 30 seconds
  - Automatic reminder delivery via Telex
- **Telex Integration** (`utils/telex.py`)
  - Send messages back to users
  - Configurable webhook URL
  - Error handling and logging
- **Database Enhancements**
  - Added `sent` column to track delivery status
  - `get_due_tasks()` function
  - `mark_task_sent()` function
- **Scheduler Module** (`scheduler.py`)
  - Background job management
  - Start/stop lifecycle
  - Manual trigger endpoint
- **Logging System** (`utils/logger.py`)
  - File logging (`logs/app.log`)
  - Console logging
  - Multiple log levels (info, warning, error, debug)
- **Documentation**
  - Comprehensive README
  - Testing guide (TESTING.md)

### Changed
- Server now auto-starts scheduler on startup
- Database schema includes reminder tracking

## [0.1.0] - 2025-11-02

### Added
- **Core Functionality**
  - Natural language processing for task extraction
  - SQLite database for task storage
  - FastAPI webhook server
  - CLI interface
- **Modules**
  - `agents/task_agent.py` - Business logic
  - `db/database.py` - Database operations
  - `utils/nlp.py` - NLP processing
  - `server.py` - FastAPI server
  - `main.py` - CLI interface
- **Features**
  - Natural language task input
  - Time parsing (various formats)
  - User-friendly emoji responses
  - Error validation and handling
- **API Endpoints**
  - `GET /` - Health check
  - `POST /webhook/telex` - Receive messages
  - `GET /docs` - Interactive API documentation
- **Testing**
  - Basic NLP tests (`test_nlp.py`)
- **Project Setup**
  - `.gitignore` for Python projects
  - `requirements.txt` with dependencies
  - Virtual environment support

### Technical Stack
- Python 3.8+
- FastAPI for web framework
- SQLite for database
- dateparser for NLP
- pytest for testing
- APScheduler for background jobs

---

## Version History

- **v0.3.0** - Task Management & Testing (2025-11-03)
- **v0.2.0** - Scheduler & Reminders (2025-11-03)
- **v0.1.0** - Initial Release (2025-11-02)
