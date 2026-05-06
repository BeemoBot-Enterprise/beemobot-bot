# Last updated: 2026-05-06
"""Async client for the Beemo backend API. Uses aiohttp so it never blocks the bot's event loop."""
import logging
import aiohttp
from config import BEEMO_API_BASE_URL

logger = logging.getLogger(__name__)
DEFAULT_TIMEOUT = aiohttp.ClientTimeout(total=10)


async def _request(method: str, path: str, json: dict | None = None):
    url = f"{BEEMO_API_BASE_URL}{path}"
    try:
        async with aiohttp.ClientSession(timeout=DEFAULT_TIMEOUT) as session:
            async with session.request(method, url, json=json) as resp:
                if resp.status >= 400:
                    body = await resp.text()
                    logger.warning("%s %s -> %d: %s", method, url, resp.status, body)
                    return None
                return await resp.json()
    except aiohttp.ClientError as exc:
        logger.error("%s %s failed: %s", method, url, exc)
        return None


async def get_profile(puuid: str):
    return await _request("GET", f"/profile/{puuid}")


async def get_eligible(giver_puuid: str, receiver_puuid: str):
    return await _request(
        "GET",
        f"/rep/eligible?giverPuuid={giver_puuid}&receiverPuuid={receiver_puuid}",
    )


async def give_rep(payload: dict):
    return await _request("POST", "/rep/give", json=payload)
