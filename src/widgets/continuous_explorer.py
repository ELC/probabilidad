from enum import StrEnum
from typing import Any

import ipywidgets as widgets
from IPython.display import display
from pydantic import BaseModel, ConfigDict

from core import ExponentialParams, NormalParams, Settings
from distributions import (
    DensityGridInput,
    evaluate_density_grid,
    make_exponential,
    make_normal,
    tail_probability_of_continuous,
)
from distributions.evaluations import TailProbabilityInput
from visualization import DensityChartInput, chart_density


class DistributionFamily(StrEnum):
    NORMAL = "Normal"
    EXPONENTIAL = "Exponencial"


class ContinuousDistributionExplorerInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    settings: Settings = Settings()


def build_continuous_distribution_explorer(input_data: ContinuousDistributionExplorerInput) -> widgets.Widget:
    family_dropdown = widgets.Dropdown(
        options=[family.value for family in DistributionFamily],
        value=DistributionFamily.NORMAL.value,
        description="Familia",
    )
    parameter_one_slider = widgets.FloatSlider(min=-5.0, max=5.0, step=0.5, value=0.0, description="μ")
    parameter_two_slider = widgets.FloatSlider(min=0.5, max=5.0, step=0.1, value=1.0, description="σ")
    lower_slider = widgets.FloatSlider(min=-5.0, max=5.0, step=0.1, value=-1.0, description="x_min")
    upper_slider = widgets.FloatSlider(min=-5.0, max=5.0, step=0.1, value=1.0, description="x_max")
    probability_label = widgets.HTML(value="")
    output = widgets.Output()

    def render(_change: Any | None = None) -> None:
        family = DistributionFamily(family_dropdown.value)
        if family is DistributionFamily.NORMAL:
            distribution = make_normal(
                NormalParams(mean=parameter_one_slider.value, standard_deviation=max(parameter_two_slider.value, 0.1))
            )
        else:
            distribution = make_exponential(ExponentialParams(rate=max(parameter_two_slider.value, 0.1)))
        density = evaluate_density_grid(DensityGridInput(distribution=distribution, settings=input_data.settings))
        probability = tail_probability_of_continuous(
            TailProbabilityInput(
                distribution=distribution,
                lower_bound=lower_slider.value,
                upper_bound=upper_slider.value,
            )
        )
        probability_label.value = (
            f"<b>P({lower_slider.value:.2f} ≤ X ≤ {upper_slider.value:.2f})</b> = {probability.probability:.4f}"
        )
        chart = chart_density(DensityChartInput(density_grid=density, settings=input_data.settings))
        with output:
            output.clear_output(wait=True)
            display(chart)

    for control in (family_dropdown, parameter_one_slider, parameter_two_slider, lower_slider, upper_slider):
        control.observe(render, names="value")
    render()
    return widgets.VBox([
        widgets.HBox([family_dropdown, parameter_one_slider, parameter_two_slider]),
        widgets.HBox([lower_slider, upper_slider]),
        probability_label,
        output,
    ])
