import altair as alt
import pandas as pd
from pydantic import BaseModel, ConfigDict

from core import Settings
from inference.mean_ci import MeanConfidenceInterval
from visualization.theme import apply_theme

_ARBITRARY = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class ConfidenceIntervalChartInput(BaseModel):
    model_config = _ARBITRARY

    intervals: tuple[MeanConfidenceInterval, ...]
    target_mean: float | None = None
    title: str = "Intervalos de confianza repetidos"
    settings: Settings = Settings()


def chart_confidence_interval(input_data: ConfidenceIntervalChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    records = []
    for index, interval in enumerate(input_data.intervals, start=1):
        contains_target = (
            input_data.target_mean is None or interval.lower_bound <= input_data.target_mean <= interval.upper_bound
        )
        records.append({
            "replicate": index,
            "lower": interval.lower_bound,
            "upper": interval.upper_bound,
            "point": interval.point_estimate,
            "covers": contains_target,
        })
    data = pd.DataFrame.from_records(records)
    bars = (
        alt
        .Chart(data)
        .mark_rule(strokeWidth=2.0)
        .encode(
            x="lower:Q",
            x2="upper:Q",
            y=alt.Y("replicate:O", title="Réplica"),
            color=alt.Color(
                "covers:N",
                scale=alt.Scale(
                    domain=[False, True],
                    range=[theme.palette.danger, theme.palette.primary],
                ),
                legend=alt.Legend(title="Cubre la media", orient="bottom"),
            ),
        )
    )
    points = (
        alt
        .Chart(data)
        .mark_point(filled=True, color=theme.palette.accent, size=theme.point_size)
        .encode(x="point:Q", y="replicate:O")
    )
    layers = [bars, points]
    if input_data.target_mean is not None:
        target_label = "Media verdadera"
        target = (
            alt
            .Chart(pd.DataFrame({"target": [input_data.target_mean], "marca": [target_label]}))
            .mark_rule(strokeDash=[6, 4])
            .encode(
                x="target:Q",
                color=alt.Color(
                    "marca:N",
                    scale=alt.Scale(domain=[target_label], range=[theme.palette.muted]),
                    legend=alt.Legend(title=None, orient="bottom"),
                ),
            )
        )
        layers.append(target)
    layered = alt.layer(*layers).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)
