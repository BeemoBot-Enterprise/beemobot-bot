import os
from dotenv import load_dotenv
#Color to style the console output
from colorama import Fore, Back, Style
load_dotenv()

# Verification before launch of the app
def security_check():
    # Check if the environment is set correctly
    verify_env()

def verify_env():
    if os.getenv("BOT_TOKEN") is None and os.getenv("RIOT_API_KEY") is None:
        print(Back.RED+"Please make sure the BOT_TOKEN and RIOT_API_KEY environment variable are set properly."+Style.RESET_ALL)
        exit(1)
    else :
        print(Back.GREEN+"BOT_TOKEN and RIOT_API_KEY are set correctly"+Style.RESET_ALL)
        return