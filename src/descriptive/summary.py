from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from core import Observations
from descriptive.dispersion import DispersionStatistics, compute_dispersion
from descriptive.location import LocationStatistics, compute_location
from descriptive.outliers import OutlierReport, detect_outliers_tukey


class DescriptiveStatistics(BaseModel):
    model_config = ConfigDict(frozen=True)

    location: LocationStatistics
    dispersion: DispersionStatistics
    outliers: OutlierReport


def summarize_observations(observations: DataFrame[Observations]) -> DescriptiveStatistics:
    return DescriptiveStatistics(
        location=compute_location(observations),
        dispersion=compute_dispersion(observations),
        outliers=detect_outliers_tukey(observations),
    )
