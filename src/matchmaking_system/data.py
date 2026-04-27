from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_URL = "https://zenodo.org/records/5978831/files/games.csv?download=1"
RAW_DATA_PATH = Path("data/raw/games.csv")


def load_games(path: str | Path = RAW_DATA_PATH) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Missing dataset at {path}. Run `python scripts/download_data.py` first."
        )
    return pd.read_csv(path)


def prepare_match_records(df: pd.DataFrame, include_draws: bool = False) -> pd.DataFrame:
    records = df.copy()
    records.columns = [column.strip().lower() for column in records.columns]

    required = {"white_rating", "black_rating", "winner"}
    missing = required.difference(records.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    records["rating_gap"] = records["white_rating"] - records["black_rating"]
    records["abs_rating_gap"] = records["rating_gap"].abs()
    records["avg_rating"] = (records["white_rating"] + records["black_rating"]) / 2

    if "turns" in records.columns:
        records["long_game"] = records["turns"] >= records["turns"].median()

    if not include_draws:
        records = records[records["winner"].isin(["white", "black"])].copy()
        records["white_win"] = (records["winner"] == "white").astype(int)

    return records
