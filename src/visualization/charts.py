import altair as alt
import numpy as np
import pandas as pd
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict, Field
from scipy import stats

from core import FrequencyTable, Observations, Settings
from descriptive.summary import DescriptiveStatistics
from distributions.evaluations import DensityGrid, ProbabilityMassTable
from inference.mean_ci import MeanConfidenceInterval
from sampling.bootstrap import BootstrapMeanResult
from sampling.clt import CLTSimulationResult
from sampling.lln import LLNSimulationResult
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
        .mark_bar(opacity=theme.bar_opacity, color=theme.palette.primary)
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


def chart_frequency_table(input_data: FrequencyChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    base = alt.Chart(input_data.frequency_table)
    bars = base.mark_bar(opacity=theme.bar_opacity, color=theme.palette.primary).encode(
        x=alt.X("midpoint:Q", title="Marca de clase"),
        y=alt.Y("absolute_frequency:Q", title="Frecuencia absoluta"),
        tooltip=["interval_start", "interval_end", "absolute_frequency", "relative_frequency"],
    )
    ogive = base.mark_line(color=theme.palette.secondary, strokeWidth=theme.line_stroke_width).encode(
        x=alt.X("midpoint:Q"),
        y=alt.Y(
            "cumulative_relative_frequency:Q",
            axis=alt.Axis(title="Frecuencia rel. acumulada", titleColor=theme.palette.secondary),
        ),
    )
    layered = alt.layer(bars, ogive).resolve_scale(y="independent").properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)


class DensityChartInput(BaseModel):
    model_config = _ARBITRARY

    density_grid: DensityGrid
    title: str | None = None
    settings: Settings = Settings()


def chart_density(input_data: DensityChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    data = pd.DataFrame({"x": input_data.density_grid.grid, "density": input_data.density_grid.density})
    title = input_data.title or f"Densidad — {input_data.density_grid.distribution_name}"
    chart = (
        alt
        .Chart(data)
        .mark_line(color=theme.palette.primary, strokeWidth=theme.line_stroke_width)
        .encode(
            x=alt.X("x:Q", title="x"),
            y=alt.Y("density:Q", title="f(x)"),
        )
        .properties(title=title)
    )
    return apply_theme(chart, input_data.settings)


class ProbabilityMassChartInput(BaseModel):
    model_config = _ARBITRARY

    probability_mass: ProbabilityMassTable
    title: str | None = None
    settings: Settings = Settings()


def chart_probability_mass(input_data: ProbabilityMassChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    title = input_data.title or f"Masa de probabilidad — {input_data.probability_mass.distribution_name}"
    chart = (
        alt
        .Chart(input_data.probability_mass.table)
        .mark_bar(opacity=theme.bar_opacity, color=theme.palette.primary)
        .encode(
            x=alt.X("outcome:O", title="Resultado"),
            y=alt.Y("probability:Q", title="P(X = x)"),
            tooltip=["outcome", "probability"],
        )
        .properties(title=title)
    )
    return apply_theme(chart, input_data.settings)


class CLTComparisonChartInput(BaseModel):
    model_config = _ARBITRARY

    clt_result: CLTSimulationResult
    bin_count: int = Field(default=40, ge=5)
    title: str = "Medias estandarizadas vs. Normal(0,1)"
    settings: Settings = Settings()


def chart_clt_comparison(input_data: CLTComparisonChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    data = pd.DataFrame({"standardized_mean": input_data.clt_result.standardized_means})
    histogram = (
        alt
        .Chart(data)
        .mark_bar(opacity=theme.bar_opacity, color=theme.palette.primary)
        .encode(
            x=alt.X("standardized_mean:Q", bin=alt.Bin(maxbins=input_data.bin_count), title="Media estandarizada"),
            y=alt.Y("count()", stack=None, title="Frecuencia"),
        )
    )
    grid = np.linspace(-4.0, 4.0, input_data.settings.grid_resolution)
    bin_width = 8.0 / input_data.bin_count
    expected_count = stats.norm.pdf(grid) * input_data.clt_result.standardized_means.size * bin_width
    overlay_data = pd.DataFrame({"x": grid, "y": expected_count})
    overlay = (
        alt
        .Chart(overlay_data)
        .mark_line(color=theme.palette.secondary, strokeWidth=theme.line_stroke_width)
        .encode(x="x:Q", y="y:Q")
    )
    layered = alt.layer(histogram, overlay).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)


class LLNChartInput(BaseModel):
    model_config = _ARBITRARY

    lln_result: LLNSimulationResult
    title: str = "Ley de los grandes números"
    settings: Settings = Settings()


def chart_lln_running_mean(input_data: LLNChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    data = pd.DataFrame({"step": input_data.lln_result.step, "running_mean": input_data.lln_result.running_mean})
    running = (
        alt
        .Chart(data)
        .mark_line(color=theme.palette.primary, strokeWidth=theme.line_stroke_width)
        .encode(x=alt.X("step:Q", title="Tamaño de muestra"), y=alt.Y("running_mean:Q", title="Media acumulada"))
    )
    expected = (
        alt
        .Chart(pd.DataFrame({"expected_mean": [input_data.lln_result.underlying_mean]}))
        .mark_rule(color=theme.palette.secondary, strokeDash=[6, 4])
        .encode(y="expected_mean:Q")
    )
    layered = alt.layer(running, expected).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)


class BootstrapDistributionChartInput(BaseModel):
    model_config = _ARBITRARY

    bootstrap_result: BootstrapMeanResult
    bin_count: int = Field(default=40, ge=5)
    title: str = "Distribución bootstrap de la media"
    settings: Settings = Settings()


def chart_bootstrap_distribution(input_data: BootstrapDistributionChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    data = pd.DataFrame({"bootstrap_mean": input_data.bootstrap_result.bootstrap_means})
    histogram = (
        alt
        .Chart(data)
        .mark_bar(opacity=theme.bar_opacity, color=theme.palette.primary)
        .encode(
            x=alt.X("bootstrap_mean:Q", bin=alt.Bin(maxbins=input_data.bin_count), title="Media bootstrap"),
            y=alt.Y("count()", title="Frecuencia"),
        )
    )
    bounds = pd.DataFrame({
        "boundary": ["lower", "upper", "point"],
        "value": [
            input_data.bootstrap_result.lower_quantile,
            input_data.bootstrap_result.upper_quantile,
            input_data.bootstrap_result.point_estimate,
        ],
    })
    rules = (
        alt
        .Chart(bounds)
        .mark_rule(strokeWidth=2.0)
        .encode(
            x="value:Q",
            color=alt.Color(
                "boundary:N",
                scale=alt.Scale(range=[theme.palette.secondary, theme.palette.secondary, theme.palette.accent]),
            ),
        )
    )
    layered = alt.layer(histogram, rules).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)


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
            color=alt.Color("covers:N", scale=alt.Scale(range=[theme.palette.danger, theme.palette.primary])),
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
        target = (
            alt
            .Chart(pd.DataFrame({"target": [input_data.target_mean]}))
            .mark_rule(color=theme.palette.muted, strokeDash=[6, 4])
            .encode(x="target:Q")
        )
        layers.append(target)
    layered = alt.layer(*layers).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)


class DescriptiveSummaryChartInput(BaseModel):
    model_config = _ARBITRARY

    observations: DataFrame[Observations]
    statistics: DescriptiveStatistics
    title: str = "Boxplot con marcas de resumen"
    settings: Settings = Settings()


def chart_descriptive_summary(input_data: DescriptiveSummaryChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    box = (
        alt
        .Chart(input_data.observations)
        .mark_boxplot(extent=1.5, color=theme.palette.primary, size=40)
        .encode(x=alt.X("value:Q", title="Valor"))
    )
    mean_mark = (
        alt
        .Chart(pd.DataFrame({"mean": [input_data.statistics.location.mean]}))
        .mark_rule(color=theme.palette.accent, strokeWidth=theme.line_stroke_width, strokeDash=[4, 4])
        .encode(x="mean:Q")
    )
    layered = alt.layer(box, mean_mark).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)
