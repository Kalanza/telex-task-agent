import logging
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_dir / 'app.log'),  # Log to file
        logging.StreamHandler()                     # Also log to console
    ]
)

logger = logging.getLogger(__name__)


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
    level = level.lower()
    
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "debug":
        logger.debug(message)
    else:
        logger.info(message)  # Default to info
