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


@dataclass
class FplData:
    manager_id: int
    overview: Overview
    manager_history: ManagerHistory
    manager_transfers: List[Transfer]
    manager_summary: ManagerSummary
    player_stats_by_gameweek: Dict[int, GameweekPlayerStats]
    manager_picks_by_gameweek: Dict[int, ManagerPicks]


def create_fpl_data(
    manager_id: int,
) -> FplData:
    # overview
    overview_url = f"{BASE_URL}/bootstrap-static/"
    overview: Overview = _request(
        overview_url, FplSchema(schema=Overview, is_list=False)
    )

    # manager history
    manager_history_url = f"{BASE_URL}/entry/{manager_id}/history/"
    manager_history: ManagerHistory = _request(
        manager_history_url, FplSchema(schema=ManagerHistory, is_list=False)
    )

    # manager transfers
    manager_transfers_url = f"{BASE_URL}/entry/{manager_id}/transfers/"
    manager_transfers: List[Transfer] = _request(
        manager_transfers_url, FplSchema(schema=Transfer, is_list=True)
    )

    # manager summary
    manager_summary_url = f"{BASE_URL}/entry/{manager_id}/"
    manager_summary: ManagerSummary = _request(
        manager_summary_url, FplSchema(schema=ManagerSummary, is_list=False)
    )

    # get latest gameweek
    latest_finished_gw = 1
    for event in overview.events:
        if event.finished and event.id > latest_finished_gw:
            latest_finished_gw = event.id

    manager_picks_by_gameweek: Dict[int, ManagerPicks] = {}
    player_stats_by_gameweek: Dict[int, GameweekPlayerStats] = {}
    for gw in range(1, latest_finished_gw + 1):
        picks_url = f"{BASE_URL}/entry/{manager_id}/event/{gw}/picks/"
        manager_picks_by_gameweek[gw] = _request(
            picks_url, FplSchema(schema=ManagerPicks, is_list=False)
        )

        player_stats_url = f"{BASE_URL}/event/{gw}/live/"
        player_stats_by_gameweek[gw] = _request(
            player_stats_url, FplSchema(schema=GameweekPlayerStats, is_list=False)
        )

    return FplData(
        manager_id=manager_id,
        overview=overview,
        manager_history=manager_history,
        manager_transfers=manager_transfers,
        manager_summary=manager_summary,
        player_stats_by_gameweek=player_stats_by_gameweek,
        manager_picks_by_gameweek=manager_picks_by_gameweek,
    )


def _request(url: str, fpl_schema: FplSchema) -> Union[BaseModel, List[BaseModel]]:
    response = requests.get(url)
    json = response.json()
    if fpl_schema.is_list:
        return parse_obj_as(List[fpl_schema.schema], json)
    else:
        return fpl_schema.schema.parse_obj(json)
