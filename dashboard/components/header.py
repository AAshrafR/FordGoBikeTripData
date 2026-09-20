"""The sticky bar across the top of the page."""

from __future__ import annotations

from dash import html


def build_header():
    """Brand, page identity and the data window indicator."""

    return html.Header(
        className="top-header",
        children=[
            html.Div(
                className="header-brand",
                children=[
                    html.Div("GB", className="brand-mark"),
                    html.Div(
                        className="brand-text",
                        children=[
                            html.Div("FORD GOBIKE", className="brand-name"),
                            html.Div(
                                "MOBILITY INTELLIGENCE",
                                className="brand-subtitle",
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className="header-center",
                children=[
                    html.Div("MOBILITY CONTROL ROOM", className="header-title"),
                    html.Div(
                        "Urban trip behaviour and rider analytics",
                        className="header-description",
                    ),
                ],
            ),
            html.Div(
                className="header-status",
                children=[
                    html.Div(className="status-dot"),
                    html.Div(
                        children=[
                            html.Div("DATA WINDOW", className="status-label"),
                            html.Div("FEB 2019", className="status-value"),
                        ]
                    ),
                ],
            ),
        ],
    )
