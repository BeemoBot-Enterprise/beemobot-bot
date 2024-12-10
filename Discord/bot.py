import discord
from discord.ext import commands
from Discord.Commands.global_commands import setup_global_commands  # Import commands from the commands folder
from colorama import Fore, Back, Style
import logging

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Optional, enable message content intents if needed

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        setup_global_commands(self)  # Register global commands
        await self.tree.sync()  # Sync commands with Discord
        print(Fore.GREEN+"Slash commands have been synced."+Style.RESET_ALL)

# Create the bot instance
bot = MyBot()

@bot.event
async def on_ready():
    print(Back.YELLOW+f"Bot is ready as {bot.user}"+Style.RESET_ALL)
