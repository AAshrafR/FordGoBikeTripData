"""
The station map.

Built from station-level aggregates, never from raw trips: one marker per dock
instead of one per journey is the difference between an instant render and a
frozen tab.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboard.datasource.stations import map_center
from dashboard.figures import theme
from dashboard.figures.theme import empty_figure, style_map


# Plotly Express renamed these in 5.24 alongside the trace classes.
_scatter_map = getattr(px, "scatter_map", None) or px.scatter_mapbox

NO_COORDS_MESSAGE = "Station coordinates are missing from the dataset."


def station_map(profile: pd.DataFrame, metric: str = "volume") -> go.Figure:
    """Stations as circles, sized by traffic.

    Two readings of the same dots, switched from the sidebar:
      volume   — colour follows total trips, showing where demand clusters.
      net_flow — colour diverges around zero, showing which docks fill up and
                 which empty out. That's the rebalancing view.
    """

    if profile.empty:
        return empty_figure(NO_COORDS_MESSAGE)

    if metric == "net_flow":
        color_column = "net_flow"
        color_scale = theme.DIVERGING
        midpoint = 0
        title = "Station balance — green gains bikes, amber loses them"
    else:
        color_column = "total_trips"
        color_scale = theme.SEQUENTIAL
        midpoint = None
        title = "Station activity across the network"

    fig = _scatter_map(
        profile,
        lat="latitude",
        lon="longitude",
        size="total_trips",
        color=color_column,
        color_continuous_scale=color_scale,
        color_continuous_midpoint=midpoint,
        size_max=26,
        hover_name="station",
        custom_data=["departures", "arrivals", "net_flow", "total_trips"],
        title=title,
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Departures: %{customdata[0]:,}<br>"
            "Arrivals: %{customdata[1]:,}<br>"
            "Net flow: %{customdata[2]:+,}<br>"
            "Total: %{customdata[3]:,} trips"
            "<extra></extra>"
        )
    )

    fig.update_coloraxes(
        colorbar=dict(
            title_text="",
            thickness=9,
            len=0.6,
            x=0.99,
            xanchor="right",
            y=0.5,
            outlinewidth=0,
            tickfont=dict(size=10, color=theme.MUTED),
        )
    )

    return style_map(fig, map_center(profile))
