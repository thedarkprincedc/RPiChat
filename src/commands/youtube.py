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
            logger.error("not eeeee")
        logging.debug(args)
        self.chat.send(
            f"processing request...",
            user_id
        )
       
        file_id = self.downloader.download_youtube(url)
        
        if file_id:
            self.chat.send(
                self.format_download_complete(self.host, file_id),
                user_id
            )

    def format_download_complete(self, ip_address, file_id):
        return (
            f"*Download Complete*\n"
            f"<http://{ip_address}/files/{file_id}|Download File>"
        )