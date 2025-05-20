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
        rank = get_rank_by_id_and_region(get_user_id_by_name_tag_and_region(name, tag, region), region)
        icon_link = slash_user(name, tag, region)
        embed = embed_user_info(rank, name, icon_link)
        await interation.response.send_message(embed=embed, ephemeral=True)
    
    # Add a "shroom" to someone with their name and tag /shroom
    @bot.tree.command(name="shroom",
                description="Add a shroom to someone")
    @app_commands.describe(name="The summoner name", tag="The tag of the user",region="The server region")
    async def self(interation: discord.Interaction,name:str , tag:str, region: typing.Literal["EUW","EUNE","NA","BR","JP","KR","LA","LAS","OC","TR","RU"]):
        region = region_real_name(region)
        user_id = get_user_id_by_name_tag_and_region(name, tag, region)
        icon_link = get_icon_by_iconId(get_user_icon_id_by_user_id_and_region(user_id, region), lol_watcher, DEFAULT_REGION)
        embed = embed_shroom(name, tag, region, icon_link, shrooms=2, respects=4)
        await interation.response.send_message(embed=embed)
    
    #Add a "respect" to someone with their name and tag /respect
    @bot.tree.command(name="respect",
                description="Add a respect to someone")
    @app_commands.describe(name="The summoner name", tag="The tag of the user",region="The server region")
    async def self(interation: discord.Interaction,name:str , tag:str, region: typing.Literal["EUW","EUNE","NA","BR","JP","KR","LA","LAS","OC","TR","RU"]):
        region = region_real_name(region)
        user_id = get_user_id_by_name_tag_and_region(name, tag, region)
        icon_link = get_icon_by_iconId(get_user_icon_id_by_user_id_and_region(user_id, region), lol_watcher, DEFAULT_REGION)
        embed = embed_respect(name, tag, region, icon_link, shrooms=2, respects=4)
        await interation.response.send_message(embed=embed)
        
        
