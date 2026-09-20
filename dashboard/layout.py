"""
Page assembly.

The whole document is put together here from the component builders, so the
shape of the dashboard is readable in one screen instead of buried in six
hundred lines of nested html.Div calls.

The grid is three columns wide; cards declare how many they span.
"""

from __future__ import annotations

import pandas as pd
from dash import html

from dashboard.components.footer import build_footer
from dashboard.components.header import build_header
from dashboard.components.kpi import build_kpi_grid
from dashboard.components.layout_blocks import chart_card, section
from dashboard.components.sidebar import build_sidebar
from dashboard.datasource.geo import has_coordinates


def _page_intro():
    """Title block at the top of the main column."""

    return html.Div(
        className="page-intro",
        children=[
            html.Div(
                className="page-intro-left",
                children=[
                    html.H1("GoBike Analytics", className="page-title"),
                    html.Div(
                        "Trip activity, rider composition and station flow",
                        className="page-description",
                    ),
                ],
            ),
            html.Div("FEB 2019", className="period-badge"),
        ],
    )


def _sections(show_map: bool):
    """The analytical bands, in reading order.

    Three cards fill a row. When the dataset has no coordinates the map and the
    two charts derived from it are dropped, and the remaining cards close the
    gap on their own — the grid does not need to be re-specified.
    """

    geography = (
        [section("GEOGRAPHY", [chart_card("station-map", span=3, is_map=True)])]
        if show_map
        else []
    )

    station_cards = [
        chart_card("top-start-stations"),
        chart_card("top-end-stations"),
    ]

    # Reads station coordinates, so it follows the map.
    if show_map:
        station_cards.append(chart_card("station-imbalance"))

    return [
        section(
            "RIDERS",
            [
                chart_card("user-type-chart"),
                chart_card("gender-chart"),
                chart_card("age-distribution"),
            ],
        ),
        section(
            "TRIP DURATION",
            [
                chart_card("duration-distribution"),
                chart_card("duration-by-user", span=2),
            ],
        ),
        *geography,
        section("STATIONS", station_cards),
        section(
            "TRIP BEHAVIOUR",
            [
                chart_card("age-duration-scatter", span=3 if not show_map else 2),
            ]
            + ([chart_card("distance-by-user")] if show_map else []),
        ),
    ]


def build_layout(df: pd.DataFrame):
    """Build the complete page for a given dataset."""

    show_map = has_coordinates(df)

    return html.Div(
        className="app-container",
        children=[
            build_header(),
            html.Div(
                className="dashboard-body",
                children=[
                    build_sidebar(df),
                    html.Main(
                        className="main-content",
                        children=[
                            _page_intro(),
                            build_kpi_grid(),
                            *_sections(show_map),
                        ],
                    ),
                ],
            ),
            build_footer(),
        ],
    )
