import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from core import Settings
from distributions.continuous import ContinuousDistribution
from distributions.discrete import DiscreteDistribution

_ARBITRARY = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class CLTSimulationInput(BaseModel):
    model_config = _ARBITRARY

    distribution: ContinuousDistribution | DiscreteDistribution
    sample_size_per_replicate: int = Field(default=30, ge=1)
    replicates: int = Field(default=5_000, ge=2)
    settings: Settings = Settings()


class CLTSimulationResult(BaseModel):
    model_config = _ARBITRARY

    sample_means: np.ndarray
    standardized_means: np.ndarray
    underlying_mean: float
    underlying_standard_deviation: float
    sample_size_per_replicate: int


def simulate_clt(input_data: CLTSimulationInput) -> CLTSimulationResult:
    rng = np.random.default_rng(input_data.settings.random_seed)
    samples = input_data.distribution.frozen_distribution.rvs(
        size=(input_data.replicates, input_data.sample_size_per_replicate),
        random_state=rng,
    )
    sample_means = samples.mean(axis=1)
    underlying_mean = float(input_data.distribution.frozen_distribution.mean())
    underlying_standard_deviation = float(input_data.distribution.frozen_distribution.std())
    standard_error = underlying_standard_deviation / np.sqrt(input_data.sample_size_per_replicate)
    standardized_means = (sample_means - underlying_mean) / standard_error
    return CLTSimulationResult(
        sample_means=sample_means,
        standardized_means=standardized_means,
        underlying_mean=underlying_mean,
        underlying_standard_deviation=underlying_standard_deviation,
        sample_size_per_replicate=input_data.sample_size_per_replicate,
    )
