import math

from core import (
    BinomialParams,
    DiscreteUniformParams,
    GeometricParams,
    HypergeometricParams,
    PoissonParams,
)
from distributions import (
    make_binomial,
    make_discrete_uniform,
    make_geometric,
    make_hypergeometric,
    make_poisson,
)


def test_make_binomial_mean() -> None:
    distribution = make_binomial(BinomialParams(trials=10, success_probability=0.4))
    assert math.isclose(distribution.frozen_distribution.mean(), 4.0)


def test_make_poisson_mean() -> None:
    distribution = make_poisson(PoissonParams(rate=3.5))
    assert math.isclose(distribution.frozen_distribution.mean(), 3.5)


def test_make_geometric_mean() -> None:
    distribution = make_geometric(GeometricParams(success_probability=0.25))
    assert math.isclose(distribution.frozen_distribution.mean(), 4.0)


def test_make_hypergeometric_pmf_sums_to_one() -> None:
    distribution = make_hypergeometric(HypergeometricParams(population_size=20, success_states=7, draws=5))
    total = sum(distribution.frozen_distribution.pmf(k) for k in range(6))
    assert math.isclose(total, 1.0, rel_tol=1e-9)


def test_make_discrete_uniform_range() -> None:
    distribution = make_discrete_uniform(DiscreteUniformParams(minimum=1, maximum=6))
    assert math.isclose(distribution.frozen_distribution.mean(), 3.5)
