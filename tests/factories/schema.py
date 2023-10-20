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


def overview_factory() -> Overview:
    return Overview.parse_obj(OVERVIEW_TEST_DATA)


def manager_picks_factory() -> ManagerPicks:
    return ManagerPicks.parse_obj(MANAGER_PICKS_TEST_DATA)


def gameweek_player_stats_factory() -> GameweekPlayerStats:
    return GameweekPlayerStats.parse_obj(GAMEWEEK_PLAYER_STATS_TEST_DATA)


def manager_summary_factory() -> ManagerSummary:
    return ManagerSummary.parse_obj(MANAGER_SUMMARY_TEST_DATA)


def manager_history_factory() -> ManagerHistory:
    return ManagerHistory.parse_obj(MANAGER_HISTORY_TEST_DATA)


def manager_transfers_factory() -> List[Transfer]:
    return parse_obj_as(List[Transfer], MANAGER_TRANSFERS_TEST_DATA)


def league_2h2_factory() -> LeagueH2H:
    return LeagueH2H.parse_obj(LEAGUE_H2H_TEST_DATA)
