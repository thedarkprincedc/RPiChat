import logging

logger = logging.getLogger("youtube_dl_command")

class YoutubeDLCommand:

    def __init__(self, chat, youtubeService):
        self.chat = chat
        self.youtubeService = youtubeService

    def execute(self, args, user_id):
        url = args[0]
        if not url:
            logger.error("not eeeee")
        logging.debug(args)
        #payload={"text": "Check this!! <https://www.synology.com|Click here> for details!"}
        self.youtubeService.download_video_by_url(url)
        self.chat.send(
            f"🤖 Responding <{url}|mega mana>",
            user_id
        )