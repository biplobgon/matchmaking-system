from __future__ import annotations


def expected_score(player_rating: float, opponent_rating: float) -> float:
    """Return the Elo expected score for player_rating against opponent_rating."""
    return 1 / (1 + 10 ** ((opponent_rating - player_rating) / 400))


def elo_update(
    rating: float,
    opponent_rating: float,
    actual_score: float,
    k_factor: float = 32,
) -> float:
    """Update a player's Elo rating after a match."""
    return rating + k_factor * (actual_score - expected_score(rating, opponent_rating))
