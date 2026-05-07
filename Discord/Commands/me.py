# Last updated: 2026-05-07
import discord
from discord import app_commands
from Discord.Commands.api_beemo import get_profile, _request


def register_me(bot):
    @bot.tree.command(name="me", description="Affiche ta réputation BeemoBot")
    @app_commands.describe(riot_id="Ton Riot ID au format Name-Tag (ex: Nunch-N7789)")
    async def me_cmd(interaction: discord.Interaction, riot_id: str):
        await interaction.response.defer(ephemeral=True)
        summ = await _request("GET", f"/lol/summoner/{riot_id}")
        if not summ or not summ.get("puuid"):
            await interaction.followup.send("❌ Riot ID introuvable.", ephemeral=True)
            return
        profile = await get_profile(summ["puuid"])
        if not profile:
            await interaction.followup.send("❌ Profil introuvable.", ephemeral=True)
            return

        net = profile["counts"]["respects"] - profile["counts"]["shrooms"]
        embed = discord.Embed(
            title=f"{profile['gameName']}#{profile['tagLine']}",
            color=0xF5C242 if net >= 0 else 0xDC2626,
        )
        embed.add_field(name="⭐ Respects", value=str(profile["counts"]["respects"]))
        embed.add_field(name="🍄 Shrooms", value=str(profile["counts"]["shrooms"]))
        embed.add_field(name="🍯 Honey", value=str(profile["honey"]))
        embed.add_field(name="Score net", value=f"{net:+d}")
        await interaction.followup.send(embed=embed, ephemeral=True)
