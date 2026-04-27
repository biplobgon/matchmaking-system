# Portfolio Solution

## Objective

Build a working, interview-ready matchmaking system prototype that shows data discovery, EDA, ML modeling, system design, and offline policy evaluation.

## Public Dataset Choice

The project uses the Lichess chess games dataset:

- Kaggle: https://www.kaggle.com/datasets/datasnaek/chess
- Zenodo mirror: https://zenodo.org/records/5978831
- Direct CSV: https://zenodo.org/records/5978831/files/games.csv?download=1

This is not a full commercial multiplayer telemetry dataset, but it is a strong public proxy for 1v1 competitive matchmaking because it has:

- Stable player IDs.
- Pre-match ratings for both competitors.
- Observed outcomes.
- Game duration proxy through turn count.
- Time-control context.

## Why This Showcases AI/ML Ability

The repo demonstrates the full path from raw public data to a deployable policy concept:

1. Data sourcing and reproducibility through a download script.
2. EDA that connects rating gaps to fairness and outcome uncertainty.
3. Feature engineering for Elo probability, skill gap, and engagement proxies.
4. Baseline and ML outcome prediction.
5. Offline policy simulation across random, closest-skill, and multi-objective match selection.
6. Production thinking around guardrails, logging, retraining, and A/B testing.

## Proposed End-to-End System

### 1. Queue Intake

Capture player and session state:

- Player ID and current rating.
- Game mode and region.
- Queue entry time.
- Latency estimate.
- Party metadata.
- Recent match outcomes and churn-risk features.

### 2. Candidate Generation

Generate feasible player pairs or teams using hard constraints:

- Same game mode.
- Compatible region and platform.
- Rating gap below an expanding threshold.
- Latency below a maximum threshold.
- Party and role rules for team games.

### 3. Match Scoring

Score candidates with a multi-objective function:

```text
match_score =
    fairness_weight * skill_fairness
  + uncertainty_weight * outcome_uncertainty
  + wait_weight * queue_relief
  + latency_weight * latency_compatibility
  + engagement_weight * engagement_score
```

The current implementation provides the first reusable version of this idea in `src/matchmaking_system/policies.py`.

### 4. Outcome Modeling

Use historical matches to estimate win probability. The notebooks compare:

- Elo expected score.
- Logistic regression.
- Random forest.

The system should prefer the simplest calibrated model that improves match-quality scoring without hurting interpretability.

### 5. Offline Evaluation

Before any online test, compare policies on historical and simulated queues:

- Average absolute rating gap.
- Fairness score.
- Predicted outcome uncertainty.
- Average wait time.
- Match-quality score.

The notebook `02_matchmaking_modeling_and_policy.ipynb` includes this offline policy comparison.

### 6. Online Experimentation

Roll out with guardrails:

- No large increase in stomp rate.
- No large increase in p95 wait time.
- No worsening for new or low-confidence players.
- Monitor next-session return rate, rematch rate, and abandon rate.

## Extension Ideas

- Add Glicko or TrueSkill-style uncertainty.
- Build a team formation optimizer.
- Add cold-start handling for new players.
- Add a FastAPI scoring endpoint.
- Add MLflow experiment tracking.
- Add a small Streamlit dashboard for policy comparison.
