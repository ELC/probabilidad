from typing import Any

from pydantic import BaseModel, ConfigDict
from scipy import stats

from core import (
    ChiSquareParams,
    ContinuousUniformParams,
    ExponentialParams,
    FParams,
    NormalParams,
    StudentTParams,
)


class ContinuousDistribution(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    name: str
    spanish_name: str
    frozen_distribution: Any


def make_normal(parameters: NormalParams) -> ContinuousDistribution:
    return ContinuousDistribution(
        name="normal",
        spanish_name="Normal",
        frozen_distribution=stats.norm(loc=parameters.mean, scale=parameters.standard_deviation),
    )


def make_continuous_uniform(parameters: ContinuousUniformParams) -> ContinuousDistribution:
    width = parameters.maximum - parameters.minimum
    return ContinuousDistribution(
        name="continuous_uniform",
        spanish_name="Uniforme continua",
        frozen_distribution=stats.uniform(loc=parameters.minimum, scale=width),
    )


def make_exponential(parameters: ExponentialParams) -> ContinuousDistribution:
    return ContinuousDistribution(
        name="exponential",
        spanish_name="Exponencial",
        frozen_distribution=stats.expon(scale=1.0 / parameters.rate),
    )


def make_chi_square(parameters: ChiSquareParams) -> ContinuousDistribution:
    return ContinuousDistribution(
        name="chi_square",
        spanish_name="Chi cuadrado",
        frozen_distribution=stats.chi2(df=parameters.degrees_of_freedom),
    )


def make_student_t(parameters: StudentTParams) -> ContinuousDistribution:
    return ContinuousDistribution(
        name="student_t",
        spanish_name="t de Student",
        frozen_distribution=stats.t(df=parameters.degrees_of_freedom),
    )


def make_f(parameters: FParams) -> ContinuousDistribution:
    return ContinuousDistribution(
        name="f",
        spanish_name="F de Fisher",
        frozen_distribution=stats.f(
            dfn=parameters.numerator_degrees_of_freedom,
            dfd=parameters.denominator_degrees_of_freedom,
        ),
    )
