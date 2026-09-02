import subprocess
import config
from pathlib import Path
import logging
from logging_config import setup_logging

logger = logging.getLogger("youtube_service")


class YoutubeService:
    def __init__(self):
        pass
    
    def download_video_by_url(self, url):
        result = subprocess.run(
            [
                "yt-dlp",
                "--quiet", "--no-warnings",
                "--paths", f"home:{config.AppConfig.OUTPUT_FILES}",
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
            return None
        
        filepath = result.stdout.strip()
        filename = Path(filepath).name
       
        return {
            "filename": filename
        }