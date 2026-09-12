from flask import Flask, send_from_directory
from pathlib import Path
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
    

def create_app(debug=None):
    if debug is None:
        debug = AppConfig.DEBUG

    setup_logging(
        log_file="logs/main.log", 
        console_level=logging.DEBUG if debug else logging.INFO
    )

    logging.info(f"debug mode: {debug}")

    app = Flask(__name__)

    # -------------------------
    # Clients / services
    # -------------------------

    chat = ChatClient(
        webhook_url=AppConfig.SYNOLOGY_CHAT_WEBHOOK_URL
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
    logger.info(AppConfig.RPI_SQLITE_PATH)
    downloadRepository = DownloadRepository(AppConfig.RPI_SQLITE_PATH)
    downloadRepository.initialize()

    youtubeService = YoutubeService(AppConfig.RPI_OUTPUT_DIR)
    router.register(
        "youtubedl",
        YoutubeCommand(
            AppConfig.RPI_SERVER_URL,
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

        file_path = Path(AppConfig.RPI_OUTPUT_DIR) / row["filename"]

        if not file_path.is_file():
            return {"error": "File not found"}, 404
      
        return send_from_directory(
            AppConfig.RPI_OUTPUT_DIR,
            row['filename'],
            as_attachment=True,
            download_name=row["filename"]
        )

    check_dependencies(AppConfig)
   
    return app
