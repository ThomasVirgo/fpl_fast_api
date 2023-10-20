from typing import List

from pydantic import parse_obj_as
from fpl.schema import (
    GameweekPlayerStats,
    LeagueH2H,
    ManagerHistory,
    ManagerPicks,
    ManagerSummary,
    Overview,
    Transfer,
)
from tests.data.league_h2h import LEAGUE_H2H_TEST_DATA
from tests.data.manager_history import MANAGER_HISTORY_TEST_DATA
from tests.data.manager_transfers import MANAGER_TRANSFERS_TEST_DATA
from tests.data.overview import OVERVIEW_TEST_DATA
from tests.data.manager_picks import MANAGER_PICKS_TEST_DATA
from tests.data.gameweek_player_stats import GAMEWEEK_PLAYER_STATS_TEST_DATA
from tests.data.manager_summary import MANAGER_SUMMARY_TEST_DATA


def overview_factory(as_dict: bool = False) -> Overview:
    data = Overview.parse_obj(OVERVIEW_TEST_DATA)
    if as_dict:
        return data.dict()
    else:
        return data


def manager_picks_factory(as_dict: bool = False) -> ManagerPicks:
    data = ManagerPicks.parse_obj(MANAGER_PICKS_TEST_DATA)
    if as_dict:
        return data.dict()
    else:
        return data


def gameweek_player_stats_factory(as_dict: bool = False) -> GameweekPlayerStats:
    data = GameweekPlayerStats.parse_obj(GAMEWEEK_PLAYER_STATS_TEST_DATA)
    if as_dict:
        return data.dict()
    else:
        return data


def manager_summary_factory(as_dict: bool = False) -> ManagerSummary:
    data = ManagerSummary.parse_obj(MANAGER_SUMMARY_TEST_DATA)
    if as_dict:
        return data.dict()
    else:
        return data


def manager_history_factory(as_dict: bool = False) -> ManagerHistory:
    data = ManagerHistory.parse_obj(MANAGER_HISTORY_TEST_DATA)
    if as_dict:
        return data.dict()
    else:
        return data


def manager_transfers_factory(as_dict: bool = False) -> List[Transfer]:
    data = parse_obj_as(List[Transfer], MANAGER_TRANSFERS_TEST_DATA)
    if as_dict:
        return [x.dict() for x in data]
    else:
        return data


def league_2h2_factory(as_dict: bool = False) -> LeagueH2H:
    data = LeagueH2H.parse_obj(LEAGUE_H2H_TEST_DATA)
    if as_dict:
        return data.dict()
    else:
        return data
