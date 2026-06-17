from typing import Any

import ipywidgets as widgets
import numpy as np
import pandas as pd
from IPython.display import display
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from core import NormalParams, Observations, Settings
from descriptive import FrequencyTableInput, build_frequency_table, summarize_observations
from visualization import (
    ObservationsOverviewInput,
    chart_observations_overview,
)


class DescriptiveExplorerInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    settings: Settings = Settings()


def _generate_synthetic_observations(parameters: NormalParams, sample_size: int, seed: int) -> DataFrame[Observations]:
    rng = np.random.default_rng(seed)
    samples = rng.normal(loc=parameters.mean, scale=parameters.standard_deviation, size=sample_size)
    return Observations.validate(pd.DataFrame({"value": samples.astype(float)}))


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
