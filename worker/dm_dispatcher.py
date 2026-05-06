# Last updated: 2026-05-06
"""Polls dm_queue and sends Discord DMs with rep buttons."""
import asyncio
import logging
import os
import psycopg2
import discord
from worker.riot_poller import DB_DSN
from Discord.Commands.rep_buttons import MatchRepView

logger = logging.getLogger(__name__)
DM_INTERVAL_S = int(os.getenv("DM_INTERVAL_S", "30"))


async def dispatch_loop(bot: discord.Client):
    """Bot must be ready before calling. Loops forever."""
    while True:
        try:
            await _process_batch(bot)
        except Exception:
            logger.exception("dm dispatch crashed")
        await asyncio.sleep(DM_INTERVAL_S)


async def _process_batch(bot: discord.Client):
    conn = psycopg2.connect(DB_DSN)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, discord_id, match_id, participants "
                "FROM dm_queue WHERE status = 'pending' AND attempts < 3 "
                "ORDER BY created_at LIMIT 20"
            )
            rows = cur.fetchall()

            for row_id, discord_id, match_id, participants in rows:
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
                    cur.execute(
                        "UPDATE dm_queue SET status='sent', sent_at=NOW() WHERE id=%s",
                        (row_id,),
                    )
                except discord.Forbidden:
                    cur.execute(
                        "UPDATE dm_queue SET status='failed', last_error='dm_forbidden', attempts=attempts+1 WHERE id=%s",
                        (row_id,),
                    )
                except Exception as exc:
                    logger.exception("DM failed: %s", exc)
                    cur.execute(
                        "UPDATE dm_queue SET attempts=attempts+1, last_error=%s WHERE id=%s",
                        (str(exc)[:200], row_id),
                    )
                conn.commit()
                await asyncio.sleep(1.5)  # rate limit DMs
    finally:
        conn.close()
