from matchmaking import Player, choose_best_pair, elo_update, expected_score
from matchmaking_system.simulation import fairness_from_ratings, simulate_policy


def test_expected_score_is_even_for_equal_ratings() -> None:
    assert expected_score(1200, 1200) == 0.5


def test_elo_update_increases_winner_rating() -> None:
    assert elo_update(1200, 1200, actual_score=1) > 1200


def test_choose_best_pair_prefers_closer_ratings() -> None:
    players = [
        Player("p1", rating=1200),
        Player("p2", rating=1210),
        Player("p3", rating=1800),
    ]

    match = choose_best_pair(players)

    assert match is not None
    assert {match.player_a.player_id, match.player_b.player_id} == {"p1", "p2"}


def test_fairness_from_ratings_is_highest_for_equal_ratings() -> None:
    assert fairness_from_ratings(1500, 1500) > fairness_from_ratings(1500, 1900)


def test_simulate_policy_returns_policy_metrics() -> None:
    players = [
        Player("p1", rating=1200, wait_seconds=30),
        Player("p2", rating=1220, wait_seconds=90),
        Player("p3", rating=1600, wait_seconds=10),
        Player("p4", rating=1620, wait_seconds=20),
    ]

    result = simulate_policy(players, policy_name="closest_skill", rounds=5)

    assert result.policy_name == "closest_skill"
    assert result.average_abs_rating_gap >= 0
