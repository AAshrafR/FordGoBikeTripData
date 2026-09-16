import pandas as pd
from config import (
    CATEGORICAL_COLS,
    MAX_AGE,
    MAX_DURATION_MIN,
)


def converted_data_types(
    df: pd.DataFrame, categorical_cols: list = None
) -> pd.DataFrame:
  if categorical_cols is None:
    categorical_cols = CATEGORICAL_COLS

  df_converted = df.copy()
  for col in categorical_cols:
    if col in df_converted.columns:
      df_converted[col] = df_converted[col].astype("category")

  df_converted["start_station_id"] = (
      df_converted["start_station_id"].astype("Int64").astype("string")
  )
  df_converted["end_station_id"] = (
      df_converted["end_station_id"].astype("Int64").astype("string")
  )
  df_converted["bike_id"] = df_converted["bike_id"].astype(str)
  df_converted["member_birth_year"] = df_converted["member_birth_year"].astype(
      "Int64"
  )

  return df_converted


def check_nulls(df: pd.DataFrame) -> pd.DataFrame:
  null_counts = df.isnull().sum()
  null_pct = (df.isnull().mean() * 100).round(2)
  return pd.DataFrame({"null_count": null_counts, "null_percentage": null_pct})


def impute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
  df_imputed = df.copy()
  df_imputed = df_imputed.dropna(subset=["start_station_id", "end_station_id"])

  median_birth_year = int(df_imputed["member_birth_year"].median())
  df_imputed["member_birth_year"] = df_imputed["member_birth_year"].fillna(
      median_birth_year
  )

  mode_gender = df_imputed["member_gender"].mode()[0]
  df_imputed["member_gender"] = df_imputed["member_gender"].fillna(mode_gender)

  return df_imputed


def check_outliers(
    df: pd.DataFrame, target_cols: list = ["duration_min", "member_age"]
) -> pd.DataFrame:
  summary = []
  for col in target_cols:
    if col not in df.columns:
      continue
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

    summary.append({
        "Feature": col,
        "Min": round(float(df[col].min()), 2),
        "Q1": round(float(q1), 2),
        "Median": round(float(df[col].median()), 2),
        "Q3": round(float(q3), 2),
        "Max": round(float(df[col].max()), 2),
        "IQR_Lower": round(float(lower_bound), 2),
        "IQR_Upper": round(float(upper_bound), 2),
        "Outliers_Count": len(outliers),
        "Outliers (%)": round((len(outliers) / len(df)) * 100, 2),
    })

  return pd.DataFrame(summary)


def remove_outliers(
    df: pd.DataFrame,
    max_duration_min: float = MAX_DURATION_MIN,
    max_age: int = MAX_AGE,
) -> pd.DataFrame:
  initial_count = len(df)
  mask = (df["duration_min"] <= max_duration_min) & (df["member_age"] <= max_age)
  df_cleaned = df[mask].copy()

  removed = initial_count - len(df_cleaned)
  print(
      f"Outliers removed: {removed:,} rows ({(removed / initial_count) * 100:.2f}%)"
  )
  return df_cleaned