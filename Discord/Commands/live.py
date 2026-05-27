# Copyright (c) 2024-2026 BeemoBot Enterprise
# All rights reserved.
# Last updated: 2026-05-07
import discord
from Discord.Commands.api_beemo import get_scout
from Discord.Commands.embed_factory import embed_scout


def register_live(bot):
    @bot.tree.command(name="live", description="Scout ta game en cours")
    async def live_cmd(interaction: discord.Interaction):
        # Defer public — le scout intéresse toute la team Discord, pas que
        # le caller. Les erreurs en revanche restent ephemeral pour ne pas
        # polluer le channel quand quelqu'un spam la commande hors game.
        await interaction.response.defer(thinking=True)
        data = await get_scout(str(interaction.user.id))

        if data is None:
            return await interaction.followup.send(
                "⚠️ Erreur API — réessaie dans quelques secondes."
            )
        if data.get("error") == "not_linked":
            return await interaction.followup.send(
                "❌ Lie ton compte d'abord avec `/link`."
            )
        if data.get("error") == "not_in_game":
            return await interaction.followup.send(
                "❌ Tu n'es pas en game actuellement."
            )

        await interaction.followup.send(embed=embed_scout(data))
