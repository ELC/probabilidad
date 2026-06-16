import sympy as sp
from pydantic import BaseModel, ConfigDict

from core import NormalParams

_ARBITRARY = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class BayesStatement(BaseModel):
    model_config = _ARBITRARY

    formula: sp.Basic
    posterior_symbol: sp.Symbol


class TotalProbabilityStatement(BaseModel):
    model_config = _ARBITRARY

    formula: sp.Basic
    partition_size: int


class StandardizationStatement(BaseModel):
    model_config = _ARBITRARY

    formula: sp.Basic
    standard_variable: sp.Symbol


def bayes_theorem() -> BayesStatement:
    likelihood, prior, evidence = sp.symbols("P_B_given_A P_A P_B", positive=True)
    posterior = sp.Symbol("P_A_given_B", positive=True)
    formula = sp.Eq(posterior, (likelihood * prior) / evidence)
    return BayesStatement(formula=formula, posterior_symbol=posterior)


def total_probability_theorem(partition_size: int = 3) -> TotalProbabilityStatement:
    index = sp.symbols("i", integer=True, positive=True)
    likelihood = sp.IndexedBase("P_B_given_A")
    prior = sp.IndexedBase("P_A")
    evidence = sp.Symbol("P_B")
    summation = sp.Sum(likelihood[index] * prior[index], (index, 1, partition_size))
    formula = sp.Eq(evidence, summation)
    return TotalProbabilityStatement(formula=formula, partition_size=partition_size)


def standardize_normal(parameters: NormalParams) -> StandardizationStatement:
    raw_variable = sp.Symbol("X", real=True)
    standard_variable = sp.Symbol("Z", real=True)
    formula = sp.Eq(standard_variable, (raw_variable - sp.Float(parameters.mean)) / sp.Float(parameters.standard_deviation))
    return StandardizationStatement(formula=formula, standard_variable=standard_variable)
