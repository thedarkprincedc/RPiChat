import requests

class SynologyService:
    def __init__(self, synology_url, synology_username, synology_password):
        self.base_url = synology_url
        self.login_params = {
            "api": "SYNO.API.Auth",
            "version": "3",  # Version 3+ supports modern DSM versions
            "method": "login",
            "account": synology_username,
            "passwd": synology_password,
            "session": "FileStation",  # Name your app/session context
            "format": "cookie"         # or "sid"
        }
        self.sid = None

    def login(self):
        url = f"{self.base_url}/auth.cgi"
        response = requests.get(url, params=self.login_params)
        data = response.json()
        if data.get("success"):
            self.sid = data["data"]["sid"]
            print("Login successful!")

    def get_downloads(self):
        list_params = {
            "api": "SYNO.DownloadStation.Task",
            "version": "1",
            "method": "list",
            "additional": "detail,transfer"  # Gives progress, speeds, and file sizes
        }
        task_url = f"{self.base_url}/DownloadStation/task.cgi"
        response = requests.get(task_url, params=list_params)
        return response.json()

        