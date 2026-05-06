# Last updated: 2026-05-06
import sys
from colorama import Back, Style
from config import BOT_TOKEN_TEST, RIOT_API_KEY
from Logs.logs import verification_error, verification_success

REQUIRED_ENV = {
    "BOT_TOKEN_TEST": BOT_TOKEN_TEST,
    "RIOT_API_KEY": RIOT_API_KEY,
}


def security_check():
    """Verify required env is present before booting the bot."""
    missing = [name for name, value in REQUIRED_ENV.items() if not value]
    if missing:
        msg = f"Missing required env variables: {', '.join(missing)}"
        print(Back.RED + msg + Style.RESET_ALL)
        verification_error(msg)
        sys.exit(1)
    verification_success()
    print(Back.GREEN + "Environment variables are set correctly" + Style.RESET_ALL)
