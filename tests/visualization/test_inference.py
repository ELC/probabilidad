import json

from core import Settings
from inference import MeanKnownVarianceInput, build_confidence_interval_for_mean_known_variance
from visualization import ConfidenceIntervalChartInput, chart_confidence_interval


def test_chart_confidence_interval_with_target(fixed_settings: Settings) -> None:
    intervals = tuple(
        build_confidence_interval_for_mean_known_variance(
            MeanKnownVarianceInput(
                sample_mean=mean,
                population_standard_deviation=1.0,
                sample_size=25,
                confidence_level=0.95,
            )
        )
        for mean in (-0.5, 0.0, 0.5)
    )
    chart = chart_confidence_interval(
        ConfidenceIntervalChartInput(intervals=intervals, target_mean=0.0, settings=fixed_settings)
    )
    assert chart.to_dict()


def test_chart_confidence_interval_without_target(fixed_settings: Settings) -> None:
    intervals = (
        build_confidence_interval_for_mean_known_variance(
            MeanKnownVarianceInput(
                sample_mean=0.0,
                population_standard_deviation=1.0,
                sample_size=25,
                confidence_level=0.95,
            )
        ),
    )
    chart = chart_confidence_interval(ConfidenceIntervalChartInput(intervals=intervals, settings=fixed_settings))
    assert chart.to_dict()


def test_chart_confidence_interval_uses_firebrick_for_misses(fixed_settings: Settings) -> None:
    intervals = tuple(
        build_confidence_interval_for_mean_known_variance(
            MeanKnownVarianceInput(
                sample_mean=mean,
                population_standard_deviation=1.0,
                sample_size=25,
                confidence_level=0.95,
            )
        )
        for mean in (-0.5, 0.0, 0.5)
    )
    chart = chart_confidence_interval(
        ConfidenceIntervalChartInput(intervals=intervals, target_mean=0.0, settings=fixed_settings)
    )
    spec_text = json.dumps(chart.to_dict(format="vega"))
    assert "#B22222" in spec_text.upper()
