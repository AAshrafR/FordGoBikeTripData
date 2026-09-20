"""
Loading and preparing the trip table.

Same calling convention as the original single-file app: push the project root
onto sys.path, then use the project's own src.data_loading and
src.feature_engineering. Nothing is redefined here that the project already
defines somewhere else.
"""

from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

import pandas as pd


# This file sits at <root>/dashboard/datasource/loader.py, so the project root
# is three levels up.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loading import load_data
from src.feature_engineering import engineer_features

from dashboard.datasource.geo import add_trip_geometry


DATA_PATH = PROJECT_ROOT / "data" / "fordgobike_cleaned.csv"

REFERENCE_YEAR = 2019

# Features the engineering step produces. If the cleaned CSV already carries
# them we skip the recomputation.
ENGINEERED_FEATURES = {"member_age", "age_group", "trip_duration_min"}

# `start_time` / `end_time` are stored as MM:SS.f, not calendar timestamps —
# there is no real date column in the source data. That rules out hour-of-day
# and weekday features: parsing MM:SS.f as a clock time would silently produce
# wrong hours, and there is nothing to derive a weekday from. The dashboard
# works only with what the data actually contains: trip duration.


@lru_cache(maxsize=1)
def get_trips() -> pd.DataFrame:
    """Load and prepare the data required by the dashboard.

    Cached for the lifetime of the process. Callers must treat the result as
    read-only — copy before mutating, or the next caller inherits the change.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset was not found at: {DATA_PATH}")

    df = load_data(DATA_PATH)

    if not ENGINEERED_FEATURES.issubset(df.columns):
        df = engineer_features(df, reference_year=REFERENCE_YEAR)

    if "trip_duration_min" not in df.columns:
        df["trip_duration_min"] = df["duration_sec"] / 60

    df = add_trip_geometry(df)

    return df


def dropdown_options(df: pd.DataFrame, column: str) -> list[dict[str, str]]:
    """Build sorted dropdown options from the distinct values of a column."""

    if column not in df.columns:
        return []

    return [
        {"label": value, "value": value}
        for value in sorted(df[column].dropna().astype(str).unique())
    ]
