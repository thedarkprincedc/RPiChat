import logging
from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)

class ChatWebhook:

    def __init__(self, router):
        self.router = router

        self.blueprint = Blueprint(
            "chat_webhook",
            __name__,
        )

        self.blueprint.add_url_rule(
            "/webhook/chat",
            view_func=self.handle,
            methods=["POST"],
        )

    def handle(self):
        """Handle an incoming Synology Chat webhook."""

        data = request.get_json(silent=True) or {}
        formdata = request.form.to_dict()

        logger.info("Received Chat webhook")
       
        # Extract the message.
        message = formdata["text"]
        user_id = formdata["user_id"]
        
        logger.debug(request.form.to_dict())
       
        if not message:
            return jsonify({
                "error": "No message provided"
            }), 400

        logger.info("Received command: %s", message)

        # Pass the command to the router.
        response = self.router.handle(message, user_id)

        return jsonify({
            "text": response
        })
