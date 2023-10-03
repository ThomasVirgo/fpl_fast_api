from dataclasses import dataclass
from typing import Union, Dict, Optional
from functools import cached_property
from pydantic import BaseModel
from typing import List


class BaseModelCached(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        keep_untouched = (cached_property,)


# ------------------------- Overview --------------------------------
# https://fantasy.premierleague.com/api/bootstrap-static/


class Event(BaseModelCached):
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


class Team(BaseModelCached):
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


class Player(BaseModelCached):
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


class Overview(BaseModelCached):
    events: List[Event]
    teams: List[Team]
    elements: List[Player]

    @cached_property
    def player_id_to_name(self) -> Dict[int, str]:
        return {
            player.id: f"{player.first_name} {player.second_name}"
            for player in self.elements
        }


# ------------------------- MANAGER PICKS --------------------------------
# https://fantasy.premierleague.com/api/entry/{manager_id}/event/{event_id}/picks/


class EntryHistory(BaseModelCached):
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


class Pick(BaseModelCached):
    element: int
    position: int
    multiplier: int
    is_captain: bool
    is_vice_captain: bool


@dataclass(frozen=True)
class PickExtended:
    element: int
    position: int
    multiplier: int
    is_captain: bool
    is_vice_captain: bool
    points: int
    name: str


class ManagerPicks(BaseModelCached):
    entry_history: EntryHistory
    picks: List[Pick]

    @cached_property
    def captain_id(self) -> Optional[int]:
        for pick in self.picks:
            if pick.is_captain:
                return pick.element
        return None

    def picks_extended(
        self, player_id_to_points: Dict[int, int], player_id_to_name: Dict[int, str]
    ) -> List[PickExtended]:
        return [
            PickExtended(
                **dict(pick),
                points=player_id_to_points[pick.element],
                name=player_id_to_name[pick.element],
            )
            for pick in self.picks
        ]


# ------------------------- Element Info per Gameweek --------------------------------
# https://fantasy.premierleague.com/api/event/{event_id}/live/


class Stats(BaseModelCached):
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


class PlayerStats(BaseModelCached):
    id: int
    stats: Stats


class GameweekPlayerStats(BaseModelCached):
    elements: List[PlayerStats]

    @cached_property
    def player_id_to_points(self) -> Dict[int, int]:
        return {player.id: player.stats.total_points for player in self.elements}


# ------------------------- Manager Summary --------------------------------
# https://fantasy.premierleague.com/api/entry/{manager_id}/


class ManagerSummary(BaseModelCached):
    id: int
    player_first_name: str
    player_last_name: str
    player_region_name: str
    summary_overall_points: int
    summary_overall_rank: int
    name: str


# ------------------------- Manager History --------------------------------
# https://fantasy.premierleague.com/api/entry/{manager_id}/history/


class CurrentHistory(BaseModelCached):
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


class PastHistory(BaseModelCached):
    season_name: str
    total_points: int
    rank: int


@dataclass
class GameweekBest:
    gameweek: int
    value: int


@dataclass
class ManagerHistoryStats:
    best_previous_season: PastHistory
    best_gameweek_overall_rank: GameweekBest
    best_gameweek_rank: GameweekBest
    best_gameweek_points: GameweekBest
    most_points_on_bench: GameweekBest
    most_transfers: GameweekBest
    gameweek_to_overall_rank: Dict[int, int]


class ManagerHistory(BaseModelCached):
    current: List[CurrentHistory]
    past: List[PastHistory]

    def sort_and_return_best(self, attribute: str, highest_is_best: bool):
        sorted_by_attribute = sorted(
            self.current, key=lambda x: getattr(x, attribute), reverse=highest_is_best
        )
        best = sorted_by_attribute[0]
        return GameweekBest(best.event, getattr(best, attribute))

    @cached_property
    def best_previous_season(self) -> PastHistory:
        sorted_by_rank = sorted(self.past, key=lambda x: x.rank)
        return sorted_by_rank[0]

    @cached_property
    def best_gameweek_overall_rank(self) -> GameweekBest:
        return self.sort_and_return_best(
            attribute="overall_rank", highest_is_best=False
        )

    @cached_property
    def best_gameweek_rank(self) -> GameweekBest:
        return self.sort_and_return_best(attribute="rank", highest_is_best=False)

    @cached_property
    def best_gameweek_points(self) -> GameweekBest:
        return self.sort_and_return_best(attribute="points", highest_is_best=True)

    @cached_property
    def most_points_on_bench(self) -> GameweekBest:
        return self.sort_and_return_best(
            attribute="points_on_bench", highest_is_best=True
        )

    @cached_property
    def most_transfers(self) -> GameweekBest:
        return self.sort_and_return_best(
            attribute="event_transfers", highest_is_best=True
        )

    @cached_property
    def gameweek_to_overall_rank(self) -> Dict[int, int]:
        return {history.event: history.overall_rank for history in self.current}

    @cached_property
    def stats(self) -> ManagerHistoryStats:
        return ManagerHistoryStats(
            best_previous_season=self.best_previous_season,
            best_gameweek_overall_rank=self.best_gameweek_overall_rank,
            best_gameweek_rank=self.best_gameweek_rank,
            best_gameweek_points=self.best_gameweek_points,
            most_points_on_bench=self.most_points_on_bench,
            most_transfers=self.most_transfers,
            gameweek_to_overall_rank=self.gameweek_to_overall_rank,
        )


# ------------------------- Manager Transfers --------------------------------
# https://fantasy.premierleague.com/api/entry/{manager_id}/transfers/


class Transfer(BaseModelCached):
    element_in: int
    element_in_cost: int
    element_out: int
    element_out_cost: int
    entry: int
    event: int
    time: str
