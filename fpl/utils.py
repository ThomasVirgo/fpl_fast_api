from dataclasses import dataclass
from typing import List

from fpl.data_loading import H2HData


@dataclass
class H2HRow:
    name: str
    h2h_rank: int
    expected_rank: int
    points: int
    chips_played: str
    current_overall_rank: int
    best_gameweek_rank: str
    best_previous_season: str
    most_points_on_bench: str
    most_transfers: str
    h2h_points: int


def extract_h2h_rows(h2h_data: H2HData) -> List[H2HRow]:
    rows: List[H2HRow] = []
    for manager_data in h2h_data.standings.results:
        manager_id = manager_data.entry
        if manager_id is None:
            continue
        manager_stats = h2h_data.manager_id_to_stats[manager_id]

        name = manager_data.player_name
        h2h_rank = manager_data.rank
        chips_played = ", ".join(manager_stats.chips_played)
        best_previous_season = manager_stats.best_previous_season
        if best_previous_season:
            best_previous_season_str = f"Season: {manager_stats.best_previous_season.season_name}\nRank: {manager_stats.best_previous_season.rank}\nPoints: {manager_stats.best_previous_season.total_points}"
        else:
            best_previous_season_str = ""
        best_gameweek_rank = str(manager_stats.best_gameweek_rank)
        most_points_on_bench = str(manager_stats.most_points_on_bench)
        most_transfers = str(manager_stats.most_transfers)

        gameweek_to_overall_rank = manager_stats.gameweek_to_overall_rank
        latest_gw = max(gameweek_to_overall_rank.keys())
        current_overall_rank = gameweek_to_overall_rank[latest_gw]

        rows.append(
            H2HRow(
                name=name,
                h2h_rank=h2h_rank,
                expected_rank=1,
                points=manager_data.points_for,
                chips_played=chips_played,
                current_overall_rank=current_overall_rank,
                best_gameweek_rank=best_gameweek_rank,
                best_previous_season=best_previous_season_str,
                most_points_on_bench=most_points_on_bench,
                most_transfers=most_transfers,
                h2h_points=manager_data.total,
            )
        )
    sorted_by_points = sorted(rows, key=lambda x: x.points, reverse=True)
    for i, row in enumerate(sorted_by_points):
        row.expected_rank = i + 1

    return sorted(sorted_by_points, key=lambda x: x.h2h_rank)
