# Last updated: 2026-05-06
import discord
from Discord.Commands.api_beemo import give_rep


class MatchRepView(discord.ui.View):
    def __init__(self, giver_discord_id: str, match_id: str, participants: list, guild_id: str | None):
        super().__init__(timeout=86400)  # 24h
        self.giver_discord_id = giver_discord_id
        self.match_id = match_id
        self.guild_id = guild_id
        for p in participants[:8]:  # cap UI buttons
            self.add_item(self._btn(p, "shroom"))
            self.add_item(self._btn(p, "respect"))

    def _btn(self, participant: dict, kind: str):
        emoji = "🍄" if kind == "shroom" else "⭐"
        style = discord.ButtonStyle.danger if kind == "shroom" else discord.ButtonStyle.success
        button = discord.ui.Button(
            label=f"{emoji} {participant['championName']}",
            style=style,
            custom_id=f"{kind}-{self.match_id}-{participant['puuid'][:8]}",
        )

        async def callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            payload = {
                "giverDiscordId": self.giver_discord_id,
                "receiverPuuid": participant["puuid"],
                "matchId": self.match_id,
                "type": kind,
                "guildId": self.guild_id,
            }
            result = await give_rep(payload)
            if result:
                await interaction.followup.send(
                    f"✅ {kind.title()} envoyé sur {participant['championName']}",
                    ephemeral=True,
                )
                button.disabled = True
                await interaction.message.edit(view=self)
            else:
                await interaction.followup.send("❌ Échec.", ephemeral=True)

        button.callback = callback
        return button
