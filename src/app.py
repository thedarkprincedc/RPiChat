from flask import Flask

from chat.client import ChatClient
from chat.webhook import ChatWebhook

from commands.router import CommandRouter
from commands.status import StatusCommand
import config

def create_app():

    app = Flask(__name__)

    # -------------------------
    # Clients / services
    # -------------------------

    chat = ChatClient(
        webhook_url=config.AppConfig.SYNLOGY_CHAT_WEBHOOK_URL
   )

    # -------------------------
    # Commands
    # -------------------------

    router = CommandRouter()

    router.register(
        "status",
        StatusCommand(chat),
    )

    # -------------------------
    # Webhook
    # -------------------------

    webhook = ChatWebhook(router)

    app.register_blueprint(
        webhook.blueprint
    )

    return app
