import requests

class UgreenService:
    def __init__(self, ugreen_url, ugreen_username, ugreen_password):
        self.ugreen_url = ugreen_url
        self.login_params = {
            "username": ugreen_username,
            "password": ugreen_password
        }
        self.token = None
        
    def login(self):
        url = f"{self.ugreen_url}/token"
        response = requests.get(url, params=self.login_params)
        response.raise_for_status()
        data = response.json()
        if data["code"] != 200:
            raise RuntimeError(data.get("msg", "UGREEN login failed"))

        self.token = data["data"]["token"]

    def get(self, path, **params):
        if not self.token:
            self.login()

        params["token"] = self.token

        return requests.get(
            f"http://{self.host}:4115{path}",
            params=params,
        )
    
    def get_downloads(self):
        pass