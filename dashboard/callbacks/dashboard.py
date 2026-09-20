"""
The single dashboard callback.

One callback drives the whole page: the filters change, every KPI and figure is
rebuilt from the same filtered frame. Splitting it per chart would mean
re-filtering the dataset a dozen times for one interaction.

Output order is defined once in the id lists and reused to build both the
decorator and the returned tuple, which removes the classic failure mode of
silently swapping two figures when a chart is added.
"""

from __future__ import annotations

import pandas as pd
from dash import Input, Output

from dashboard import figures
from dashboard.datasource.geo import has_coordinates
from dashboard.datasource.stations import station_profile


KPI_IDS = [
    "kpi-trips",
    "kpi-duration",
    "kpi-distance",
    "kpi-stations",
    "kpi-age",
]

FIGURE_IDS = [
    "duration-distribution",
    "user-type-chart",
    "gender-chart",
    "age-distribution",
    "station-map",
    "top-start-stations",
    "top-end-stations",
    "station-imbalance",
    "age-duration-scatter",
    "duration-by-user",
    "distance-by-user",
]

# These read station coordinates and are absent from the layout without them.
GEO_FIGURE_IDS = {"station-map", "station-imbalance", "distance-by-user"}


def filter_trips(df: pd.DataFrame, user_type, gender, age_group) -> pd.DataFrame:
    """Apply the sidebar filters.

    A cleared dropdown sends None, which means 'no restriction' rather than
    'match nothing'. The masks are combined and applied once so we make a
    single copy of the frame instead of one per filter.
    """

    mask = pd.Series(True, index=df.index)

    conditions = [
        ("user_type", user_type),
        ("member_gender", gender),
        ("age_group", age_group),
    ]

    for column, selected in conditions:
        if selected and column in df.columns:
            mask &= df[column].astype(str) == str(selected)

    return df[mask]


def _format_kpis(trips: pd.DataFrame, profile: pd.DataFrame) -> list[str]:
    """Turn the filtered frame into the five headline strings.

    Medians throughout: durations and distances are heavily right-skewed, and a
    mean reports a typical ride as longer than most rides actually are.
    """

    if trips.empty:
        return ["0", "—", "—", "0", "—"]

    def median_of(column: str) -> str:
        if column not in trips.columns:
            return "—"

        value = trips[column].median()

        return f"{value:.1f}" if pd.notna(value) else "—"

    return [
        f"{len(trips):,}",
        median_of("trip_duration_min"),
        median_of("trip_distance_km"),
        f"{len(profile):,}" if not profile.empty else "—",
        median_of("member_age"),
    ]


def register_callbacks(app, df: pd.DataFrame) -> None:
    """Wire the sidebar inputs to every output on the page."""

    show_map = has_coordinates(df)

    active_figures = [
        figure_id
        for figure_id in FIGURE_IDS
        if show_map or figure_id not in GEO_FIGURE_IDS
    ]

    outputs = [Output(kpi_id, "children") for kpi_id in KPI_IDS] + [
        Output(figure_id, "figure") for figure_id in active_figures
    ]

    @app.callback(
        outputs,
        Input("user-type-filter", "value"),
        Input("gender-filter", "value"),
        Input("age-group-filter", "value"),
        Input("map-metric", "value"),
    )
    def update_dashboard(user_type, gender, age_group, map_metric):
        trips = filter_trips(df, user_type, gender, age_group)

        profile = station_profile(trips) if show_map else pd.DataFrame()

        kpis = _format_kpis(trips, profile)

        if trips.empty:
            blank = figures.empty_figure()
            return kpis + [blank] * len(active_figures)

        # Lambdas so only the figures actually on the page get built.
        builders = {
            "duration-distribution": lambda: figures.duration_distribution(trips),
            "user-type-chart": lambda: figures.trips_by_user_type(trips),
            "gender-chart": lambda: figures.gender_mix(trips),
            "age-distribution": lambda: figures.age_distribution(trips),
            "station-map": lambda: figures.station_map(profile, map_metric),
            "top-start-stations": lambda: figures.top_stations(trips, "start"),
            "top-end-stations": lambda: figures.top_stations(trips, "end"),
            "station-imbalance": lambda: figures.station_imbalance(profile),
            "age-duration-scatter": lambda: figures.age_vs_duration(trips),
            "duration-by-user": lambda: figures.duration_by_user_type(trips),
            "distance-by-user": lambda: figures.distance_by_user_type(trips),
        }

        return kpis + [builders[figure_id]() for figure_id in active_figures]
