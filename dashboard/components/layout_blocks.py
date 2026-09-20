"""
Small builders for the repeated pieces of the page.

Sections are a thin label bar and a grid of cards — no explanatory paragraphs.
Each chart carries its own title, which is where a reader looks anyway.
"""

from __future__ import annotations

from dash import dcc, html


# The modebar is clutter the CSS already fades out until hover.
GRAPH_CONFIG = {
    "displayModeBar": False,
    "responsive": True,
    "displaylogo": False,
}

MAP_CONFIG = {
    "displayModeBar": True,
    "modeBarButtonsToRemove": ["lasso2d", "select2d", "toImage"],
    "responsive": True,
    "displaylogo": False,
    "scrollZoom": True,
}


def chart_card(graph_id: str, *, span: int = 1, is_map: bool = False):
    """A graph wrapped in the dashboard's card chrome.

    `span` is how many of the three grid columns the card occupies.
    """

    classes = ["chart-card", f"span-{span}"]

    if is_map:
        classes.append("chart-map")

    return html.Div(
        className=" ".join(classes),
        children=dcc.Graph(
            id=graph_id,
            config=MAP_CONFIG if is_map else GRAPH_CONFIG,
            className="chart-graph",
        ),
    )


def section(label: str, cards):
    """A labelled band of chart cards."""

    return html.Section(
        className="dashboard-section",
        children=[
            html.Div(label, className="section-label"),
            html.Div(className="chart-grid", children=cards),
        ],
    )
