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

        # Force=True parses the body as JSON even if the Content-Type header isn't set perfectly
        #all_json_data = request.get_json(force=True)
        
        # all_json_data is now a standard Python dictionary containing the whole payload
        #print(all_json_data) 
        #print(request.get_data())
        #print(request.get_json())
        logger.info("Received Chat webhook")
       
        # Extract the message.
        #message = data.get("text", "").strip()
        message = formdata["text"]
        user_id = formdata["user_id"]
        
        logger.debug(request.form.to_dict())
        # user_id = data.get("user_id", "").strip()
        # logger.debug("Received")
        # logger.debug(request.get_data(as_text=True))
        # logger.debug(request.headers)
        # logger.debug(request.data)
        # print(request.form.get())
        #print(user_id)
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
