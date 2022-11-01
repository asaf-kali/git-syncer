import requests

from git_syncer.models import Runnable


class GetIP(Runnable):
    @property
    def verbose_name(self) -> str:
        return "Get IP"

    def run(self) -> str:
        response = requests.get("https://ipinfo.io/ip")
        ip_address = response.text
        return f"My IP address: {ip_address}"
