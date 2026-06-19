import numpy as np
import pytest

from core import BinomialParams, NormalParams
from distributions import make_binomial, make_normal
from exercises import (
    BooleanAnswerInput,
    CategoricalChoiceInput,
    DistributionMatchInput,
    IntervalContainsInput,
    NumericAnswerInput,
    verify_boolean_answer,
    verify_categorical_choice,
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


@pytest.mark.parametrize(
    ("input_data", "expected_passed"),
    [
        pytest.param(
            BooleanAnswerInput(student_answer=True, expected_answer=True),
            True,
            id="both_true",
        ),
        pytest.param(
            BooleanAnswerInput(student_answer=False, expected_answer=False),
            True,
            id="both_false",
        ),
        pytest.param(
            BooleanAnswerInput(student_answer=True, expected_answer=False),
            False,
            id="student_true_expected_false",
        ),
        pytest.param(
            BooleanAnswerInput(student_answer=False, expected_answer=True),
            False,
            id="student_false_expected_true",
        ),
    ],
)
def test_verify_boolean_answer(input_data: BooleanAnswerInput, *, expected_passed: bool) -> None:
    result = verify_boolean_answer(input_data)
    assert result.passed is expected_passed


def test_categorical_choice_passes_when_matches() -> None:
    result = verify_categorical_choice(
        CategoricalChoiceInput(
            student_choice="discreta",
            expected_choice="discreta",
            allowed_choices=frozenset({"discreta", "continua"}),
        )
    )
    assert result.passed


def test_categorical_choice_fails_when_wrong_choice() -> None:
    result = verify_categorical_choice(
        CategoricalChoiceInput(
            student_choice="continua",
            expected_choice="discreta",
            allowed_choices=frozenset({"discreta", "continua"}),
        )
    )
    assert not result.passed


def test_categorical_choice_rejects_student_choice_outside_allowed() -> None:
    result = verify_categorical_choice(
        CategoricalChoiceInput(
            student_choice="ordinal",
            expected_choice="discreta",
            allowed_choices=frozenset({"discreta", "continua"}),
        )
    )
    assert not result.passed


def test_categorical_choice_rejects_expected_outside_allowed() -> None:
    result = verify_categorical_choice(
        CategoricalChoiceInput(
            student_choice="discreta",
            expected_choice="ordinal",
            allowed_choices=frozenset({"discreta", "continua"}),
        )
    )
    assert not result.passed
