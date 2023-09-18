import requests
from typing import List

BASE_URL = "https://fantasy.premierleague.com/api"

endpoints = {"overview": f"{BASE_URL}/bootstrap-static/"}


class FPLClient:
    def __init__(self, manager_id: int) -> None:
        self.manager_id = manager_id
        self.data = {}

    def get_urls(self) -> List[str]:
        overview_url = endpoints["overview"]
        return [overview_url]

    def retrieve_data_from_endpoints(self):
        for url in self.get_urls():
            response_json = requests.get(url).json()
            self.data[url] = response_json
        return self.data
