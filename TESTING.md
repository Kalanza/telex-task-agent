# Testing the Reminder System

## Quick Test Guide

### 1. Start the Server
```bash
python server.py
```

You should see:
```
INFO: Database initialized successfully
INFO: ✅ Reminder scheduler started (checking every 30 seconds)
INFO: Uvicorn running on http://0.0.0.0:9000
```

### 2. Create a Task with a Time in the Past (for immediate testing)
```powershell
$body = @{
    sender = "alice"
    message = "remind me at 2pm to test the system"  # Use a past time
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:9000/webhook/telex" -Method POST -ContentType "application/json" -Body $body
```

### 3. Manually Trigger Reminder Check
```bash
curl http://localhost:9000/trigger-reminders
```

### 4. Check Logs
Look for:
```
INFO: Running reminder check...
INFO: Found 1 due task(s)
INFO: Processing reminder for task #1: 'test the system' for user 'alice'
INFO: Reminder sent to alice: ⏰ Reminder: test the system (Task #1)
INFO: ✅ Reminder sent and marked: Task #1
```

### 5. Test with Future Time
```powershell
$body = @{
    sender = "bob"
    message = "remind me in 2 minutes to call mom"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:9000/webhook/telex" -Method POST -ContentType "application/json" -Body $body
```

Wait 2 minutes and the scheduler will automatically send the reminder!

## Endpoints

- **GET /** - Health check
- **POST /webhook/telex** - Receive messages from Telex
- **GET /trigger-reminders** - Manually trigger reminder check (testing only)
- **GET /docs** - Interactive API documentation

## Environment Variables

```bash
# Optional: Configure Telex webhook URL
export TELEX_WEBHOOK_URL="https://your-telex-instance.com/api/webhook"
```

## Database Schema

Tasks table now includes:
- `id` - Primary key
- `user` - Username
- `task` - Task description
- `time` - Scheduled time (ISO format)
- `status` - Task status ('pending', 'sent', 'completed')
- `sent` - Boolean flag (0 = not sent, 1 = sent)

## Troubleshooting

### Reminders not sending?
1. Check logs: `cat logs/app.log`
2. Verify database has due tasks: Check `db/tasks.db`
3. Ensure scheduler is running: Look for "Reminder scheduler started" message
4. Manually trigger: `curl http://localhost:9000/trigger-reminders`

### How often does it check?
Every 30 seconds by default. Modify in `scheduler.py`:
```python
scheduler.add_job(reminder_job, 'interval', seconds=30)  # Change this
```
