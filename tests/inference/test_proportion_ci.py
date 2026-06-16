import math

import pytest

from inference import ProportionInput, build_confidence_interval_for_proportion


def test_proportion_ci_centered_on_point_estimate() -> None:
    result = build_confidence_interval_for_proportion(
        ProportionInput(successes=200, sample_size=400, confidence_level=0.95)
    )
    assert math.isclose(result.point_estimate, 0.5)
    assert result.lower_bound < 0.5 < result.upper_bound


def test_proportion_ci_clips_to_unit_interval() -> None:
    result = build_confidence_interval_for_proportion(
        ProportionInput(successes=1, sample_size=2, confidence_level=0.99)
    )
    assert result.lower_bound >= 0.0
    assert result.upper_bound <= 1.0


def test_proportion_ci_rejects_more_successes_than_sample_size() -> None:
    with pytest.raises(ValueError, match="successes"):
        build_confidence_interval_for_proportion(
            ProportionInput(successes=5, sample_size=4, confidence_level=0.95)
        )
