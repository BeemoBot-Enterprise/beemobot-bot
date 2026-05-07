# Last updated: 2026-05-06
import logging
from enum import IntEnum
from io import BytesIO
from collections import Counter
import discord
import requests
from PIL import Image
from Riot.riot_watcher import lol_watcher
from Riot.riot_toolbox import get_item_name_by_id

logger = logging.getLogger(__name__)

class Runes:
    top = "attachment://image_top.png"
    jungle = "attachment://image_jungle.png"
    mid = "attachment://image_mid.png"
    bot = "attachment://image_bot.png"
    support = "attachment://image_supp.png"

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

# Discord blurple — fallback color when an image can't be fetched (e.g. expired
# CDN URL). Lots of embeds reference Discord attachment URLs that expire ~24h.
DEFAULT_EMBED_COLOR = (88, 101, 242)


def get_dominant_color(image_url, fallback=DEFAULT_EMBED_COLOR):
    try:
        response = requests.get(image_url, timeout=5)
        if response.status_code != 200:
            logger.warning(
                "dominant_color: %d for %s, falling back",
                response.status_code,
                image_url,
            )
            return fallback
        image = Image.open(BytesIO(response.content)).resize((50, 50)).convert('RGB')
        return Counter(list(image.getdata())).most_common(1)[0][0]
    except Exception as exc:
        logger.warning("dominant_color failed for %s: %s, falling back", image_url, exc)
        return fallback


def get_dominant_color_from_file(file_path):
    image = Image.open(file_path).resize((50, 50)).convert('RGB')
    return Counter(list(image.getdata())).most_common(1)[0][0]


def embed_user_info(infos, Name, icon_link, summoner_level=0):
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
        description=f"Here the infos we gathered on {Name} (Level {summoner_level})",
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
        color=0x00ff00
    )
    
    embed.set_thumbnail(url=TeemoImages.TEEMO)
    
    rune_file_map = {
        "top": "image_top.png",
        "mid": "image_mid.png",
        "bot": "image_bot.png",
        "jungle": "image_jungle.png",
        "support": "image_supp.png"
    }
    
    if role in rune_file_map:
        file_name = rune_file_map[role]
        embed.set_image(url=f"attachment://{file_name}")
        # embed.add_field(name=f"{role.capitalize()} Runes", value=f"Rune details for {role.capitalize()} role", inline=False)
        
        file_path = f"Runes/{file_name}"
        try:
            dominant_color = get_dominant_color_from_file(file_path)
            color_hex = int('%02x%02x%02x' % dominant_color, 16)
            embed.color = color_hex
        except (OSError, ValueError) as exc:
            logger.warning("Failed to compute dominant color: %s", exc)
    
    embed.set_footer(text="provided by BeemoBot")
    return embed, rune_file_map.get(role)

def _severity_emoji(severity: str) -> str:
    return {"red": "🔴", "yellow": "🟡", "green": "🟢"}.get(severity, "⚪")


def embed_debrief(data: dict) -> discord.Embed:
    """Embed for /debrief — recap of last match with heuristic verdicts."""
    win = data.get("win", False)
    color = 0x2ECC71 if win else 0xE74C3C
    title = f"{'🏆' if win else '💀'} Debrief — {data.get('championName', 'Champion')}"

    stats = data.get("stats", {})
    verdicts = data.get("verdicts", [])

    description = (
        f"**Score** : `{data.get('score', 'B')}` · "
        f"**Durée** : `{data.get('durationMin', 0)} min` · "
        f"**Queue** : `{data.get('queueType', 'UNKNOWN')}`\n\n"
        f"**KDA** `{stats.get('kda', 0)}` · "
        f"**CS/min** `{stats.get('csPerMin', 0)}` · "
        f"**Vision/min** `{stats.get('visionPerMin', 0)}`\n"
        f"**Gold/min** `{stats.get('goldPerMin', 0)}` · "
        f"**Dmg/Gold** `{stats.get('damageRatio', 0)}` · "
        f"**KP** `{min(int(stats.get('killParticipation', 0) * 100), 100)}%`"
    )

    embed = discord.Embed(title=title, description=description, color=color)

    if verdicts:
        verdict_text = "\n".join(
            f"{_severity_emoji(v.get('severity', 'green'))} {v.get('msg', '')}"
            for v in verdicts
            if v.get('msg')
        )
        embed.add_field(name="🎯 Verdicts", value=verdict_text, inline=False)

    embed.set_footer(text=f"Match {data.get('matchId', '?')}")
    return embed


def embed_predict(data: dict) -> discord.Embed:
    """Embed for /predict — win probability based on rank averages."""
    win_pct = data.get("winPct", 50)
    color = 0x2ECC71 if win_pct >= 55 else 0xE74C3C if win_pct <= 45 else 0xF1C40F

    self_team = str(data.get("self", {}).get("teamId", 100))
    other_team = "200" if self_team == "100" else "100"
    scores = data.get("teamScores", {})

    description = (
        f"**Probabilité de win** : `{win_pct}%`\n\n"
        f"🟦 **Ton équipe** — score moyen `{scores.get(self_team, 0)}`\n"
        f"🟥 **Adverse** — score moyen `{scores.get(other_team, 0)}`\n"
        f"**Diff** : `{data.get('diff', 0)}`\n\n"
        f"_{data.get('explanation', '')}_"
    )

    return discord.Embed(
        title=f"🎯 Prédiction — {win_pct}%",
        description=description,
        color=color,
    )


def embed_last_game(match_data, name, region):
    if not match_data:
        embed = discord.Embed(
            title="No Recent Games",
            description=f"No recent games found for {name}",
            color=0xff0000
        )
        return embed
    
    kda = f"{match_data['kills']}/{match_data['deaths']}/{match_data['assists']}"
    kda_ratio = (match_data['kills'] + match_data['assists']) / max(match_data['deaths'], 1)
    
    win_color = 0x00ff00 if match_data['win'] else 0xff0000
    win_text = "Victory" if match_data['win'] else "Defeat"
    
    duration_min = match_data['gameDuration'] // 60
    duration_sec = match_data['gameDuration'] % 60
    
    embed = discord.Embed(
        title=f"{name}'s Last Game - {win_text}",
        description=f"Champion: **{match_data['champion']}**\nKDA: **{kda}** ({kda_ratio:.2f})\nDuration: {duration_min}:{duration_sec:02d}",
        color=win_color
    )
    
    items_str = ""
    for item_id in match_data['items']:
        if item_id != 0:
            item_name = get_item_name_by_id(item_id, lol_watcher, 'euw1')
            if item_name:
                items_str += f"{item_name}, "
    if items_str:
        items_str = items_str[:-2]
        embed.add_field(name="Items", value=items_str, inline=False)
    
    embed.set_author(
        name="BeemoBot",
        url="https://github.com/BeemoBot-Enterprise",
        icon_url="https://avatars.githubusercontent.com/u/189348916?s=200&v=4"
    )
    
    embed.set_footer(text="provided by BeemoBot")
    return embed