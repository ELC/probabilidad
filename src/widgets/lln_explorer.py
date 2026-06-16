from typing import Any

import ipywidgets as widgets
from IPython.display import display
from pydantic import BaseModel, ConfigDict

from core import BinomialParams, Settings
from distributions import make_binomial
from sampling import LLNSimulationInput, simulate_lln
from visualization import LLNChartInput, chart_lln_running_mean


class LLNExplorerInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    settings: Settings = Settings()


def build_lln_explorer(input_data: LLNExplorerInput) -> widgets.Widget:
    probability_slider = widgets.FloatSlider(min=0.05, max=0.95, step=0.05, value=0.3, description="p")
    horizon_slider = widgets.IntSlider(min=200, max=10_000, step=200, value=2_000, description="horizonte")
    output = widgets.Output()

    def render(_change: Any | None = None) -> None:
        distribution = make_binomial(BinomialParams(trials=1, success_probability=probability_slider.value))
        lln_result = simulate_lln(
            LLNSimulationInput(
                distribution=distribution,
                horizon=horizon_slider.value,
                settings=input_data.settings,
            )
        )
        chart = chart_lln_running_mean(LLNChartInput(lln_result=lln_result, settings=input_data.settings))
        with output:
            output.clear_output(wait=True)
            display(chart)

    for control in (probability_slider, horizon_slider):
        control.observe(render, names="value")
    render()
    return widgets.VBox([probability_slider, horizon_slider, output])
