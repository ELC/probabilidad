from typing import Any, Self

import ipywidgets as widgets
import numpy as np
import pandas as pd
from IPython.display import display
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict, Field, model_validator

from core import NormalParams, Observations, Settings
from descriptive import FrequencyTableInput, build_frequency_table, summarize_observations
from visualization import (
    FrequencyPolygonChartInput,
    ObservationsOverviewInput,
    chart_cumulative_frequency_polygon,
    chart_histogram_with_frequency_polygon,
    chart_observations_overview,
)


class DescriptiveExplorerInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    settings: Settings = Settings()


class IntervalWidthExplorerInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    observations: DataFrame[Observations]
    settings: Settings = Settings()
    minimum_width: float = Field(default=0.5, gt=0.0)
    maximum_width: float = Field(default=3.0, gt=0.0)
    step: float = Field(default=0.25, gt=0.0)
    initial_width: float = Field(default=1.0, gt=0.0)

    @model_validator(mode="after")
    def _validate_widths(self) -> Self:
        if self.minimum_width >= self.maximum_width:
            msg = "minimum_width must be less than maximum_width"
            raise ValueError(msg)
        if not self.minimum_width <= self.initial_width <= self.maximum_width:
            msg = "initial_width must be inside the slider range"
            raise ValueError(msg)
        return self


def _generate_synthetic_observations(parameters: NormalParams, sample_size: int, seed: int) -> DataFrame[Observations]:
    rng = np.random.default_rng(seed)
    samples = rng.normal(loc=parameters.mean, scale=parameters.standard_deviation, size=sample_size)
    return pd.DataFrame({"value": samples.astype(float)}).pipe(DataFrame[Observations])


def _slider_widths(input_data: IntervalWidthExplorerInput) -> tuple[float, ...]:
    width_count = round((input_data.maximum_width - input_data.minimum_width) / input_data.step)
    widths = {
        round(input_data.minimum_width + index * input_data.step, 10)
        for index in range(width_count + 1)
    }
    widths.add(round(input_data.initial_width, 10))
    return tuple(sorted(width for width in widths if width <= input_data.maximum_width))


def _fixed_domains(input_data: IntervalWidthExplorerInput) -> tuple[tuple[float, float], tuple[float, float]]:
    tables = [
        build_frequency_table(FrequencyTableInput(observations=input_data.observations, bin_width=width))
        for width in _slider_widths(input_data)
    ]
    x_domain = (
        min(float(table["interval_start"].min()) for table in tables),
        max(float(table["interval_end"].max()) for table in tables),
    )
    max_relative_frequency = max(float(table["relative_frequency"].max()) for table in tables)
    relative_y_domain = (0.0, min(1.0, max_relative_frequency * 1.05))
    return x_domain, relative_y_domain


def build_descriptive_explorer(input_data: DescriptiveExplorerInput) -> widgets.Widget:
    mean_slider = widgets.FloatSlider(min=-10.0, max=10.0, step=0.5, value=0.0, description="μ")
    deviation_slider = widgets.FloatSlider(min=0.5, max=5.0, step=0.1, value=1.0, description="σ")
    sample_slider = widgets.IntSlider(min=20, max=500, step=10, value=120, description="n")
    bin_slider = widgets.IntSlider(min=4, max=40, step=1, value=12, description="bins")
    output = widgets.Output()

    def render(_change: Any | None = None) -> None:
        observations = _generate_synthetic_observations(
            NormalParams(mean=mean_slider.value, standard_deviation=deviation_slider.value),
            sample_slider.value,
            input_data.settings.random_seed,
        )
        statistics = summarize_observations(observations)
        frequency_table = build_frequency_table(
            FrequencyTableInput(observations=observations, bin_count=bin_slider.value)
        )
        overview = chart_observations_overview(
            ObservationsOverviewInput(
                observations=observations,
                frequency_table=frequency_table,
                statistics=statistics,
                settings=input_data.settings,
            )
        )
        with output:
            output.clear_output(wait=True)
            display(overview)

    for control in (mean_slider, deviation_slider, sample_slider, bin_slider):
        control.observe(render, names="value")
    render()
    return widgets.VBox([
        widgets.HBox([mean_slider, deviation_slider]),
        widgets.HBox([sample_slider, bin_slider]),
        output,
    ])


def build_interval_width_explorer(input_data: IntervalWidthExplorerInput) -> widgets.Widget:
    x_domain, relative_y_domain = _fixed_domains(input_data)
    width_slider = widgets.FloatSlider(
        min=input_data.minimum_width,
        max=input_data.maximum_width,
        step=input_data.step,
        value=input_data.initial_width,
        description="ancho",
        readout_format=".2f",
    )
    frequency_output = widgets.Output(layout=widgets.Layout(width="100%"))
    cumulative_output = widgets.Output(layout=widgets.Layout(width="100%"))

    def render(_change: Any | None = None) -> None:
        frequency_table = build_frequency_table(
            FrequencyTableInput(
                observations=input_data.observations,
                bin_width=width_slider.value,
            )
        )
        frequency_chart = chart_histogram_with_frequency_polygon(
            FrequencyPolygonChartInput(
                frequency_table=frequency_table,
                title="Frecuencia por intervalo",
                settings=input_data.settings,
                x_domain=x_domain,
                y_domain=relative_y_domain,
            )
        )
        cumulative_chart = chart_cumulative_frequency_polygon(
            FrequencyPolygonChartInput(
                frequency_table=frequency_table,
                title="Frecuencia acumulada",
                settings=input_data.settings,
                x_domain=x_domain,
                y_domain=(0.0, 1.0),
            )
        )
        with frequency_output:
            frequency_output.clear_output(wait=True)
            display(frequency_chart)
        with cumulative_output:
            cumulative_output.clear_output(wait=True)
            display(cumulative_chart)

    width_slider.observe(render, names="value")
    render()
    return widgets.VBox([
        width_slider,
        frequency_output,
        cumulative_output,
    ])
