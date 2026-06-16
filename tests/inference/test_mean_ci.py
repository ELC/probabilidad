import math

from inference import (
    MeanKnownVarianceInput,
    MeanUnknownVarianceInput,
    build_confidence_interval_for_mean_known_variance,
    build_confidence_interval_for_mean_unknown_variance,
)


def test_known_variance_ci_known_case() -> None:
    result = build_confidence_interval_for_mean_known_variance(
        MeanKnownVarianceInput(
            sample_mean=12.0,
            population_standard_deviation=3.0,
            sample_size=36,
            confidence_level=0.95,
        )
    )
    assert math.isclose(result.point_estimate, 12.0)
    assert math.isclose(result.margin_of_error, 1.96 * 0.5, abs_tol=1e-3)


def test_unknown_variance_ci_has_wider_critical_than_normal() -> None:
    known = build_confidence_interval_for_mean_known_variance(
        MeanKnownVarianceInput(
            sample_mean=0.0,
            population_standard_deviation=1.0,
            sample_size=5,
            confidence_level=0.95,
        )
    )
    unknown = build_confidence_interval_for_mean_unknown_variance(
        MeanUnknownVarianceInput(
            sample_mean=0.0,
            sample_standard_deviation=1.0,
            sample_size=5,
            confidence_level=0.95,
        )
    )
    assert unknown.critical_value > known.critical_value
