import requests

class ProxmoxService:
    def __init__(self, proxmox_url):
        self.proxmox_url = proxmox_url