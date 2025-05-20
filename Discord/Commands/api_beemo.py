import requests

BASE_URL = "https://api.beemobot.fr/game"

def give_shroom(username):
    url = f"{BASE_URL}/shroom"
    payload = {"username": username}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erreur give_shroom : {e}")
        return None

def give_respect(username):
    url = f"{BASE_URL}/respect"
    payload = {"username": username}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erreur give_respect : {e}")
        return None

def get_user_stats(username):
    url = f"{BASE_URL}/stats/{username}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erreur get_user_stats : {e}")
        return None

def get_top_shrooms():
    url = f"{BASE_URL}/top/shrooms"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erreur get_top_shrooms : {e}")
        return None

def get_top_respects():
    url = f"{BASE_URL}/top/respects"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(response.json())
        return response.json()
    except requests.RequestException as e:
        print(f"Erreur get_top_respects : {e}")
        return None
