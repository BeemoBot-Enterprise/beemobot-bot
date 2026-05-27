# Copyright (c) 2024-2026 BeemoBot Enterprise
# All rights reserved.
"""
/lookup name tag region — fiche complète d'un joueur LoL.

Marche pour N'IMPORTE QUEL compte existant chez Riot, pas besoin d'avoir
été touché par BeemoBot avant. Combine :
  - Riot Account-v1 + Summoner-v4 (identité, niveau)
  - League-v4 (rank SoloQ)
  - Champion-mastery-v4 (champion main)
  - Match-v5 (3 dernières games avec KDA + win/loss)
  - BeemoBot /profile/:puuid (rep reçus + honey)

Embed compact — pensé pour être lu en 2 secondes pendant une game.
"""
import typing
import discord
from discord import app_commands
from config import WEBAPP_URL
from Riot.riot_toolbox import region_real_name
from Discord.Commands.api_beemo import get_lol_profile, get_profile

REGION_LITERAL = typing.Literal[
    "EUW", "EUNE", "NA", "BR", "JP", "KR", "LA", "LAS", "OC", "TR", "RU"
]


def register_lookup(bot):
    @bot.tree.command(
        name="lookup",
        description="Fiche complète d'un joueur LoL (rank, main, 3 dernières games, rep BeemoBot)",
    )
    @app_commands.describe(
        name="Game name du joueur (avant le #)",
        tag="Tag line (après le #, sans le #)",
        region="Serveur Riot du joueur",
    )
    async def lookup_cmd(
        interaction: discord.Interaction,
        name: str,
        tag: str,
        region: REGION_LITERAL,
    ):
        await interaction.response.defer()
        # Catch-all : éviter le spinner infini si quoi que ce soit pète.
        try:
            platform = region_real_name(region)
            riot_id = f"{name}-{tag}"

            # 1) Riot full profile (existe pour tout compte LoL, pas que BeemoBot)
            riot = await get_lol_profile(riot_id, platform)
            if not riot or not isinstance(riot, dict) or not riot.get("summoner"):
                await interaction.followup.send(
                    f"❌ Aucun invocateur trouvé pour **{name}#{tag}** sur **{region}**. "
                    f"Vérifie l'orthographe du nom, du tag et de la région."
                )
                return

            summoner = riot["summoner"]
            ranks = riot.get("ranks") or []
            top_champs = riot.get("topChampions") or []
            recent = riot.get("recentMatches") or []

            # 2) BeemoBot rep (zéro si compte jamais vu par Beemo)
            beemo = await get_profile(summoner["puuid"]) or {}
            counts = beemo.get("counts") or {"respects": 0, "shrooms": 0}
            respects = counts.get("respects", 0)
            shrooms = counts.get("shrooms", 0)
            honey = beemo.get("honey", 0)
            net = respects - shrooms

            # 3) Embed compact
            embed = discord.Embed(
                title=f"{summoner.get('gameName', name)}#{summoner.get('tagLine', tag)}",
                url=f"{WEBAPP_URL}/profile/{name}-{tag}",
                color=0xF5C242 if net >= 0 else 0xDC2626,
            )
            embed.set_footer(
                text=f"Niv {summoner.get('summonerLevel', '?')} · {region} · demandé par {interaction.user.display_name}",
                icon_url=interaction.user.display_avatar.url,
            )

            # Rank SoloQ ou unranked
            solo = next(
                (r for r in ranks if r.get("queueType") == "RANKED_SOLO_5x5"),
                None,
            )
            if solo:
                rank_value = (
                    f"**{solo['tier']} {solo['rank']}** · {solo['leaguePoints']} LP\n"
                    f"{solo['wins']}V / {solo['losses']}D · **{solo['winRate']}%** WR"
                )
                if solo.get("hotStreak"):
                    rank_value += " 🔥"
            else:
                rank_value = "Unranked"
            embed.add_field(name="🏆 SoloQ", value=rank_value, inline=True)

            # Champion main
            if top_champs:
                t = top_champs[0]
                embed.add_field(
                    name="⭐ Champion main",
                    value=(
                        f"**{t['championName']}**\n"
                        f"Niv {t['championLevel']} · {int(t['championPoints']):,} pts".replace(",", " ")
                    ),
                    inline=True,
                )
            else:
                embed.add_field(name="⭐ Champion main", value="—", inline=True)

            # Réputation BeemoBot (toujours montrée même si zéro)
            if respects + shrooms + honey > 0:
                rep_value = (
                    f"⭐ {respects}  ·  🍄 {shrooms}  ·  🍯 {honey}\n"
                    f"Score net : **{net:+d}**"
                )
            else:
                rep_value = "Jamais reçu de rep BeemoBot."
            embed.add_field(name="🤝 Réputation", value=rep_value, inline=False)

            # 3 dernières games
            if recent:
                lines = []
                for m in recent[:3]:
                    p = m.get("participant") or {}
                    champ = p.get("championName", "?")
                    kda = f"{p.get('kills', 0)}/{p.get('deaths', 0)}/{p.get('assists', 0)}"
                    result = "🏆" if p.get("win") else "💀"
                    lines.append(f"{result} **{champ}** · KDA {kda}")
                embed.add_field(
                    name="🎮 3 dernières games",
                    value="\n".join(lines),
                    inline=False,
                )

            await interaction.followup.send(embed=embed)
        except Exception as exc:
            # Discord laisse l'interaction en "loading" si on followup pas.
            try:
                await interaction.followup.send(
                    f"❌ Erreur lookup : `{type(exc).__name__}`. Vérifie le nom/tag/région."
                )
            except Exception:
                pass
