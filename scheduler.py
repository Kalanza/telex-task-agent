from apscheduler.schedulers.background import BackgroundScheduler
from db.database import get_due_tasks, mark_task_sent
from utils.telex import send_reminder
from utils.logger import log
from datetime import datetime

# Global scheduler instance
scheduler = None


def reminder_job():
    """
    Background job that checks for due tasks and sends reminders.
    Runs periodically to check if any tasks need reminders.
    """
    try:
        log("Running reminder check...", "debug")
        
        # Get all tasks that are due and haven't been sent
        tasks = get_due_tasks()
        
        if not tasks:
            log("No due tasks found", "debug")
            return
        
        log(f"Found {len(tasks)} due task(s)", "info")
        
        # Send reminder for each due task
        for task in tasks:
            task_id, user, task_text, time_str, status, sent = task
            
            log(f"Processing reminder for task #{task_id}: '{task_text}' for user '{user}'", "info")
            
            # Send the reminder
            success = send_reminder(user, task_text, task_id)
            
            if success:
                # Mark task as sent
                mark_task_sent(task_id)
                log(f"✅ Reminder sent and marked: Task #{task_id}", "info")
            else:
                log(f"❌ Failed to send reminder for task #{task_id}", "error")
                
    except Exception as e:
        log(f"Error in reminder job: {e}", "error")


def start_scheduler():
    """
    Start the background scheduler for reminder checking.
    Checks for due tasks every 30 seconds.
    """
    global scheduler
    
    if scheduler is not None:
        log("Scheduler already running", "warning")
        return
    
    try:
        scheduler = BackgroundScheduler()
        
        # Add job to check for reminders every 30 seconds
        scheduler.add_job(
            reminder_job,
            'interval',
            seconds=30,
            id='reminder_check',
            name='Check for due reminders',
            replace_existing=True
        )
        
        scheduler.start()
        log("✅ Reminder scheduler started (checking every 30 seconds)", "info")
        
    except Exception as e:
        log(f"Failed to start scheduler: {e}", "error")
        raise


def stop_scheduler():
    """Stop the background scheduler."""
    global scheduler
    
    if scheduler is not None:
        scheduler.shutdown()
        scheduler = None
        log("Scheduler stopped", "info")
