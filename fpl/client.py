from typing import List
import requests

BASE_URL = "https://fantasy.premierleague.com/api"


class FPLClient:
    def __init__(self, manager_id: int) -> None:
        self.manager_id = manager_id
        self.overview_url = f"{BASE_URL}/bootstrap-static/"
        overview_json = requests.get(self.overview_url).json()
        self.events = overview_json.get("events", [])
        self.data = {self.overview_url: overview_json}

    def get_urls(self) -> List[str]:
        manager_summary = f"{BASE_URL}/entry/{self.manager_id}/"
        manager_history = f"{BASE_URL}/entry/{self.manager_id}/history/"
        manager_transfers = f"{BASE_URL}/entry/{self.manager_id}/transfers/"

        latest_finished_gw = 1
        for event in self.events:
            finished = event["finished"]
            if finished and event["id"] > latest_finished_gw:
                latest_finished_gw = event["id"]

        manager_picks_urls = []
        gw_info_urls = []
        for gw in range(1, latest_finished_gw + 1):
            manager_picks_urls.append(
                f"{BASE_URL}/entry/{self.manager_id}/event/{gw}/picks/"
            )
            gw_info_urls.append(f"{BASE_URL}/event/{gw}/live/")

        return (
            manager_picks_urls
            + gw_info_urls
            + [manager_summary, manager_history, manager_transfers]
        )

    def retrieve_data_from_endpoints(self):
        for url in self.get_urls():
            response_json = requests.get(url).json()
            self.data[url] = response_json
        return self.data
