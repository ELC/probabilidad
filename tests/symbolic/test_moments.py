import math

import sympy as sp

from core import (
    BinomialParams,
    ContinuousUniformParams,
    ExponentialParams,
    NormalParams,
    PoissonParams,
)
from symbolic import (
    compute_binomial_moments,
    compute_continuous_uniform_moments,
    compute_exponential_moments,
    compute_normal_moments,
    compute_poisson_moments,
)


def test_normal_moments_match_parameters() -> None:
    moments = compute_normal_moments(NormalParams(mean=2.5, standard_deviation=3.0))
    assert math.isclose(float(moments.expectation), 2.5)
    assert math.isclose(float(moments.variance), 9.0)
    assert math.isclose(float(moments.standard_deviation), 3.0)
    assert moments.name == "Normal"


def test_continuous_uniform_moments() -> None:
    moments = compute_continuous_uniform_moments(ContinuousUniformParams(minimum=0.0, maximum=4.0))
    assert math.isclose(float(moments.expectation), 2.0)
    assert math.isclose(float(moments.variance), 16 / 12)


def test_exponential_moments() -> None:
    moments = compute_exponential_moments(ExponentialParams(rate=2.0))
    assert math.isclose(float(moments.expectation), 0.5)
    assert math.isclose(float(moments.variance), 0.25)


def test_binomial_moments() -> None:
    moments = compute_binomial_moments(BinomialParams(trials=10, success_probability=0.3))
    assert math.isclose(float(moments.expectation), 3.0)
    assert math.isclose(float(moments.variance), 10 * 0.3 * 0.7)


def test_poisson_moments() -> None:
    moments = compute_poisson_moments(PoissonParams(rate=4.0))
    assert math.isclose(float(moments.expectation), 4.0)
    assert math.isclose(float(moments.variance), 4.0)


def test_moments_are_sympy_expressions() -> None:
    moments = compute_poisson_moments(PoissonParams(rate=1.0))
    assert isinstance(moments.expectation, sp.Expr)
