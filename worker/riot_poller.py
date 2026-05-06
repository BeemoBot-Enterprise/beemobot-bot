# Last updated: 2026-05-06
"""Polls Riot match history for linked users and writes dm_queue entries."""
import asyncio
import logging
import os
import psycopg2
import psycopg2.extras
import aiohttp
from typing import Optional
from worker.rate_limiter import RIOT_BUCKET

logger = logging.getLogger(__name__)

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
DB_DSN = os.getenv("WORKER_DB_DSN") or (
    f"host={os.getenv('DB_HOST', 'localhost')} "
    f"port={os.getenv('DB_PORT', '5432')} "
    f"dbname={os.getenv('DB_DATABASE', 'postgres')} "
    f"user={os.getenv('DB_USER', 'postgres')} "
    f"password={os.getenv('DB_PASSWORD', '')}"
)


async def _riot_get(session: aiohttp.ClientSession, url: str, retry: int = 3) -> Optional[dict]:
    for attempt in range(retry):
        await RIOT_BUCKET.acquire()
        try:
            async with session.get(url, headers={"X-Riot-Token": RIOT_API_KEY}) as r:
                if r.status == 200:
                    return await r.json()
                if r.status == 429:
                    delay = int(r.headers.get("Retry-After", "5"))
                    logger.warning("429 from Riot, sleeping %ds", delay)
                    await asyncio.sleep(delay)
                    continue
                if r.status == 404:
                    return None
                logger.warning("Riot returned %d for %s", r.status, url)
                return None
        except aiohttp.ClientError as exc:
            logger.error("Riot request failed: %s", exc)
            await asyncio.sleep(2 ** attempt)
    return None


async def poll_user(session: aiohttp.ClientSession, user: dict, conn) -> int:
    """Poll one user, insert dm_queue entries for new matches. Returns count of new dm_queue inserts."""
    puuid = user["riot_puuid"]
    last_match = user["last_polled_match_id"]

    history_url = (
        f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count=10"
    )
    match_ids = await _riot_get(session, history_url)
    if not match_ids:
        return 0

    new_matches = []
    for mid in match_ids:
        if mid == last_match:
            break
        new_matches.append(mid)

    if not new_matches:
        return 0

    inserted = 0
    with conn.cursor() as cur:
        for mid in new_matches:
            details = await _riot_get(
                session, f"https://europe.api.riotgames.com/lol/match/v5/matches/{mid}"
            )
            if not details:
                continue

            participants = details["info"]["participants"]
            participant_puuids = [p["puuid"] for p in participants]

            cur.execute(
                "SELECT discord_id, riot_puuid, riot_game_name, riot_tag_line "
                "FROM users WHERE riot_puuid = ANY(%s) AND linked_at IS NOT NULL",
                (participant_puuids,),
            )
            linked_in_match = cur.fetchall()

            for row in linked_in_match:
                others_payload = []
                for p in participants:
                    if p["puuid"] == row[1]:
                        continue
                    others_payload.append({
                        "puuid": p["puuid"],
                        "championName": p["championName"],
                        "kills": p["kills"],
                        "deaths": p["deaths"],
                        "assists": p["assists"],
                        "win": p["win"],
                        "teamId": p["teamId"],
                    })
                cur.execute(
                    "INSERT INTO dm_queue (discord_id, match_id, participants) "
                    "VALUES (%s, %s, %s::jsonb) "
                    "ON CONFLICT (discord_id, match_id) DO NOTHING",
                    (row[0], mid, psycopg2.extras.Json(others_payload)),
                )
                inserted += cur.rowcount

        cur.execute(
            "INSERT INTO match_poll_state (user_puuid, last_polled_match_id, last_polled_at) "
            "VALUES (%s, %s, NOW()) "
            "ON CONFLICT (user_puuid) DO UPDATE SET "
            "last_polled_match_id = EXCLUDED.last_polled_match_id, "
            "last_polled_at = EXCLUDED.last_polled_at",
            (puuid, new_matches[0]),
        )
    conn.commit()
    return inserted


async def poll_all() -> None:
    conn = psycopg2.connect(DB_DSN)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT u.riot_puuid, u.discord_id, u.riot_game_name, u.riot_tag_line, "
                "       s.last_polled_match_id "
                "FROM users u "
                "LEFT JOIN match_poll_state s ON u.riot_puuid = s.user_puuid "
                "WHERE u.linked_at IS NOT NULL AND u.riot_puuid IS NOT NULL"
            )
            users = [
                {"riot_puuid": r[0], "discord_id": r[1], "riot_game_name": r[2],
                 "riot_tag_line": r[3], "last_polled_match_id": r[4]}
                for r in cur.fetchall()
            ]
        async with aiohttp.ClientSession() as session:
            total = 0
            for user in users:
                total += await poll_user(session, user, conn)
        logger.info("poll_all done: %d new matches enqueued", total)
    finally:
        conn.close()
