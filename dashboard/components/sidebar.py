"""
The filter rail.

Every control lives here and feeds the single dashboard callback. Age groups
are hard-coded rather than read from the data so the order stays chronological
instead of alphabetical.
"""

from __future__ import annotations

import pandas as pd
from dash import dcc, html

from dashboard.datasource.loader import dropdown_options


AGE_GROUPS = [
    ("Under 18", "Under 18"),
    ("18–24", "18-24"),
    ("25–34", "25-34"),
    ("35–44", "35-44"),
    ("45–54", "45-54"),
    ("55–64", "55-64"),
    ("65+", "65+"),
]


def _filter_block(label: str, control):
    """Label plus control, spaced consistently down the rail."""

    return html.Div(
        className="sidebar-filter",
        children=[
            html.Label(label, className="sidebar-filter-label"),
            control,
        ],
    )


def build_sidebar(df: pd.DataFrame):
    """Assemble the filter rail from the values present in the data."""

    return html.Aside(
        className="sidebar",
        children=[
            html.Div(
                className="sidebar-header",
                children=[
                    html.Div("EXPLORE", className="sidebar-eyebrow"),
                    html.H2("Rider filters", className="sidebar-title"),
                ],
            ),

            _filter_block(
                "USER TYPE",
                dcc.Dropdown(
                    id="user-type-filter",
                    options=dropdown_options(df, "user_type"),
                    placeholder="All user types",
                    clearable=True,
                    className="sidebar-dropdown",
                ),
            ),

            _filter_block(
                "GENDER",
                dcc.Dropdown(
                    id="gender-filter",
                    options=dropdown_options(df, "member_gender"),
                    placeholder="All genders",
                    clearable=True,
                    className="sidebar-dropdown",
                ),
            ),

            _filter_block(
                "AGE GROUP",
                dcc.Dropdown(
                    id="age-group-filter",
                    options=[
                        {"label": label, "value": value}
                        for label, value in AGE_GROUPS
                    ],
                    placeholder="All age groups",
                    clearable=True,
                    className="sidebar-dropdown",
                ),
            ),

            html.Div(className="sidebar-divider"),

            _filter_block(
                "MAP VIEW",
                dcc.RadioItems(
                    id="map-metric",
                    options=[
                        {"label": "Trip volume", "value": "volume"},
                        {"label": "Net bike flow", "value": "net_flow"},
                    ],
                    value="volume",
                    className="sidebar-radio",
                    inputClassName="sidebar-radio-input",
                    labelClassName="sidebar-radio-label",
                ),
            ),

            html.Div(className="sidebar-divider"),

            html.Div(
                className="sidebar-dataset",
                children=[
                    html.Div("DATASET", className="sidebar-dataset-label"),
                    html.Div("Ford GoBike", className="sidebar-dataset-title"),
                    html.Div(
                        [
                            "February 2019",
                            html.Br(),
                            "San Francisco Bay Area",
                            html.Br(),
                            f"{len(df):,} trips",
                        ],
                        className="sidebar-dataset-meta",
                    ),
                ],
            ),

            html.Div(
                className="sidebar-footer",
                children=[
                    html.Span("FILTERS"),
                    html.Span([html.Span(className="ready-dot"), " READY"]),
                ],
            ),
        ],
    )
