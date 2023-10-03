from fpl.data_loading import FplData
from typing import List
from dataclasses import dataclass


@dataclass(frozen=True)
class CaptaincyScore:
    gameweek: int
    captain_name: str
    captain_points: int
    highest_scorer_name: str
    highest_scorer_points_if_captain: int


class FplWrapped:
    def __init__(self, fpl_data: FplData) -> None:
        self.fpl_data = fpl_data

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
        player_id_to_name = self.fpl_data.overview.player_id_to_name
        captaincy_scores = []
        for gw in gameweeks:
            manager_picks = self.fpl_data.manager_picks_by_gameweek[gw]
            player_stats = self.fpl_data.player_stats_by_gameweek[gw]
            player_id_to_points = player_stats.player_id_to_points
            picks_extended = manager_picks.picks_extended(
                player_id_to_name=player_id_to_name,
                player_id_to_points=player_id_to_points,
            )
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
