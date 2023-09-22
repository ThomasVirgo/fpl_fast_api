from typing import Union
from pydantic import BaseModel
from typing import List

# ------------------------- Overview --------------------------------
# https://fantasy.premierleague.com/api/bootstrap-static/


class Event(BaseModel):
    id: int
    deadline_time: str
    average_entry_score: int
    finished: bool
    highest_score: Union[int, None]
    most_selected: Union[int, None]
    most_transferred_in: Union[int, None]
    top_element: Union[int, None]
    most_captained: Union[int, None]
    most_vice_captained: Union[int, None]


class Team(BaseModel):
    id: int
    draw: int
    loss: int
    win: int
    name: str
    points: int
    position: int
    short_name: str
    strength: int
    strength_overall_home: int
    strength_overall_away: int
    strength_attack_home: int
    strength_attack_away: int
    strength_defence_home: int
    strength_defence_away: int


class Player(BaseModel):
    id: int
    element_type: int
    first_name: str
    now_cost: int
    photo: str
    points_per_game: str
    second_name: str
    selected_by_percent: str
    team: int
    total_points: int
    transfers_in: int
    transfers_out: int
    minutes: int
    goals_scored: int
    assists: int
    clean_sheets: int
    goals_conceded: int
    own_goals: int
    penalties_saved: int
    penalties_missed: int
    yellow_cards: int
    red_cards: int
    saves: int
    bonus: int
    starts: int


class Overview(BaseModel):
    events: List[Event]
    teams: List[Team]
    elements: List[Player]


# ------------------------- MANAGER PICKS --------------------------------
# https://fantasy.premierleague.com/api/entry/{manager_id}/event/{event_id}/picks/


class EntryHistory(BaseModel):
    event: int
    points: int
    total_points: int
    rank: int
    rank_sort: int
    overall_rank: int
    bank: int
    value: int
    event_transfers: int
    event_transfers_cost: int
    points_on_bench: int


class Pick(BaseModel):
    element: int
    position: int
    multiplier: int
    is_captain: bool
    is_vice_captain: bool


class ManagerPicks(BaseModel):
    entry_history: EntryHistory
    picks: List[Pick]


# ------------------------- Element Info per Gameweek --------------------------------
# https://fantasy.premierleague.com/api/event/{event_id}/live/


class Stats(BaseModel):
    minutes: int
    goals_scored: int
    assists: int
    clean_sheets: int
    goals_conceded: int
    own_goals: int
    penalties_saved: int
    penalties_missed: int
    yellow_cards: int
    red_cards: int
    saves: int
    bonus: int
    bps: int
    influence: str
    creativity: str
    threat: str
    ict_index: str
    starts: int
    expected_goals: str
    expected_assists: str
    expected_goal_involvements: str
    expected_goals_conceded: str
    total_points: int
    in_dreamteam: bool


class GameweekPlayerStats(BaseModel):
    id: int
    stats: Stats


class GameweekPlayerStats(BaseModel):
    elements: List[GameweekPlayerStats]


# ------------------------- Manager Summary --------------------------------
# https://fantasy.premierleague.com/api/entry/{manager_id}/


class ManagerSummary(BaseModel):
    id: int
    player_first_name: str
    player_last_name: str
    player_region_name: str
    summary_overall_points: int
    summary_overall_rank: int
    name: str


# ------------------------- Manager History --------------------------------
# https://fantasy.premierleague.com/api/entry/{manager_id}/history/


class CurrentHistory(BaseModel):
    event: int
    points: int
    total_points: int
    rank: int
    rank_sort: int
    overall_rank: int
    bank: int
    value: int
    event_transfers: int
    event_transfers_cost: int
    points_on_bench: int


class PastHistory(BaseModel):
    season_name: str
    total_points: int
    rank: int


class ManagerHistory(BaseModel):
    current: List[CurrentHistory]
    past: List[PastHistory]


# ------------------------- Manager Transfers --------------------------------
# https://fantasy.premierleague.com/api/entry/{manager_id}/transfers/


class Transfer(BaseModel):
    element_in: int
    element_in_cost: int
    element_out: int
    element_out_cost: int
    entry: int
    event: int
    time: str
