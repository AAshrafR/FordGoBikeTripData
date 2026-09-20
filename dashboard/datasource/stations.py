"""
Station-level aggregations.

A station appears in the trip table twice — once as an origin, once as a
destination — so we roll each side up separately and then merge. The result is
a few hundred rows instead of a few hundred thousand, which is what makes the
maps render instantly.
"""

from __future__ import annotations

import pandas as pd

from dashboard.datasource.geo import has_coordinates


def station_profile(df: pd.DataFrame) -> pd.DataFrame:
    """One row per station with departures, arrivals and net flow.

    Net flow is arrivals minus departures. A negative number means the station
    drains over the period and needs bikes trucked in; a positive one means
    bikes pile up there. That's the single most actionable number on the map.
    """

    if not has_coordinates(df) or df.empty:
        return pd.DataFrame(
            columns=[
                "station_id", "station", "latitude", "longitude",
                "departures", "arrivals", "total_trips", "net_flow",
            ]
        )

    departures = _side_summary(df, "start", "departures")
    arrivals = _side_summary(df, "end", "arrivals")

    profile = departures.merge(
        arrivals,
        on="station_id",
        how="outer",
        suffixes=("", "_end"),
    )

    # A station may only ever appear on one side of a trip in a filtered slice,
    # so fill the identity columns from whichever side actually has them.
    for column in ("station", "latitude", "longitude"):
        profile[column] = profile[column].fillna(profile[f"{column}_end"])

    profile = profile.drop(
        columns=[c for c in profile.columns if c.endswith("_end")]
    )

    profile[["departures", "arrivals"]] = (
        profile[["departures", "arrivals"]].fillna(0).astype(int)
    )

    profile["total_trips"] = profile["departures"] + profile["arrivals"]
    profile["net_flow"] = profile["arrivals"] - profile["departures"]

    return profile.dropna(subset=["latitude", "longitude"])


def _side_summary(df: pd.DataFrame, side: str, count_name: str) -> pd.DataFrame:
    """Count trips per station for one end of the trip."""

    columns = {
        f"{side}_station_id": "station_id",
        f"{side}_station_name": "station",
        f"{side}_station_latitude": "latitude",
        f"{side}_station_longitude": "longitude",
    }

    subset = df[list(columns)].rename(columns=columns)

    summary = (
        subset
        .groupby("station_id", as_index=False)
        .agg(
            station=("station", "first"),
            latitude=("latitude", "first"),
            longitude=("longitude", "first"),
            **{count_name: ("station", "size")},
        )
    )

    return summary


def map_center(profile: pd.DataFrame) -> dict[str, float]:
    """Centre the map on the stations we're actually showing."""

    if profile.empty:
        # Downtown San Francisco, so an empty filter still lands somewhere sane.
        return {"lat": 37.78, "lon": -122.41}

    return {
        "lat": float(profile["latitude"].mean()),
        "lon": float(profile["longitude"].mean()),
    }
