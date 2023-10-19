from fpl.schema import ManagerPicks, Overview
from tests.data.overview import OVERVIEW_TEST_DATA
from tests.data.manager_picks import MANAGER_PICKS_TEST_DATA


def overview_factory() -> Overview:
    return Overview.parse_obj(OVERVIEW_TEST_DATA)


def manager_picks_factory() -> ManagerPicks:
    return ManagerPicks.parse_obj(MANAGER_PICKS_TEST_DATA)
