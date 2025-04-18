import discord
from discord import app_commands
from Logs.logs import command_used
from Discord.Embeds_Factory.global_commands_embeds import *
from Riot.riot_watcher import *
from Discord.Commands.embed_factory import *
import typing


# NE PAS TOUCHER SVP
def setup_global_commands(bot):
    # Get full user info by summoner name and tag /user
    @bot.tree.command(name="user",
                description="get basic user infos")
    @app_commands.describe(name="The summoner name", tag="The tag of the user",region="The server region")
    async def self(interation: discord.Interaction,name:str , tag:str, region: typing.Literal["EUW","EUNE","NA","BR","JP","KR","LA","LAS","OC","TR","RU"]):
        
        region=region_real_name(region)
        SU = slash_user(name, tag, region)
        GUIBNTAR = get_user_id_by_name_tag_and_region(name, tag, region)
        GRBIAR = get_rank_by_id_and_region(GUIBNTAR, region)
        EUI = embed_user_info(GRBIAR, name, SU)
        
        await interation.response.send_message(embed=EUI, ephemeral=True)