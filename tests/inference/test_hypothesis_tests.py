import pytest

from inference import (
    OneSampleMeanTestInput,
    OneSampleProportionTestInput,
)
from inference import test_one_sample_mean as run_one_sample_mean_test
from inference import test_one_sample_proportion as run_one_sample_proportion_test
from inference.hypothesis_tests import Alternative


def test_mean_test_two_sided_rejects_large_deviation() -> None:
    result = run_one_sample_mean_test(
        OneSampleMeanTestInput(
            sample_mean=12.0,
            sample_standard_deviation=3.0,
            sample_size=36,
            null_mean=10.0,
            alternative=Alternative.TWO_SIDED,
            significance_level=0.05,
        )
    )
    assert result.reject_null
    assert result.alternative is Alternative.TWO_SIDED


def test_mean_test_greater_one_sided() -> None:
    result = run_one_sample_mean_test(
        OneSampleMeanTestInput(
            sample_mean=12.0,
            sample_standard_deviation=3.0,
            sample_size=36,
            null_mean=11.0,
            alternative=Alternative.GREATER,
            significance_level=0.05,
        )
    )
    assert result.reject_null


def test_mean_test_less_one_sided() -> None:
    result = run_one_sample_mean_test(
        OneSampleMeanTestInput(
            sample_mean=10.0,
            sample_standard_deviation=3.0,
            sample_size=36,
            null_mean=12.0,
            alternative=Alternative.LESS,
            significance_level=0.05,
        )
    )
    assert result.reject_null


def test_proportion_test_two_sided() -> None:
    result = run_one_sample_proportion_test(
        OneSampleProportionTestInput(
            successes=600,
            sample_size=1_000,
            null_proportion=0.5,
            alternative=Alternative.TWO_SIDED,
        )
    )
    assert result.reject_null


def test_proportion_test_greater_branch() -> None:
    result = run_one_sample_proportion_test(
        OneSampleProportionTestInput(
            successes=70,
            sample_size=100,
            null_proportion=0.5,
            alternative=Alternative.GREATER,
        )
    )
    assert result.reject_null
    assert result.alternative is Alternative.GREATER


def test_proportion_test_less_branch() -> None:
    result = run_one_sample_proportion_test(
        OneSampleProportionTestInput(
            successes=30,
            sample_size=100,
            null_proportion=0.5,
            alternative=Alternative.LESS,
        )
    )
    assert result.reject_null


def test_proportion_test_rejects_excessive_successes() -> None:
    with pytest.raises(ValueError, match="successes"):
        run_one_sample_proportion_test(
            OneSampleProportionTestInput(
                successes=200,
                sample_size=100,
                null_proportion=0.5,
            )
        )
