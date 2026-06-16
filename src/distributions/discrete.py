from typing import Any

from pydantic import BaseModel, ConfigDict
from scipy import stats

from core import (
    BinomialParams,
    DiscreteUniformParams,
    GeometricParams,
    HypergeometricParams,
    PoissonParams,
)


class DiscreteDistribution(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    name: str
    spanish_name: str
    frozen_distribution: Any


def make_binomial(parameters: BinomialParams) -> DiscreteDistribution:
    return DiscreteDistribution(
        name="binomial",
        spanish_name="Binomial",
        frozen_distribution=stats.binom(n=parameters.trials, p=parameters.success_probability),
    )


def make_poisson(parameters: PoissonParams) -> DiscreteDistribution:
    return DiscreteDistribution(
        name="poisson",
        spanish_name="Poisson",
        frozen_distribution=stats.poisson(mu=parameters.rate),
    )


def make_geometric(parameters: GeometricParams) -> DiscreteDistribution:
    return DiscreteDistribution(
        name="geometric",
        spanish_name="Geométrica",
        frozen_distribution=stats.geom(p=parameters.success_probability),
    )


def make_hypergeometric(parameters: HypergeometricParams) -> DiscreteDistribution:
    return DiscreteDistribution(
        name="hypergeometric",
        spanish_name="Hipergeométrica",
        frozen_distribution=stats.hypergeom(
            M=parameters.population_size,
            n=parameters.success_states,
            N=parameters.draws,
        ),
    )


def make_discrete_uniform(parameters: DiscreteUniformParams) -> DiscreteDistribution:
    return DiscreteDistribution(
        name="discrete_uniform",
        spanish_name="Uniforme discreta",
        frozen_distribution=stats.randint(low=parameters.minimum, high=parameters.maximum + 1),
    )
