# Matchmaking System Design

## Problem

Competitive games need matches that feel fair, start quickly, and keep players engaged. A pure skill-rating approach can create technically balanced games that still feel bad because it ignores wait time, network quality, party constraints, role needs, recent loss streaks, and player churn risk.

## Users

- Players who want fair, low-latency matches.
- Game operators who want healthier retention and fewer frustrating sessions.
- Data scientists and ML engineers who need measurable policy tradeoffs.

## Matchmaking Objectives

The system optimizes several goals at once:

- Skill balance: predicted win probability should be close to 50%.
- Latency: network quality should remain within acceptable thresholds.
- Wait time: queues should not grow indefinitely.
- Composition: teams should satisfy role, party, platform, and region constraints.
- Engagement: avoid patterns correlated with churn, such as repeated stomps.
- Exploration: safely test alternate matching policies.

## Baseline Architecture

1. Player enters queue with profile, rating, region, party metadata, and session context.
2. Candidate generator finds feasible opponents or teams.
3. Scoring layer ranks candidate matches by weighted objectives.
4. Policy layer selects a match, logs decision context, and emits assignment.
5. Post-match pipeline updates ratings and computes quality labels.

## Rating Model

Start with Elo because it is transparent and interview-friendly:

- Expected score: `1 / (1 + 10 ** ((opponent_rating - player_rating) / 400))`
- Rating update: `new_rating = rating + k_factor * (actual_score - expected_score)`

Production systems often move toward uncertainty-aware ratings such as Glicko, TrueSkill, or custom Bayesian models.

## Multi-Objective Scoring

Example candidate score:

```text
score = (
    fairness_weight * fairness_score
    + latency_weight * latency_score
    + wait_weight * wait_time_score
    + retention_weight * retention_score
    + composition_weight * composition_score
)
```

Hard constraints should reject invalid matches before scoring. Soft constraints should influence ranking.

## Reinforcement Learning Extension

An RL-inspired policy can treat matchmaking as a sequential decision problem:

- State: queue composition, player profiles, wait times, recent outcomes.
- Action: choose a feasible match or wait.
- Reward: match quality, retention lift, queue health, fairness, and latency.
- Guardrails: fairness thresholds, regional constraints, and maximum wait time.

Offline policy evaluation is important before any online rollout.

## Metrics

- Match quality: predicted win probability distribution, stomp rate, comeback rate.
- Retention: next-day retention, session length, rematch rate.
- Queue health: p50/p95 wait time, abandonment rate.
- Fairness: rating gap, uncertainty gap, party mismatch rate.
- Reliability: assignment latency and failed match creation rate.

## Risks

- Optimizing retention can conflict with perceived fairness.
- Cold-start players can be over- or under-matched.
- RL policies can learn undesirable shortcuts without guardrails.
- Offline metrics may not fully predict live player sentiment.
