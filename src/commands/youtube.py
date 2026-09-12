import logging
from logging_config import setup_logging
from urllib.parse import quote

logger = logging.getLogger("youtube_dl_command")

class YoutubeCommand:

    def __init__(self, host, chat, downloader):
        self.host = host
        self.chat = chat
        self.downloader = downloader

    def execute(self, args, user_id):
        url = args[0]

        if not url:
           logger.error("No YouTube URL provided")
           return
        
        self.chat.send(
            f"Processing request...",
            user_id
        )

        self.downloader.download_youtube(url, user_id)