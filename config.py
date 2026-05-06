# Last updated: 2026-05-06
"""Centralized configuration: env vars and region/routing maps."""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Secrets / env ---
BOT_TOKEN_PROD = os.getenv("BOT_TOKEN_PROD")
BOT_TOKEN_TEST = os.getenv("BOT_TOKEN_TEST")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
BEEMO_API_BASE_URL = os.getenv("BEEMO_API_BASE_URL", "https://api.beemobot.fr")
WEBAPP_URL = os.getenv("WEBAPP_URL", "http://localhost:3000")

# --- Riot defaults ---
DEFAULT_REGION = "euw1"
DEFAULT_API_REGION = "EUROPE"
DDRAGON_BASE = "https://ddragon.leagueoflegends.com"

# --- Region mapping (display tag -> Riot platform) ---
REGION_REAL_NAMES = {
    "EUW": "euw1",
    "EUNE": "eun1",
    "NA": "na1",
    "BR": "br1",
    "JP": "jp1",
    "KR": "kr",
    "LA": "la1",
    "LAS": "la2",
    "OC": "oc1",
    "TR": "tr1",
    "RU": "ru",
}

# --- Region routing (Riot platform -> regional cluster) ---
REGION_ROUTING = {
    "euw1": "europe",
    "eun1": "europe",
    "tr1": "europe",
    "ru": "europe",
    "na1": "americas",
    "br1": "americas",
    "la1": "americas",
    "la2": "americas",
    "kr": "asia",
    "jp1": "asia",
    "oc1": "sea",
}
