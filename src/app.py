from flask import Flask
from chat.client import ChatClient
from chat.webhook import ChatWebhook
from commands.router import CommandRouter
from commands.status import StatusCommand
from commands.stocks import StocksCommand
from commands.youtube import YoutubeCommand
from services.stock_service import StockService
from services.youtube_service import YoutubeService
from services.download_service import DownloadService
from services.download_repository import DownloadRepository
from config import AppConfig
import logging
from logging_config import setup_logging
import shutil
from routes.files import files_bp

logger = logging.getLogger("app")

def check_dependencies(config, dependencies):
    for program in dependencies:
        available = shutil.which(program)
        if not available:
            logger.warning(f"{program} dependency not found")
        else:
            logger.info(f"{program} dependency found")

    if not config.SYNOLOGY_CHAT_WEBHOOK_URL:
        raise RuntimeError("SYNOLOGY_CHAT_WEBHOOK_URL is not configured")
    

def create_app(debug=None):
    if debug is None:
        debug = AppConfig.DEBUG

    setup_logging(
        log_file="logs/main.log", 
        console_level=logging.DEBUG if debug else logging.INFO
    )

    logging.info(f"debug mode: {debug}")

    app = Flask(__name__)
    app.config.from_object(AppConfig)

    # -------------------------
    # Clients / services
    # -------------------------

    chat = ChatClient(
        webhook_url=app.config["SYNOLOGY_CHAT_WEBHOOK_URL"]
    )

    # -------------------------
    # Commands
    # -------------------------

    router = CommandRouter(chat)

    router.register("status", StatusCommand(chat))
    router.register("stocks", StocksCommand(chat, StockService()))
    router.register("youtubedl",
        YoutubeCommand(app.config["RPI_SERVER_URL"],
            create_download_service(app, chat)
        )
    )

    # -------------------------
    # Webhook
    # -------------------------

    webhook = ChatWebhook(router)
    app.register_blueprint(webhook.blueprint)
    app.register_blueprint(files_bp)
    check_dependencies(AppConfig, ["ffmpeg"])
    return app

def create_download_service(app, chat):
    youtube = YoutubeService(
        app.config["RPI_OUTPUT_DIR"]
    )

    repository = DownloadRepository(
        app.config["RPI_SQLITE_PATH"]
    )

    app.config["DOWNLOAD_REPOSITORY"] = repository

    return DownloadService(
        youtube,
        repository,
        chat
    )
    
