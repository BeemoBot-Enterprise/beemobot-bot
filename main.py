# Last updated: 2026-05-06
"""Bot entry point. Defaults to BOT_TOKEN_TEST in dev, BOT_TOKEN_PROD when ENV=production."""
import os
import logging
from Verification.verification import security_check
from Discord.bot import bot
from config import BOT_TOKEN_PROD, BOT_TOKEN_TEST

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")


def launch():
    security_check()
    token = BOT_TOKEN_PROD if os.getenv("ENV") == "production" else BOT_TOKEN_TEST
    bot.run(token)


if __name__ == "__main__":
    launch()
