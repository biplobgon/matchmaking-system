from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from random import Random
from statistics import mean

from matchmaking_system.elo import expected_score
from matchmaking_system.policies import Player, score_candidate


@dataclass(frozen=True)
class PolicyResult:
    policy_name: str
    average_abs_rating_gap: float
    average_fairness_score: float
    average_wait_seconds: float
    average_total_score: float


def random_policy(players: list[Player], rng: Random) -> tuple[Player, Player]:
    return tuple(rng.sample(players, 2))  # type: ignore[return-value]


def closest_skill_policy(players: list[Player]) -> tuple[Player, Player]:
    return min(combinations(players, 2), key=lambda pair: abs(pair[0].rating - pair[1].rating))


def multi_objective_policy(players: list[Player]) -> tuple[Player, Player]:
    candidates = [score_candidate(a, b) for a, b in combinations(players, 2)]
    best = max(candidates, key=lambda candidate: candidate.total_score)
    return best.player_a, best.player_b


def simulate_policy(
    players: list[Player],
    policy_name: str,
    rounds: int = 100,
    seed: int = 7,
) -> PolicyResult:
    if len(players) < 2:
        raise ValueError("At least two players are required.")

    rng = Random(seed)
    gaps: list[float] = []
    fairness_scores: list[float] = []
    wait_times: list[float] = []
    total_scores: list[float] = []

    for _ in range(rounds):
        queue = rng.sample(players, min(len(players), 20))
        if policy_name == "random":
            player_a, player_b = random_policy(queue, rng)
        elif policy_name == "closest_skill":
            player_a, player_b = closest_skill_policy(queue)
        elif policy_name == "multi_objective":
            player_a, player_b = multi_objective_policy(queue)
        else:
            raise ValueError(f"Unknown policy: {policy_name}")

        candidate = score_candidate(player_a, player_b)
        gaps.append(abs(player_a.rating - player_b.rating))
        fairness_scores.append(candidate.fairness_score)
        wait_times.append((player_a.wait_seconds + player_b.wait_seconds) / 2)
        total_scores.append(candidate.total_score)

    return PolicyResult(
        policy_name=policy_name,
        average_abs_rating_gap=mean(gaps),
        average_fairness_score=mean(fairness_scores),
        average_wait_seconds=mean(wait_times),
        average_total_score=mean(total_scores),
    )


def fairness_from_ratings(player_a_rating: float, player_b_rating: float) -> float:
    win_prob = expected_score(player_a_rating, player_b_rating)
    return 1 - abs(win_prob - 0.5) * 2
