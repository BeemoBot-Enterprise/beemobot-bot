# Last updated: 2026-05-06
"""Worker entrypoint. Loops every WORKER_INTERVAL_S."""
import asyncio
import logging
import os
from dotenv import load_dotenv

load_dotenv()
from worker.riot_poller import poll_all

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger("worker")

WORKER_INTERVAL_S = int(os.getenv("WORKER_INTERVAL_S", "300"))


async def main():
    while True:
        try:
            await poll_all()
        except Exception:
            logger.exception("poll_all crashed")
        logger.info("Sleeping %ds", WORKER_INTERVAL_S)
        await asyncio.sleep(WORKER_INTERVAL_S)


if __name__ == "__main__":
    asyncio.run(main())
