import logging
from logging_config import setup_logging
from urllib.parse import quote

logger = logging.getLogger("youtube_dl_command")

class YoutubeCommand:

    def __init__(self, chat, youtubeService):
        self.chat = chat
        self.youtubeService = youtubeService

    def execute(self, args, user_id):
        url = args[0]
        if not url:
            logger.error("not eeeee")
        logging.debug(args)
        self.chat.send(
            f"processing request...",
            user_id
        )
        #payload={"text": "Check this!! <https://www.synology.com|Click here> for details!"}
        result = self.youtubeService.download_video_by_url(url)
        if result:
            self.chat.send(
                self.format_download_complete(result['filename']),
                user_id
            )

    def format_download_complete(self, filename):
        encoded_filename = quote(filename, safe="")
        download_url = f"http://192.168.1.100:8080/files/{encoded_filename}"

        return (
            "*Download Complete*\n"
            f"*File:* `{filename}`\n"
            "*Status:* Done\n\n"
            f"<{download_url}|Download File>"
        )