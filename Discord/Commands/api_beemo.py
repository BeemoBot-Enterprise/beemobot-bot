# Last updated: 2026-05-06
"""Async client for the Beemo backend API. Uses aiohttp so it never blocks the bot's event loop."""
import logging
import aiohttp
from config import BEEMO_API_BASE_URL

logger = logging.getLogger(__name__)

GAME_URL = f"{BEEMO_API_BASE_URL}/game"
DEFAULT_TIMEOUT = aiohttp.ClientTimeout(total=10)


async def _post_json(path: str, payload: dict):
    url = f"{GAME_URL}{path}"
    try:
        async with aiohttp.ClientSession(timeout=DEFAULT_TIMEOUT) as session:
            async with session.post(url, json=payload) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as exc:
        logger.error("POST %s failed: %s", url, exc)
        return None


async def _get_json(path: str):
    url = f"{GAME_URL}{path}"
    try:
        async with aiohttp.ClientSession(timeout=DEFAULT_TIMEOUT) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as exc:
        logger.error("GET %s failed: %s", url, exc)
        return None


async def give_shroom(username: str):
    return await _post_json("/shroom", {"username": username})


async def give_respect(username: str):
    return await _post_json("/respect", {"username": username})


async def get_user_stats(username: str):
    return await _get_json(f"/stats/{username}")


async def get_top_shrooms():
    return await _get_json("/top/shrooms")


async def get_top_respects():
    return await _get_json("/top/respects")
