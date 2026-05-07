# Last updated: 2026-05-07
import discord
from discord import app_commands
from Discord.Commands.api_beemo import _request, get_eligible, give_rep


class JudgeView(discord.ui.View):
    def __init__(self, giver_discord_id: str, giver_puuid: str, receiver_puuid: str, match_id: str, can_shroom: bool, can_respect: bool):
        super().__init__(timeout=300)
        self.giver_discord_id = giver_discord_id
        self.giver_puuid = giver_puuid
        self.receiver_puuid = receiver_puuid
        self.match_id = match_id
        if can_shroom:
            self.add_item(self._button("🍄 Shroom", "shroom", discord.ButtonStyle.danger))
        if can_respect:
            self.add_item(self._button("⭐ Respect", "respect", discord.ButtonStyle.success))

    def _button(self, label: str, kind: str, style: discord.ButtonStyle):
        button = discord.ui.Button(label=label, style=style, custom_id=f"{kind}-{self.match_id}")

        async def callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            payload = {
                "giverDiscordId": self.giver_discord_id,
                "receiverPuuid": self.receiver_puuid,
                "matchId": self.match_id,
                "type": kind,
                "guildId": str(interaction.guild_id) if interaction.guild_id else None,
            }
            result = await give_rep(payload)
            if result:
                await interaction.followup.send(
                    f"✅ {kind.title()} envoyé pour le match `{self.match_id}` (weight {result['weight']})",
                    ephemeral=True,
                )
            else:
                await interaction.followup.send("❌ Échec de l'envoi.", ephemeral=True)

        button.callback = callback
        return button


def register_judge(bot):
    @bot.tree.command(name="judge", description="Juge un joueur que tu as croisé en game")
    @app_commands.describe(riot_id="Riot ID de la cible (ex: Nunch-N7789)")
    async def judge_cmd(interaction: discord.Interaction, riot_id: str):
        await interaction.response.defer(ephemeral=True)
        target = await _request("GET", f"/lol/summoner/{riot_id}")
        if not target or not target.get("puuid"):
            await interaction.followup.send("❌ Riot ID introuvable.", ephemeral=True)
            return

        me = await _request("GET", "/profile/by-discord/" + str(interaction.user.id))
        if not me or not me.get("puuid"):
            await interaction.followup.send(
                "❌ Tu dois lier ton compte Riot d'abord — utilise `/link`.",
                ephemeral=True,
            )
            return

        eligible = await get_eligible(me["puuid"], target["puuid"])
        if not eligible or not eligible.get("matches"):
            await interaction.followup.send(
                "❌ Aucun match commun trouvé dans tes 20 dernières games.",
                ephemeral=True,
            )
            return

        await interaction.followup.send(
            f"🎯 **Matches éligibles avec {target['gameName']}#{target['tagLine']}** :",
            ephemeral=True,
        )
        for m in eligible["matches"][:5]:
            view = JudgeView(
                giver_discord_id=str(interaction.user.id),
                giver_puuid=me["puuid"],
                receiver_puuid=target["puuid"],
                match_id=m["matchId"],
                can_shroom=m["canShroom"],
                can_respect=m["canRespect"],
            )
            await interaction.followup.send(
                f"Match `{m['matchId']}`",
                view=view,
                ephemeral=True,
            )
