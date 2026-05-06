# Last updated: 2026-05-06
import logging
import requests
from riotwatcher import LolWatcher, RiotWatcher
from config import RIOT_API_KEY, DEFAULT_API_REGION
from Riot.riot_toolbox import get_icon_by_iconId, region_to_routing

logger = logging.getLogger(__name__)

lol_watcher = LolWatcher(RIOT_API_KEY)
riot_watcher = RiotWatcher(RIOT_API_KEY)

DEFAULT_HTTP_TIMEOUT = 10

# ================================================================================================
# ====================================== User Infos ==============================================
# ================================================================================================


def get_puuid_by_name_and_tag(name, tag):
    return riot_watcher.account.by_riot_id(DEFAULT_API_REGION, name, tag)["puuid"]


def get_summoner_by_puuid(puuid, region):
    return lol_watcher.summoner.by_puuid(region, puuid)


def get_user_id_by_name_tag_and_region(name, tag, region):
    return get_puuid_by_name_and_tag(name, tag)


def get_user_icon_id_by_user_id_and_region(puuid, region):
    summoner_data = get_summoner_by_puuid(puuid, region)
    return summoner_data["profileIconId"]


def get_rank_by_puuid(puuid, region):
    url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
    headers = {"X-Riot-Token": RIOT_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=DEFAULT_HTTP_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        logger.warning("Rank fetch failed for puuid=%s region=%s: %s", puuid, region, exc)
        return []


def get_rank_by_id_and_region(puuid, region):
    return get_rank_by_puuid(puuid, region)


def get_user_full_data(name, tag, region):
    puuid = get_puuid_by_name_and_tag(name, tag)
    summoner_data = get_summoner_by_puuid(puuid, region)
    rank_data = get_rank_by_puuid(puuid, region)
    icon_url = get_icon_by_iconId(summoner_data["profileIconId"], lol_watcher, region)

    return {
        "rank": rank_data,
        "summoner_level": summoner_data.get("summonerLevel", 0),
        "icon_url": icon_url,
        "name": name,
    }


def slash_user(name, tag, region):
    puuid = get_user_id_by_name_tag_and_region(name, tag, region)
    icon_id = get_user_icon_id_by_user_id_and_region(puuid, region)
    return get_icon_by_iconId(icon_id, lol_watcher, region)


def get_last_match_data(name, tag, region):
    puuid = get_puuid_by_name_and_tag(name, tag)
    routing_region = region_to_routing(region)
    headers = {"X-Riot-Token": RIOT_API_KEY}

    try:
        ids_url = (
            f"https://{routing_region}.api.riotgames.com"
            f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
        )
        response = requests.get(
            ids_url,
            headers=headers,
            params={"start": 0, "count": 1},
            timeout=DEFAULT_HTTP_TIMEOUT,
        )
        response.raise_for_status()
        match_ids = response.json()

        if not match_ids:
            return None

        match_id = match_ids[0]
        match_url = f"https://{routing_region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        match_response = requests.get(match_url, headers=headers, timeout=DEFAULT_HTTP_TIMEOUT)
        match_response.raise_for_status()
        match_data = match_response.json()

        for participant in match_data["info"]["participants"]:
            if participant["puuid"] == puuid:
                return {
                    "champion": participant["championName"],
                    "kills": participant["kills"],
                    "deaths": participant["deaths"],
                    "assists": participant["assists"],
                    "items": [participant.get(f"item{i}", 0) for i in range(7)],
                    "win": participant["win"],
                    "gameDuration": match_data["info"]["gameDuration"],
                    "gameMode": match_data["info"]["gameMode"],
                }
        return None
    except requests.RequestException as exc:
        logger.warning("Last match fetch failed for %s#%s: %s", name, tag, exc)
        return None
