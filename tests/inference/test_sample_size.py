from inference import (
    SampleSizeForMeanInput,
    SampleSizeForProportionInput,
    sample_size_for_mean,
    sample_size_for_proportion,
)


def test_sample_size_for_mean_known_case() -> None:
    result = sample_size_for_mean(
        SampleSizeForMeanInput(
            population_standard_deviation=3.0,
            margin_of_error=1.0,
            confidence_level=0.95,
        )
    )
    assert result.required_sample_size >= 35


def test_sample_size_for_proportion_default_worst_case() -> None:
    result = sample_size_for_proportion(
        SampleSizeForProportionInput(margin_of_error=0.03, confidence_level=0.95)
    )
    assert 1_000 < result.required_sample_size < 1_500


def test_sample_size_quadruples_when_margin_halves() -> None:
    base = sample_size_for_mean(
        SampleSizeForMeanInput(population_standard_deviation=1.0, margin_of_error=0.1)
    )
    half_margin = sample_size_for_mean(
        SampleSizeForMeanInput(population_standard_deviation=1.0, margin_of_error=0.05)
    )
    ratio = half_margin.required_sample_size / base.required_sample_size
    assert 3.9 <= ratio <= 4.1
