# Last updated: 2026-01-21
import os
from riotwatcher import LolWatcher, RiotWatcher, ApiError
from colorama import Fore, Back, Style
from toolbox import *
from Riot.riot_toolbox import *

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
DEFAULT_REGION = 'euw1'
DEFAULT_API_REGION = 'EUROPE'

lol_watcher = LolWatcher(RIOT_API_KEY)
riot_watcher = RiotWatcher(RIOT_API_KEY)

# ================================================================================================
# ====================================== User Infos ==============================================
# ================================================================================================

def get_puuid_by_name_and_tag(name, tag):
    print("get_puuid_by_name_tag_and_region")
    return riot_watcher.account.by_riot_id(DEFAULT_API_REGION, name, tag)["puuid"]

def get_summoner_by_puuid(puuid, region):
    print("get_summoner_by_puuid")
    summoner_data = lol_watcher.summoner.by_puuid(region, puuid)
    print(f"Summoner data: {summoner_data}")
    return summoner_data

def get_user_id_by_name_tag_and_region(name, tag, region):
    print("get_user_id_by_name_tag_and_region")
    return get_puuid_by_name_and_tag(name, tag)

# ================================================================================================
def get_user_icon_id_by_user_id_and_region(puuid, region):
    print("get_user_icon_id_by_user_id_and_region")
    summoner_data = get_summoner_by_puuid(puuid, region)
    return summoner_data["profileIconId"]

def get_rank_by_id_and_region(puuid, region):
    print("get_rank_by_id_and_region")
    summoner_data = get_summoner_by_puuid(puuid, region)
    encrypted_id = summoner_data.get('id')
    if encrypted_id:
        rank_data = lol_watcher.league.by_summoner(region, encrypted_id)
        return rank_data
    return []

def get_user_full_data(name, tag, region):
    print("get_user_full_data")
    puuid = get_puuid_by_name_and_tag(name, tag)
    summoner_data = get_summoner_by_puuid(puuid, region)
    encrypted_id = summoner_data.get('id')
    
    print(f"Encrypted Summoner ID: {encrypted_id}")
    
    rank_data = []
    if encrypted_id:
        print(f"Calling league.by_summoner with region={region}, id={encrypted_id}")
        rank_data = lol_watcher.league.by_summoner(region, encrypted_id)
        print(f"Rank data received: {rank_data}")
    else:
        print("No encrypted ID found in summoner data")
    
    icon_url = get_icon_by_iconId(summoner_data["profileIconId"], lol_watcher, region)
    
    return {
        'rank': rank_data,
        'summoner_level': summoner_data.get('summonerLevel', 0),
        'icon_url': icon_url,
        'name': name
    }

def slash_user(name, tag, region):
    print("slash_user")
    
    puuid = get_user_id_by_name_tag_and_region(name, tag, region)
    icon_id = get_user_icon_id_by_user_id_and_region(puuid, region)
    icon_url = get_icon_by_iconId(icon_id, lol_watcher, region)
    
    return icon_url

# print('rank :')
# print(get_rank_by_id_and_region(get_user_id_by_name_tag_and_region("MFF电竞 VX WTWTTC", "LPL整队", "euw1"), "euw1"))
