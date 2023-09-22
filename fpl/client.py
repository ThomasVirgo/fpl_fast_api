from typing import List, Dict, Tuple, Union
import requests
from pydantic import BaseModel, parse_obj_as
from dataclasses import dataclass
from fpl.schema import (
    ManagerPicks,
    Overview,
    ManagerHistory,
    ManagerSummary,
    Transfer,
    GameweekPlayerStats,
)

BASE_URL = "https://fantasy.premierleague.com/api"


@dataclass
class FplSchema:
    schema: BaseModel
    is_list: bool


def get_overview_and_create_endpoint_to_schema(
    manager_id: int,
) -> Tuple[Overview, Dict[str, FplSchema]]:
    # retrieve the overview so can work out latest gameweek
    overview_url = f"{BASE_URL}/bootstrap-static/"
    overview_json = requests.get(overview_url).json()
    overview = Overview.parse_obj(overview_json)

    # base endpoint to schema
    endpoint_to_schema = {
        f"{BASE_URL}/entry/{manager_id}/": FplSchema(
            schema=ManagerSummary, is_list=False
        ),
        f"{BASE_URL}/entry/{manager_id}/history/": FplSchema(
            schema=ManagerHistory, is_list=False
        ),
        f"{BASE_URL}/entry/{manager_id}/transfers/": FplSchema(
            schema=Transfer, is_list=True
        ),
    }

    # get latest gameweek
    latest_finished_gw = 1
    for event in overview.events:
        if event.finished and event.id > latest_finished_gw:
            latest_finished_gw = event.id

    # create endpoint urls
    for gw in range(1, latest_finished_gw + 1):
        endpoint_to_schema[
            f"{BASE_URL}/entry/{manager_id}/event/{gw}/picks/"
        ] = FplSchema(schema=ManagerPicks, is_list=False)
        endpoint_to_schema[f"{BASE_URL}/event/{gw}/live/"] = FplSchema(
            schema=GameweekPlayerStats, is_list=False
        )

    return overview, endpoint_to_schema


class FPLClient:
    def __init__(self, endpoint_to_schema: Dict[str, FplSchema]) -> None:
        self.endpoint_to_schema = endpoint_to_schema

    def _request(
        self, url: str, schema: FplSchema
    ) -> Union[BaseModel, List[BaseModel]]:
        response = requests.get(url)
        json = response.json()
        if schema.is_list:
            return parse_obj_as(List[schema.schema], json)
        else:
            return schema.schema.parse_obj(json)

    def retrieve_all_data(self) -> Dict[str, BaseModel]:
        fpl_data = {}
        for endpoint, fpl_schema in self.endpoint_to_schema.items():
            fpl_data[endpoint] = self._request(endpoint, fpl_schema)
        return fpl_data
