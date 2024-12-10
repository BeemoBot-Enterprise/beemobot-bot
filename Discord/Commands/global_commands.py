import discord
from discord import app_commands
from Logs.logs import command_used

def setup_global_commands(bot):
    # Define a slash command
    @bot.tree.command(name="hello", description="Say hello!")
    async def hello(interaction: discord.Interaction):
        command_used("hello", interaction.user)
        await interaction.response.send_message("Hello! 👋")

    # Add more commands here if needed
