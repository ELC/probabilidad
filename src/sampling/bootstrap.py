from typing import Self

import numpy as np
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict, Field, model_validator

from core import Observations, RichMarkdownModel, Settings

_ARBITRARY = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class BootstrapInput(BaseModel):
    model_config = _ARBITRARY

    observations: DataFrame[Observations]
    replicates: int = Field(default=5_000, ge=2)
    confidence_level: float = Field(default=0.95, gt=0.0, lt=1.0)
    settings: Settings = Settings()

    @model_validator(mode="after")
    def _check_not_empty(self) -> Self:
        if self.observations.empty:
            msg = "observations cannot be empty"
            raise ValueError(msg)
        return self


class BootstrapMeanResult(RichMarkdownModel):
    model_config = _ARBITRARY

    bootstrap_means: np.ndarray
    point_estimate: float
    lower_quantile: float
    upper_quantile: float
    confidence_level: float


def bootstrap_mean(input_data: BootstrapInput) -> BootstrapMeanResult:
    rng = np.random.default_rng(input_data.settings.random_seed)
    values = input_data.observations["value"].to_numpy()
    indexes = rng.integers(low=0, high=values.size, size=(input_data.replicates, values.size))
    bootstrap_means = values[indexes].mean(axis=1)
    tail = (1.0 - input_data.confidence_level) / 2.0
    lower_quantile, upper_quantile = np.quantile(bootstrap_means, [tail, 1.0 - tail])
    return BootstrapMeanResult(
        bootstrap_means=bootstrap_means,
        point_estimate=float(values.mean()),
        lower_quantile=float(lower_quantile),
        upper_quantile=float(upper_quantile),
        confidence_level=input_data.confidence_level,
    )
