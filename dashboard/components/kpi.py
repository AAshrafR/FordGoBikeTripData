"""
The headline numbers.

Each card is declared once here as (id, label, caption) and rendered in order,
so adding a metric is a one-line change plus an Output on the callback.
"""

from __future__ import annotations

from dash import html


KPI_CARDS = [
    ("kpi-trips", "TOTAL TRIPS", "Trips in the current selection", True),
    ("kpi-duration", "MEDIAN TRIP", "Minutes per trip", False),
    ("kpi-distance", "MEDIAN DISTANCE", "Straight-line kilometres", False),
    ("kpi-stations", "ACTIVE STATIONS", "Docks with traffic", False),
    ("kpi-age", "MEDIAN AGE", "Years", False),
]


def build_kpi_grid():
    """Render the KPI row. Values are filled in by the dashboard callback."""

    return html.Div(
        className="kpi-grid",
        children=[
            html.Div(
                className="kpi-card kpi-highlight" if highlight else "kpi-card",
                children=[
                    html.Div(label, className="kpi-label"),
                    html.Div(id=card_id, className="kpi-value", children="—"),
                    html.Div(caption, className="kpi-foot"),
                ],
            )
            for card_id, label, caption, highlight in KPI_CARDS
        ],
    )
