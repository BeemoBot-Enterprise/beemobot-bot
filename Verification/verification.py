import os
from dotenv import load_dotenv
from colorama import Fore, Back, Style
from Logs.logs import verification_error, verification_success

load_dotenv()

# Verification before launch of the app
def security_check():
    # Check if the environment is set correctly
    verify_env()

def verify_env():
    if os.getenv("BOT_TOKEN") is None or os.getenv("RIOT_API_KEY") is None or os.getenv("BOT_TOKEN") == "" or os.getenv("RIOT_API_KEY") == "":
        print(Back.RED + "Please make sure the BOT_TOKEN and RIOT_API_KEY environment variable are set properly." + Style.RESET_ALL)
        verification_error("Environment variables are not set correctly")
        exit(1)
    else:
        verification_success()
        print(Back.GREEN + "BOT_TOKEN and RIOT_API_KEY are set correctly" + Style.RESET_ALL)
        
