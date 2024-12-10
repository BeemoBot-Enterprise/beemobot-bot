from Verification.verification import security_check
from Discord.bot import bot  # Import bot instance
import os

bot_token = os.getenv("BOT_TOKEN_PROD")  # Get the bot token from the environment variables
bot_token_test = os.getenv("BOT_TOKEN_TEST") # Get the development bot token from the environment variables

def Launch():
    # Always verify security before launching the app
    security_check()
    
    # Run the bot
    bot.run(bot_token_test) 

if __name__ == "__main__":
    Launch()