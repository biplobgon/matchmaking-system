from matchmaking import Player, choose_best_pair, elo_update, expected_score


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
