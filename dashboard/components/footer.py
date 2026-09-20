"""The closing strip of the page."""

from __future__ import annotations

from dash import html


def build_footer():
    return html.Footer(
        className="footer",
        children=[
            html.Span("FORD GOBIKE / MOBILITY INTELLIGENCE"),
            html.Span("FEBRUARY 2019"),
        ],
    )
