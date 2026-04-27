from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable


@dataclass(frozen=True)
class Player:
    player_id: str
    rating: float
    wait_seconds: int = 0
    latency_ms: int = 50


@dataclass(frozen=True)
class MatchCandidate:
    player_a: Player
    player_b: Player
    fairness_score: float
    wait_score: float
    latency_score: float

    @property
    def total_score(self) -> float:
        return (
            0.60 * self.fairness_score
            + 0.25 * self.wait_score
            + 0.15 * self.latency_score
        )


def expected_score(player_rating: float, opponent_rating: float) -> float:
    return 1 / (1 + 10 ** ((opponent_rating - player_rating) / 400))


def elo_update(
    rating: float,
    opponent_rating: float,
    actual_score: float,
    k_factor: float = 32,
) -> float:
    return rating + k_factor * (actual_score - expected_score(rating, opponent_rating))


def score_candidate(player_a: Player, player_b: Player) -> MatchCandidate:
    rating_gap = abs(player_a.rating - player_b.rating)
    fairness_score = max(0.0, 1 - rating_gap / 800)

    avg_wait = (player_a.wait_seconds + player_b.wait_seconds) / 2
    wait_score = min(1.0, avg_wait / 180)

    latency_gap = abs(player_a.latency_ms - player_b.latency_ms)
    latency_score = max(0.0, 1 - latency_gap / 200)

    return MatchCandidate(
        player_a=player_a,
        player_b=player_b,
        fairness_score=fairness_score,
        wait_score=wait_score,
        latency_score=latency_score,
    )


def choose_best_pair(players: Iterable[Player]) -> MatchCandidate | None:
    candidates = [score_candidate(a, b) for a, b in combinations(players, 2)]
    if not candidates:
        return None
    return max(candidates, key=lambda candidate: candidate.total_score)
