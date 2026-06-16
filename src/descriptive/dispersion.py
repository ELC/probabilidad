import numpy as np
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from core import Observations


class DispersionStatistics(BaseModel):
    model_config = ConfigDict(frozen=True)

    sample_variance: float
    sample_standard_deviation: float
    range_width: float
    interquartile_range: float
    coefficient_of_variation: float


def compute_dispersion(observations: DataFrame[Observations]) -> DispersionStatistics:
    values = observations["value"].to_numpy()
    sample_variance = float(np.var(values, ddof=1))
    sample_standard_deviation = float(np.sqrt(sample_variance))
    first_quartile, third_quartile = np.quantile(values, [0.25, 0.75])
    mean = float(np.mean(values))
    coefficient_of_variation = sample_standard_deviation / mean if mean != 0.0 else float("nan")
    return DispersionStatistics(
        sample_variance=sample_variance,
        sample_standard_deviation=sample_standard_deviation,
        range_width=float(np.max(values) - np.min(values)),
        interquartile_range=float(third_quartile - first_quartile),
        coefficient_of_variation=coefficient_of_variation,
    )
