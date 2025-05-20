import discord
from discord import app_commands
from Logs.logs import command_used
from Discord.Embeds_Factory.global_commands_embeds import *
from Riot.riot_watcher import *
from Discord.Commands.embed_factory import *
import typing
from Discord.Commands.api_beemo import *

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
        give_shroom(name+'_'+tag)
        user_stats = get_user_stats(name+'_'+tag)
        embed = embed_shroom(name, tag, region, icon_link, user_stats['data']['shrooms'], user_stats['data']['respects'])
        await interation.response.send_message(embed=embed)
    
    #Add a "respect" to someone with their name and tag /respect
    @bot.tree.command(name="respect",
                description="Add a respect to someone")
    @app_commands.describe(name="The summoner name", tag="The tag of the user",region="The server region")
    async def self(interation: discord.Interaction,name:str , tag:str, region: typing.Literal["EUW","EUNE","NA","BR","JP","KR","LA","LAS","OC","TR","RU"]):
        region = region_real_name(region)
        user_id = get_user_id_by_name_tag_and_region(name, tag, region)
        icon_link = get_icon_by_iconId(get_user_icon_id_by_user_id_and_region(user_id, region), lol_watcher, DEFAULT_REGION)
        give_respect(name+'_'+tag)
        user_stats = get_user_stats(name+'_'+tag)
        embed = embed_respect(name, tag, region, icon_link, user_stats['data']['shrooms'], user_stats['data']['respects'])
        await interation.response.send_message(embed=embed)
        
    #Display a simple maessage
    @bot.tree.command(name="help_orion",
                description="A message from Orion")
    async def self(interation: discord.Interaction):
        embed = embed_help_orion()
        await interation.response.send_message(embed=embed)
    
    #Display the top 10 shrooms
    @bot.tree.command(name="top_shrooms",
                description="Display the top 10 shrooms")
    async def self(interation: discord.Interaction):
        top_shrooms = get_top_shrooms()
        embed = embed_top_shrooms(top_shrooms)
        await interation.response.send_message(embed=embed, ephemeral=True)
        
    #Display the top 10 respects
    @bot.tree.command(name="top_respects",
                description="Display the top 10 respects")
    async def self(interation: discord.Interaction):
        top_respects = get_top_respects()
        embed = embed_top_respects(top_respects)
        await interation.response.send_message(embed=embed, ephemeral=True)
    
    #Display the current best teemo runes for the asked role (top, mid, bot, jungle, support)
    @bot.tree.command(name="runes",
                description="Display the best runes for teemo")
    @app_commands.describe(role="The role you want to see the runes for")
    async def self(interation: discord.Interaction, role: typing.Literal["top","mid","bot","jungle","support"]):
        embed = embed_runes(role)
        await interation.response.send_message(embed=embed, ephemeral=True)
