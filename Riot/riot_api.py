# import os
# import requests
# from dotenv import load_dotenv
# from riotwatcher import LolWatcher, ApiError
# from toolbox import *

# # Base URL for Riot API, carefull base url isn't the same for all request, check https://developer.riotgames.com/apis
# RIOT_API_BASE_URL = "https://euw1.api.riotgames.com/lol"

# # Get Riot API key from environment variables
# RIOT_API_KEY = os.getenv("RIOT_API_KEY")

# # Headers for authentication
# HEADERS = {
#     "X-Riot-Token": RIOT_API_KEY
# }

# def get_puuid_by_name(summoner_name):
#     summoner_name = split_summoner_name_and_tag(summoner_name)
#     name = summoner_name[0]
#     tag = summoner_name[1]
#     url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
#     response = requests.get(url, headers=HEADERS)
#     print(response.json())
#     if response.status_code == 200:
#         return response.json()["puuid"]  # Return the JSON data
#     else:
#         return {"error": response.status_code, "message": response.json()}

# def get_summoner_by_puuid(puuid):
#     url = f"{RIOT_API_BASE_URL}/summoner/v4/summoners/by-puuid/{puuid}"
#     response = requests.get(url, headers=HEADERS)
#     if response.status_code == 200:
#         return response.json()  # Return the JSON data
#     else:
#         return {"error": response.status_code, "message": response.json()}
