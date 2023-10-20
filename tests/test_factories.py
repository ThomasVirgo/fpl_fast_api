from tests.factories import schema


def test_all_factories():
    schema.overview_factory()
    schema.manager_history_factory()
    schema.manager_picks_factory()
    schema.manager_summary_factory()
    schema.manager_transfers_factory()
    schema.gameweek_player_stats_factory()
    schema.league_2h2_factory()
