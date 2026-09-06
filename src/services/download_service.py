import uuid

class DownloadService():
    def __init__(self, youtubeService, downloadRepository):
        self.youtubeService = youtubeService
        self.repository = downloadRepository

    def download_youtube(self, url):
        download_id = uuid.uuid4().hex
        file_id = self.repository.create(
            download_id=download_id,
            url=url,
            #created_at=None
            #status="downloading"
        )

        try:
            path = self.youtubeService.download(url)
            self.repository.complete(
                download_id=file_id,
                filename=path.name,
                path=str(path)
            )
            return file_id
        except Exception as e:
            self.repository.fail(file_id, str(e))
            raise
    