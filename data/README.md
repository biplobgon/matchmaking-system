# Data

The raw dataset is intentionally not committed.

## Source

- Dataset: Chess Game Dataset (Lichess)
- Kaggle: https://www.kaggle.com/datasets/datasnaek/chess
- Zenodo mirror: https://zenodo.org/records/5978831
- Direct CSV: https://zenodo.org/records/5978831/files/games.csv?download=1

The dataset includes 20,000+ online Lichess games with player IDs, ratings, winners, time controls, opening metadata, and move text. For this project, it is used as a public proxy for 1v1 competitive matchmaking.

## Download

```bash
python scripts/download_data.py
```

This writes:

```text
data/raw/games.csv
```

## Modeling Target

The primary supervised learning target is whether the white player wins. Draws are filtered for binary outcome modeling, but kept during EDA to understand fairness and match quality.

## Matchmaking Interpretation

- `white_id`, `black_id`: player identifiers
- `white_rating`, `black_rating`: pre-match skill signals
- `winner`: observed outcome
- `increment_code`: time-control context
- `turns`, `victory_status`: engagement and match-quality proxies
