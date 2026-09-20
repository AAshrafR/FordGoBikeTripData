"""
Application factory.

Keeping construction in a function means the app can be imported for tests or
served by gunicorn without the module-level side effects that make a Dash app
awkward to reuse.
"""

from __future__ import annotations

import dash

from dashboard.callbacks.dashboard import register_callbacks
from dashboard.datasource.loader import get_trips
from dashboard.layout import build_layout


def create_app() -> dash.Dash:
    """Load the data, build the page and wire the callbacks."""

    df = get_trips()

    app = dash.Dash(
        __name__,
        title="GoBike | Mobility Intelligence",
        update_title=None,
        suppress_callback_exceptions=True,
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ],
    )

    app.layout = build_layout(df)

    register_callbacks(app, df)

    return app
