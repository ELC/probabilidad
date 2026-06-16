import math

import pytest
from pydantic import ValidationError

from core import BinomialParams, NormalParams, Settings
from distributions import (
    DensityGridInput,
    MomentsInput,
    ProbabilityMassInput,
    QuantileInput,
    SurvivalInput,
    TailProbabilityInput,
    compute_numeric_moments,
    evaluate_density_grid,
    evaluate_probability_mass,
    make_binomial,
    make_normal,
    quantile_of_continuous,
    survival_of_continuous,
    tail_probability_of_continuous,
)


def test_evaluate_density_grid_shape() -> None:
    distribution = make_normal(NormalParams(mean=0.0, standard_deviation=1.0))
    settings = Settings()
    result = evaluate_density_grid(DensityGridInput(distribution=distribution, settings=settings))
    assert result.grid.size == settings.grid_resolution
    assert math.isclose(result.cumulative[-1], 1.0, abs_tol=1e-2)


def test_density_grid_rejects_inverted_quantiles() -> None:
    distribution = make_normal(NormalParams())
    with pytest.raises(ValidationError):
        DensityGridInput(distribution=distribution, lower_quantile=0.9, upper_quantile=0.1)


def test_evaluate_probability_mass_uses_explicit_bounds() -> None:
    distribution = make_binomial(BinomialParams(trials=4, success_probability=0.5))
    result = evaluate_probability_mass(
        ProbabilityMassInput(distribution=distribution, lower_outcome=0, upper_outcome=4)
    )
    assert math.isclose(result.table["probability"].sum(), 1.0)
    assert len(result.table) == 5


def test_evaluate_probability_mass_defaults_to_quantile_window() -> None:
    distribution = make_binomial(BinomialParams(trials=20, success_probability=0.5))
    result = evaluate_probability_mass(ProbabilityMassInput(distribution=distribution))
    assert len(result.table) > 0


def test_tail_probability_full_range_is_one() -> None:
    distribution = make_normal(NormalParams())
    result = tail_probability_of_continuous(TailProbabilityInput(distribution=distribution))
    assert math.isclose(result.probability, 1.0)


def test_tail_probability_only_lower_bound() -> None:
    distribution = make_normal(NormalParams())
    result = tail_probability_of_continuous(TailProbabilityInput(distribution=distribution, lower_bound=0.0))
    assert math.isclose(result.probability, 0.5, abs_tol=1e-6)


def test_tail_probability_only_upper_bound() -> None:
    distribution = make_normal(NormalParams())
    result = tail_probability_of_continuous(TailProbabilityInput(distribution=distribution, upper_bound=0.0))
    assert math.isclose(result.probability, 0.5, abs_tol=1e-6)


def test_quantile_of_continuous_median_for_normal() -> None:
    distribution = make_normal(NormalParams(mean=4.0, standard_deviation=1.0))
    result = quantile_of_continuous(QuantileInput(distribution=distribution, probability=0.5))
    assert math.isclose(result.quantile, 4.0)


def test_survival_complements_cdf() -> None:
    distribution = make_normal(NormalParams())
    result = survival_of_continuous(SurvivalInput(distribution=distribution, threshold=0.0))
    assert math.isclose(result.survival_probability, 0.5, abs_tol=1e-6)


def test_compute_numeric_moments_returns_finite_values() -> None:
    distribution = make_normal(NormalParams(mean=2.0, standard_deviation=3.0))
    moments = compute_numeric_moments(MomentsInput(distribution=distribution))
    assert math.isclose(moments.mean, 2.0)
    assert math.isclose(moments.standard_deviation, 3.0)
    assert math.isclose(moments.skewness, 0.0, abs_tol=1e-6)
