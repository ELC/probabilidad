from typing import Any

import altair as alt
import numpy as np
import pandas as pd
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict, Field

from core import FrequencyTable, Observations, Settings
from core.theme import ChartTheme
from visualization.theme import apply_theme

_ARBITRARY = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class HistogramChartInput(BaseModel):
    model_config = _ARBITRARY

    observations: DataFrame[Observations]
    bin_count: int = Field(default=20, ge=1)
    title: str = "Histograma"
    settings: Settings = Settings()


def chart_histogram(input_data: HistogramChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    chart = (
        alt
        .Chart(input_data.observations)
        .mark_bar(opacity=theme.bar_opacity, color=theme.palette.primary, binSpacing=0)
        .encode(
            x=alt.X("value:Q", bin=alt.Bin(maxbins=input_data.bin_count), title="Valor"),
            y=alt.Y("count()", title="Frecuencia"),
        )
        .properties(title=input_data.title)
    )
    return apply_theme(chart, input_data.settings)


class FrequencyChartInput(BaseModel):
    model_config = _ARBITRARY

    frequency_table: DataFrame[FrequencyTable]
    title: str = "Distribución de frecuencias"
    settings: Settings = Settings()


def _build_frequency_chart(
    frequency_table: DataFrame[FrequencyTable],
    title: str,
    theme: ChartTheme,
) -> Any:
    bars_label = "Frecuencia relativa"
    ogive_label = "Frecuencia rel. acumulada"
    color_scale = alt.Scale(
        domain=[bars_label, ogive_label],
        range=[theme.palette.primary, theme.palette.secondary],
    )
    legend = alt.Legend(title=None, orient="bottom")
    bars_data = frequency_table.assign(series=bars_label, baseline=0.0)
    ogive_data = frequency_table.assign(series=ogive_label)
    bars = (
        alt
        .Chart(bars_data)
        .mark_rect(opacity=theme.bar_opacity)
        .encode(
            x=alt.X("interval_start:Q", title="Valor"),
            x2="interval_end:Q",
            y=alt.Y("relative_frequency:Q", title="Frecuencia relativa"),
            y2="baseline:Q",
            color=alt.Color("series:N", scale=color_scale, legend=legend),
            tooltip=["interval_start", "interval_end", "absolute_frequency", "relative_frequency"],
        )
    )
    ogive = (
        alt
        .Chart(ogive_data)
        .mark_line(strokeWidth=theme.line_stroke_width, point=True)
        .encode(
            x=alt.X("midpoint:Q"),
            y=alt.Y("cumulative_relative_frequency:Q"),
            color=alt.Color("series:N", scale=color_scale, legend=legend),
        )
    )
    return alt.layer(bars, ogive).properties(title=title)


def chart_frequency_table(input_data: FrequencyChartInput) -> alt.Chart:
    chart = _build_frequency_chart(
        input_data.frequency_table,
        input_data.title,
        input_data.settings.chart_theme,
    )
    return apply_theme(chart, input_data.settings)


class StemLeafChartInput(BaseModel):
    model_config = _ARBITRARY

    observations: DataFrame[Observations]
    title: str = "Diagrama de tallo y hoja"
    settings: Settings = Settings()


def chart_stem_leaf(input_data: StemLeafChartInput) -> alt.Chart:
    values = np.floor(input_data.observations["value"].to_numpy() * 10).astype(int)
    source = pd.DataFrame({
        "stem": values // 10,
        "leaf": values % 10,
    }).sort_values(["stem", "leaf"], ignore_index=True)
    source["position"] = source.groupby("stem").cumcount().add(1)
    chart = (
        alt.Chart(source)
        .mark_text(align="left", baseline="middle", dx=-5)
        .encode(
            x=alt.X(
                "position:Q",
                title="",
                axis=alt.Axis(ticks=False, labels=False, grid=False),
            ),
            y=alt.Y("stem:O", title="Tallo", axis=alt.Axis(tickSize=0)),
            text=alt.Text("leaf:O"),
            tooltip=["stem", "leaf"],
        )
        .properties(title=input_data.title, width="container", height=input_data.settings.chart_theme.height)
    )
    return apply_theme(chart, input_data.settings, set_size=False)


class FrequencyPolygonChartInput(BaseModel):
    model_config = _ARBITRARY

    frequency_table: DataFrame[FrequencyTable]
    title: str = "Histograma y polígono de frecuencias"
    settings: Settings = Settings()


def chart_histogram_with_frequency_polygon(input_data: FrequencyPolygonChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    bars = (
        alt.Chart(input_data.frequency_table)
        .mark_rect(opacity=theme.bar_opacity, color=theme.palette.primary)
        .encode(
            x=alt.X("interval_start:Q", title="Minutos de espera"),
            x2="interval_end:Q",
            y=alt.Y("relative_frequency:Q", axis=alt.Axis(format="%"), title="Frecuencia relativa"),
            tooltip=["interval", "absolute_frequency", "relative_frequency"],
        )
    )
    polygon = (
        alt.Chart(input_data.frequency_table)
        .mark_line(point=True, color=theme.palette.secondary, strokeWidth=theme.line_stroke_width)
        .encode(
            x=alt.X("midpoint:Q", title="Minutos de espera"),
            y=alt.Y("relative_frequency:Q", axis=alt.Axis(format="%")),
        )
    )
    chart = alt.layer(bars, polygon).properties(
        title=input_data.title,
        width="container",
        height=theme.height,
    )
    return apply_theme(chart, input_data.settings, set_size=False)


def chart_cumulative_frequency_polygon(input_data: FrequencyPolygonChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    bars = (
        alt.Chart(input_data.frequency_table)
        .mark_rect(opacity=theme.bar_opacity, color=theme.palette.primary)
        .encode(
            x=alt.X("interval_start:Q", title="Minutos de espera"),
            x2="interval_end:Q",
            y=alt.Y("relative_frequency:Q", axis=alt.Axis(format="%"), title="Frecuencia relativa"),
            tooltip=["interval", "cumulative_absolute_frequency", "cumulative_relative_frequency"],
        )
    )
    polygon = (
        alt.Chart(input_data.frequency_table)
        .mark_line(point=True, color=theme.palette.secondary, strokeWidth=theme.line_stroke_width)
        .encode(
            x=alt.X("midpoint:Q", title="Minutos de espera"),
            y=alt.Y("cumulative_relative_frequency:Q", axis=alt.Axis(format="%")),
        )
    )
    chart = alt.layer(bars, polygon).properties(
        title=input_data.title,
        width="container",
        height=theme.height,
    )
    return apply_theme(chart, input_data.settings, set_size=False)
