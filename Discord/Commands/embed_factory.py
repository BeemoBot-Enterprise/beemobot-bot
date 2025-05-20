import discord
from enum import *
import requests
from PIL import Image
from io import BytesIO
from collections import Counter

class Runes:
    top = "https://cdn.discordapp.com/attachments/572836578267889664/1374504793740939294/image.png?ex=682e4ad7&is=682cf957&hm=46d612ad066a1a22120e4fc1fbabbedd450e9368dcc9122f4ae83be914a2b302&"
    jungle = "https://cdn.discordapp.com/attachments/572836578267889664/1374504928281886871/image.png?ex=682e4af7&is=682cf977&hm=a4ff389b5c092c279d791583b08320827b2ee125d849ebdda7724433119dd842&"
    mid = "https://cdn.discordapp.com/attachments/572836578267889664/1374505043130060952/image.png?ex=682e4b13&is=682cf993&hm=ea80a3ec65251c00bb4bab0ee5ce2eac3cde59cb01ec8154cc89b12f73333ab4&"
    bot = "https://cdn.discordapp.com/attachments/572836578267889664/1374505119017861241/image.png?ex=682e4b25&is=682cf9a5&hm=518bb18a3c114df857595104556bd606d55fb10b4a2c677e6a5a51dc733275d7&"
    support = "https://cdn.discordapp.com/attachments/572836578267889664/1374505207962275962/image.png?ex=682e4b3a&is=682cf9ba&hm=abfc01fd290a34396c87476e31360199df12fd08f509ca13568eb1e10a827960&"

class TeemoImages:
    DARKTEEMO = "https://cdn.discordapp.com/attachments/572836578267889664/1374512593447682069/width512.png?ex=682e521b&is=682d009b&hm=dfcc1fa6c5fea93db84dbb25f493b966735e726b0f369a1e47279f2983635fd0&"
    BEEMO = "https://cdn.discordapp.com/attachments/572836578267889664/1374512508798242855/width508.png?ex=682e5207&is=682d0087&hm=eec4cc5551424f0948ad25cf7779e60d507ef15ce96342c7b836cc59d24b4d7f&"
    TEEMO = "https://cdn.discordapp.com/attachments/572836578267889664/1374512685223514235/width800.png?ex=682e5231&is=682d00b1&hm=40facf50cfc539c2658c79c12e957b19487ef0289647151f5fb901895488c4f4&"
    TEEMO_MUSHROOM = "https://static.wikia.nocookie.net/leagueoflegends/images/0/0c/Teemo_Mushroom_Trap_Render.png/revision/latest?cb=20240926204910"
    
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

#SHROOM
def embed_shroom(name, tag, region, icon_link, shrooms, respects):    
    # Obtenir la couleur dominante de l'image
    dominant_color = get_dominant_color(icon_link)
    color_hex = int('%02x%02x%02x' % dominant_color, 16)  # Convertir RGB en hexadécimal
    
    embed=discord.Embed(
        title="Teemo is SHROOMING",
        description="You just Shroomed this guy",
        color=color_hex
        )
    embed.set_author(
        name="BeemoBot",
        url="https://github.com/BeemoBot-Enterprise",
        icon_url="https://avatars.githubusercontent.com/u/189348916?s=200&v=4"
        )
    embed.add_field(
        name="User", 
        value=f"```{name}#{tag}```",
        inline=True
        )
    embed.add_field(
        name="Region",
        value=f"```{region}```",
        inline=True
        )
    embed.add_field(
        name="",
        value="─────────────────────────",
        inline=False
        )
    embed.add_field(
        name="Shrooms", 
        value=f"```{shrooms}```",
        inline=True
        )
    embed.add_field(
        name="Respects", 
        value=f"```{respects}```",
        inline=True
        )
    embed.set_thumbnail(url=icon_link)
    embed.set_footer(text="provided by BeemoBot")
    embed.set_image(url=TeemoImages.DARKTEEMO)
    return embed

def embed_respect(name, tag, region, icon_link, shrooms, respects):    
    # Obtenir la couleur dominante de l'image
    dominant_color = get_dominant_color(icon_link)
    color_hex = int('%02x%02x%02x' % dominant_color, 16)  # Convertir RGB en hexadécimal
    
    embed=discord.Embed(
        title="Teemo is RESPECTING",
        description="You Respect this guy",
        color=color_hex
        )
    embed.set_author(
        name="BeemoBot",
        url="https://github.com/BeemoBot-Enterprise",
        icon_url="https://avatars.githubusercontent.com/u/189348916?s=200&v=4"
        )
    embed.add_field(
        name="User", 
        value=f"```{name}#{tag}```",
        inline=True
        )
    embed.add_field(
        name="Region",
        value=f"```{region}```",
        inline=True
        )
    embed.add_field(
        name="",
        value="─────────────────────────",
        inline=False
        )
    embed.add_field(
        name="Shrooms", 
        value=f"```{shrooms}```",
        inline=True
        )
    embed.add_field(
        name="Respects", 
        value=f"```{respects}```",
        inline=True
        )
    embed.set_thumbnail(url=icon_link)
    embed.set_footer(text="provided by BeemoBot")
    embed.set_image(url=TeemoImages.BEEMO)
    return embed

def embed_help_orion():
    Icon = "https://cdn.discordapp.com/attachments/1301209240379199591/1374372873950466179/Minimalistic-vector-hd-rocket-clipart-simple-hd-fly-into-the_194958_wh860.png?ex=682dcffb&is=682c7e7b&hm=ac776562e6e341024b93b62b1c12811408d437df4fc255660c29c228192c680f&"
    # Obtenir la couleur dominante de l'image
    dominant_color = get_dominant_color(Icon)
    color_hex = int('%02x%02x%02x' % dominant_color, 16)  # Convertir RGB en hexadécimal
    
    embed = discord.Embed(
        title="Message d'Orion",
        description="Orion, le meilleur compagnon qu'un cosmonaute puisse avoir va vous guider pour la suite. Rendez-vous au stand de Stellar pour en apprendre plus sur lui.",
        color=color_hex
    )
    embed.set_thumbnail(url=Icon)
    return embed

def embed_top_shrooms(top_shrooms):
    # Obtenir la couleur dominante de l'image
    dominant_color = get_dominant_color(TeemoImages.TEEMO_MUSHROOM)
    color_hex = int('%02x%02x%02x' % dominant_color, 16)  # Convertir RGB en hexadécimal
    
    embed = discord.Embed(
        title="Top 10 Shrooms",
        description="Here is the top 10 shrooms",
        color=color_hex
    )
    embed.set_thumbnail(url=TeemoImages.TEEMO_MUSHROOM)
    if top_shrooms.get("status") == "success" and isinstance(top_shrooms.get("data"), list):
        for i, user in enumerate(top_shrooms["data"]):
            embed.add_field(name=f"#{i+1} {user['username']}", value=f"Shrooms: {user['shrooms']}", inline=False)
    else:
        embed.add_field(name="No data", value="No shrooms data found", inline=False)

    
    return embed

def embed_top_respects(top_respects):
    # Obtenir la couleur dominante de l'image
    dominant_color = get_dominant_color(TeemoImages.TEEMO)
    color_hex = int('%02x%02x%02x' % dominant_color, 16)  # Convertir RGB en hexadécimal
    
    embed = discord.Embed(
        title="Top 10 Respects",
        description="Here is the top 10 respects",
        color=color_hex
    )
    embed.set_thumbnail(url=TeemoImages.TEEMO)
    
    if top_respects.get("status") == "success" and isinstance(top_respects.get("data"), list):
        for i, user in enumerate(top_respects["data"]):
            embed.add_field(name=f"#{i+1} {user['username']}", value=f"Respects: {user['respects']}", inline=False)
    else:
        embed.add_field(name="No data", value="No respects data found", inline=False)

    
    return embed

def embed_runes(role):
    
    embed = discord.Embed(
        title="Best Runes for Teemo",
        description=f"Here is the best runes for {role}",
        color=0x00ff00  # Couleur par défaut, peut être modifiée selon la couleur dominante
    )
    
    embed.set_thumbnail(url=TeemoImages.TEEMO)
    # Ajouter les runes spécifiques au rôle
    if role == "top":
        embed.set_image(url=Runes.top)
        embed.add_field(name="Top Runes", value="Rune details for Top role", inline=False)
        # Obtenir la couleur dominante de l'image
        dominant_color = get_dominant_color(Runes.top)
        color_hex = int('%02x%02x%02x' % dominant_color, 16)  # Convertir RGB en hexadécimal
    elif role == "mid":
        embed.set_image(url=Runes.mid)
        embed.add_field(name="Mid Runes", value="Rune details for Mid role", inline=False)
        # Obtenir la couleur dominante de l'image
        dominant_color = get_dominant_color(Runes.mid)
        color_hex = int('%02x%02x%02x' % dominant_color, 16)
    elif role == "bot":
        embed.set_image(url=Runes.bot)
        embed.add_field(name="Bot Runes", value="Rune details for Bot role", inline=False)
        # Obtenir la couleur dominante de l'image
        dominant_color = get_dominant_color(Runes.bot)
        color_hex = int('%02x%02x%02x' % dominant_color, 16)
    elif role == "jungle":
        embed.set_image(url=Runes.jungle)
        embed.add_field(name="Jungle Runes", value="Rune details for Jungle role", inline=False)
        # Obtenir la couleur dominante de l'image
        dominant_color = get_dominant_color(Runes.jungle)
        color_hex = int('%02x%02x%02x' % dominant_color, 16)
    elif role == "support":
        embed.set_image(url=Runes.support)
        embed.add_field(name="Support Runes", value="Rune details for Support role", inline=False)
        # Obtenir la couleur dominante de l'image
        dominant_color = get_dominant_color(Runes.support)
        color_hex = int('%02x%02x%02x' % dominant_color, 16)
    
    embed.color = color_hex  # Mettre à jour la couleur de l'embed avec la couleur dominante
    embed.set_footer(text="provided by BeemoBot")
    return embed