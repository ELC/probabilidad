from enum import StrEnum
from typing import Any

import ipywidgets as widgets
from IPython.display import display
from pydantic import BaseModel, ConfigDict

from core import BinomialParams, PoissonParams, Settings
from distributions import (
    ProbabilityMassInput,
    evaluate_probability_mass,
    make_binomial,
    make_poisson,
)
from visualization import ProbabilityMassChartInput, chart_probability_mass


class DiscreteFamily(StrEnum):
    BINOMIAL = "Binomial"
    POISSON = "Poisson"


class DiscreteDistributionExplorerInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    settings: Settings = Settings()


def build_discrete_distribution_explorer(input_data: DiscreteDistributionExplorerInput) -> widgets.Widget:
    family_dropdown = widgets.Dropdown(
        options=[family.value for family in DiscreteFamily],
        value=DiscreteFamily.BINOMIAL.value,
        description="Familia",
    )
    trials_slider = widgets.IntSlider(min=1, max=50, step=1, value=10, description="n")
    probability_slider = widgets.FloatSlider(min=0.01, max=0.99, step=0.01, value=0.4, description="p / λ")
    output = widgets.Output()

    def render(_change: Any | None = None) -> None:
        family = DiscreteFamily(family_dropdown.value)
        if family is DiscreteFamily.BINOMIAL:
            distribution = make_binomial(
                BinomialParams(trials=trials_slider.value, success_probability=probability_slider.value)
            )
        else:
            distribution = make_poisson(PoissonParams(rate=max(probability_slider.value * trials_slider.value, 0.1)))
        probability_mass = evaluate_probability_mass(ProbabilityMassInput(distribution=distribution))
        chart = chart_probability_mass(
            ProbabilityMassChartInput(probability_mass=probability_mass, settings=input_data.settings)
        )
        with output:
            output.clear_output(wait=True)
            display(chart)

    for control in (family_dropdown, trials_slider, probability_slider):
        control.observe(render, names="value")
    render()
    return widgets.VBox([
        widgets.HBox([family_dropdown, trials_slider, probability_slider]),
        output,
    ])
