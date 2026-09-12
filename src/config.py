import os
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class AppConfig:
    """A central hub for all project configurations."""
    # variables
    SYNOLOGY_CHAT_WEBHOOK_URL = os.getenv("SYNOLOGY_CHAT_WEBHOOK_URL")
    SYNOLOGY_URL = os.getenv("SYNOLOGY_URL")
    # 
    RPI_PORT = os.getenv("PORT") or 8080
    RPI_SERVER_URL = f"localhost:{RPI_PORT}"
    # directories
    RPI_OUTPUT_DIR = os.getenv("OUTPUT_DIR") or Path("./output").resolve()
    RPI_DATA_DIR = os.getenv("DATA_DIR") or Path("./data").resolve()
    RPI_LOG_DIR = os.getenv("LOG_DIR") or Path("./logs").resolve()
    # paths
    RPI_SQLITE_PATH = os.getenv("SQLITE_PATH") or RPI_DATA_DIR / "db.sqlite"
    RPI_LOG_PATH = os.getenv("LOG_PATH") or RPI_LOG_DIR / "main.log"

    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # scripts
    RPI_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RPI_DATA_DIR.mkdir(parents=True, exist_ok=True)
    RPI_LOG_DIR.mkdir(parents=True, exist_ok=True)
