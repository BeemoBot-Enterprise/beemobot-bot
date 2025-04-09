# Return the current game version
def get_game_version(lol_watcher, DEFAULT_REGION):
    return lol_watcher.data_dragon.versions_for_region(DEFAULT_REGION)["n"]

# Return the icon of a player by his iconId
def get_icon_by_iconId(iconId, lol_watcher, DEFAULT_REGION):
    return f"http://ddragon.leagueoflegends.com/cdn/{get_game_version(lol_watcher, DEFAULT_REGION)['profileicon']}/img/profileicon/{iconId}.png"

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