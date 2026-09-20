"""
Figure builders.

Every function here is pure: give it a DataFrame, get a Plotly figure back.
No global state and no Dash imports, which means they can be called from a
notebook or a test as easily as from a callback.
"""

from dashboard.figures.activity import (
    duration_distribution,
    trips_by_hour,
    weekday_hour_heatmap,
)
from dashboard.figures.behavior import (
    age_vs_duration,
    distance_by_user_type,
    duration_by_user_type,
)
from dashboard.figures.geo import station_map
from dashboard.figures.riders import (
    age_distribution,
    gender_mix,
    trips_by_user_type,
)
from dashboard.figures.stations import station_imbalance, top_stations
from dashboard.figures.theme import empty_figure, style_figure, style_map

__all__ = [
    "age_distribution",
    "age_vs_duration",
    "distance_by_user_type",
    "duration_by_user_type",
    "duration_distribution",
    "empty_figure",
    "gender_mix",
    "station_imbalance",
    "station_map",
    "style_figure",
    "style_map",
    "top_stations",
    "trips_by_hour",
    "trips_by_user_type",
    "weekday_hour_heatmap",
]
