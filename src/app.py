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
from scheduler.service import SchedulerService

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

    check_dependencies(
        AppConfig, 
        ["ffmpeg"]
    )

    # -------------------------
    # Services
    # -------------------------

    chat = ChatClient(
        webhook_url=app.config["SYNOLOGY_CHAT_WEBHOOK_URL"]
    )

    stock_service = StockService()

    download_service = create_download_service(app, chat)

    # -------------------------
    # Commands
    # -------------------------

    router = CommandRouter(chat)

    router.register("status", StatusCommand(chat))

    router.register("stocks", StocksCommand(chat, StockService()))

    router.register("youtubedl",
        YoutubeCommand(
            app.config["RPI_SERVER_URL"],
            download_service
        )
    )

    # -------------------------
    # Webhook / routes
    # -------------------------

    webhook = ChatWebhook(router)
    app.register_blueprint(webhook.blueprint)
    app.register_blueprint(files_bp)

    # -------------------------
    # Scheduler
    # ------------------------- 
    
    scheduler = SchedulerService()

    scheduler.add_interval_job(
        download_service.youtubeService.cleanup_downloads,
        minutes=365,
        job_id="cleanup-downloads",
        kwargs={"max_age_days": 7},
    )

    scheduler.add_interval_job(
        stock_service.stock_info_download,
        minutes=60,
        job_id="stock-update",
        kwargs={
            "tickers": ["AAPL"],
            "output_path": app.config["RPI_OUTPUT_DIR"] / "stocks.csv"
        },
    )

    scheduler.start()

    return app

def create_download_service(app, chat):
    youtube = YoutubeService(
        app.config["RPI_OUTPUT_DIR"]
    )

    repository = DownloadRepository(
        app.config["RPI_SQLITE_PATH"]
    )

    #app.config["DOWNLOAD_REPOSITORY"] = repository

    return DownloadService(
        youtube,
        repository,
        chat
    )