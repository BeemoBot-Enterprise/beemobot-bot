# Last updated: 2026-05-07
import os
import sys
from colorama import Back, Style
from config import BOT_TOKEN_PROD, BOT_TOKEN_TEST, RIOT_API_KEY
from Logs.logs import verification_error, verification_success


def security_check():
    """Verify required env is present before booting the bot.

    In production (ENV=production) we require BOT_TOKEN_PROD; otherwise
    BOT_TOKEN_TEST. RIOT_API_KEY is always required.
    """
    is_prod = os.getenv("ENV") == "production"
    required = {
        "BOT_TOKEN_PROD" if is_prod else "BOT_TOKEN_TEST": BOT_TOKEN_PROD if is_prod else BOT_TOKEN_TEST,
        "RIOT_API_KEY": RIOT_API_KEY,
    }

    missing = [name for name, value in required.items() if not value]
    if missing:
        msg = f"Missing required env variables: {', '.join(missing)}"
        print(Back.RED + msg + Style.RESET_ALL)
        verification_error(msg)
        sys.exit(1)
    verification_success()
    print(Back.GREEN + "Environment variables are set correctly" + Style.RESET_ALL)
