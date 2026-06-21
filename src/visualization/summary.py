from typing import Any

import altair as alt
import pandas as pd
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from core import FrequencyTable, Observations, Settings
from core.theme import ChartTheme
from descriptive.summary import DescriptiveStatistics, summarize_observations
from visualization.frequency import _build_frequency_chart
from visualization.theme import apply_theme

_ARBITRARY = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class DescriptiveSummaryChartInput(BaseModel):
    model_config = _ARBITRARY

    observations: DataFrame[Observations]
    statistics: DescriptiveStatistics
    title: str = "Boxplot con marcas de resumen"
    settings: Settings = Settings()
    apply_theme: bool = True


class BoxplotExampleChartInput(BaseModel):
    model_config = _ARBITRARY

    values: tuple[float, ...]
    title: str = ""
    settings: Settings = Settings()
    apply_theme: bool = True


def _build_descriptive_summary_chart(
    observations: DataFrame[Observations],
    statistics: DescriptiveStatistics,
    title: str,
    theme: ChartTheme,
) -> Any:
    box = (
        alt
        .Chart(observations)
        .mark_boxplot(extent=1.5, color=theme.palette.primary, size=40)
        .encode(x=alt.X("value:Q", title="Valor"))
    )
    mean_label = "Media muestral"
    mean_mark = (
        alt
        .Chart(pd.DataFrame({"mean": [statistics.location.mean], "marca": [mean_label]}))
        .mark_rule(strokeWidth=theme.line_stroke_width, strokeDash=[4, 4])
        .encode(
            x="mean:Q",
            color=alt.Color(
                "marca:N",
                scale=alt.Scale(domain=[mean_label], range=[theme.palette.accent]),
                legend=alt.Legend(title=None, orient="bottom"),
            ),
        )
    )
    return alt.layer(box, mean_mark).properties(title=title)


def chart_descriptive_summary(input_data: DescriptiveSummaryChartInput) -> alt.Chart:
    chart = _build_descriptive_summary_chart(
        input_data.observations,
        input_data.statistics,
        input_data.title,
        input_data.settings.chart_theme,
    )
    if input_data.apply_theme:
        return apply_theme(chart, input_data.settings)
    return chart


def chart_boxplot_example(input_data: BoxplotExampleChartInput) -> alt.Chart:
    observations = pd.DataFrame({"value": input_data.values}).pipe(DataFrame[Observations])
    statistics = summarize_observations(observations)
    chart_input = DescriptiveSummaryChartInput(
        observations=observations,
        statistics=statistics,
        title=input_data.title,
        settings=input_data.settings,
        apply_theme=input_data.apply_theme,
    )
    return chart_descriptive_summary(chart_input)


class TypicalValuesComparisonChartInput(BaseModel):
    model_config = _ARBITRARY

    original_statistics: DescriptiveStatistics
    comparison_statistics: DescriptiveStatistics
    original_label: str = "Muestra original"
    comparison_label: str = "Con observación extrema"
    title: str = "Media y mediana ante una observación extrema"
    settings: Settings = Settings()


def _build_typical_values_comparison_data(input_data: TypicalValuesComparisonChartInput) -> pd.DataFrame:
    original = input_data.original_statistics.location
    comparison = input_data.comparison_statistics.location
    return pd.DataFrame({
        "scenario": [
            input_data.original_label,
            input_data.original_label,
            input_data.comparison_label,
            input_data.comparison_label,
        ],
        "measure": ["Media", "Mediana", "Media", "Mediana"],
        "value": [original.mean, original.median, comparison.mean, comparison.median],
    })


def chart_typical_values_comparison(input_data: TypicalValuesComparisonChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    data = _build_typical_values_comparison_data(input_data)
    scenario_order = [input_data.original_label, input_data.comparison_label]
    measure_order = ["Media", "Mediana"]
    color = alt.Color(
        "measure:N",
        scale=alt.Scale(domain=measure_order, range=[theme.palette.accent, theme.palette.primary]),
        legend=alt.Legend(title=None, orient="bottom"),
    )
    lines = (
        alt
        .Chart(data)
        .mark_line(strokeWidth=theme.line_stroke_width)
        .encode(
            x=alt.X("scenario:N", sort=scenario_order, title="Muestra"),
            y=alt.Y("value:Q", title="Minutos"),
            color=color,
            detail="measure:N",
        )
    )
    points = (
        alt
        .Chart(data)
        .mark_point(filled=True, size=theme.point_size)
        .encode(
            x=alt.X("scenario:N", sort=scenario_order, title="Muestra"),
            y=alt.Y("value:Q", title="Minutos"),
            color=color,
            shape=alt.Shape("measure:N", sort=measure_order, legend=None),
            tooltip=[
                alt.Tooltip("scenario:N", title="Muestra"),
                alt.Tooltip("measure:N", title="Medida"),
                alt.Tooltip("value:Q", title="Minutos", format=".2f"),
            ],
        )
    )
    layered = alt.layer(lines, points).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)


class ObservationsOverviewInput(BaseModel):
    model_config = _ARBITRARY

    observations: DataFrame[Observations]
    frequency_table: DataFrame[FrequencyTable]
    statistics: DescriptiveStatistics
    frequency_title: str = "Distribución de frecuencias"
    summary_title: str = "Boxplot con marcas de resumen"
    settings: Settings = Settings()


def chart_observations_overview(input_data: ObservationsOverviewInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    histogram = _build_frequency_chart(
        input_data.frequency_table,
        input_data.frequency_title,
        theme,
    ).properties(width=theme.width, height=theme.height)
    boxplot = _build_descriptive_summary_chart(
        input_data.observations,
        input_data.statistics,
        input_data.summary_title,
        theme,
    ).properties(width=theme.width, height=120)
    composed = alt.vconcat(histogram, boxplot, spacing=10).resolve_scale(x="shared")
    return apply_theme(composed, input_data.settings, set_size=False)
