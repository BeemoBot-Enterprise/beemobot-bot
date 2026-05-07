# Last updated: 2026-05-07
import discord
from Discord.Commands.api_beemo import get_debrief
from Discord.Commands.embed_factory import embed_debrief


def register_debrief(bot):
    @bot.tree.command(name="debrief", description="Analyse de ta dernière game")
    async def debrief_cmd(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        data = await get_debrief(str(interaction.user.id))

        if data is None:
            return await interaction.followup.send(
                "⚠️ Erreur API — réessaie dans quelques secondes.", ephemeral=True
            )
        if data.get("error") == "not_linked":
            return await interaction.followup.send(
                "❌ Lie ton compte d'abord avec `/link`.", ephemeral=True
            )
        if data.get("error") == "no_recent_match":
            return await interaction.followup.send(
                "❌ Aucune game récente trouvée.", ephemeral=True
            )

        await interaction.followup.send(embed=embed_debrief(data), ephemeral=True)
