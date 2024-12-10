import logging
from datetime import datetime

# Configure the logger
LOG_FILE = 'logs/logs_holder/bot.log'
LOG_LEVEL = logging.INFO

logging.basicConfig(
    filename=LOG_FILE,
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
