from fpl.data_loading import FplData
from typing import List, Dict
from dataclasses import dataclass
from functools import lru_cache

from fpl.schema import PickExtended


@dataclass(frozen=True)
class CaptaincyScore:
    gameweek: int
    captain_name: str
    captain_points: int
    highest_scorer_name: str
    highest_scorer_points_if_captain: int


@dataclass(frozen=True)
class BenchScore:
    pass


class FplWrapped:
    def __init__(self, fpl_data: FplData) -> None:
        self.fpl_data = fpl_data

    @property
    @lru_cache()
    def gw_to_extended_picks(self) -> Dict[int, List[PickExtended]]:
        gw_to_picks = {}
        player_id_to_name = self.fpl_data.overview.player_id_to_name
        for gw in self.gameweeks:
            manager_picks = self.fpl_data.manager_picks_by_gameweek[gw]
            player_stats = self.fpl_data.player_stats_by_gameweek[gw]
            player_id_to_points = player_stats.player_id_to_points
            picks_extended = manager_picks.picks_extended(
                player_id_to_name=player_id_to_name,
                player_id_to_points=player_id_to_points,
            )
            gw_to_picks[gw] = picks_extended
        return gw_to_picks

    @property
    @lru_cache()
    def gameweeks(self) -> List[int]:
        return list(self.fpl_data.manager_picks_by_gameweek.keys())

    def captaincy(self) -> List[CaptaincyScore]:
        """
        calculates how many gameweeks the manager picked the correct captain
        and how many points were lost as a result of not picking the correct captain
        """
        if len(self.fpl_data.manager_picks_by_gameweek) != len(
            self.fpl_data.player_stats_by_gameweek
        ):
            raise AssertionError("mismatch in manager picks and player stats lengths")

        gameweeks = self.fpl_data.manager_picks_by_gameweek.keys()
        gw_to_extended_picks = self.gw_to_extended_picks
        captaincy_scores = []
        for gw in gameweeks:
            picks_extended = gw_to_extended_picks[gw]
            captain_points = None
            captain_name = None
            captain_multipler = None
            max_points = 0
            max_points_name = None
            for pick in picks_extended:
                points = pick.points
                name = pick.name
                if pick.is_captain:
                    captain_points = points
                    captain_name = pick.name
                    captain_multipler = pick.multiplier
                if points > max_points:
                    max_points = points
                    max_points_name = name

            if captain_name is None:
                continue

            if max_points > captain_points:
                captaincy_scores.append(
                    CaptaincyScore(
                        gameweek=gw,
                        captain_name=captain_name,
                        captain_points=captain_points * captain_multipler,
                        highest_scorer_name=max_points_name,
                        highest_scorer_points_if_captain=max_points * captain_multipler,
                    )
                )
        return captaincy_scores

    def bench(self) -> List[BenchScore]:
        pass
