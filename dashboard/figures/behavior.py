"""How rider profile shapes the trip itself."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboard.figures import theme
from dashboard.figures.theme import empty_figure, style_figure


def age_vs_duration(df: pd.DataFrame) -> go.Figure:
    """Age against trip length.

    Every trip as its own point would be a quarter of a million markers and an
    unusable browser tab, so we sample. The seed is fixed, which means the
    chart doesn't reshuffle itself every time a filter changes.
    """

    required = {"member_age", "trip_duration_min"}

    if not required.issubset(df.columns) or df.empty:
        return empty_figure()

    columns = list(required) + (["user_type"] if "user_type" in df.columns else [])
    points = df[columns].dropna()

    points = points[
        points["member_age"].between(16, 80)
        & (points["trip_duration_min"] <= points["trip_duration_min"].quantile(0.99))
    ]

    if points.empty:
        return empty_figure()

    if len(points) > theme.SCATTER_SAMPLE_SIZE:
        points = points.sample(theme.SCATTER_SAMPLE_SIZE, random_state=42)

    fig = px.scatter(
        points,
        x="member_age",
        y="trip_duration_min",
        color="user_type" if "user_type" in points.columns else None,
        opacity=0.35,
        title="Age against duration",
        labels={"member_age": "", "trip_duration_min": "", "user_type": ""},
        color_discrete_sequence=theme.CATEGORICAL,
    )

    fig.update_traces(
        marker=dict(size=5, line=dict(width=0)),
        hovertemplate="Age %{x} · %{y:.0f} min<extra></extra>",
    )

    return style_figure(fig)


def duration_by_user_type(df: pd.DataFrame) -> go.Figure:
    """Median trip length per membership type.

    Median rather than mean: a handful of multi-hour trips pull the average far
    enough to reverse the story the chart tells.
    """

    required = {"user_type", "trip_duration_min"}

    if not required.issubset(df.columns) or df.empty:
        return empty_figure()

    summary = (
        df.groupby("user_type", as_index=False)["trip_duration_min"]
        .median()
        .sort_values("trip_duration_min")
    )

    fig = px.bar(
        summary,
        x="user_type",
        y="trip_duration_min",
        title="Median duration by user type",
        labels={"user_type": "", "trip_duration_min": ""},
        text=summary["trip_duration_min"].map(lambda value: f"{value:.1f}"),
    )

    fig.update_traces(
        marker_color=theme.CONTRAST,
        marker_line_width=0,
        textposition="outside",
        textfont=dict(size=11, color=theme.MUTED),
        hovertemplate="<b>%{x}</b><br>%{y:.1f} min<extra></extra>",
        cliponaxis=False,
    )

    return style_figure(fig)


def distance_by_user_type(df: pd.DataFrame) -> go.Figure:
    """Distance covered per trip, by membership type.

    Pairs with the duration chart to separate two explanations for a long trip:
    riding further, or riding slower.
    """

    required = {"user_type", "trip_distance_km"}

    if not required.issubset(df.columns) or df.empty:
        return empty_figure("Station coordinates are missing from the dataset.")

    trips = df[df["trip_distance_km"] > 0]

    if trips.empty:
        return empty_figure()

    upper = float(trips["trip_distance_km"].quantile(0.99))

    fig = px.box(
        trips[trips["trip_distance_km"] <= upper],
        x="user_type",
        y="trip_distance_km",
        color="user_type",
        points=False,
        title="Distance per trip (km)",
        labels={"user_type": "", "trip_distance_km": ""},
        color_discrete_sequence=theme.CATEGORICAL,
    )

    fig.update_traces(
        marker_line_width=0,
        hovertemplate="%{y:.2f} km<extra></extra>",
    )

    fig.update_layout(showlegend=False)

    return style_figure(fig)
