import os
import sys
from dotenv import load_dotenv

load_dotenv()

class AppConfig:
    """A central hub for all project configurations."""
    SYNLOGY_CHAT_WEBHOOK_URL = os.getenv("SYNLOGY_CHAT_WEBHOOK_URL")
    PORT = os.getenv("PORT") or 8080

    if not SYNLOGY_CHAT_WEBHOOK_URL:
        print("Error: SYNLOGY_CHAT_WEBHOOK_URL is missing from environment")
        sys.exit(1)

    #API_KEY = os.getenv("API_KEY")
    #DB_URL = os.getenv("DATABASE_URL")
    #DEBUG = os.getenv("DEBUG_MODE", "False") == "True"