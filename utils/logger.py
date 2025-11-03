import logging
from datetime import datetime
from pathlib import Path
import sys

# Create logs directory if it doesn't exist
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# Check if running on Windows with limited encoding
WINDOWS_ENCODING_FIX = sys.platform == 'win32' and sys.stdout.encoding.lower() in ['cp1252', 'windows-1252']

# Configure logging with UTF-8 encoding for Windows compatibility
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_dir / 'app.log', encoding='utf-8'),  # Log to file with UTF-8
        logging.StreamHandler()                                       # Console logging
    ]
)

logger = logging.getLogger(__name__)


def _clean_emoji(message: str) -> str:
    """Remove or replace emojis for Windows console compatibility."""
    if not WINDOWS_ENCODING_FIX:
        return message
    
    # Replace common emojis with ASCII equivalents
    replacements = {
        '✅': '[OK]',
        '❌': '[ERROR]',
        '⏰': '[REMINDER]',
        '❓': '[?]',
        '🔄': '[RELOAD]',
        '📝': '[LOG]',
        '💾': '[SAVE]',
        '🚀': '[LAUNCH]',
    }
    
    for emoji, replacement in replacements.items():
        message = message.replace(emoji, replacement)
    
    return message


def log(message: str, level: str = "info") -> None:
    """
    Simple logging function with multiple log levels.
    
    Args:
        message: The message to log
        level: Log level - "info", "warning", "error", "debug" (default: "info")
    
    Examples:
        log("Server started")
        log("Missing required field", "warning")
        log("Database connection failed", "error")
    """
    # Clean emojis for Windows console if needed
    clean_message = _clean_emoji(message)
    
    level = level.lower()
    
    if level == "info":
        logger.info(clean_message)
    elif level == "warning":
        logger.warning(clean_message)
    elif level == "error":
        logger.error(clean_message)
    elif level == "debug":
        logger.debug(clean_message)
    else:
        logger.info(clean_message)  # Default to info
