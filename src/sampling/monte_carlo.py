import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from core import RichMarkdownModel, Settings
from distributions.continuous import ContinuousDistribution
from distributions.discrete import DiscreteDistribution

_ARBITRARY = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class MonteCarloInput(BaseModel):
    model_config = _ARBITRARY

    distribution: ContinuousDistribution | DiscreteDistribution
    sample_size: int = Field(ge=1)
    settings: Settings = Settings()


class MonteCarloResult(RichMarkdownModel):
    model_config = _ARBITRARY

    samples: np.ndarray
    sample_size: int


def run_monte_carlo(input_data: MonteCarloInput) -> MonteCarloResult:
    samples = input_data.distribution.frozen_distribution.rvs(
        size=input_data.sample_size,
        random_state=np.random.default_rng(input_data.settings.random_seed),
    )
    return MonteCarloResult(samples=np.asarray(samples), sample_size=input_data.sample_size)
