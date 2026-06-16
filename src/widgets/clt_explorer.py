from enum import StrEnum
from typing import Any

import ipywidgets as widgets
from IPython.display import display
from pydantic import BaseModel, ConfigDict

from core import ContinuousUniformParams, ExponentialParams, Settings
from distributions import make_continuous_uniform, make_exponential
from sampling import CLTSimulationInput, simulate_clt
from visualization import CLTComparisonChartInput, chart_clt_comparison


class CLTSourceDistribution(StrEnum):
    UNIFORM = "Uniforme(0, 1)"
    EXPONENTIAL = "Exponencial(λ=1)"


class CLTExplorerInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    settings: Settings = Settings()


def build_clt_explorer(input_data: CLTExplorerInput) -> widgets.Widget:
    source_dropdown = widgets.Dropdown(
        options=[source.value for source in CLTSourceDistribution],
        value=CLTSourceDistribution.EXPONENTIAL.value,
        description="Origen",
    )
    sample_slider = widgets.IntSlider(min=2, max=120, step=1, value=5, description="n por réplica")
    replicates_slider = widgets.IntSlider(min=500, max=15_000, step=500, value=5_000, description="réplicas")
    output = widgets.Output()

    def render(_change: Any | None = None) -> None:
        source = CLTSourceDistribution(source_dropdown.value)
        if source is CLTSourceDistribution.UNIFORM:
            distribution = make_continuous_uniform(ContinuousUniformParams())
        else:
            distribution = make_exponential(ExponentialParams())
        clt_result = simulate_clt(
            CLTSimulationInput(
                distribution=distribution,
                sample_size_per_replicate=sample_slider.value,
                replicates=replicates_slider.value,
                settings=input_data.settings,
            )
        )
        chart = chart_clt_comparison(CLTComparisonChartInput(clt_result=clt_result, settings=input_data.settings))
        with output:
            output.clear_output(wait=True)
            display(chart)

    for control in (source_dropdown, sample_slider, replicates_slider):
        control.observe(render, names="value")
    render()
    return widgets.VBox([source_dropdown, sample_slider, replicates_slider, output])
