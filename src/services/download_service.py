import uuid
from threading import Thread
import logging
from logging_config import setup_logging


logger = logging.getLogger("youtube_dl_command")

class DownloadService():
    def __init__(self, youtubeService, downloadRepository, chat):
        self.youtubeService = youtubeService
        self.repository = downloadRepository
        self.host = "localhost:8080"
        self.chat = chat

    def download_youtube(self, url, user_id):
        thread = Thread(
            target=self._download_youtube,
            args=(url, user_id),
            daemon=True
        )
        thread.start()

    def _download_youtube(self, url, user_id):
        try:
            download_id = uuid.uuid4().hex
            file_id = self.repository.create(
                download_id=download_id,
                url=url,
                #created_at=None
                #status="downloading"
            )

            path = self.youtubeService.download(url)

            self.repository.complete(
                download_id=file_id,
                filename=path.name,
                path=str(path)
            )

            size = self._format_size(path.stat().st_size)

            self.chat.send(
                self._format_download_complete(
                    self.host,
                    file_id,
                    path.name,
                    size
                ),
                user_id
            )
        except Exception as e:
            self.repository.fail(file_id, str(e))
            logger.exception("YouTube download failed: %s", url)
            self.chat.send(
                "Download failed.",
                user_id
            )

    def _format_download_complete(self, host, file_id, filename, size):
        url = f"http://{host}/files/{file_id}"
        return (
            f"*Download Complete*\n"
            f"*File:* {filename}\n"
            f"*Size:* {size}\n"
            f"<{url}|Download File>"
        )

    def _format_size(self, size):
        for unit in ("B", "KB", "MB", "GB", "TB"):
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024

        return f"{size:.1f} PB"
