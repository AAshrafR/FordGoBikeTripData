"""
How long trips last.

There is no clock-time or weekday signal in this dataset — start_time /
end_time are stored as MM:SS.f, not calendar timestamps — so this module only
covers what duration_sec actually supports: how long a trip runs.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboard.figures import theme
from dashboard.figures.theme import empty_figure, style_figure


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
