# Last updated: 2026-05-06
def split_summoner_name_and_tag(summoner_name):
    """Split 'Name#Tag' into ['Name', 'Tag']."""
    return summoner_name.split("#")
