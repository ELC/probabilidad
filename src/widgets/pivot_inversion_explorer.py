from enum import StrEnum
from typing import Any

import altair as alt
import ipywidgets as widgets
import numpy as np
import pandas as pd
from IPython.display import display
from pydantic import BaseModel, ConfigDict, Field
from scipy import stats

from core import Settings
from inference import (
    MeanKnownVarianceInput,
    MeanUnknownVarianceInput,
    VarianceInput,
    build_confidence_interval_for_mean_known_variance,
    build_confidence_interval_for_mean_unknown_variance,
    build_confidence_interval_for_variance,
)
from visualization.theme import apply_theme


class PivotCase(StrEnum):
    NORMAL = "Normal (σ conocido)"
    STUDENT_T = "t de Student"
    CHI_SQUARED = "χ² (varianza)"


class PivotInversionExplorerInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    settings: Settings = Settings()
    sample_mean: float = 12.0
    sample_standard_deviation: float = Field(default=3.0, gt=0.0)


def _reference_distribution(case: PivotCase, sample_size: int) -> Any:
    if case is PivotCase.NORMAL:
        return stats.norm()
    if case is PivotCase.STUDENT_T:
        return stats.t(df=sample_size - 1)
    return stats.chi2(df=sample_size - 1)


def _pivot_axis_label(case: PivotCase) -> str:
    if case is PivotCase.NORMAL:
        return "Pivote Z"
    if case is PivotCase.STUDENT_T:
        return "Pivote T"
    return "Pivote χ²"


def _pivot_grid(case: PivotCase, distribution: Any, quantile_low: float, quantile_high: float) -> np.ndarray:
    if case is PivotCase.CHI_SQUARED:
        upper = max(quantile_high * 1.15, distribution.ppf(0.999))
        return np.linspace(0.0, upper, 401)
    span = max(abs(quantile_low), abs(quantile_high)) + 1.5
    return np.linspace(-span, span, 401)


def _build_pivot_chart(
    case: PivotCase,
    sample_size: int,
    confidence_level: float,
    settings: Settings,
) -> tuple[alt.LayerChart, float, float]:
    distribution = _reference_distribution(case, sample_size)
    tail = (1.0 - confidence_level) / 2.0
    quantile_low = float(distribution.ppf(tail))
    quantile_high = float(distribution.isf(tail))
    grid = _pivot_grid(case, distribution, quantile_low, quantile_high)
    density = pd.DataFrame({"q": grid, "density": distribution.pdf(grid)})
    inside = density[(density["q"] >= quantile_low) & (density["q"] <= quantile_high)]
    theme = settings.chart_theme
    line = (
        alt.Chart(density)
        .mark_line(color=theme.palette.primary, strokeWidth=theme.line_stroke_width)
        .encode(x=alt.X("q:Q", title=_pivot_axis_label(case)), y=alt.Y("density:Q", title="f(q)"))
    )
    area = (
        alt.Chart(inside)
        .mark_area(opacity=theme.band_opacity, color=theme.palette.primary)
        .encode(x="q:Q", y="density:Q")
    )
    rules = (
        alt.Chart(pd.DataFrame({"q": [quantile_low, quantile_high]}))
        .mark_rule(color=theme.palette.secondary, strokeWidth=2.0)
        .encode(x="q:Q")
    )
    chart = alt.layer(area, line, rules).properties(
        title=f"Espacio del pivote · masa central {confidence_level:.0%}",
        width=theme.width // 2,
        height=theme.height,
    )
    return chart, quantile_low, quantile_high


def _bounds_for_case(
    case: PivotCase,
    input_data: PivotInversionExplorerInput,
    sample_size: int,
    confidence_level: float,
) -> tuple[float, float, float, str]:
    if case is PivotCase.NORMAL:
        interval = build_confidence_interval_for_mean_known_variance(
            MeanKnownVarianceInput(
                sample_mean=input_data.sample_mean,
                population_standard_deviation=input_data.sample_standard_deviation,
                sample_size=sample_size,
                confidence_level=confidence_level,
            )
        )
        return interval.lower_bound, interval.upper_bound, interval.point_estimate, "μ"
    if case is PivotCase.STUDENT_T:
        interval_t = build_confidence_interval_for_mean_unknown_variance(
            MeanUnknownVarianceInput(
                sample_mean=input_data.sample_mean,
                sample_standard_deviation=input_data.sample_standard_deviation,
                sample_size=sample_size,
                confidence_level=confidence_level,
            )
        )
        return interval_t.lower_bound, interval_t.upper_bound, interval_t.point_estimate, "μ"
    interval_var = build_confidence_interval_for_variance(
        VarianceInput(
            sample_variance=input_data.sample_standard_deviation**2,
            sample_size=sample_size,
            confidence_level=confidence_level,
        )
    )
    return interval_var.lower_bound, interval_var.upper_bound, interval_var.point_estimate, "σ²"


def _build_parameter_chart(
    lower_bound: float,
    upper_bound: float,
    point_estimate: float,
    parameter_label: str,
    settings: Settings,
) -> alt.LayerChart:
    theme = settings.chart_theme
    span = max(upper_bound - lower_bound, 1e-6)
    margin = span * 0.35
    domain = [lower_bound - margin, upper_bound + margin]
    bracket = (
        alt.Chart(pd.DataFrame({"lower": [lower_bound], "upper": [upper_bound], "y": [1.0]}))
        .mark_rule(color=theme.palette.primary, strokeWidth=6.0)
        .encode(x=alt.X("lower:Q", scale=alt.Scale(domain=domain), title=parameter_label), x2="upper:Q", y="y:Q")
    )
    point = (
        alt.Chart(pd.DataFrame({"value": [point_estimate], "y": [1.0]}))
        .mark_point(filled=True, color=theme.palette.accent, size=theme.point_size * 1.5)
        .encode(x="value:Q", y="y:Q")
    )
    bounds_marks = (
        alt.Chart(pd.DataFrame({"value": [lower_bound, upper_bound]}))
        .mark_rule(color=theme.palette.secondary, strokeWidth=2.0)
        .encode(x="value:Q")
    )
    chart = alt.layer(bracket, bounds_marks, point).properties(
        title=f"Espacio de {parameter_label} · IC tras invertir el pivote",
        width=theme.width // 2,
        height=theme.height,
    )
    return chart


def build_pivot_inversion_explorer(input_data: PivotInversionExplorerInput) -> widgets.Widget:
    case_dropdown = widgets.Dropdown(
        options=[case.value for case in PivotCase],
        value=PivotCase.NORMAL.value,
        description="Pivote",
    )
    confidence_slider = widgets.FloatSlider(min=0.80, max=0.99, step=0.01, value=0.95, description="1-α")
    sample_slider = widgets.IntSlider(min=5, max=200, step=1, value=36, description="n")
    summary_label = widgets.HTML(value="")
    output = widgets.Output()

    def render(_change: Any | None = None) -> None:
        case = PivotCase(case_dropdown.value)
        confidence_level = float(confidence_slider.value)
        sample_size = int(sample_slider.value)
        pivot_chart, quantile_low, quantile_high = _build_pivot_chart(
            case, sample_size, confidence_level, input_data.settings
        )
        lower_bound, upper_bound, point_estimate, parameter_label = _bounds_for_case(
            case, input_data, sample_size, confidence_level
        )
        parameter_chart = _build_parameter_chart(
            lower_bound, upper_bound, point_estimate, parameter_label, input_data.settings
        )
        composed = alt.hconcat(pivot_chart, parameter_chart, spacing=24)
        summary_label.value = (
            f"<b>Cuantiles del pivote</b>: a = {quantile_low:.3f}, b = {quantile_high:.3f}"
            f" · <b>IC para {parameter_label}</b>: [{lower_bound:.3f}, {upper_bound:.3f}]"
            f" · estimación puntual = {point_estimate:.3f}"
        )
        with output:
            output.clear_output(wait=True)
            display(apply_theme(composed, input_data.settings, set_size=False))

    for control in (case_dropdown, confidence_slider, sample_slider):
        control.observe(render, names="value")
    render()
    return widgets.VBox([
        widgets.HBox([case_dropdown, confidence_slider, sample_slider]),
        summary_label,
        output,
    ])
