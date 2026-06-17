import math

import numpy as np
from pydantic import BaseModel, ConfigDict, Field
from scipy import stats

from core import RichMarkdownModel
from distributions.continuous import ContinuousDistribution
from distributions.discrete import DiscreteDistribution

_ARBITRARY = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class VerificationResult(RichMarkdownModel):
    model_config = _ARBITRARY

    passed: bool
    message: str


class NumericAnswerInput(BaseModel):
    model_config = _ARBITRARY

    student_answer: float
    expected_answer: float
    absolute_tolerance: float = Field(default=1e-4, ge=0.0)
    relative_tolerance: float = Field(default=1e-3, ge=0.0)


def verify_numeric_answer(input_data: NumericAnswerInput) -> VerificationResult:
    is_close = math.isclose(
        input_data.student_answer,
        input_data.expected_answer,
        abs_tol=input_data.absolute_tolerance,
        rel_tol=input_data.relative_tolerance,
    )
    if is_close:
        return VerificationResult(passed=True, message=f"OK — esperado {input_data.expected_answer:.6f}")
    return VerificationResult(
        passed=False,
        message=(
            f"Diferencia: tu respuesta {input_data.student_answer:.6f}, esperado {input_data.expected_answer:.6f}"
        ),
    )


class IntervalContainsInput(BaseModel):
    model_config = _ARBITRARY

    lower_bound: float
    upper_bound: float
    target_value: float


def verify_interval_contains(input_data: IntervalContainsInput) -> VerificationResult:
    if input_data.lower_bound > input_data.upper_bound:
        return VerificationResult(passed=False, message="lower_bound > upper_bound: intervalo inválido")
    contains = input_data.lower_bound <= input_data.target_value <= input_data.upper_bound
    if contains:
        return VerificationResult(
            passed=True,
            message=f"OK — el intervalo [{input_data.lower_bound:.4f}, {input_data.upper_bound:.4f}] contiene {input_data.target_value:.4f}",
        )
    return VerificationResult(
        passed=False,
        message=(
            f"El intervalo [{input_data.lower_bound:.4f}, {input_data.upper_bound:.4f}] no contiene "
            f"{input_data.target_value:.4f}"
        ),
    )


class DistributionMatchInput(BaseModel):
    model_config = _ARBITRARY

    student_samples: np.ndarray
    expected_distribution: ContinuousDistribution | DiscreteDistribution
    significance_level: float = Field(default=0.05, gt=0.0, lt=1.0)


def verify_distribution_match(input_data: DistributionMatchInput) -> VerificationResult:
    if isinstance(input_data.expected_distribution, ContinuousDistribution):
        statistic, p_value = stats.kstest(
            input_data.student_samples,
            input_data.expected_distribution.frozen_distribution.cdf,
        )
        passed = bool(p_value > input_data.significance_level)
        return VerificationResult(
            passed=passed,
            message=(
                f"KS = {float(statistic):.4f}, p = {float(p_value):.4f} — "
                f"{'no se rechaza H₀' if passed else 'se rechaza H₀'} "
                f"contra {input_data.expected_distribution.spanish_name}"
            ),
        )
    unique_values = np.unique(input_data.student_samples)
    expected_counts: np.ndarray = (
        np.asarray(
            input_data.expected_distribution.frozen_distribution.pmf(unique_values),
            dtype=float,
        )
        * input_data.student_samples.size
    )
    observed_counts = np.array(
        [np.sum(input_data.student_samples == value) for value in unique_values],
        dtype=float,
    )
    expected_counts = expected_counts * observed_counts.sum() / expected_counts.sum()
    statistic, p_value = stats.chisquare(observed_counts, f_exp=expected_counts)
    passed = bool(p_value > input_data.significance_level)
    return VerificationResult(
        passed=passed,
        message=(
            f"χ² = {float(statistic):.4f}, p = {float(p_value):.4f} — "
            f"{'no se rechaza H₀' if passed else 'se rechaza H₀'} "
            f"contra {input_data.expected_distribution.spanish_name}"
        ),
    )
