import math

from core import (
    ChiSquareParams,
    ContinuousUniformParams,
    ExponentialParams,
    FParams,
    NormalParams,
    StudentTParams,
)
from distributions import (
    make_chi_square,
    make_continuous_uniform,
    make_exponential,
    make_f,
    make_normal,
    make_student_t,
)


def test_make_normal_carries_parameters() -> None:
    distribution = make_normal(NormalParams(mean=2.0, standard_deviation=3.0))
    assert math.isclose(distribution.frozen_distribution.mean(), 2.0)
    assert math.isclose(distribution.frozen_distribution.std(), 3.0)
    assert distribution.name == "normal"


def test_make_continuous_uniform_range() -> None:
    distribution = make_continuous_uniform(ContinuousUniformParams(minimum=2.0, maximum=6.0))
    assert math.isclose(distribution.frozen_distribution.mean(), 4.0)


def test_make_exponential_rate() -> None:
    distribution = make_exponential(ExponentialParams(rate=2.0))
    assert math.isclose(distribution.frozen_distribution.mean(), 0.5)


def test_make_chi_square_mean_equals_degrees() -> None:
    distribution = make_chi_square(ChiSquareParams(degrees_of_freedom=7))
    assert math.isclose(distribution.frozen_distribution.mean(), 7.0)


def test_make_student_t_carries_degrees_of_freedom() -> None:
    distribution = make_student_t(StudentTParams(degrees_of_freedom=12.0))
    assert distribution.spanish_name == "t de Student"
    assert distribution.frozen_distribution.kwds["df"] == 12.0


def test_make_f_carries_two_degrees() -> None:
    distribution = make_f(FParams(numerator_degrees_of_freedom=4, denominator_degrees_of_freedom=10))
    kwargs = distribution.frozen_distribution.kwds
    assert kwargs["dfn"] == 4
    assert kwargs["dfd"] == 10
