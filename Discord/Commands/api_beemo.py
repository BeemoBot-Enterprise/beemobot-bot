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


async def _request(
    method: str,
    path: str,
    json: dict | None = None,
    internal: bool = False,
    expose_404: bool = False,
):
    url = f"{BEEMO_API_BASE_URL}{path}"
    headers = _internal_headers() if internal else None
    try:
        async with aiohttp.ClientSession(timeout=DEFAULT_TIMEOUT) as session:
            async with session.request(method, url, json=json, headers=headers) as resp:
                if resp.status == 404 and expose_404:
                    # Caller asked to see structured 404 bodies (e.g. {"error": "not_linked"}).
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
    return await _request("GET", f"/lol/debrief/by-discord/{discord_id}", expose_404=True)


async def get_predict(discord_id: str):
    return await _request("GET", f"/lol/predict/by-discord/{discord_id}", expose_404=True)


async def get_scout(discord_id: str):
    return await _request("GET", f"/lol/scout/by-discord/{discord_id}", expose_404=True)


async def get_build(discord_id: str):
    return await _request("GET", f"/lol/build/by-discord/{discord_id}", expose_404=True)


async def get_profile(puuid: str):
    return await _request("GET", f"/profile/{puuid}")


async def get_profile_by_discord(discord_id: str):
    return await _request("GET", f"/profile/by-discord/{discord_id}", expose_404=True)


async def claim_match_honey(discord_id: str):
    """Claim 10 honey pour la dernière game si dans la fenêtre 10 min."""
    return await _request(
        "POST",
        f"/economy/claim/by-discord/{discord_id}",
        expose_404=True,
    )


async def get_lol_profile(riot_id: str, region: str):
    """Resolve un Riot ID arbitraire (existant ou non en DB BeemoBot) via
    l'endpoint LoL qui fait l'aller-retour vers Riot Account-v1 + Summoner-v4
    + League + Mastery + Match history. Utilisé par /lookup pour permettre
    de chercher des joueurs jamais vus par BeemoBot."""
    from urllib.parse import quote
    encoded = quote(riot_id, safe="-")
    return await _request(
        "GET",
        f"/lol/summoner/{encoded}/profile?region={region}",
    )


async def search_users(query: str, limit: int = 5):
    """Autocomplete par pseudo Discord ou Riot ID. Utilisé par /lookup.

    URL-encode le `query` parce que les Riot IDs contiennent un # qui
    cassait l'URL (le # marque le fragment côté aiohttp et tout ce qui
    suit était dropped — on cherchait juste 'Nunch' au lieu de 'Nunch#N7789').
    """
    from urllib.parse import quote
    encoded = quote(query, safe="")
    return await _request(
        "GET",
        f"/profile/search?q={encoded}&mode=both&limit={limit}",
    )


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
