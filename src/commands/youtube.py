from urllib.parse import urlparse
from commands.exceptions import CommandValidationError

class YoutubeCommand:
    def __init__(self, host, downloader):
        self.host = host
        self.downloader = downloader

    def execute(self, args, user_id):
        url = self.validate(args)
        self.downloader.download_youtube(url, user_id)

    def validate(self, args):
        if len(args) != 1:
            raise CommandValidationError(
                "Usage: /youtube <url>"
            )
        
        url = args[0]

        if not self.is_valid_url(url):
            raise CommandValidationError(
                "Please provide a valid URL."
            )

        return url

    def is_valid_url(self, url: str) -> bool:
        try:
            parsed = urlparse(url)

            if parsed.scheme not in ("http", "https"):
                return False

            return parsed.netloc.lower() in {
                "youtube.com",
                "www.youtube.com",
                "m.youtube.com",
                "youtu.be",
                "www.youtu.be",
            }

        except ValueError:
            return False
