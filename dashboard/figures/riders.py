"""Who rides: membership, gender and age."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboard.figures import theme
from dashboard.figures.theme import empty_figure, style_figure


def trips_by_user_type(df: pd.DataFrame) -> go.Figure:
    """Subscribers versus casual customers, as a share of all trips."""

    if "user_type" not in df.columns or df.empty:
        return empty_figure()

    counts = (
        df["user_type"].astype(str).value_counts()
        .rename_axis("user_type").reset_index(name="trips")
    )

    counts["share"] = counts["trips"] / counts["trips"].sum()

    fig = px.bar(
        counts,
        x="user_type",
        y="trips",
        title="Trips by user type",
        labels={"user_type": "", "trips": ""},
        text=counts["share"].map(lambda value: f"{value:.0%}"),
    )

    fig.update_traces(
        marker_color=theme.ACCENT,
        marker_line_width=0,
        textposition="outside",
        textfont=dict(size=11, color=theme.MUTED),
        hovertemplate="<b>%{x}</b><br>%{y:,} trips<extra></extra>",
        cliponaxis=False,
    )

    return style_figure(fig)


def gender_mix(df: pd.DataFrame) -> go.Figure:
    """Rider gender split."""

    if "member_gender" not in df.columns or df.empty:
        return empty_figure()

    counts = (
        df["member_gender"].astype(str).value_counts()
        .rename_axis("gender").reset_index(name="trips")
    )

    fig = px.pie(
        counts,
        names="gender",
        values="trips",
        hole=0.68,
        title="Gender mix",
        color_discrete_sequence=theme.CATEGORICAL,
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        textfont=dict(size=11, color="#ffffff"),
        marker=dict(line=dict(color="#ffffff", width=2)),
        hovertemplate="<b>%{label}</b><br>%{value:,} trips<extra></extra>",
    )

    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", y=-0.05, x=0.5, xanchor="center"),
    )

    # The donut hole is wasted space otherwise; the total belongs there.
    fig.add_annotation(
        text=f"<b>{counts['trips'].sum():,}</b>",
        showarrow=False,
        font=dict(size=17, color=theme.INK, family=theme.FONT_FAMILY),
        x=0.5,
        y=0.5,
    )

    return style_figure(fig)


def age_distribution(df: pd.DataFrame) -> go.Figure:
    """Age profile, split by membership type.

    Ages above 80 are almost certainly placeholder birth years rather than real
    octogenarian commuters, so the axis stops there and the title says so.
    """

    if "member_age" not in df.columns or df.empty:
        return empty_figure()

    ages = df[df["member_age"].between(16, 80)]

    if ages.empty:
        return empty_figure()

    fig = px.histogram(
        ages,
        x="member_age",
        color="user_type" if "user_type" in ages.columns else None,
        nbins=30,
        barmode="overlay",
        opacity=0.72,
        title="Rider age (16–80)",
        labels={"member_age": "", "user_type": ""},
        color_discrete_sequence=theme.CATEGORICAL,
    )

    fig.update_traces(
        marker_line_width=0,
        hovertemplate="Age %{x}<br>%{y:,} trips<extra></extra>",
    )

    fig.update_yaxes(title_text="")

    return style_figure(fig)
