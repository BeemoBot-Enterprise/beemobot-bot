# Last updated: 2026-01-21
import os
from riotwatcher import LolWatcher, RiotWatcher, ApiError
from colorama import Fore, Back, Style
from toolbox import *
from Riot.riot_toolbox import *
import requests

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
    summoner_data = lol_watcher.summoner.by_puuid(region, puuid)
    print(f"[DEBUG] Summoner API Response Keys: {list(summoner_data.keys())}")
    print(f"[DEBUG] Full Summoner Data: {summoner_data}")
    return summoner_data

def get_user_id_by_name_tag_and_region(name, tag, region):
    print("get_user_id_by_name_tag_and_region")
    return get_puuid_by_name_and_tag(name, tag)

# ================================================================================================
def get_user_icon_id_by_user_id_and_region(puuid, region):
    print("get_user_icon_id_by_user_id_and_region")
    summoner_data = get_summoner_by_puuid(puuid, region)
    return summoner_data["profileIconId"]

def get_rank_by_puuid(puuid, region):
    url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        rank_data = response.json()
        print(f"[DEBUG] Rank data from PUUID endpoint: {rank_data}")
        return rank_data
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to get rank by PUUID: {e}")
        return []

def get_rank_by_id_and_region(puuid, region):
    return get_rank_by_puuid(puuid, region)

def get_user_full_data(name, tag, region):
    puuid = get_puuid_by_name_and_tag(name, tag)
    summoner_data = get_summoner_by_puuid(puuid, region)
    
    rank_data = get_rank_by_puuid(puuid, region)
    
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

def get_last_match_data(name, tag, region):
    puuid = get_puuid_by_name_and_tag(name, tag)
    routing_region = region_to_routing(region)
    
    url = f"https://{routing_region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    params = {"start": 0, "count": 1}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        match_ids = response.json()
        
        if not match_ids:
            return None
        
        match_id = match_ids[0]
        match_url = f"https://{routing_region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        match_response = requests.get(match_url, headers=headers)
        match_response.raise_for_status()
        match_data = match_response.json()
        
        for participant in match_data['info']['participants']:
            if participant['puuid'] == puuid:
                return {
                    'champion': participant['championName'],
                    'kills': participant['kills'],
                    'deaths': participant['deaths'],
                    'assists': participant['assists'],
                    'items': [
                        participant.get('item0', 0),
                        participant.get('item1', 0),
                        participant.get('item2', 0),
                        participant.get('item3', 0),
                        participant.get('item4', 0),
                        participant.get('item5', 0),
                        participant.get('item6', 0)
                    ],
                    'win': participant['win'],
                    'gameDuration': match_data['info']['gameDuration'],
                    'gameMode': match_data['info']['gameMode']
                }
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to get last match: {e}")
        return None

# print('rank :')
# print(get_rank_by_id_and_region(get_user_id_by_name_tag_and_region("MFF电竞 VX WTWTTC", "LPL整队", "euw1"), "euw1"))
