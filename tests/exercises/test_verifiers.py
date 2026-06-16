import numpy as np

from core import BinomialParams, NormalParams
from distributions import make_binomial, make_normal
from exercises import (
    DistributionMatchInput,
    IntervalContainsInput,
    NumericAnswerInput,
    verify_distribution_match,
    verify_interval_contains,
    verify_numeric_answer,
)


def test_numeric_answer_passes_when_close() -> None:
    result = verify_numeric_answer(NumericAnswerInput(student_answer=1.0001, expected_answer=1.0))
    assert result.passed


def test_numeric_answer_fails_when_far() -> None:
    result = verify_numeric_answer(NumericAnswerInput(student_answer=1.5, expected_answer=1.0))
    assert not result.passed


def test_interval_contains_target() -> None:
    result = verify_interval_contains(IntervalContainsInput(lower_bound=0.0, upper_bound=1.0, target_value=0.5))
    assert result.passed


def test_interval_does_not_contain_target() -> None:
    result = verify_interval_contains(IntervalContainsInput(lower_bound=0.0, upper_bound=1.0, target_value=2.0))
    assert not result.passed


def test_interval_rejects_inverted_bounds() -> None:
    result = verify_interval_contains(IntervalContainsInput(lower_bound=1.0, upper_bound=0.0, target_value=0.5))
    assert not result.passed


def test_distribution_match_continuous_passes_for_correct_samples() -> None:
    rng = np.random.default_rng(0)
    samples = rng.normal(size=500)
    distribution = make_normal(NormalParams())
    result = verify_distribution_match(
        DistributionMatchInput(student_samples=samples, expected_distribution=distribution)
    )
    assert result.passed


def test_distribution_match_continuous_fails_for_wrong_samples() -> None:
    rng = np.random.default_rng(0)
    samples = rng.uniform(low=-3.0, high=3.0, size=500)
    distribution = make_normal(NormalParams())
    result = verify_distribution_match(
        DistributionMatchInput(student_samples=samples, expected_distribution=distribution)
    )
    assert not result.passed


def test_distribution_match_discrete_passes_for_correct_samples() -> None:
    rng = np.random.default_rng(0)
    samples = rng.binomial(n=10, p=0.5, size=1_000)
    distribution = make_binomial(BinomialParams(trials=10, success_probability=0.5))
    result = verify_distribution_match(
        DistributionMatchInput(student_samples=samples, expected_distribution=distribution)
    )
    assert result.passed


def test_distribution_match_discrete_fails_for_wrong_samples() -> None:
    rng = np.random.default_rng(0)
    samples = rng.binomial(n=10, p=0.1, size=1_000)
    distribution = make_binomial(BinomialParams(trials=10, success_probability=0.5))
    result = verify_distribution_match(
        DistributionMatchInput(student_samples=samples, expected_distribution=distribution)
    )
    assert not result.passed
