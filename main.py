from Verification.verification import security_check
from Discord.bot import bot  # Import bot instance
import os

def Launch():
    # Always verify security before launching the app
    security_check()
    
    # Run the bot
    bot.run(os.getenv("BOT_TOKEN"))  # Ensure your bot token is stored securely

if __name__ == "__main__":
    Launch()