# Last updated: 2026-05-06
import discord
from discord import app_commands
from config import WEBAPP_URL


def register_link(bot):
    @bot.tree.command(name="link", description="Lie ton compte Discord à ton compte Riot")
    async def link_cmd(interaction: discord.Interaction):
        embed = discord.Embed(
            title="🔗 Lie ton compte Riot",
            description=(
                "Pour donner des shrooms ou des respects, tu dois lier ton compte Riot une fois.\n\n"
                f"👉 [Clique ici pour lier]({WEBAPP_URL}/auth/link)\n\n"
                "*Une seule fois pour toujours.*"
            ),
            color=0x5865F2,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
