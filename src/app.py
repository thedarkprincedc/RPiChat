from flask import Flask, send_from_directory

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
import config
import logging
from logging_config import setup_logging
import shutil

logger = logging.getLogger("app")

def check_dependencies(config):
    dependencies = ["ffmpeg"]

    for program in dependencies:
        available = shutil.which(program)
        if not available:
            logger.warning(f"{program} dependency not found")
        else:
            logger.info(f"{program} dependency found")

    if not config.SYNOLOGY_CHAT_WEBHOOK_URL:
        raise RuntimeError("SYNOLOGY_CHAT_WEBHOOK_URL is not configured")
    

def create_app():
    app = Flask(__name__)

    # -------------------------
    # Clients / services
    # -------------------------

    chat = ChatClient(
        webhook_url=config.AppConfig.SYNOLOGY_CHAT_WEBHOOK_URL
    )

    # -------------------------
    # Commands
    # -------------------------

    router = CommandRouter()

    router.register(
        "status",
        StatusCommand(chat),
    )

    router.register(
        "stocks",
        StocksCommand(chat, StockService()),
    )
    logger.info(config.AppConfig.SQLITE_PATH)
    downloadRepository = DownloadRepository(config.AppConfig.SQLITE_PATH)
    downloadRepository.initialize()

    youtubeService = YoutubeService(config.AppConfig.OUTPUT_FILES)
    router.register(
        "youtubedl",
        YoutubeCommand(
            "localhost:8080",
            chat, 
            DownloadService(
                youtubeService,
                downloadRepository
            )
        )
    )

    # -------------------------
    # Webhook
    # -------------------------

    webhook = ChatWebhook(router)

    app.register_blueprint(
        webhook.blueprint
    )
    
    @app.route("/files/<download_id>")
    def files(download_id):
        row = downloadRepository.get(download_id)
       
        if row is None:
            return {"error": "Download not found"}, 404
        print(row['filename'])
        print(config.AppConfig.OUTPUT_FILES)
        return send_from_directory(
            config.AppConfig.OUTPUT_FILES,
            row['filename']
        )

    check_dependencies(config.AppConfig)
   
    return app
