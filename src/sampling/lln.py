import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from core import RichMarkdownModel, Settings
from distributions.continuous import ContinuousDistribution
from distributions.discrete import DiscreteDistribution

_ARBITRARY = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class LLNSimulationInput(BaseModel):
    model_config = _ARBITRARY

    distribution: ContinuousDistribution | DiscreteDistribution
    horizon: int = Field(default=2_000, ge=2)
    settings: Settings = Settings()


class LLNSimulationResult(RichMarkdownModel):
    model_config = _ARBITRARY

    step: np.ndarray
    running_mean: np.ndarray
    underlying_mean: float


def simulate_lln(input_data: LLNSimulationInput) -> LLNSimulationResult:
    rng = np.random.default_rng(input_data.settings.random_seed)
    samples = input_data.distribution.frozen_distribution.rvs(size=input_data.horizon, random_state=rng)
    cumulative_sum = np.cumsum(samples)
    step = np.arange(1, input_data.horizon + 1, dtype=float)
    running_mean = cumulative_sum / step
    return LLNSimulationResult(
        step=step,
        running_mean=running_mean,
        underlying_mean=float(input_data.distribution.frozen_distribution.mean()),
    )


class LLNMultipleTrajectoriesInput(BaseModel):
    model_config = _ARBITRARY

    distribution: ContinuousDistribution | DiscreteDistribution
    horizon: int = Field(default=2_000, ge=2)
    trajectory_count: int = Field(default=20, ge=2)
    settings: Settings = Settings()


class LLNMultipleTrajectoriesResult(RichMarkdownModel):
    model_config = _ARBITRARY

    step: np.ndarray
    running_means: np.ndarray
    underlying_mean: float


def simulate_lln_multiple_trajectories(
    input_data: LLNMultipleTrajectoriesInput,
) -> LLNMultipleTrajectoriesResult:
    rng = np.random.default_rng(input_data.settings.random_seed)
    samples = input_data.distribution.frozen_distribution.rvs(
        size=(input_data.trajectory_count, input_data.horizon),
        random_state=rng,
    )
    cumulative_sum = np.cumsum(samples, axis=1)
    step = np.arange(1, input_data.horizon + 1, dtype=float)
    running_means = cumulative_sum / step
    return LLNMultipleTrajectoriesResult(
        step=step,
        running_means=running_means,
        underlying_mean=float(input_data.distribution.frozen_distribution.mean()),
    )
