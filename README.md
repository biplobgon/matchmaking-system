# Matchmaking System

Fair, retention-aware gaming matchmaking system using Elo baselines, outcome modeling, and multi-objective match scoring.

## Business Question

How can we match players fairly while improving engagement and long-term retention?

## Dataset

This project uses the public Lichess chess games dataset as a compact proxy for 1v1 competitive matchmaking. It contains 20,000+ games with player IDs, ratings, winners, time controls, and game metadata. The dataset is available on Kaggle and mirrored on Zenodo for direct reproducible download.

- Kaggle: https://www.kaggle.com/datasets/datasnaek/chess
- Zenodo mirror: https://zenodo.org/records/5978831
- Direct CSV: https://zenodo.org/records/5978831/files/games.csv?download=1

Why chess works for this portfolio project:

- It has explicit pre-match skill ratings for both players.
- It has observed outcomes, which lets us evaluate rating-based fairness.
- It naturally maps to 1v1 matchmaking before extending to team and battle-royale settings.
- It is small enough to run locally but realistic enough to support EDA, modeling, and policy simulation.

## Project Snapshot

| Area | Details |
| --- | --- |
| Domain | Gaming AI Systems |
| Core problem | Fair player matching |
| Business impact | Improved retention |
| Baseline methods | Elo expected-score matching |
| Advanced methods | Outcome modeling, policy simulation, RL-ready reward design |
| Innovation | Balancing skill fairness, wait time, outcome uncertainty, and engagement proxies |

## System Goals

- Create balanced matches with predictable win probabilities.
- Reduce churn by avoiding repeated frustrating matchups.
- Support cold-start players with confidence-aware rating estimates.
- Optimize across fairness, wait time, ping, role composition, party size, and engagement signals.
- Provide offline evaluation and online experimentation paths.

## Repository Structure

```text
.
|-- data/
|   `-- README.md
|-- docs/
|   `-- system_design.md
|-- notebooks/
|   |-- 01_lichess_matchmaking_eda.ipynb
|   `-- 02_matchmaking_modeling_and_policy.ipynb
|-- scripts/
|   `-- download_data.py
|-- src/
|   |-- matchmaking.py
|   `-- matchmaking_system/
|       |-- data.py
|       |-- elo.py
|       |-- features.py
|       |-- policies.py
|       `-- simulation.py
|-- tests/
|   `-- test_matchmaking.py
|-- .gitignore
|-- pyproject.toml
`-- README.md
```

## Quick Start

```bash
python -m pip install -e ".[dev]"
python scripts/download_data.py
pytest
```

Open the notebooks after downloading the data:

```bash
jupyter lab notebooks/
```

## Portfolio Story

1. `01_lichess_matchmaking_eda.ipynb`: quantify rating gaps, color advantage, time-control effects, and outcome predictability.
2. `02_matchmaking_modeling_and_policy.ipynb`: train a win-probability model, define match quality metrics, and simulate candidate selection policies.
3. `src/matchmaking_system/`: reusable system components for data loading, feature engineering, Elo baselines, policy scoring, and offline simulation.
4. `docs/system_design.md`: architecture, metrics, guardrails, and productionization path.

## Roadmap

1. Build a deterministic Elo-based baseline matcher.
2. Add wait-time and latency-aware constraints.
3. Introduce multi-objective scoring for candidate matches.
4. Simulate engagement-sensitive matchmaking policies.
5. Compare random, closest-skill, and model-assisted policies offline.
6. Extend from 1v1 matching to team formation with role and party constraints.
