# Last updated: 2026-05-07
import discord


def register_help(bot):
    @bot.tree.command(name="help", description="Liste toutes les commandes du bot")
    async def help_cmd(interaction: discord.Interaction):
        embed = discord.Embed(
            title="🐝 Commandes BeemoBot",
            description="Tape `/` dans n'importe quel channel pour voir l'autocomplete.",
            color=0x5865F2,
        )

        embed.add_field(
            name="⭐ Réputation",
            value=(
                "`/link` — Lie ton compte Discord à ton compte Riot\n"
                "`/me` — Affiche TA réputation (auto-détecte ton Discord)\n"
                "`/lookup <user|query>` — Cherche la réputation de quelqu'un d'autre\n"
                "`/live` — Scout ta game en cours (rank, mastery, threats)\n"
                "`/predict` — Prédiction win% basée sur les ranks de la game\n"
                "`/build` — 3 items à build en fonction du matchup\n"
                "`/debrief` — Analyse heuristique de ta dernière game\n"
                "`/judge <riot_id>` — Donne un Shroom 🍄 ou Respect ⭐ après une game commune"
            ),
            inline=False,
        )

        embed.add_field(
            name="🎮 League of Legends",
            value=(
                "`/lastgame <name> <tag> <region>` — Détails de la dernière game\n"
                "`/runes <role>` — Build de runes optimal pour Teemo"
            ),
            inline=False,
        )

        embed.add_field(
            name="✨ Divers",
            value=(
                "`/help` — Cette aide\n"
                "`/help_orion` — Message d'Orion"
            ),
            inline=False,
        )

        embed.add_field(
            name="🛠️ Admin",
            value="`/setup <enabled> <channel>` — Configure le bot pour ce serveur",
            inline=False,
        )

        embed.set_footer(text="BeemoBot • Rep system v1")
        await interaction.response.send_message(embed=embed, ephemeral=True)
