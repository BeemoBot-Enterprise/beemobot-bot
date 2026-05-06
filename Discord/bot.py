# Last updated: 2026-05-06
import logging
import discord
from discord.ext import commands
from colorama import Back, Fore, Style
from Discord.Commands.global_commands import setup_global_commands

logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        setup_global_commands(self)
        await self.tree.sync()
        print(Fore.GREEN + "Slash commands have been synced." + Style.RESET_ALL)


bot = MyBot()


@bot.event
async def on_ready():
    print(Back.YELLOW + f"Bot is ready as {bot.user}" + Style.RESET_ALL)
    from worker.dm_dispatcher import dispatch_loop
    bot.loop.create_task(dispatch_loop(bot))
