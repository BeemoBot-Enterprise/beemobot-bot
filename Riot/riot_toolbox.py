# Last updated: 2026-05-06
import logging
import requests
from config import REGION_REAL_NAMES, REGION_ROUTING, DEFAULT_REGION, DDRAGON_BASE

logger = logging.getLogger(__name__)


def get_game_version(lol_watcher, region=DEFAULT_REGION):
    """Return the current game data dragon versions dict for a region."""
    return lol_watcher.data_dragon.versions_for_region(region)["n"]


def get_icon_by_iconId(iconId, lol_watcher, region=DEFAULT_REGION):
    """Return the URL of a player's profile icon."""
    versions = get_game_version(lol_watcher, region)
    return f"{DDRAGON_BASE}/cdn/{versions['profileicon']}/img/profileicon/{iconId}.png"


def get_item_name_by_id(item_id, lol_watcher, region=DEFAULT_REGION):
    """Return the name of an item by its ID, or None if item_id == 0."""
    if item_id == 0:
        return None

    try:
        version = get_game_version(lol_watcher, region)["item"]
        url = f"{DDRAGON_BASE}/cdn/{version}/data/en_US/item.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        items_data = response.json()

        item_info = items_data["data"].get(str(item_id))
        if item_info:
            return item_info["name"]
        return f"Item {item_id}"
    except requests.RequestException as exc:
        logger.warning("Failed to fetch item %s: %s", item_id, exc)
        return f"Item {item_id}"


def region_real_name(region):
    """Map a display region tag (EUW, KR…) to a Riot platform (euw1, kr…)."""
    return REGION_REAL_NAMES.get(region, DEFAULT_REGION)


def region_to_routing(region):
    """Map a Riot platform (euw1, kr…) to its regional cluster (europe, asia…)."""
    return REGION_ROUTING.get(region, "europe")
