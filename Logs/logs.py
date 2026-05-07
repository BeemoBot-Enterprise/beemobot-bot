# Last updated: 2026-05-07
import logging
from datetime import datetime
from pathlib import Path

# Resolve path relative to this file so it works no matter the CWD,
# and create the directory if missing (e.g. fresh container).
LOG_DIR = Path(__file__).parent / 'logs_holder'
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / 'bot.log'
LOG_LEVEL = logging.INFO

# Log to file (for local dev) AND stdout (so Coolify / docker logs see it).
logging.basicConfig(
    handlers=[
        logging.FileHandler(str(LOG_FILE)),
        logging.StreamHandler(),
    ],
    level=LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

def log_timestamp():
    """Helper function to get the current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Logging functions
def starting_bot():
    logger.info('Bot started')

def stopping_bot():
    logger.info('Bot stopped')

def command_used(command, user):
    logger.info(f'Command used: {command} by {user}')

def command_error(command, error):
    logger.error(f'Error in command "{command}": {error}')

def command_success(command):
    logger.info(f'Command "{command}" executed successfully')

def error(error_msg):
    logger.error(f'Error: {error_msg}')

def verification_error(error_msg):
    logger.error(f'Verification error: {error_msg}')

def verification_success():
    logger.info('Verification succeeded')

def log_info(info_msg):
    logger.info(info_msg)
