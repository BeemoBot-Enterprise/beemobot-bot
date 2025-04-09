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

def get_id_by_puuid_and_region(puuid, region):
    print("get_id_by_puuid_and_region")
    return lol_watcher.summoner.by_puuid(region, puuid)["id"]

def get_user_id_by_name_tag_and_region(name, tag, region):
    print("get_user_id_by_name_tag_and_region")
    GPBNAT = get_puuid_by_name_and_tag(name, tag)
    GIBPAR = get_id_by_puuid_and_region(GPBNAT, region)
    return GIBPAR
# ================================================================================================
def get_user_icon_id_by_user_id_and_region(id, region):
    print("get_user_icon_id_by_user_id_and_region")
    return lol_watcher.summoner.by_id(region, id)["profileIconId"]

def get_rank_by_id_and_region(id, region):
    print("get_rank_by_id_and_region")
    return lol_watcher.league.by_summoner(region, id)

def slash_user(name, tag, region):
    print("slash_user")
    
    GUIBNTAR = get_user_id_by_name_tag_and_region(name, tag, region)
    GUIIBUIAR = get_user_icon_id_by_user_id_and_region(GUIBNTAR, region)
    GIBI = get_icon_by_iconId(GUIIBUIAR, lol_watcher, region)
    
    return GIBI

# print('rank :')
# print(get_rank_by_id_and_region(get_user_id_by_name_tag_and_region("MFF电竞 VX WTWTTC", "LPL整队", "euw1"), "euw1"))
