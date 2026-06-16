import sympy as sp
from pydantic import BaseModel, ConfigDict
from sympy.stats import Binomial, E, Exponential, Normal, Poisson, Uniform, variance

from core import (
    BinomialParams,
    ContinuousUniformParams,
    ExponentialParams,
    NormalParams,
    PoissonParams,
)


class SymbolicMoments(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    name: str
    expectation: sp.Expr
    variance: sp.Expr
    standard_deviation: sp.Expr

    @classmethod
    def from_random_variable(cls, name: str, random_variable: sp.Symbol) -> "SymbolicMoments":
        symbolic_expectation = sp.simplify(E(random_variable))
        symbolic_variance = sp.simplify(variance(random_variable))
        return cls(
            name=name,
            expectation=symbolic_expectation,
            variance=symbolic_variance,
            standard_deviation=sp.sqrt(symbolic_variance),
        )


def compute_normal_moments(parameters: NormalParams) -> SymbolicMoments:
    random_variable = Normal("X", sp.Float(parameters.mean), sp.Float(parameters.standard_deviation))
    return SymbolicMoments.from_random_variable("Normal", random_variable)


def compute_continuous_uniform_moments(parameters: ContinuousUniformParams) -> SymbolicMoments:
    random_variable = Uniform("U", sp.Float(parameters.minimum), sp.Float(parameters.maximum))
    return SymbolicMoments.from_random_variable("Uniforme continua", random_variable)


def compute_exponential_moments(parameters: ExponentialParams) -> SymbolicMoments:
    random_variable = Exponential("T", sp.Float(parameters.rate))
    return SymbolicMoments.from_random_variable("Exponencial", random_variable)


def compute_binomial_moments(parameters: BinomialParams) -> SymbolicMoments:
    random_variable = Binomial(
        "Y", parameters.trials, sp.Rational(parameters.success_probability).limit_denominator(1_000_000)
    )
    return SymbolicMoments.from_random_variable("Binomial", random_variable)


def compute_poisson_moments(parameters: PoissonParams) -> SymbolicMoments:
    random_variable = Poisson("K", sp.Float(parameters.rate))
    return SymbolicMoments.from_random_variable("Poisson", random_variable)
