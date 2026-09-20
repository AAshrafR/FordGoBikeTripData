import pandas as pd


def convert_to_nullable_integer(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Convert selected columns to Pandas nullable integer type.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        columns (list[str]): Column names to convert.

    Returns:
        pd.DataFrame: DataFrame with converted columns.
    """
    df = df.copy()

    for col in columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    return df


def convert_to_category(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Convert selected columns to categorical type.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        columns (list[str]): Column names to convert.

    Returns:
        pd.DataFrame: DataFrame with converted columns.
    """
    df = df.copy()

    for col in columns:
        df[col] = df[col].astype("category")

    return df


def time_to_seconds(time_series: pd.Series) -> pd.Series:
    """
    Convert MM:SS.f time values to seconds.

    Parameters:
        time_series (pd.Series): Series containing MM:SS.f values.

    Returns:
        pd.Series: Time values converted to seconds.
    """
    parts = time_series.astype("string").str.split(":")

    minutes = pd.to_numeric(parts.str[0], errors="coerce")
    seconds = pd.to_numeric(parts.str[1], errors="coerce")

    return minutes * 60 + seconds


def add_time_validation_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add helper columns used to validate start/end times against duration.

    The source data stores start_time and end_time in MM:SS.f format.
    Therefore, they are converted to seconds instead of being parsed
    directly as timestamps.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with time-validation columns.
    """
    df = df.copy()

    df["start_time_sec"] = time_to_seconds(df["start_time"])
    df["end_time_sec"] = time_to_seconds(df["end_time"])

    df["calculated_end_sec"] = (
        df["start_time_sec"] + df["duration_sec"]
    ) % 3600

    # Circular difference keeps the result in approximately [-1800, 1800].
    df["time_difference"] = (
        (
            df["start_time_sec"]
            + df["duration_sec"]
            - df["end_time_sec"]
            + 1800
        )
        % 3600
    ) - 1800

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill missing values using the cleaning strategy from the notebook.

    Numeric columns use their median.
    Categorical member_gender uses an explicit 'Unknown' category.
    Other categorical/string columns use their mode.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame after missing-value treatment.
    """
    df = df.copy()

    for col in df.columns:
        if col == "member_gender":
            if not isinstance(df[col].dtype, pd.CategoricalDtype):
                df[col] = df[col].astype("category")

            if "Unknown" not in df[col].cat.categories:
                df[col] = df[col].cat.add_categories("Unknown")

            df[col] = df[col].fillna("Unknown")

        elif pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())

        elif isinstance(df[col].dtype, pd.CategoricalDtype):
            mode = df[col].mode(dropna=True)
            if not mode.empty:
                if mode.iloc[0] not in df[col].cat.categories:
                    df[col] = df[col].cat.add_categories([mode.iloc[0]])
                df[col] = df[col].fillna(mode.iloc[0])

        else:
            mode = df[col].mode(dropna=True)
            if not mode.empty:
                df[col] = df[col].fillna(mode.iloc[0])

    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicated rows from the dataset.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame without duplicate rows.
    """
    return df.drop_duplicates().copy()


def cap_outliers(
    df: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    """
    Cap values outside the IQR fences. (Useful for continuous variables 
    like trip_duration, but less ideal for strict bounds like human age).

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        column (str): Numeric column to process.

    Returns:
        pd.DataFrame: DataFrame with IQR-based capping applied.
    """
    df = df.copy()

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr

    # If the column is an integer type, cast the fences to integers
    if pd.api.types.is_integer_dtype(df[column]):
        lower_fence = int(round(lower_fence))
        upper_fence = int(round(upper_fence))

    df[column] = df[column].clip(
        lower=lower_fence,
        upper=upper_fence,
    )

    return df


def handle_age_outliers(
    df: pd.DataFrame,
    min_age: int = 12,
    max_age: int = 80,
) -> pd.DataFrame:
    """
    Filter unrealistic age values based on domain constraints.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        min_age (int): Minimum valid user age (default 12).
        max_age (int): Maximum valid user age (default 80).

    Returns:
        pd.DataFrame: DataFrame with unrealistic ages removed.
    """
    # Keep only rows where member_age is within our realistic bounds
    # (This assumes member_age has already been calculated)
    filtered_df = df[
        (df["member_age"] >= min_age) & (df["member_age"] <= max_age)
    ].copy()
    
    return filtered_df