import os
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class AppConfig:
    """A central hub for all project configurations."""
    SYNOLOGY_CHAT_WEBHOOK_URL = os.getenv("SYNOLOGY_CHAT_WEBHOOK_URL")
    SYNOLOGY_URL = os.getenv("SYNOLOGY_URL")
    PORT = os.getenv("PORT") or 8080
    OUTPUT_FILES = os.getenv("OUTPUT_FILES") or Path("./output").resolve()
    
    if not SYNOLOGY_CHAT_WEBHOOK_URL:
        print("Error: SYNOLOGY_CHAT_WEBHOOK_URL is missing from environment")
        sys.exit(1)

    #API_KEY = os.getenv("API_KEY")
    #DB_URL = os.getenv("DATABASE_URL")
    #DEBUG = os.getenv("DEBUG_MODE", "False") == "True"