import numpy as np
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from core import Observations


class StandardizedObservations(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    sample_mean: float
    sample_standard_deviation: float
    z_scores: np.ndarray


def standardize_observations(observations: DataFrame[Observations]) -> StandardizedObservations:
    values = observations["value"].to_numpy()
    sample_mean = float(np.mean(values))
    sample_standard_deviation = float(np.std(values, ddof=1))
    if sample_standard_deviation == 0.0:
        z_scores = np.zeros_like(values, dtype=float)
    else:
        z_scores = (values - sample_mean) / sample_standard_deviation
    return StandardizedObservations(
        sample_mean=sample_mean,
        sample_standard_deviation=sample_standard_deviation,
        z_scores=z_scores,
    )
