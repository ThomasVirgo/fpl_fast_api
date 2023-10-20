from typing import Union, Dict, List

from pydantic import BaseModel
from tests.factories import schema


def create_url_to_response(
    manager_id: int,
) -> Dict[str, Union[BaseModel, List[BaseModel]]]:
    url_to_response = {
        "https://fantasy.premierleague.com/api/bootstrap-static/": schema.overview_factory(
            as_dict=True
        ),
        f"https://fantasy.premierleague.com/api/entry/{manager_id}/": schema.manager_summary_factory(
            as_dict=True
        ),
    }
    for event_id in range(1, 39):
        url_to_response[
            f"https://fantasy.premierleague.com/api/entry/{manager_id}/event/{event_id}/picks/"
        ] = schema.manager_picks_factory(as_dict=True)
        url_to_response[
            f"https://fantasy.premierleague.com/api/event/{event_id}/live/"
        ] = schema.gameweek_player_stats_factory(as_dict=True)
    return url_to_response
