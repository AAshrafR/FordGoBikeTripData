import pandas as pd


def average_duration_by_user_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate average trip duration in minutes by user type.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Average duration for each user type.
    """
    return (
        df.groupby("user_type", observed=True)["trip_duration_min"]
        .mean()
        .round(2)
        .reset_index(name="average_duration_min")
    )


def correlation_matrix(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Calculate a Pearson correlation matrix for selected numeric columns.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        columns (list[str]): Numeric columns to include.

    Returns:
        pd.DataFrame: Correlation matrix.
    """
    return df[columns].corr()


def user_distribution_by_age_gender(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Count users by age and member gender.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Counts grouped by age and gender.
    """
    return (
        df.groupby(["member_age", "member_gender"], observed=True)
        .size()
        .reset_index(name="user_count")
    )


def top_start_stations(
    df: pd.DataFrame,
    n: int = 10,
) -> pd.DataFrame:
    """
    Return the most frequently used start stations.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        n (int): Number of stations to return.

    Returns:
        pd.DataFrame: Top start stations and trip counts.
    """
    return (
        df["start_station_name"]
        .value_counts()
        .head(n)
        .rename_axis("start_station_name")
        .reset_index(name="trip_count")
    )


def top_end_stations(
    df: pd.DataFrame,
    n: int = 10,
) -> pd.DataFrame:
    """
    Return the most frequently used end stations.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        n (int): Number of stations to return.

    Returns:
        pd.DataFrame: Top end stations and trip counts.
    """
    return (
        df["end_station_name"]
        .value_counts()
        .head(n)
        .rename_axis("end_station_name")
        .reset_index(name="trip_count")
    )
