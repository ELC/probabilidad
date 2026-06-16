from typing import Any

import ipywidgets as widgets
import numpy as np
from IPython.display import display
from pydantic import BaseModel, ConfigDict

from core import Settings
from inference import (
    MeanConfidenceInterval,
    MeanKnownVarianceInput,
    build_confidence_interval_for_mean_known_variance,
)
from visualization import ConfidenceIntervalChartInput, chart_confidence_interval


class MeanCIExplorerInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    settings: Settings = Settings()


def _simulate_intervals(
    true_mean: float,
    population_standard_deviation: float,
    sample_size: int,
    confidence_level: float,
    replicates: int,
    seed: int,
) -> tuple[MeanConfidenceInterval, ...]:
    rng = np.random.default_rng(seed)
    samples = rng.normal(loc=true_mean, scale=population_standard_deviation, size=(replicates, sample_size))
    sample_means = samples.mean(axis=1)
    return tuple(
        build_confidence_interval_for_mean_known_variance(
            MeanKnownVarianceInput(
                sample_mean=float(mean),
                population_standard_deviation=population_standard_deviation,
                sample_size=sample_size,
                confidence_level=confidence_level,
            )
        )
        for mean in sample_means
    )


def build_mean_ci_explorer(input_data: MeanCIExplorerInput) -> widgets.Widget:
    true_mean_slider = widgets.FloatSlider(min=-5.0, max=5.0, step=0.5, value=0.0, description="μ")
    deviation_slider = widgets.FloatSlider(min=0.5, max=5.0, step=0.1, value=1.0, description="σ")
    sample_slider = widgets.IntSlider(min=5, max=200, step=5, value=30, description="n")
    confidence_slider = widgets.FloatSlider(min=0.80, max=0.99, step=0.01, value=0.95, description="1-α")
    replicates_slider = widgets.IntSlider(min=10, max=80, step=5, value=40, description="réplicas")
    coverage_label = widgets.HTML(value="")
    output = widgets.Output()

    def render(_change: Any | None = None) -> None:
        intervals = _simulate_intervals(
            true_mean_slider.value,
            deviation_slider.value,
            sample_slider.value,
            confidence_slider.value,
            replicates_slider.value,
            input_data.settings.random_seed,
        )
        coverage = sum(
            1 for interval in intervals if interval.lower_bound <= true_mean_slider.value <= interval.upper_bound
        ) / len(intervals)
        coverage_label.value = f"<b>Cobertura observada: {coverage:.0%}</b> (nominal {confidence_slider.value:.0%})"
        chart = chart_confidence_interval(
            ConfidenceIntervalChartInput(
                intervals=intervals,
                target_mean=true_mean_slider.value,
                settings=input_data.settings,
            )
        )
        with output:
            output.clear_output(wait=True)
            display(chart)

    for control in (true_mean_slider, deviation_slider, sample_slider, confidence_slider, replicates_slider):
        control.observe(render, names="value")
    render()
    return widgets.VBox([
        widgets.HBox([true_mean_slider, deviation_slider]),
        widgets.HBox([sample_slider, confidence_slider, replicates_slider]),
        coverage_label,
        output,
    ])
