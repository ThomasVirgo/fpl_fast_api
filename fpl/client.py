import requests
from typing import List

BASE_URL = "https://fantasy.premierleague.com/api"


class FPLClient:
    def __init__(self, manager_id: int) -> None:
        self.manager_id = manager_id
        self.data = {}

    def get_urls(self) -> List[str]:
        overview = f"{BASE_URL}/bootstrap-static/"
        manager_summary = f"{BASE_URL}/entry/{self.manager_id}/"
        manager_history = f"{BASE_URL}/entry/{self.manager_id}/history/"
        manager_transfers = f"{BASE_URL}/entry/{self.manager_id}/transfers/"

        return [overview, manager_summary, manager_history, manager_transfers]

    def retrieve_data_from_endpoints(self):
        for url in self.get_urls():
            response_json = requests.get(url).json()
            self.data[url] = response_json
        return self.data
