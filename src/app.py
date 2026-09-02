from flask import Flask, send_from_directory

from chat.client import ChatClient
from chat.webhook import ChatWebhook

from commands.router import CommandRouter
from commands.status import StatusCommand
from commands.stocks import StocksCommand
from commands.youtube import YoutubeCommand
from services.stock_service import StockService
from services.youtube_service import YoutubeService

import config

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

    router.register(
        "youtubedl",
        YoutubeCommand(chat, YoutubeService())
    )

    # -------------------------
    # Webhook
    # -------------------------

    webhook = ChatWebhook(router)

    app.register_blueprint(
        webhook.blueprint
    )

    @app.route("/files/<path:filename>")
    def files(filename):
        return send_from_directory(config.AppConfig.OUTPUT_FILES, filename)

    return app
