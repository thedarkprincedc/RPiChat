import subprocess
from pathlib import Path
import logging
from logging_config import setup_logging
#import uuid

logger = logging.getLogger("youtube_service")

class YoutubeService:
    def __init__(self, output_dir):
        self.output_dir = output_dir
    
    def download(self, url):
        result = subprocess.run(
            [
                "yt-dlp",
                "--quiet", "--no-warnings",
                "--restrict-filenames",
                "--paths", f"home:{self.output_dir}",
                "--paths", "temp:./incomplete",
                "-o", "%(title)s.%(ext)s",
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
                "--merge-output-format", "mp4",
                "--print", "after_move:filepath",
                url,
            ],
            capture_output=True,
            text=True,
        )
        

        if result.returncode != 0:
            logger.error("yt-dlp stderr: %s", result.stderr.strip())
            raise RuntimeError("yt-dlp failed")
        
        filepath = result.stdout.strip()
        
        return Path(filepath)