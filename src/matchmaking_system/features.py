from __future__ import annotations

import pandas as pd

from matchmaking_system.elo import expected_score


def add_matchmaking_features(df: pd.DataFrame) -> pd.DataFrame:
    features = df.copy()
    features["elo_white_win_prob"] = [
        expected_score(white_rating, black_rating)
        for white_rating, black_rating in zip(
            features["white_rating"], features["black_rating"], strict=False
        )
    ]
    features["elo_uncertainty"] = 1 - (features["elo_white_win_prob"] - 0.5).abs() * 2
    features["skill_bucket"] = pd.cut(
        features["avg_rating"],
        bins=[0, 1200, 1600, 2000, 3000],
        labels=["novice", "intermediate", "advanced", "expert"],
        include_lowest=True,
    )

    if "increment_code" in features.columns:
        base_minutes = features["increment_code"].astype(str).str.extract(r"^(\d+)")[0]
        features["base_time_seconds"] = pd.to_numeric(base_minutes, errors="coerce")

    return features


def modeling_frame(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    features = add_matchmaking_features(df)
    columns = [
        "white_rating",
        "black_rating",
        "rating_gap",
        "abs_rating_gap",
        "avg_rating",
        "elo_white_win_prob",
        "elo_uncertainty",
    ]
    if "turns" in features.columns:
        columns.append("turns")
    if "base_time_seconds" in features.columns:
        columns.append("base_time_seconds")

    x = features[columns].fillna(features[columns].median(numeric_only=True))
    y = features["white_win"]
    return x, y
