import numpy as np
from pandera.typing import DataFrame
from pydantic import ConfigDict

from core import Observations, RichMarkdownModel


class LocationStatistics(RichMarkdownModel):
    model_config = ConfigDict(frozen=True)

    mean: float
    median: float
    first_quartile: float
    third_quartile: float
    minimum: float
    maximum: float
    sample_size: int


def compute_location(observations: DataFrame[Observations]) -> LocationStatistics:
    values = observations["value"].to_numpy()
    quartiles = np.quantile(values, [0.25, 0.5, 0.75])
    return LocationStatistics(
        mean=float(np.mean(values)),
        median=float(quartiles[1]),
        first_quartile=float(quartiles[0]),
        third_quartile=float(quartiles[2]),
        minimum=float(np.min(values)),
        maximum=float(np.max(values)),
        sample_size=int(values.size),
    )
