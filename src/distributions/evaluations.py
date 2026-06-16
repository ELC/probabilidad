from typing import Self

import numpy as np
import pandas as pd
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict, Field, model_validator

from core import PMFTable, Settings
from distributions.continuous import ContinuousDistribution
from distributions.discrete import DiscreteDistribution

_ARBITRARY = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class DensityGrid(BaseModel):
    model_config = _ARBITRARY

    grid: np.ndarray
    density: np.ndarray
    cumulative: np.ndarray
    distribution_name: str


class ProbabilityMassTable(BaseModel):
    model_config = _ARBITRARY

    table: DataFrame[PMFTable]
    distribution_name: str


class TailProbabilityResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    lower_bound: float | None = None
    upper_bound: float | None = None
    probability: float = Field(ge=0.0, le=1.0)


class QuantileResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    probability: float = Field(ge=0.0, le=1.0)
    quantile: float


class SurvivalResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    threshold: float
    survival_probability: float = Field(ge=0.0, le=1.0)


class DensityGridInput(BaseModel):
    model_config = _ARBITRARY

    distribution: ContinuousDistribution
    lower_quantile: float = Field(default=0.001, gt=0.0, lt=1.0)
    upper_quantile: float = Field(default=0.999, gt=0.0, lt=1.0)
    settings: Settings = Settings()

    @model_validator(mode="after")
    def _validate_quantiles(self) -> Self:
        if self.lower_quantile >= self.upper_quantile:
            msg = "lower_quantile must be strictly less than upper_quantile"
            raise ValueError(msg)
        return self


class ProbabilityMassInput(BaseModel):
    model_config = _ARBITRARY

    distribution: DiscreteDistribution
    lower_outcome: int | None = None
    upper_outcome: int | None = None


class TailProbabilityInput(BaseModel):
    model_config = _ARBITRARY

    distribution: ContinuousDistribution
    lower_bound: float | None = None
    upper_bound: float | None = None


class QuantileInput(BaseModel):
    model_config = _ARBITRARY

    distribution: ContinuousDistribution
    probability: float = Field(ge=0.0, le=1.0)


class SurvivalInput(BaseModel):
    model_config = _ARBITRARY

    distribution: ContinuousDistribution
    threshold: float


def evaluate_density_grid(input_data: DensityGridInput) -> DensityGrid:
    grid = np.linspace(
        input_data.distribution.frozen_distribution.ppf(input_data.lower_quantile),
        input_data.distribution.frozen_distribution.ppf(input_data.upper_quantile),
        input_data.settings.grid_resolution,
    )
    density = input_data.distribution.frozen_distribution.pdf(grid)
    cumulative = input_data.distribution.frozen_distribution.cdf(grid)
    return DensityGrid(
        grid=grid,
        density=density,
        cumulative=cumulative,
        distribution_name=input_data.distribution.spanish_name,
    )


def evaluate_probability_mass(input_data: ProbabilityMassInput) -> ProbabilityMassTable:
    frozen = input_data.distribution.frozen_distribution
    lower = input_data.lower_outcome if input_data.lower_outcome is not None else int(frozen.ppf(0.001))
    upper = input_data.upper_outcome if input_data.upper_outcome is not None else int(frozen.ppf(0.999))
    outcomes = np.arange(lower, upper + 1, dtype=float)
    probabilities = frozen.pmf(outcomes)
    raw_table = pd.DataFrame({"outcome": outcomes, "probability": probabilities})
    table = PMFTable.validate(raw_table)
    return ProbabilityMassTable(table=table, distribution_name=input_data.distribution.spanish_name)


def tail_probability_of_continuous(input_data: TailProbabilityInput) -> TailProbabilityResult:
    frozen = input_data.distribution.frozen_distribution
    lower_cumulative = 0.0 if input_data.lower_bound is None else float(frozen.cdf(input_data.lower_bound))
    upper_cumulative = 1.0 if input_data.upper_bound is None else float(frozen.cdf(input_data.upper_bound))
    return TailProbabilityResult(
        lower_bound=input_data.lower_bound,
        upper_bound=input_data.upper_bound,
        probability=max(0.0, min(1.0, upper_cumulative - lower_cumulative)),
    )


def quantile_of_continuous(input_data: QuantileInput) -> QuantileResult:
    return QuantileResult(
        probability=input_data.probability,
        quantile=float(input_data.distribution.frozen_distribution.ppf(input_data.probability)),
    )


def survival_of_continuous(input_data: SurvivalInput) -> SurvivalResult:
    return SurvivalResult(
        threshold=input_data.threshold,
        survival_probability=float(input_data.distribution.frozen_distribution.sf(input_data.threshold)),
    )


class DistributionMoments(BaseModel):
    model_config = ConfigDict(frozen=True)

    mean: float
    variance: float
    standard_deviation: float
    skewness: float
    excess_kurtosis: float


class MomentsInput(BaseModel):
    model_config = _ARBITRARY

    distribution: ContinuousDistribution | DiscreteDistribution


def compute_numeric_moments(input_data: MomentsInput) -> DistributionMoments:
    mean, variance, skewness, excess_kurtosis = input_data.distribution.frozen_distribution.stats(moments="mvsk")
    return DistributionMoments(
        mean=float(mean),
        variance=float(variance),
        standard_deviation=float(np.sqrt(float(variance))),
        skewness=float(skewness),
        excess_kurtosis=float(excess_kurtosis),
    )
