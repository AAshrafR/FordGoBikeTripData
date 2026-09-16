import pandas as pd
from config import (
    AGE_BINS,
    AGE_LABELS,
    DURATION_BINS,
    DURATION_LABELS,
)


def add_all_features(
    df: pd.DataFrame, current_year: int = 2019, drop_old: bool = True
) -> pd.DataFrame:
  df_featured = df.copy()

  df_featured["duration_min"] = (df_featured["duration_sec"] / 60).round(2)
  df_featured["duration_hours"] = (df_featured["duration_sec"] / 3600).round(2)
  df_featured["member_age"] = (
      current_year - df_featured["member_birth_year"]
  ).astype("Int64")

  df_featured["start_minute"] = (
      df_featured["start_time"]
      .astype(str)
      .str.split(":")
      .str[0]
      .astype(float)
      .astype("Int64")
  )

  df_featured["duration_category"] = pd.cut(
      df_featured["duration_min"],
      bins=DURATION_BINS,
      labels=DURATION_LABELS,
      right=False,
  )

  df_featured["age_group"] = pd.cut(
      df_featured["member_age"],
      bins=AGE_BINS,
      labels=AGE_LABELS,
      right=False,
  )

  if drop_old:
    df_featured = df_featured.drop(
        columns=["duration_sec", "member_birth_year"], errors="ignore"
    )

  return df_featured