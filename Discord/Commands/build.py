# Copyright (c) 2024-2026 BeemoBot Enterprise
# All rights reserved.
"""/build — suggère 3 items à acheter en game selon ton champion + la team adverse."""
import discord
from Discord.Commands.api_beemo import get_build

# Couleurs par rôle pour l'embed (touche visuelle rapide).
ROLE_COLOR = {
    "AD_CARRY": 0xE5A422,    # honey gold
    "AD_BRUISER": 0xC8413B,  # red bruiser
    "AD_ASSASSIN": 0x9D174D, # crimson assassin
    "AP_MAGE": 0x5B21B6,     # purple mage
    "AP_ASSASSIN": 0x7C3AED, # darker purple
    "TANK": 0x6B7280,        # grey tank
    "SUPPORT": 0x10B981,     # green support
    "UNKNOWN": 0x5865F2,     # discord blurple
}


def register_build(bot):
    @bot.tree.command(
        name="build",
        description="3 items à build sur ton champion en fonction de la team adverse",
    )
    async def build_cmd(interaction: discord.Interaction):
        # Public — l'idée est de partager le build à toute la team Discord.
        await interaction.response.defer(thinking=True)
        data = await get_build(str(interaction.user.id))

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

        self_info = data["self"]
        enemies = data["enemies"]
        items = data["items"]
        summary = data["enemySummary"]

        ennemy_lines = []
        for e in enemies:
            tag = e["type"].replace("_", " ").lower()
            ennemy_lines.append(f"• **{e['championName']}** ({tag})")

        ad = summary["adCount"]
        ap = summary["apCount"]
        tanks = summary["tankCount"]

        embed = discord.Embed(
            title=f"🛠 Build pour {self_info['championName']}",
            description=(
                f"**Composition adverse** : {ad} AD · {ap} AP · {tanks} tank{'s' if tanks > 1 else ''}\n"
                + "\n".join(ennemy_lines)
            ),
            color=ROLE_COLOR["UNKNOWN"],
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url,
        )

        for idx, item in enumerate(items, start=1):
            embed.add_field(
                name=f"{idx}. {item['name']}",
                value=item["why"],
                inline=False,
            )

        embed.set_footer(text="Build heuristique BeemoBot — adapte selon ton lane state.")
        await interaction.followup.send(embed=embed)
