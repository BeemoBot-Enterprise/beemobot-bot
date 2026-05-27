# Last updated: 2026-05-07
import discord
from config import WEBAPP_URL
from Discord.Commands.api_beemo import get_profile, get_profile_by_discord


def register_me(bot):
    @bot.tree.command(name="me", description="Affiche ta réputation BeemoBot")
    async def me_cmd(interaction: discord.Interaction):
        # Résultat public par défaut — visible dans le channel. Si pas lié,
        # on bascule l'erreur en ephemeral pour ne pas spam les autres.
        await interaction.response.defer()

        link = await get_profile_by_discord(str(interaction.user.id))
        if not link or link.get("error") in ("not_linked", "not_found") or not link.get("puuid"):
            embed = discord.Embed(
                title="🔗 Compte non lié",
                description=(
                    "Tu n'as pas encore lié ton compte Riot.\n\n"
                    f"👉 [Clique ici pour lier]({WEBAPP_URL}/auth/link)\n\n"
                    "Une fois lié, tape `/me` à nouveau pour voir ta réputation."
                ),
                color=0x5865F2,
            )
            # On ne peut plus envoyer en ephemeral après un defer public — on
            # envoie public mais explicite (l'utilisateur sait que c'est lui).
            embed.set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.display_avatar.url,
            )
            await interaction.followup.send(embed=embed)
            return

        profile = await get_profile(link["puuid"])
        if not profile:
            await interaction.followup.send("❌ Profil introuvable.")
            return

        net = profile["counts"]["respects"] - profile["counts"]["shrooms"]
        embed = discord.Embed(
            title=f"{profile['gameName']}#{profile['tagLine']}",
            color=0xF5C242 if net >= 0 else 0xDC2626,
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )
        embed.add_field(name="⭐ Respects", value=str(profile["counts"]["respects"]))
        embed.add_field(name="🍄 Shrooms", value=str(profile["counts"]["shrooms"]))
        embed.add_field(name="🍯 Honey", value=str(profile["honey"]))
        embed.add_field(name="Score net", value=f"{net:+d}")
        await interaction.followup.send(embed=embed)
