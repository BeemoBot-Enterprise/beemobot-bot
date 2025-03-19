import discord
from enum import *
import requests
from PIL import Image
from io import BytesIO
from collections import Counter

class Rank(IntEnum):
    UNRANKED = -1
    IRON = 0
    BRONZE = 1
    SILVER = 2
    GOLD = 3
    PLATINUM = 4
    EMERALD = 5
    DIAMOND = 6
    MASTER = 7
    GRANDMASTER = 8
    CHALLENGER = 9

def get_highest_rank_image(SoloQ, FlexQ):
    print("get_highest_rank_image")
    # Convertir les rangs en Enum pour comparaison
    soloq_rank = Rank[SoloQ.upper()]
    flexq_rank = Rank[FlexQ.upper()]
    if SoloQ == "UNRANKED" and FlexQ == "UNRANKED":
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/1/13/Season_2023_-_Unranked.png/revision/latest?cb=20231007211937'
    
    # Comparer les rangs
    if SoloQ != "UNRANKED" or FlexQ != "UNRANKED":
        highest_rank = soloq_rank if soloq_rank > flexq_rank else flexq_rank
        # Retourner l'image correspondant au rang le plus élevé
        if highest_rank == Rank.IRON:
            return 'https://static.wikia.nocookie.net/leagueoflegends/images/f/f8/Season_2023_-_Iron.png/revision/latest?cb=20231007195831'
        if highest_rank == Rank.BRONZE:
            return 'https://static.wikia.nocookie.net/leagueoflegends/images/c/cb/Season_2023_-_Bronze.png/revision/latest?cb=20231007195824'
        if highest_rank == Rank.SILVER:
            return 'https://static.wikia.nocookie.net/leagueoflegends/images/c/c4/Season_2023_-_Silver.png/revision/latest?cb=20231007195834'
        if highest_rank == Rank.GOLD:
            return 'https://static.wikia.nocookie.net/leagueoflegends/images/7/78/Season_2023_-_Gold.png/revision/latest?cb=20231007195829'
        if highest_rank == Rank.PLATINUM:
            return 'https://static.wikia.nocookie.net/leagueoflegends/images/b/bd/Season_2023_-_Platinum.png/revision/latest?cb=20231007195833'
        if highest_rank == Rank.EMERALD:
            return 'https://static.wikia.nocookie.net/leagueoflegends/images/4/4b/Season_2023_-_Emerald.png/revision/latest?cb=20231007195827'
        if highest_rank == Rank.DIAMOND:
            return 'https://static.wikia.nocookie.net/leagueoflegends/images/3/37/Season_2023_-_Diamond.png/revision/latest?cb=20231007195826'
        if highest_rank == Rank.MASTER:
            return 'https://static.wikia.nocookie.net/leagueoflegends/images/d/d5/Season_2023_-_Master.png/revision/latest?cb=20231007195832'
        if highest_rank == Rank.GRANDMASTER:
            return 'https://static.wikia.nocookie.net/leagueoflegends/images/6/64/Season_2023_-_Grandmaster.png/revision/latest?cb=20231007195830'
        if highest_rank == Rank.CHALLENGER:
            return 'https://static.wikia.nocookie.net/leagueoflegends/images/1/14/Season_2023_-_Challenger.png/revision/latest?cb=20231007195825'
    else:
        return 'https://static.wikia.nocookie.net/leagueoflegends/images/1/13/Season_2023_-_Unranked.png/revision/latest?cb=20231007211937'   

def get_dominant_color(image_url):
    # Télécharger l'image depuis l'URL
    print("get_dominant_color")
    print(image_url)
    response = requests.get(image_url)
    if response.status_code != 200:
        raise Exception(f"Impossible de télécharger l'image depuis {image_url}")
    
    # Charger l'image dans PIL
    image = Image.open(BytesIO(response.content))
    
    # Redimensionner l'image pour réduire la complexité (optionnel)
    image = image.resize((50, 50))  # Réduire la taille pour accélérer le traitement
    
    # Convertir l'image en mode RGB
    image = image.convert('RGB')
    
    # Obtenir les couleurs de chaque pixel
    pixels = list(image.getdata())
    
    # Compter les couleurs les plus fréquentes
    most_common_color = Counter(pixels).most_common(1)[0][0]  # (R, G, B)
    
    # Retourner la couleur dominante
    return most_common_color

# Exemple d'utilisation dans embed_user_info
def embed_user_info(infos, Name, icon_link):
    if len(infos) > 0:
        SoloQ = infos[0]
        SoloQ_TIER = SoloQ["tier"]
        SoloQ_Rank = str(SoloQ["tier"]) + ' ' + str(SoloQ["rank"])
        SoloQ_LP = SoloQ["leaguePoints"]
        SoloQ_WR = SoloQ["wins"] / (SoloQ["wins"] + SoloQ["losses"])
    else :
        SoloQ_TIER = "UNRANKED"
        SoloQ_Rank = ""
        SoloQ_LP = 0
        SoloQ_WR = 0
    
    if len(infos) > 1:
        FlexQ = infos[1]
        FlexQ_TIER = FlexQ["tier"]
        FlexQ_Rank = str(FlexQ["tier"]) + ' ' + str(FlexQ["rank"])
        FlexQ_LP = FlexQ["leaguePoints"]
        FlexQ_WR = FlexQ["wins"] / (FlexQ["wins"] + FlexQ["losses"])
    else :
        FlexQ_TIER = "UNRANKED"
        FlexQ_Rank = ""
        FlexQ_LP = 0
        FlexQ_WR = 0
    
    # Highest_Masteries = infos["highest_masteries"]
    Highest_Rank_Image = get_highest_rank_image(SoloQ_TIER, FlexQ_TIER)
    
    # Obtenir la couleur dominante de l'image
    dominant_color = get_dominant_color(icon_link)
    color_hex = int('%02x%02x%02x' % dominant_color, 16)  # Convertir RGB en hexadécimal
    
    # Créer l'embed
    embed = discord.Embed(
        title=f"{Name}' Infos",
        description=f"Here the infos we gathered on {Name}",
        color=color_hex
    )
    embed.set_author(
        name="BeemoBot",
        url="https://github.com/BeemoBot-Enterprise",
        icon_url="https://avatars.githubusercontent.com/u/189348916?s=200&v=4"
    )
    embed.set_thumbnail(url=icon_link)
    embed.add_field(name="SoloQ", value=f"{SoloQ_Rank} {SoloQ_LP} LP | {SoloQ_WR:.2%}")
    embed.add_field(name="FlexQ", value=f"{FlexQ_Rank} {FlexQ_LP} LP | {FlexQ_WR:.2%}")
    embed.set_footer(text="provided by BeemoBot")
    embed.set_image(url=Highest_Rank_Image)
    return embed
    
# NAME
# ICON
# COLOR
# SOLOQ
# FLEXQ
# HIGHEST MASTERIES
# WINRATE
# HIHGHEST RANK IMAGE