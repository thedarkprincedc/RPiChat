import subprocess

class YoutubeService:
    def __init__(self):
        pass
    
    def download_video_by_url(self, url):
        # result = subprocess.run(
        #     [   
        #         "youtube-dl", 
        #         "-o", "/youtube-dl/.incomplete/%(title)s.%(ext)s", 
        #         "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]", 
        #         "--exec", "touch {} && mv {} /youtube-dl/", 
        #         "--merge-output-format", "mp4", 
        #         url
        #     ],
        #     capture_output=True,
        #     text=True
        # )
        result = subprocess.run(
            [
                "yt-dlp",
                "-o", "./output/.incomplete/%(title)s.%(ext)s",
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
                "--merge-output-format", "mp4",
                url,
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("Process completed successfully")
        else:
            print("Process failed!")