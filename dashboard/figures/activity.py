"""When the network moves: hourly rhythm and how long trips last."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboard.figures import theme
from dashboard.figures.theme import empty_figure, style_figure


# Monday-first ordering, because Plotly would otherwise sort the day names
# alphabetically and put Friday at the top.
WEEKDAY_ORDER = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday",
]


def trips_by_hour(df: pd.DataFrame) -> go.Figure:
    """Trip volume across the 24-hour clock."""

    if "start_hour" not in df.columns:
        return empty_figure("Start timestamps are missing from the dataset.")

    hourly = (
        df.dropna(subset=["start_hour"])
        .groupby("start_hour", as_index=False)
        .size()
        .rename(columns={"size": "trips"})
    )

    if hourly.empty:
        return empty_figure()

    fig = px.area(
        hourly,
        x="start_hour",
        y="trips",
        title="Trips by hour of day",
        labels={"start_hour": "", "trips": ""},
    )

    fig.update_traces(
        line=dict(color=theme.ACCENT_DEEP, width=2.2),
        fillcolor=theme.ACCENT_SOFT,
        hovertemplate="<b>%{x}:00</b><br>%{y:,} trips<extra></extra>",
    )

    fig.update_xaxes(dtick=3, ticksuffix=":00")

    return style_figure(fig)


def weekday_hour_heatmap(df: pd.DataFrame) -> go.Figure:
    """Hour-by-weekday grid — where the commuter pattern becomes obvious.

    The hourly curve hides the fact that the two rush-hour spikes belong to
    weekdays only; as a grid, weekends read as a different shape entirely.
    """

    if not {"start_hour", "start_weekday"}.issubset(df.columns):
        return empty_figure("Start timestamps are missing from the dataset.")

    grid = (
        df.dropna(subset=["start_hour", "start_weekday"])
        .groupby(["start_weekday", "start_hour"], as_index=False)
        .size()
        .rename(columns={"size": "trips"})
        .pivot(index="start_weekday", columns="start_hour", values="trips")
        .reindex(WEEKDAY_ORDER)
        .fillna(0)
    )

    if grid.empty:
        return empty_figure()

    # Three-letter day names keep the left margin narrow.
    grid.index = [day[:3] for day in grid.index]

    fig = px.imshow(
        grid,
        color_continuous_scale=theme.SEQUENTIAL,
        aspect="auto",
        title="Demand by weekday and hour",
        labels=dict(x="", y="", color="Trips"),
    )

    fig.update_traces(
        hovertemplate="<b>%{y}</b> at %{x}:00<br>%{z:,} trips<extra></extra>"
    )

    fig.update_xaxes(dtick=2, ticksuffix="")
    fig.update_coloraxes(showscale=False)

    return style_figure(fig, show_grid=False)


def duration_distribution(df: pd.DataFrame) -> go.Figure:
    """How long a typical trip lasts.

    The tail runs for hours, so the view is clipped at the 99th percentile.
    The tail is real, but squashing 99% of the data into the leftmost bar to
    accommodate it hides the shape that matters.
    """

    if "trip_duration_min" not in df.columns or df.empty:
        return empty_figure()

    durations = df["trip_duration_min"].dropna()

    if durations.empty:
        return empty_figure()

    upper = float(durations.quantile(0.99))

    fig = px.histogram(
        durations[durations <= upper],
        nbins=40,
        title="Trip duration",
        labels={"value": "Minutes"},
    )

    fig.update_traces(
        marker_color=theme.ACCENT,
        marker_line_width=0,
        opacity=0.9,
        hovertemplate="%{x} min<br>%{y:,} trips<extra></extra>",
    )

    fig.update_layout(showlegend=False, bargap=0.04)
    fig.update_yaxes(title_text="")

    median = float(durations.median())

    fig.add_vline(
        x=median,
        line_dash="dot",
        line_color=theme.INK,
        line_width=1.4,
        annotation_text=f"median {median:.0f}m",
        annotation_position="top right",
        annotation_font=dict(size=10, color=theme.MUTED),
    )

    return style_figure(fig)
