# Copyright (c) 2024-2026 BeemoBot Enterprise
# All rights reserved.
"""
/lookup — chercher la réputation d'un autre joueur.

Trois formes acceptées pour la cible :
  /lookup user:@MonAmi          → résout via son Discord ID
  /lookup query:"Nunch#N7789"   → résout via le Riot ID
  /lookup query:"nunch"         → autocomplete textuel (premier match BeemoBot)

Le résultat est public dans le channel, donc tout le monde voit qui a
combien de shrooms / respects / honey.
"""
import discord
from discord import app_commands
from config import WEBAPP_URL
from Discord.Commands.api_beemo import (
    get_profile,
    get_profile_by_discord,
    search_users,
)


def register_lookup(bot):
    @bot.tree.command(
        name="lookup",
        description="Affiche la réputation d'un autre joueur (Discord mention ou Riot ID)",
    )
    @app_commands.describe(
        user="Mention Discord du joueur (laisse vide si tu utilises query)",
        query="Pseudo Discord, nom Riot ou Riot ID complet (Nunch#N7789)",
    )
    async def lookup_cmd(
        interaction: discord.Interaction,
        user: discord.User | None = None,
        query: str | None = None,
    ):
        await interaction.response.defer()

        if not user and not query:
            await interaction.followup.send(
                "❌ Donne soit une mention `user:@joueur`, soit un texte `query:nom_ou_riot_id`."
            )
            return

        # 1. Mention Discord → résolution directe via /profile/by-discord
        resolved = None
        if user:
            resolved = await get_profile_by_discord(str(user.id))
            display_who = user.display_name
            display_avatar = user.display_avatar.url
        else:
            # 2. Texte libre → /profile/search prend en charge Discord ET Riot
            #    et splitte si tag détecté.
            search = await search_users(query or "", limit=1)
            first = (search or {}).get("results", [None])[0] if search else None
            if not first:
                await interaction.followup.send(
                    f"❌ Aucun joueur trouvé pour `{query}`. Vérifie l'orthographe ou tape le Riot ID complet (`Nunch#N7789`)."
                )
                return
            resolved = first
            display_who = first.get("username") or first.get("gameName") or "Joueur"
            display_avatar = first.get("avatarUrl") or None

        # Si pas de PUUID, on peut quand même afficher l'identité Discord mais
        # pas de réputation (pas de PUUID = pas de reputation_events).
        if not resolved or not resolved.get("puuid"):
            embed = discord.Embed(
                title=f"{display_who} — compte non lié",
                description=(
                    f"Ce joueur n'a pas encore lié son compte Riot.\n\n"
                    f"Profil web : {WEBAPP_URL}/search"
                ),
                color=0x5865F2,
            )
            if display_avatar:
                embed.set_thumbnail(url=display_avatar)
            await interaction.followup.send(embed=embed)
            return

        profile = await get_profile(resolved["puuid"])
        if not profile:
            await interaction.followup.send(
                "❌ Profil introuvable côté serveur. Réessaie."
            )
            return

        net = profile["counts"]["respects"] - profile["counts"]["shrooms"]
        title = f"{profile.get('gameName') or display_who}"
        if profile.get("tagLine"):
            title += f"#{profile['tagLine']}"

        embed = discord.Embed(
            title=title,
            url=(
                f"{WEBAPP_URL}/profile/{profile['gameName']}-{profile['tagLine']}"
                if profile.get("gameName") and profile.get("tagLine")
                else None
            ),
            color=0xF5C242 if net >= 0 else 0xDC2626,
        )
        if display_avatar:
            embed.set_thumbnail(url=display_avatar)
        embed.add_field(name="⭐ Respects", value=str(profile["counts"]["respects"]))
        embed.add_field(name="🍄 Shrooms", value=str(profile["counts"]["shrooms"]))
        embed.add_field(name="🍯 Honey", value=str(profile["honey"]))
        embed.add_field(name="Score net", value=f"{net:+d}")
        embed.set_footer(
            text=f"Demandé par {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url,
        )
        await interaction.followup.send(embed=embed)
