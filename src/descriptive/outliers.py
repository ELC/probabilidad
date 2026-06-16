import numpy as np
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from core import Observations


class OutlierReport(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    lower_fence: float
    upper_fence: float
    outlier_values: np.ndarray
    outlier_count: int


def detect_outliers_tukey(observations: DataFrame[Observations], whisker_factor: float = 1.5) -> OutlierReport:
    values = observations["value"].to_numpy()
    first_quartile, third_quartile = np.quantile(values, [0.25, 0.75])
    interquartile_range = third_quartile - first_quartile
    lower_fence = float(first_quartile - whisker_factor * interquartile_range)
    upper_fence = float(third_quartile + whisker_factor * interquartile_range)
    mask = (values < lower_fence) | (values > upper_fence)
    outlier_values = values[mask]
    return OutlierReport(
        lower_fence=lower_fence,
        upper_fence=upper_fence,
        outlier_values=outlier_values,
        outlier_count=int(outlier_values.size),
    )
