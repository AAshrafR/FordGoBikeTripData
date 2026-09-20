"""
Geographic helpers built on the station coordinate columns.

The dataset gives us longitude and latitude for both ends of every trip, which
is enough to measure how far a trip actually travelled and to place stations on
a map. Everything here is vectorised — no row-wise apply.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


EARTH_RADIUS_KM = 6371.0

COORDINATE_COLUMNS = (
    "start_station_latitude",
    "start_station_longitude",
    "end_station_latitude",
    "end_station_longitude",
)


def has_coordinates(df: pd.DataFrame) -> bool:
    """True when the table carries both ends' coordinates."""

    return all(column in df.columns for column in COORDINATE_COLUMNS)


def haversine_km(lat1, lon1, lat2, lon2) -> np.ndarray:
    """Great-circle distance in kilometres between two coordinate arrays."""

    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    delta_phi = phi2 - phi1
    delta_lambda = np.radians(np.asarray(lon2) - np.asarray(lon1))

    a = (
        np.sin(delta_phi / 2) ** 2
        + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2
    )

    return 2 * EARTH_RADIUS_KM * np.arcsin(np.sqrt(a))


def add_trip_geometry(df: pd.DataFrame) -> pd.DataFrame:
    """Attach straight-line distance and speed to each trip.

    This is displacement, not the route the rider actually pedalled, so it is
    a floor on real distance — worth remembering before quoting the speed
    figure to anyone. Round trips end where they started and so measure zero;
    we flag them instead of letting them drag the average down unnoticed.
    """

    if not has_coordinates(df):
        return df

    df["trip_distance_km"] = haversine_km(
        df["start_station_latitude"],
        df["start_station_longitude"],
        df["end_station_latitude"],
        df["end_station_longitude"],
    )

    if "start_station_id" in df.columns and "end_station_id" in df.columns:
        df["is_round_trip"] = df["start_station_id"] == df["end_station_id"]

    if "trip_duration_min" in df.columns:
        hours = df["trip_duration_min"] / 60
        df["trip_speed_kmh"] = np.where(
            hours > 0,
            df["trip_distance_km"] / hours,
            np.nan,
        )

    return df
