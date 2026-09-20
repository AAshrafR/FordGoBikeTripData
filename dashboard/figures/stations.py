"""Where the network concentrates: busiest stations and imbalance."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboard.figures import theme
from dashboard.figures.theme import empty_figure, style_figure, shorten


def top_stations(df: pd.DataFrame, side: str) -> go.Figure:
    """Ten busiest stations for one end of the trip.

    `side` is 'start' or 'end'; origins get the emerald, destinations the
    amber, so the two charts sitting next to each other never get confused.
    """

    column = f"{side}_station_name"

    if column not in df.columns or df.empty:
        return empty_figure()

    counts = (
        df[column].astype(str).value_counts()
        .head(theme.TOP_STATIONS)
        .sort_values()
        .rename_axis("station").reset_index(name="trips")
    )

    # Keep the untruncated name for the tooltip.
    counts["full_name"] = counts["station"]
    counts["station"] = counts["station"].map(shorten)

    fig = px.bar(
        counts,
        x="trips",
        y="station",
        orientation="h",
        title=f"Busiest {side} stations",
        labels={"station": "", "trips": ""},
        custom_data=["full_name"],
    )

    fig.update_traces(
        marker_color=theme.ACCENT if side == "start" else theme.CONTRAST,
        marker_line_width=0,
        hovertemplate="<b>%{customdata[0]}</b><br>%{x:,} trips<extra></extra>",
    )

    fig.update_layout(margin=dict(l=160, r=18, t=52, b=38))
    fig.update_yaxes(showgrid=False)

    return style_figure(fig)


def station_imbalance(profile: pd.DataFrame) -> go.Figure:
    """The stations furthest from balance, in both directions.

    Operations cares about the extremes, not the middle: these are the docks
    that need a van. Bars point left when a station loses bikes over the period
    and right when it accumulates them.
    """

    if profile.empty:
        return empty_figure("Station coordinates are missing from the dataset.")

    extremes = pd.concat(
        [profile.nlargest(5, "net_flow"), profile.nsmallest(5, "net_flow")]
    ).sort_values("net_flow")

    extremes = extremes.assign(label=extremes["station"].map(shorten))

    fig = px.bar(
        extremes,
        x="net_flow",
        y="label",
        orientation="h",
        title="Bikes gained and lost",
        labels={"net_flow": "", "label": ""},
        custom_data=["station"],
    )

    fig.update_traces(
        marker_color=[
            theme.ACCENT if value >= 0 else theme.CONTRAST
            for value in extremes["net_flow"]
        ],
        marker_line_width=0,
        hovertemplate="<b>%{customdata[0]}</b><br>Net flow: %{x:+,}<extra></extra>",
    )

    fig.add_vline(x=0, line_color=theme.AXIS_LINE, line_width=1)
    fig.update_layout(margin=dict(l=160, r=18, t=52, b=38))
    fig.update_yaxes(showgrid=False)

    return style_figure(fig)
