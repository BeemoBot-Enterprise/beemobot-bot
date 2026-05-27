# Copyright (c) 2024-2026 BeemoBot Enterprise
# All rights reserved.
"""/claim — récupère 10 honey après une partie (fenêtre 10 min, 1 fois par game)."""
import discord
from Discord.Commands.api_beemo import claim_match_honey


def register_claim(bot):
    @bot.tree.command(
        name="claim",
        description="Récupère 10 honey juste après ta game (1 claim par game, dans les 10 min)",
    )
    async def claim_cmd(interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            data = await claim_match_honey(str(interaction.user.id))
            if not data:
                await interaction.followup.send(
                    "⚠️ Erreur API — réessaie dans quelques secondes."
                )
                return

            err = data.get("error")
            if err == "not_linked":
                await interaction.followup.send(
                    "❌ Lie ton compte Riot d'abord avec `/link`."
                )
                return
            if err == "no_recent_match":
                await interaction.followup.send(
                    "❌ Aucune game récente trouvée. Termine une partie avant de claim."
                )
                return
            if err == "claim_window_expired":
                await interaction.followup.send(
                    f"⏰ {data.get('message', 'Trop tard.')}"
                )
                return
            if err == "already_claimed":
                await interaction.followup.send(
                    f"🔁 {data.get('message', 'Déjà claim cette game.')} "
                    f"Solde actuel : **{data.get('balance', 0)} 🍯**"
                )
                return
            if err == "riot_unavailable":
                await interaction.followup.send(
                    "⚠️ Riot ne répond pas. Réessaie dans une minute."
                )
                return
            if err:
                await interaction.followup.send(f"❌ {data.get('message', err)}")
                return

            credited = data.get("credited", 10)
            balance = data.get("balance", 0)
            match_id = data.get("matchId", "?")

            embed = discord.Embed(
                title="🍯 Honey claim — +10",
                description=(
                    f"GG **{interaction.user.display_name}** ! Tu viens de récupérer "
                    f"**+{credited} honey** pour ta dernière game.\n\n"
                    f"Solde : **{balance} 🍯**"
                ),
                color=0xE5A422,
            )
            embed.set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.display_avatar.url,
            )
            embed.set_footer(text=f"Match {match_id}")
            await interaction.followup.send(embed=embed)
        except Exception as exc:
            try:
                await interaction.followup.send(
                    f"❌ Erreur claim : `{type(exc).__name__}`. Réessaie."
                )
            except Exception:
                pass
