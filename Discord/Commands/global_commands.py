# Last updated: 2026-05-06
import typing
import discord
from discord import app_commands

from Riot.riot_watcher import (
    lol_watcher,
    get_user_full_data,
    get_user_id_by_name_tag_and_region,
    get_user_icon_id_by_user_id_and_region,
    get_last_match_data,
)
from Riot.riot_toolbox import region_real_name, get_icon_by_iconId
from config import DEFAULT_REGION
from Discord.Commands.embed_factory import (
    embed_user_info,
    embed_shroom,
    embed_respect,
    embed_help_orion,
    embed_top_shrooms,
    embed_top_respects,
    embed_runes,
    embed_last_game,
)
from Discord.Commands.api_beemo import (
    give_shroom,
    give_respect,
    get_user_stats,
    get_top_shrooms,
    get_top_respects,
)

REGION_LITERAL = typing.Literal[
    "EUW", "EUNE", "NA", "BR", "JP", "KR", "LA", "LAS", "OC", "TR", "RU"
]


def setup_global_commands(bot):
    @bot.tree.command(name="user", description="Get basic user infos")
    @app_commands.describe(name="The summoner name", tag="The tag of the user", region="The server region")
    async def user_cmd(interaction: discord.Interaction, name: str, tag: str, region: REGION_LITERAL):
        region = region_real_name(region)
        user_data = get_user_full_data(name, tag, region)
        embed = embed_user_info(
            user_data["rank"], name, user_data["icon_url"], user_data["summoner_level"]
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="shroom", description="Add a shroom to someone")
    @app_commands.describe(name="The summoner name", tag="The tag of the user", region="The server region")
    async def shroom_cmd(interaction: discord.Interaction, name: str, tag: str, region: REGION_LITERAL):
        region = region_real_name(region)
        user_id = get_user_id_by_name_tag_and_region(name, tag, region)
        icon_link = get_icon_by_iconId(
            get_user_icon_id_by_user_id_and_region(user_id, region), lol_watcher, DEFAULT_REGION
        )
        username = f"{name}_{tag}"
        await give_shroom(username)
        user_stats = await get_user_stats(username)
        embed = embed_shroom(
            name, tag, region, icon_link,
            user_stats["data"]["shrooms"], user_stats["data"]["respects"],
        )
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="respect", description="Add a respect to someone")
    @app_commands.describe(name="The summoner name", tag="The tag of the user", region="The server region")
    async def respect_cmd(interaction: discord.Interaction, name: str, tag: str, region: REGION_LITERAL):
        region = region_real_name(region)
        user_id = get_user_id_by_name_tag_and_region(name, tag, region)
        icon_link = get_icon_by_iconId(
            get_user_icon_id_by_user_id_and_region(user_id, region), lol_watcher, DEFAULT_REGION
        )
        username = f"{name}_{tag}"
        await give_respect(username)
        user_stats = await get_user_stats(username)
        embed = embed_respect(
            name, tag, region, icon_link,
            user_stats["data"]["shrooms"], user_stats["data"]["respects"],
        )
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="help_orion", description="A message from Orion")
    async def help_orion_cmd(interaction: discord.Interaction):
        embed = embed_help_orion()
        await interaction.response.send_message(embed=embed)

    @bot.tree.command(name="top_shrooms", description="Display the top 10 shrooms")
    async def top_shrooms_cmd(interaction: discord.Interaction):
        top_shrooms = await get_top_shrooms()
        embed = embed_top_shrooms(top_shrooms)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="top_respects", description="Display the top 10 respects")
    async def top_respects_cmd(interaction: discord.Interaction):
        top_respects = await get_top_respects()
        embed = embed_top_respects(top_respects)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="runes", description="Display the best runes for teemo")
    @app_commands.describe(role="The role you want to see the runes for")
    async def runes_cmd(
        interaction: discord.Interaction,
        role: typing.Literal["top", "mid", "bot", "jungle", "support"],
    ):
        embed, file_name = embed_runes(role)
        if file_name:
            file = discord.File(f"Runes/{file_name}", filename=file_name)
            await interaction.response.send_message(embed=embed, file=file, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="lastgame", description="Display the last game of a summoner")
    @app_commands.describe(name="The summoner name", tag="The tag of the user", region="The server region")
    async def lastgame_cmd(
        interaction: discord.Interaction, name: str, tag: str, region: REGION_LITERAL
    ):
        region = region_real_name(region)
        match_data = get_last_match_data(name, tag, region)
        embed = embed_last_game(match_data, name, region)
        await interaction.response.send_message(embed=embed, ephemeral=True)
