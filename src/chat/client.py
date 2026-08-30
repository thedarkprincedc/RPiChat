import json
import logging
import requests

logger = logging.getLogger(__name__)

class ChatClient:
    """Client used to send messages to Synology Chat."""

    def __init__(self, webhook_url: str, timeout: float = 5.0):
        self.webhook_url = webhook_url
        self.timeout = timeout

    def send(self, message: str, user_id: str) -> bool:
        """Send a text message to Synology Chat."""
       
        try:
            data = json.dumps({ "text": message, "user_ids": [user_id] })

            response = requests.post(
                self.webhook_url,
                data=f"payload={data}",
                timeout=self.timeout,
            )

            response.raise_for_status()

            logger.debug("Message sent to Synology Chat")

            return True

        except requests.RequestException:
            logger.exception(
                "Failed to send message to Synology Chat"
            )

            return False
