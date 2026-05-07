# Last updated: 2026-05-07
"""Polls /worker/dm-queue/pending and sends Discord DMs with rep buttons.

All DB access lives in the API now; this loop is pure HTTP, the bot is just
a consumer that fetches work, sends DMs, and reports back the outcome.
"""
import asyncio
import logging
import os
import discord
from Discord.Commands.api_beemo import (
    get_pending_dms,
    mark_dm_sent,
    mark_dm_failed,
    mark_dm_forbidden,
)
from Discord.Commands.rep_buttons import MatchRepView

logger = logging.getLogger(__name__)
DM_INTERVAL_S = int(os.getenv("DM_INTERVAL_S", "30"))
BATCH_LIMIT = int(os.getenv("DM_BATCH_LIMIT", "20"))


async def dispatch_loop(bot: discord.Client):
    """Bot must be ready before calling. Loops forever."""
    while True:
        try:
            await _process_batch(bot)
        except Exception:
            logger.exception("dm dispatch crashed")
        await asyncio.sleep(DM_INTERVAL_S)


async def _process_batch(bot: discord.Client):
    payload = await get_pending_dms(limit=BATCH_LIMIT)
    if not payload:
        return
    items = payload.get("items", [])
    if not items:
        return

    logger.info("dispatching %d pending DMs", len(items))
    for item in items:
        entry_id = item["id"]
        discord_id = item["discordId"]
        match_id = item["matchId"]
        participants = item["participants"]
        try:
            user = await bot.fetch_user(int(discord_id))
            embed = discord.Embed(
                title="🎮 Game terminée — qui mérite quoi ?",
                description=f"Match `{match_id}`",
                color=0x5865F2,
            )
            for p in participants[:10]:
                embed.add_field(
                    name=p["championName"],
                    value=f"K/D/A {p['kills']}/{p['deaths']}/{p['assists']} "
                          f"{'🏆 Win' if p['win'] else '💀 Loss'}",
                    inline=False,
                )
            view = MatchRepView(
                giver_discord_id=discord_id,
                match_id=match_id,
                participants=participants,
                guild_id=None,
            )
            await user.send(embed=embed, view=view)
            await mark_dm_sent(entry_id)
        except discord.Forbidden:
            await mark_dm_forbidden(entry_id)
        except Exception as exc:
            logger.exception("DM failed for entry %s: %s", entry_id, exc)
            await mark_dm_failed(entry_id, str(exc)[:200])
        await asyncio.sleep(1.5)  # rate limit DMs
