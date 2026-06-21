import altair as alt
import numpy as np
import pandas as pd
from pydantic import BaseModel, ConfigDict, Field
from scipy import stats

from core import Settings
from sampling.bootstrap import BootstrapMeanResult
from sampling.clt import CLTSimulationResult
from sampling.lln import LLNMultipleTrajectoriesResult, LLNSimulationResult
from visualization.theme import apply_theme

_ARBITRARY = ConfigDict(arbitrary_types_allowed=True, frozen=True)


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
        .mark_bar(opacity=theme.bar_opacity, color=theme.palette.primary, binSpacing=0)
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
    expected_label = "Media teórica"
    expected = (
        alt
        .Chart(pd.DataFrame({"expected_mean": [input_data.lln_result.underlying_mean], "marca": [expected_label]}))
        .mark_rule(strokeDash=[6, 4])
        .encode(
            y="expected_mean:Q",
            color=alt.Color(
                "marca:N",
                scale=alt.Scale(domain=[expected_label], range=[theme.palette.secondary]),
                legend=alt.Legend(title=None, orient="bottom"),
            ),
        )
    )
    layered = alt.layer(running, expected).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)


class LLNMultipleTrajectoriesChartInput(BaseModel):
    model_config = _ARBITRARY

    lln_result: LLNMultipleTrajectoriesResult
    title: str = "Trayectorias de la media acumulada"
    settings: Settings = Settings()


def chart_lln_multiple_trajectories(input_data: LLNMultipleTrajectoriesChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    running_means = input_data.lln_result.running_means
    trajectory_count, horizon = running_means.shape
    step = input_data.lln_result.step
    trajectories = pd.DataFrame({
        "step": np.tile(step, trajectory_count),
        "running_mean": running_means.reshape(-1),
        "trajectory": np.repeat(np.arange(trajectory_count), horizon),
    })
    lines = (
        alt
        .Chart(trajectories)
        .mark_line(opacity=0.45, strokeWidth=1.0, color=theme.palette.primary)
        .encode(
            x=alt.X("step:Q", title="Tamaño de muestra"),
            y=alt.Y("running_mean:Q", title="Media acumulada"),
            detail="trajectory:N",
        )
    )
    expected_label = "Media teórica"
    expected = (
        alt
        .Chart(pd.DataFrame({"expected_mean": [input_data.lln_result.underlying_mean], "marca": [expected_label]}))
        .mark_rule(strokeDash=[6, 4], strokeWidth=2.0)
        .encode(
            y="expected_mean:Q",
            color=alt.Color(
                "marca:N",
                scale=alt.Scale(domain=[expected_label], range=[theme.palette.accent]),
                legend=alt.Legend(title=None, orient="bottom"),
            ),
        )
    )
    layered = alt.layer(lines, expected).properties(title=input_data.title)
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
        .mark_bar(opacity=theme.bar_opacity, color=theme.palette.primary, binSpacing=0)
        .encode(
            x=alt.X("bootstrap_mean:Q", bin=alt.Bin(maxbins=input_data.bin_count), title="Media bootstrap"),
            y=alt.Y("count()", title="Frecuencia"),
        )
    )
    lower_label = "Cuantil inferior"
    upper_label = "Cuantil superior"
    point_label = "Estimación puntual"
    bounds = pd.DataFrame({
        "boundary": [lower_label, upper_label, point_label],
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
                scale=alt.Scale(
                    domain=[lower_label, upper_label, point_label],
                    range=[theme.palette.secondary, theme.palette.secondary, theme.palette.accent],
                ),
                legend=alt.Legend(title=None, orient="bottom"),
            ),
        )
    )
    layered = alt.layer(histogram, rules).properties(title=input_data.title)
    return apply_theme(layered, input_data.settings)
