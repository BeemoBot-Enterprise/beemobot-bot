# Last updated: 2026-05-06
import logging
import os
import discord
from discord.ext import commands
from colorama import Back, Fore, Style
from Discord.Commands.global_commands import setup_global_commands

logger = logging.getLogger(__name__)

intents = discord.Intents.default()

# Si DEV_GUILD_ID est défini, on sync les slash commands d'abord sur cette
# guild spécifique (propagation INSTANTANÉE — utile pendant la démo / le
# développement quand on change la signature d'une commande). Le sync
# global suit derrière mais peut prendre jusqu'à 1h à se propager.
DEV_GUILD_ID = os.getenv("DEV_GUILD_ID")


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        setup_global_commands(self)
        if DEV_GUILD_ID:
            guild = discord.Object(id=int(DEV_GUILD_ID))
            # Copie les commandes globales sur la guild dev pour les voir
            # apparaître immédiatement.
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print(
                Fore.GREEN
                + f"Slash commands synced INSTANTLY on dev guild {DEV_GUILD_ID}."
                + Style.RESET_ALL
            )
        await self.tree.sync()
        print(Fore.GREEN + "Slash commands have been synced globally." + Style.RESET_ALL)


bot = MyBot()


@bot.event
async def on_ready():
    print(Back.YELLOW + f"Bot is ready as {bot.user}" + Style.RESET_ALL)
    from worker.dm_dispatcher import dispatch_loop
    bot.loop.create_task(dispatch_loop(bot))
