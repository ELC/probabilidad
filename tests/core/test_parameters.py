import pytest
from pydantic import ValidationError

from core import (
    BetaParams,
    BinomialParams,
    ChiSquareParams,
    ContinuousUniformParams,
    DiscreteUniformParams,
    ExponentialParams,
    FParams,
    GeometricParams,
    HypergeometricParams,
    NormalParams,
    PoissonParams,
    StandardNormalParams,
    StudentTParams,
)


def test_normal_params_defaults() -> None:
    parameters = NormalParams()
    assert parameters.mean == 0.0
    assert parameters.standard_deviation == 1.0


def test_normal_params_rejects_nonpositive_standard_deviation() -> None:
    with pytest.raises(ValidationError):
        NormalParams(standard_deviation=0.0)


def test_standard_normal_params_is_constructible() -> None:
    assert StandardNormalParams() == StandardNormalParams()


def test_continuous_uniform_validates_bounds() -> None:
    with pytest.raises(ValidationError):
        ContinuousUniformParams(minimum=1.0, maximum=0.0)


def test_continuous_uniform_default_is_unit_interval() -> None:
    parameters = ContinuousUniformParams()
    assert parameters.minimum == 0.0
    assert parameters.maximum == 1.0


def test_discrete_uniform_validates_bounds() -> None:
    with pytest.raises(ValidationError):
        DiscreteUniformParams(minimum=6, maximum=1)


def test_discrete_uniform_allows_single_value() -> None:
    parameters = DiscreteUniformParams(minimum=2, maximum=2)
    assert parameters.minimum == parameters.maximum == 2


def test_exponential_rejects_zero_rate() -> None:
    with pytest.raises(ValidationError):
        ExponentialParams(rate=0.0)


def test_binomial_rejects_negative_trials() -> None:
    with pytest.raises(ValidationError):
        BinomialParams(trials=0)


def test_poisson_rejects_zero_rate() -> None:
    with pytest.raises(ValidationError):
        PoissonParams(rate=0.0)


def test_geometric_validates_probability_range() -> None:
    with pytest.raises(ValidationError):
        GeometricParams(success_probability=1.5)


def test_hypergeometric_validates_counts() -> None:
    with pytest.raises(ValidationError):
        HypergeometricParams(population_size=10, success_states=20, draws=5)


def test_hypergeometric_validates_draws() -> None:
    with pytest.raises(ValidationError):
        HypergeometricParams(population_size=10, success_states=5, draws=20)


def test_chi_square_requires_positive_degrees() -> None:
    with pytest.raises(ValidationError):
        ChiSquareParams(degrees_of_freedom=0)


def test_student_t_requires_positive_degrees() -> None:
    with pytest.raises(ValidationError):
        StudentTParams(degrees_of_freedom=0.0)


def test_f_requires_positive_degrees() -> None:
    with pytest.raises(ValidationError):
        FParams(numerator_degrees_of_freedom=0, denominator_degrees_of_freedom=5)


def test_beta_requires_positive_shape() -> None:
    with pytest.raises(ValidationError):
        BetaParams(alpha=0.0)
