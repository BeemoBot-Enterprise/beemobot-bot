# Last updated: 2026-01-21
import requests

# Return the current game version
def get_game_version(lol_watcher, DEFAULT_REGION):
    return lol_watcher.data_dragon.versions_for_region(DEFAULT_REGION)["n"]

# Return the icon of a player by his iconId
def get_icon_by_iconId(iconId, lol_watcher, DEFAULT_REGION):
    return f"http://ddragon.leagueoflegends.com/cdn/{get_game_version(lol_watcher, DEFAULT_REGION)['profileicon']}/img/profileicon/{iconId}.png"

def get_item_name_by_id(item_id, lol_watcher, DEFAULT_REGION):
    if item_id == 0:
        return None
    
    try:
        version = get_game_version(lol_watcher, DEFAULT_REGION)['item']
        url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json"
        response = requests.get(url)
        response.raise_for_status()
        items_data = response.json()
        
        item_info = items_data['data'].get(str(item_id))
        if item_info:
            return item_info['name']
        return f"Item {item_id}"
    except Exception as e:
        print(f"Error getting item name: {e}")
        return f"Item {item_id}"

def region_real_name(region):
    if region == "EUW":
        return "euw1"
    if region == "EUNE":
        return "eun1"
    if region == "NA":
        return "na1"
    if region == "BR":
        return "br1"
    if region == "JP":
        return "jp1"
    if region == "KR":
        return "kr"
    if region == "LA":
        return "la1"
    if region == "LAS":
        return "la2"
    if region == "OC":
        return "oc1"
    if region == "TR":
        return "tr1"
    if region == "RU":
        return "ru"
    return "euw1"

def region_to_routing(region):
    if region in ["euw1", "eun1", "tr1", "ru"]:
        return "europe"
    if region in ["na1", "br1", "la1", "la2"]:
        return "americas"
    if region in ["kr", "jp1"]:
        return "asia"
    if region == "oc1":
        return "sea"
    return "europe"