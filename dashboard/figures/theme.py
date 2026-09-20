"""
One visual language for every figure.

The palette lives here rather than in a config file because it is purely a
rendering concern — Plotly can't read CSS custom properties, so these values
mirror the tokens at the top of assets/style.css. Change a colour in one place
and change it in the other.

Sizing is tuned for a three-across grid: the cards are roughly 360px wide, so
titles, ticks and margins are smaller than Plotly's defaults.
"""

from __future__ import annotations

import plotly.graph_objects as go


# ------------------------------------------------------------------
# Palette
# ------------------------------------------------------------------

INK = "#0d1714"
INK_SOFT = "#22332d"
MUTED = "#5c7068"
GRID = "rgba(13, 23, 20, 0.07)"
AXIS_LINE = "rgba(13, 23, 20, 0.12)"

ACCENT = "#10b981"
ACCENT_DEEP = "#047857"
ACCENT_SOFT = "rgba(16, 185, 129, 0.14)"
CONTRAST = "#f59e0b"
CONTRAST_DEEP = "#b45309"

CATEGORICAL = [ACCENT, INK, CONTRAST, "#0f766e", "#94a3a0", CONTRAST_DEEP]
SEQUENTIAL = ["#e3f2ec", "#9fdcc4", "#4ec09a", ACCENT, ACCENT_DEEP, "#03372a"]

# Zero is meaningful for net flow, so the ramp diverges around it:
# amber = the station loses bikes, emerald = the station gains them.
DIVERGING = [CONTRAST_DEEP, CONTRAST, "#f2f5f3", "#4ec09a", ACCENT_DEEP]

FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif"


# ------------------------------------------------------------------
# Map
# ------------------------------------------------------------------

# carto-positron needs no Mapbox token, which keeps the app credential-free.
MAP_STYLE = "carto-positron"
MAP_ZOOM = 11.6
MAP_HEIGHT = 470

# Plotly renamed the map traces in 5.24; the mapbox-prefixed names still work
# but are deprecated. Detect once here so the figure code doesn't care.
HAS_MODERN_MAPS = hasattr(go, "Scattermap")
MAP_LAYOUT_KEY = "map" if HAS_MODERN_MAPS else "mapbox"
ScatterMapTrace = go.Scattermap if HAS_MODERN_MAPS else go.Scattermapbox


# ------------------------------------------------------------------
# Sampling and limits
# ------------------------------------------------------------------

SCATTER_SAMPLE_SIZE = 5000
TOP_STATIONS = 10

# Station names run long and the cards are narrow.
LABEL_MAX_CHARS = 26


def shorten(label: str) -> str:
    """Trim a long category label so it fits the y axis of a narrow card."""

    label = str(label)

    if len(label) <= LABEL_MAX_CHARS:
        return label

    return label[: LABEL_MAX_CHARS - 1].rstrip() + "…"


# ------------------------------------------------------------------
# Styling
# ------------------------------------------------------------------

def style_figure(fig: go.Figure, *, show_grid: bool = True) -> go.Figure:
    """Apply the dashboard look to a cartesian figure."""

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=CATEGORICAL,
        font=dict(family=FONT_FAMILY, size=11, color=INK_SOFT),
        title=dict(
            font=dict(size=13, color=INK),
            x=0.01,
            xanchor="left",
            y=0.965,
            yanchor="top",
        ),
        margin=dict(l=46, r=18, t=52, b=38),
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor=ACCENT,
            font=dict(family=FONT_FAMILY, size=11, color=INK),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.0,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=10, color=MUTED),
            title_text="",
        ),
    )

    axis = dict(
        showgrid=show_grid,
        gridcolor=GRID,
        zeroline=False,
        linecolor=AXIS_LINE,
        tickfont=dict(size=10, color=MUTED),
        title_font=dict(size=10, color=MUTED),
    )

    fig.update_xaxes(**axis)
    fig.update_yaxes(**axis)

    return fig


def style_map(fig: go.Figure, center: dict, zoom: float = MAP_ZOOM) -> go.Figure:
    """Apply the dashboard look to a map figure."""

    fig.update_layout(
        **{MAP_LAYOUT_KEY: dict(style=MAP_STYLE, center=center, zoom=zoom)},
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_FAMILY, size=11, color=INK_SOFT),
        title=dict(
            font=dict(size=13, color=INK),
            x=0.01,
            xanchor="left",
            y=0.97,
            yanchor="top",
        ),
        margin=dict(l=6, r=6, t=48, b=6),
        height=MAP_HEIGHT,
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor=ACCENT,
            font=dict(family=FONT_FAMILY, size=11, color=INK),
        ),
    )

    return fig


def empty_figure(message: str = "No trips match the current filters.") -> go.Figure:
    """A blank canvas carrying an explanation.

    Returned whenever a filter combination selects nothing, so the user sees
    why the chart is empty instead of an axis with no data on it.
    """

    fig = go.Figure()

    fig.add_annotation(
        text=message,
        showarrow=False,
        font=dict(family=FONT_FAMILY, size=12, color=MUTED),
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=16, r=16, t=36, b=16),
    )

    return fig
