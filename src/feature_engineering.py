import pandas as pd


def add_member_age(
    df: pd.DataFrame,
    reference_year: int = 2026,
) -> pd.DataFrame:
    """Calculate member age from birth year."""
    df = df.copy()
    df["member_age"] = reference_year - df["member_birth_year"]
    return df


def add_trip_duration_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create trip duration features in minutes and hours."""
    df = df.copy()
    df["trip_duration_min"] = df["duration_sec"] / 60
    df["trip_duration_hour"] = df["trip_duration_min"] / 60
    return df


def add_age_group(df: pd.DataFrame) -> pd.DataFrame:
    """Create age groups for user analysis."""
    df = df.copy()

    bins = [0, 18, 25, 35, 45, 55, 65, float("inf")]
    labels = [
        "Under 18",
        "18-24",
        "25-34",
        "35-44",
        "45-54",
        "55-64",
        "65+",
    ]

    df["age_group"] = pd.cut(
        df["member_age"],
        bins=bins,
        labels=labels,
        right=False,
    )

    return df


def add_weekend_flag(df: pd.DataFrame) -> pd.DataFrame:
    """Add a weekend flag when a usable date/datetime column is available."""
    df = df.copy()

    date_column = None
    for column in ["start_datetime", "start_date", "date"]:
        if column in df.columns:
            date_column = column
            break

    if date_column is None:
        raise ValueError(
            "No date column is available. The current dataset contains "
            "MM:SS.f time strings, so weekend_flag cannot be derived "
            "reliably without a real date field."
        )

    dates = pd.to_datetime(df[date_column], errors="coerce")
    df["weekend_flag"] = dates.dt.dayofweek >= 5

    return df


def engineer_features(
    df: pd.DataFrame,
    reference_year: int = 2026,
) -> pd.DataFrame:
    """Apply feature engineering steps (call this AFTER age outliers are handled)."""
    df = add_member_age(df, reference_year)
    df = add_trip_duration_features(df)
    return df