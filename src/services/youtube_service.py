import subprocess
from pathlib import Path
import logging
from logging_config import setup_logging
#import uuid
from datetime import datetime, timedelta
from pathlib import Path

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

    def cleanup_downloads(self, max_age_days=7):
        cutoff = datetime.now() - timedelta(days=max_age_days)
        
        for path in self.output_dir.iterdir():
            if not path.is_file():
                continue

            modified = datetime.fromtimestamp(path.stat().st_mtime)

            if modified < cutoff:
                path.unlink()