from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Self

import altair as alt
import ipywidgets as widgets
import numpy as np
import pandas as pd
from IPython.display import display
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict, Field, model_validator

from core import Observations, Settings
from visualization.theme import apply_theme

_MINIMUM_SAMPLE_SIZE_FOR_STANDARD_DEVIATION = 2
_DOMAIN_PADDING_RATIO = 0.05
_RANDOM_DOMAIN_DEVIATIONS = 4.0


class SummaryEvolutionExplorerInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    observations: DataFrame[Observations]
    settings: Settings = Settings()
    manual_value: float = 20.0
    random_mean: float = 4.0
    random_standard_deviation: float = Field(default=1.2, gt=0.0)
    random_batch_size: int = Field(default=10, ge=1)

    @model_validator(mode="after")
    def _validate_observations(self) -> Self:
        if self.observations.empty:
            msg = "observations must not be empty"
            raise ValueError(msg)
        return self


@dataclass(frozen=True)
class _MeasureSpec:
    label: str
    value_title: str
    statistic: Callable[[np.ndarray], float]


def _sample_standard_deviation(values: np.ndarray) -> float:
    if values.size < _MINIMUM_SAMPLE_SIZE_FOR_STANDARD_DEVIATION:
        return 0.0
    return float(np.std(values, ddof=1))


def _sample_range(values: np.ndarray) -> float:
    return float(np.max(values) - np.min(values))


def _sample_iqr(values: np.ndarray) -> float:
    first_quartile, third_quartile = np.quantile(values, [0.25, 0.75])
    return float(third_quartile - first_quartile)


def _sample_mode(values: np.ndarray) -> float:
    rounded_values = np.rint(values).astype(int)
    unique_values, counts = np.unique(rounded_values, return_counts=True)
    return float(unique_values[counts == counts.max()].min())


_MEAN = _MeasureSpec("Media", "Minutos", lambda values: float(np.mean(values)))
_MODE = _MeasureSpec("Moda", "Minutos redondeados", _sample_mode)
_MEDIAN = _MeasureSpec("Mediana", "Minutos", lambda values: float(np.median(values)))
_STANDARD_DEVIATION = _MeasureSpec("Desvío estándar", "Minutos", _sample_standard_deviation)
_RANGE = _MeasureSpec("Rango", "Minutos", _sample_range)
_IQR = _MeasureSpec("Rango intercuartil", "Minutos", _sample_iqr)


def _history(values: np.ndarray, measures: tuple[_MeasureSpec, ...]) -> pd.DataFrame:
    rows = [
        {"n": step, "measure": measure.label, "value": measure.statistic(values[:step])}
        for step in range(1, values.size + 1)
        for measure in measures
    ]
    return pd.DataFrame(rows)


def _padded_domain(minimum: float, maximum: float) -> tuple[float, float]:
    if np.isclose(minimum, maximum):
        return minimum - 1.0, maximum + 1.0
    padding = (maximum - minimum) * _DOMAIN_PADDING_RATIO
    return minimum - padding, maximum + padding


def _random_value_bounds(input_data: SummaryEvolutionExplorerInput) -> tuple[float, float]:
    random_low = max(0.0, input_data.random_mean - _RANDOM_DOMAIN_DEVIATIONS * input_data.random_standard_deviation)
    random_high = input_data.random_mean + _RANDOM_DOMAIN_DEVIATIONS * input_data.random_standard_deviation
    return random_low, random_high


def _fixed_evolution_domain(
    input_data: SummaryEvolutionExplorerInput,
    measures: tuple[_MeasureSpec, ...],
) -> tuple[float, float]:
    random_low, random_high = _random_value_bounds(input_data)
    reference_values = np.append(
        input_data.observations["value"].to_numpy(dtype=float),
        [input_data.manual_value, random_low, random_high],
    )
    history = _history(reference_values, measures)
    return _padded_domain(float(history["value"].min()), float(history["value"].max()))


def _summary_chart(
    values: np.ndarray,
    measures: tuple[_MeasureSpec, ...],
    title: str,
    settings: Settings,
    evolution_domain: tuple[float, float],
) -> alt.Chart:
    theme = settings.chart_theme
    observations = pd.DataFrame({"value": values})
    history = _history(values, measures)
    histogram = (
        alt
        .Chart(observations)
        .mark_bar(color=theme.palette.primary, opacity=theme.bar_opacity)
        .encode(
            x=alt.X(
                "value:Q",
                bin=alt.Bin(maxbins=20),
                title="Minutos de espera",
            ),
            y=alt.Y("count()", title="Frecuencia"),
            tooltip=[alt.Tooltip("count()", title="Frecuencia")],
        )
        .properties(title="Distribución actual", width=theme.width, height=180)
    )
    color = alt.Color("measure:N", legend=alt.Legend(title=None, orient="bottom"))
    evolution = (
        alt
        .Chart(history)
        .mark_line(point=True, strokeWidth=theme.line_stroke_width)
        .encode(
            x=alt.X(
                "n:Q",
                title="Cantidad de valores incorporados",
            ),
            y=alt.Y(
                "value:Q",
                scale=alt.Scale(domain=list(evolution_domain)),
                title=measures[0].value_title,
            ),
            color=color if len(measures) > 1 else alt.value(theme.palette.secondary),
            detail="measure:N",
            tooltip=[
                alt.Tooltip("n:Q", title="n"),
                alt.Tooltip("measure:N", title="Resumen"),
                alt.Tooltip("value:Q", title="Valor", format=".2f"),
            ],
        )
        .properties(title=title, width=theme.width, height=220)
    )
    chart = alt.vconcat(histogram, evolution, spacing=10).resolve_scale(x="independent")
    return apply_theme(chart, settings, set_size=False)


def _build_summary_evolution_explorer(
    input_data: SummaryEvolutionExplorerInput,
    measures: tuple[_MeasureSpec, ...],
    title: str,
) -> widgets.Widget:
    initial_values = list(input_data.observations["value"].astype(float))
    values = list(initial_values)
    evolution_domain = _fixed_evolution_domain(input_data, measures)
    rng = np.random.default_rng(input_data.settings.random_seed)
    controls_layout = widgets.Layout(width="100%")
    value_input = widgets.FloatText(value=input_data.manual_value, description="valor")
    add_value_button = widgets.Button(description="Agregar valor")
    add_random_button = widgets.Button(description="Agregar aleatorio")
    add_random_batch_button = widgets.Button(description=f"Agregar {input_data.random_batch_size}")
    reset_button = widgets.Button(description="Reiniciar")
    output = widgets.Output(layout=widgets.Layout(width="100%"))

    def render() -> None:
        current_values = np.array(values, dtype=float)
        chart = _summary_chart(
            current_values,
            measures,
            title,
            input_data.settings,
            evolution_domain,
        )
        with output:
            output.clear_output(wait=True)
            display(chart)

    def next_random_value() -> float:
        sample = rng.normal(input_data.random_mean, input_data.random_standard_deviation)
        return round(float(max(0.0, sample)), 2)

    def add_value(_change: Any | None = None) -> None:
        values.append(float(value_input.value))
        render()

    def add_random(_change: Any | None = None) -> None:
        values.append(next_random_value())
        render()

    def add_random_batch(_change: Any | None = None) -> None:
        values.extend(next_random_value() for _ in range(input_data.random_batch_size))
        render()

    def reset(_change: Any | None = None) -> None:
        nonlocal rng
        values.clear()
        values.extend(initial_values)
        rng = np.random.default_rng(input_data.settings.random_seed)
        render()

    add_value_button.on_click(add_value)
    add_random_button.on_click(add_random)
    add_random_batch_button.on_click(add_random_batch)
    reset_button.on_click(reset)
    render()
    return widgets.VBox(
        [
            widgets.HBox(
                [
                    value_input,
                    add_value_button,
                    add_random_button,
                    add_random_batch_button,
                    reset_button,
                ],
                layout=controls_layout,
            ),
            output,
        ],
        layout=widgets.Layout(width="100%"),
    )


def build_mean_evolution_explorer(input_data: SummaryEvolutionExplorerInput) -> widgets.Widget:
    return _build_summary_evolution_explorer(input_data, (_MEAN,), "Evolución de la media")


def build_mode_evolution_explorer(input_data: SummaryEvolutionExplorerInput) -> widgets.Widget:
    return _build_summary_evolution_explorer(input_data, (_MODE,), "Evolución de la moda")


def build_median_evolution_explorer(input_data: SummaryEvolutionExplorerInput) -> widgets.Widget:
    return _build_summary_evolution_explorer(input_data, (_MEDIAN,), "Evolución de la mediana")


def build_location_evolution_explorer(input_data: SummaryEvolutionExplorerInput) -> widgets.Widget:
    return _build_summary_evolution_explorer(
        input_data,
        (_MEAN, _MODE, _MEDIAN),
        "Evolución de media, moda y mediana",
    )


def build_standard_deviation_evolution_explorer(input_data: SummaryEvolutionExplorerInput) -> widgets.Widget:
    return _build_summary_evolution_explorer(
        input_data,
        (_STANDARD_DEVIATION,),
        "Evolución del desvío estándar",
    )


def build_range_evolution_explorer(input_data: SummaryEvolutionExplorerInput) -> widgets.Widget:
    return _build_summary_evolution_explorer(input_data, (_RANGE,), "Evolución del rango")


def build_iqr_evolution_explorer(input_data: SummaryEvolutionExplorerInput) -> widgets.Widget:
    return _build_summary_evolution_explorer(input_data, (_IQR,), "Evolución del rango intercuartil")


def build_dispersion_evolution_explorer(input_data: SummaryEvolutionExplorerInput) -> widgets.Widget:
    return _build_summary_evolution_explorer(
        input_data,
        (_STANDARD_DEVIATION, _RANGE, _IQR),
        "Evolución de desvío estándar, rango e IQR",
    )
