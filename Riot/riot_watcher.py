import os
from riotwatcher import LolWatcher, RiotWatcher, ApiError
from colorama import Fore, Back, Style
from toolbox import *

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
DEFAULT_REGION = 'euw1'
DEFAULT_API_REGION = 'EUROPE'

lol_watcher = LolWatcher(RIOT_API_KEY)
riot_watcher = RiotWatcher(RIOT_API_KEY)

def get_puuid_by_name(summoner_name):
    summoner_name = split_summoner_name_and_tag(summoner_name)
    name = summoner_name[0]
    tag = summoner_name[1]
    return riot_watcher.account.by_riot_id(DEFAULT_API_REGION, name, tag)["puuid"]

def get_id_by_puuid(region, puuid):
    return lol_watcher.summoner.by_puuid(region, puuid)["id"]

def get_rank_by_summoner_id(region, id):
    return lol_watcher.league.by_summoner(region, id)

def get_icon_by_iconId(iconId):
    return f"http://ddragon.leagueoflegends.com/cdn/{get_game_version()['profileicon']}/img/profileicon/{iconId}.png"

def get_game_version():
    return lol_watcher.data_dragon.versions_for_region(DEFAULT_REGION)["n"]

print(get_game_version())
print(get_rank_by_summoner_id(DEFAULT_REGION, get_id_by_puuid(DEFAULT_REGION, get_puuid_by_name("Nunch#N7789"))))