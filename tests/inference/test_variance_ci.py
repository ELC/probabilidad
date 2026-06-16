from inference import VarianceInput, build_confidence_interval_for_variance


def test_variance_ci_brackets_point_estimate() -> None:
    result = build_confidence_interval_for_variance(
        VarianceInput(sample_variance=4.0, sample_size=20, confidence_level=0.95)
    )
    assert result.lower_bound < 4.0 < result.upper_bound
    assert result.degrees_of_freedom == 19
