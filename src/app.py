from flask import Flask

from chat.client import ChatClient
from chat.webhook import ChatWebhook

from commands.router import CommandRouter
from commands.status import StatusCommand


def create_app():

    app = Flask(__name__)

    # -------------------------
    # Clients / services
    # -------------------------

    chat = ChatClient(
        webhook_url="http://192.168.1.27:5000/webapi/entry.cgi?api=SYNO.Chat.External&method=chatbot&version=2&token=%22AJ8PmR7K8u5NhfIV2BnO3ve0sdK2ey0V8nSe7yTjtR1gr9Y9SLQCmsILxWZlA0ek%22"
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
