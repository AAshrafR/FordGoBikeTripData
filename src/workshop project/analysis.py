import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from config import (
    EXCLUDE_CORR_COLS,
    PALETTE_GENDER,
    PALETTE_USER_TYPE,)


def get_duration_by_gender(
    df: pd.DataFrame,
    duration_col: str = "duration_min",
    gender_col: str = "member_gender",
) -> pd.DataFrame:
  return (
      df.groupby(gender_col)[duration_col]
      .agg(
          Mean="mean",
          Median="median",
          Std="std",
          Min="min",
          Max="max",
          Trip_Count="count",
      )
      .round(2)
      .sort_values(by="Mean", ascending=False)
  )


def get_duration_by_user_type(
    df: pd.DataFrame,
    duration_col: str = "duration_min",
    user_col: str = "user_type",
) -> pd.DataFrame:
  return (
      df.groupby(user_col)[duration_col]
      .agg(
          Mean="mean",
          Median="median",
          Std="std",
          Min="min",
          Max="max",
          Trip_Count="count",
      )
      .round(2)
      .sort_values(by="Mean", ascending=False)
  )


def get_top_stations(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
  return (
      df["start_station_name"]
      .value_counts()
      .head(top_n)
      .reset_index(name="trip_count")
  )


def get_top_routes(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
  routes = (
      df["start_station_name"].astype(str)
      + " -> "
      + df["end_station_name"].astype(str)
  )
  return routes.value_counts().head(top_n).reset_index(name="trip_count")


def plot_boxplots(df: pd.DataFrame, save_path: str = None):
  sns.set_theme(style="whitegrid")
  fig, axes = plt.subplots(1, 2, figsize=(14, 5))

  sns.boxplot(
      x=df["duration_min"],
      ax=axes[0],
      color="#4C72B0",
      flierprops=dict(marker="o", markersize=3, alpha=0.3),
  )
  axes[0].set_title(
      "Boxplot: Trip Duration (Minutes)", fontsize=13, fontweight="bold"
  )
  axes[0].set_xlabel("Duration (min)", fontsize=11)

  sns.boxplot(
      x=df["member_age"],
      ax=axes[1],
      color="#C44E52",
      flierprops=dict(marker="o", markersize=3, alpha=0.3),
  )
  axes[1].set_title(
      "Boxplot: Member Age (Years)", fontsize=13, fontweight="bold"
  )
  axes[1].set_xlabel("Age (years)", fontsize=11)

  plt.tight_layout()
  if save_path:
    plt.savefig(save_path, dpi=300)
  plt.show()


def plot_duration_hours_distribution(
    df: pd.DataFrame, col: str = "duration_hours", bins: int = 40
):
  plt.figure(figsize=(10, 5))
  sns.histplot(data=df, x=col, bins=bins, color="#2b5c8f", kde=True)

  mean_hr = df[col].mean()
  median_hr = df[col].median()

  plt.axvline(
      mean_hr, color="red", linestyle="--", label=f"Mean: {mean_hr:.2f} hrs"
  )
  plt.axvline(
      median_hr,
      color="green",
      linestyle="-",
      label=f"Median: {median_hr:.2f} hrs",
  )

  plt.title(
      "Distribution of Trip Duration in Hours", fontsize=14, fontweight="bold"
  )
  plt.xlabel("Trip Duration (Hours)")
  plt.ylabel("Number of Trips")
  plt.legend()
  plt.tight_layout()
  plt.show()


def plot_duration_by_user_type(
    df: pd.DataFrame,
    duration_col: str = "duration_min",
    user_col: str = "user_type",
) -> pd.DataFrame:
  stats = (
      df.groupby(user_col)[duration_col]
      .agg(["mean", "median", "count"])
      .round(2)
  )

  plt.figure(figsize=(8, 5))
  ax = sns.barplot(
      data=df,
      x=user_col,
      y=duration_col,
      palette=PALETTE_USER_TYPE,
      errorbar=None,
      order=stats.index,
  )

  plt.title(
      f'Average Trip Duration by {user_col.replace("_", " ").title()}',
      fontsize=14,
      fontweight="bold",
  )
  plt.xlabel(user_col.replace("_", " ").title(), fontsize=12)
  plt.ylabel(
      f'Average Duration ({duration_col.split("_")[-1].capitalize()})',
      fontsize=12,
  )

  for p, u_type in zip(ax.patches, stats.index):
    mean_val = stats.loc[u_type, "mean"]
    median_val = stats.loc[u_type, "median"]
    ax.annotate(
        f"Mean: {mean_val:.1f} min\nMedian: {median_val:.1f} min",
        (p.get_x() + p.get_width() / 2.0, p.get_height() / 2),
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
        color="white",
    )

  sns.despine(top=True, right=True)
  plt.tight_layout()
  plt.show()

  return stats


def plot_age_by_gender(
    df: pd.DataFrame,
    age_col: str = "member_age",
    gender_col: str = "member_gender",
) -> pd.DataFrame:
  stats = (
      df.groupby(gender_col)[age_col]
      .agg(
          Mean="mean",
          Median="median",
          Std="std",
          Min="min",
          Max="max",
          Riders="count",
      )
      .round(2)
  )

  plt.figure(figsize=(9, 5))
  sns.boxplot(
      data=df,
      x=gender_col,
      y=age_col,
      order=list(PALETTE_GENDER.keys()),
      palette=PALETTE_GENDER,
      width=0.45,
      showmeans=True,
      meanprops={
          "marker": "o",
          "markerfacecolor": "white",
          "markeredgecolor": "black",
          "markersize": 7,
      },
  )

  plt.title(
      f"{age_col.replace('_', ' ').title()} by {gender_col.replace('_', ' ').title()}",
      fontsize=14,
      fontweight="bold",
  )
  plt.xlabel(gender_col.replace("_", " ").title(), fontsize=12)
  plt.ylabel("Age (Years)", fontsize=12)

  sns.despine(top=True, right=True)
  plt.tight_layout()
  plt.show()

  return stats


def plot_correlation_heatmap(
    df: pd.DataFrame, exclude_cols: list = None
) -> pd.DataFrame:
  if exclude_cols is None:
    exclude_cols = EXCLUDE_CORR_COLS

  numeric_df = df.select_dtypes(include=[np.number]).drop(
      columns=[c for c in exclude_cols if c in df.columns], errors="ignore"
  )

  corr = numeric_df.corr()

  plt.figure(figsize=(8, 6))
  mask = np.triu(np.ones_like(corr, dtype=bool))

  sns.heatmap(
      corr,
      mask=mask,
      annot=True,
      fmt=".2f",
      cmap="Blues",
      vmin=-1,
      vmax=1,
      square=True,
      linewidths=0.5,
      cbar_kws={"shrink": 0.8, "label": "Correlation Coefficient (r)"},
  )

  plt.title(
      "Correlation Matrix of Numerical Features", fontsize=14, fontweight="bold"
  )
  plt.xticks(rotation=45, ha="right")
  plt.yticks(rotation=0)
  plt.tight_layout()
  plt.show()

  return corr