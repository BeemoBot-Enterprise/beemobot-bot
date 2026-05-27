# Last updated: 2026-05-07
import asyncio
import typing
import discord
from discord import app_commands

from Riot.riot_watcher import (
    get_user_full_data,
    get_last_match_data,
)
from Riot.riot_toolbox import region_real_name
from config import DEFAULT_REGION
from Discord.Commands.embed_factory import (
    embed_help_orion,
    embed_runes,
    embed_last_game,
)
from Discord.Commands.link import register_link
from Discord.Commands.me import register_me
from Discord.Commands.judge import register_judge
from Discord.Commands.setup_admin import register_setup
from Discord.Commands.help import register_help
from Discord.Commands.debrief import register_debrief
from Discord.Commands.predict import register_predict
from Discord.Commands.live import register_live
from Discord.Commands.lookup import register_lookup
from Discord.Commands.build import register_build
from Discord.Commands.claim import register_claim

REGION_LITERAL = typing.Literal[
    "EUW", "EUNE", "NA", "BR", "JP", "KR", "LA", "LAS", "OC", "TR", "RU"
]


def setup_global_commands(bot):
    register_link(bot)
    register_me(bot)
    register_judge(bot)
    register_setup(bot)
    register_help(bot)
    register_debrief(bot)
    register_predict(bot)
    register_live(bot)
    register_lookup(bot)
    register_build(bot)
    register_claim(bot)

    @bot.tree.command(name="help_orion", description="A message from Orion")
    async def help_orion_cmd(interaction: discord.Interaction):
        embed = embed_help_orion()
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="runes", description="Display the best runes for teemo")
    @app_commands.describe(role="The role you want to see the runes for")
    async def runes_cmd(
        interaction: discord.Interaction,
        role: typing.Literal["top", "mid", "bot", "jungle", "support"],
    ):
        embed, file_name = embed_runes(role)
        if file_name:
            file = discord.File(f"Runes/{file_name}", filename=file_name)
            await interaction.response.send_message(embed=embed, file=file)
        else:
            await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="lastgame", description="Display the last game of a summoner")
    @app_commands.describe(name="The summoner name", tag="The tag of the user", region="The server region")
    async def lastgame_cmd(
        interaction: discord.Interaction, name: str, tag: str, region: REGION_LITERAL
    ):
        # riotwatcher is sync and chains 3 Riot calls — would freeze the event
        # loop and trip the 3s deadline. defer first, then offload to a thread.
        await interaction.response.defer()
        region = region_real_name(region)
        match_data = await asyncio.to_thread(get_last_match_data, name, tag, region)
        embed = embed_last_game(match_data, name, region)
        await interaction.followup.send(embed=embed)
