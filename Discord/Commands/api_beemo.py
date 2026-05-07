# Last updated: 2026-05-07
"""Async client for the Beemo backend API. Uses aiohttp so it never blocks the bot's event loop."""
import logging
import aiohttp
from config import BEEMO_API_BASE_URL, INTERNAL_API_KEY

logger = logging.getLogger(__name__)
DEFAULT_TIMEOUT = aiohttp.ClientTimeout(total=10)


def _internal_headers() -> dict[str, str]:
    """Headers attached to /worker/* server-to-server calls."""
    return {"X-Internal-Key": INTERNAL_API_KEY} if INTERNAL_API_KEY else {}


async def _request(method: str, path: str, json: dict | None = None, internal: bool = False):
    url = f"{BEEMO_API_BASE_URL}{path}"
    headers = _internal_headers() if internal else None
    try:
        async with aiohttp.ClientSession(timeout=DEFAULT_TIMEOUT) as session:
            async with session.request(method, url, json=json, headers=headers) as resp:
                if resp.status == 404:
                    # 404 may carry a structured error body — expose it to callers.
                    try:
                        return await resp.json()
                    except Exception:
                        return None
                if resp.status >= 400:
                    body = await resp.text()
                    logger.warning("%s %s -> %d: %s", method, url, resp.status, body)
                    return None
                if resp.content_length == 0 or resp.status == 204:
                    return {}
                return await resp.json()
    except aiohttp.ClientError as exc:
        logger.error("%s %s failed: %s", method, url, exc)
        return None


# ─── Public endpoints ─────────────────────────────────────────────────────────

async def get_debrief(discord_id: str):
    return await _request("GET", f"/lol/debrief/by-discord/{discord_id}")


async def get_profile(puuid: str):
    return await _request("GET", f"/profile/{puuid}")


async def get_eligible(giver_puuid: str, receiver_puuid: str):
    return await _request(
        "GET",
        f"/rep/eligible?giverPuuid={giver_puuid}&receiverPuuid={receiver_puuid}",
    )


async def give_rep(payload: dict):
    return await _request("POST", "/rep/give", json=payload)


# ─── Worker endpoints (internal, X-Internal-Key required) ─────────────────────

async def get_pending_dms(limit: int = 20):
    """Fetch pending DM queue entries the bot still owes to send."""
    return await _request("GET", f"/worker/dm-queue/pending?limit={limit}", internal=True)


async def mark_dm_sent(entry_id: int):
    return await _request("POST", f"/worker/dm-queue/{entry_id}/sent", internal=True)


async def mark_dm_failed(entry_id: int, error: str):
    return await _request(
        "POST",
        f"/worker/dm-queue/{entry_id}/failed",
        json={"error": error},
        internal=True,
    )


async def mark_dm_forbidden(entry_id: int):
    return await _request("POST", f"/worker/dm-queue/{entry_id}/forbidden", internal=True)
