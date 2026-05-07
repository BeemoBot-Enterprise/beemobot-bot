# Last updated: 2026-05-07
"""Bot entry point. Defaults to BOT_TOKEN_TEST in dev, BOT_TOKEN_PROD when ENV=production."""
import asyncio
import os
import logging
from Verification.verification import security_check
from Discord.bot import bot
from worker.health_server import run_health_server
from config import BOT_TOKEN_PROD, BOT_TOKEN_TEST

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")


async def launch():
    security_check()
    token = BOT_TOKEN_PROD if os.getenv("ENV") == "production" else BOT_TOKEN_TEST

    async with bot:
        # Health endpoint runs in the same loop and reads live bot state.
        asyncio.create_task(run_health_server(bot))
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(launch())
