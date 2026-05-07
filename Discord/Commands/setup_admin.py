# Last updated: 2026-05-07
import discord
from discord import app_commands
from Discord.Commands.api_beemo import _request


def register_setup(bot):
    @bot.tree.command(name="setup", description="Admin: configure BeemoBot pour ce serveur")
    @app_commands.describe(
        enabled="Activer ou désactiver les DMs proactifs",
        channel="Channel public optionnel pour annoncer les events",
    )
    @app_commands.default_permissions(administrator=True)
    async def setup_cmd(
        interaction: discord.Interaction,
        enabled: bool = True,
        channel: discord.TextChannel | None = None,
    ):
        if not interaction.guild_id:
            await interaction.response.send_message("Commande serveur uniquement.", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        result = await _request(
            "POST",
            f"/admin/guild/{interaction.guild_id}",
            json={
                "repEnabled": enabled,
                "publicChannelId": str(channel.id) if channel else None,
            },
        )
        if result:
            await interaction.followup.send(
                f"✅ Config mise à jour. Rep: {'on' if enabled else 'off'}, "
                f"channel: {channel.mention if channel else 'aucun'}",
                ephemeral=True,
            )
        else:
            await interaction.followup.send("❌ Échec.", ephemeral=True)
