import math

from pydantic import BaseModel, ConfigDict, Field
from scipy import stats

from core import RichMarkdownModel

_FROZEN = ConfigDict(frozen=True)


class MeanKnownVarianceInput(BaseModel):
    model_config = _FROZEN

    sample_mean: float
    population_standard_deviation: float = Field(gt=0.0)
    sample_size: int = Field(ge=1)
    confidence_level: float = Field(default=0.95, gt=0.0, lt=1.0)


class MeanUnknownVarianceInput(BaseModel):
    model_config = _FROZEN

    sample_mean: float
    sample_standard_deviation: float = Field(gt=0.0)
    sample_size: int = Field(ge=2)
    confidence_level: float = Field(default=0.95, gt=0.0, lt=1.0)


class MeanConfidenceInterval(RichMarkdownModel):
    model_config = _FROZEN

    point_estimate: float
    lower_bound: float
    upper_bound: float
    margin_of_error: float
    critical_value: float
    standard_error: float
    confidence_level: float


def build_confidence_interval_for_mean_known_variance(input_data: MeanKnownVarianceInput) -> MeanConfidenceInterval:
    tail = (1.0 - input_data.confidence_level) / 2.0
    critical_value = float(stats.norm.isf(tail))
    standard_error = input_data.population_standard_deviation / math.sqrt(input_data.sample_size)
    margin_of_error = critical_value * standard_error
    return MeanConfidenceInterval(
        point_estimate=input_data.sample_mean,
        lower_bound=input_data.sample_mean - margin_of_error,
        upper_bound=input_data.sample_mean + margin_of_error,
        margin_of_error=margin_of_error,
        critical_value=critical_value,
        standard_error=standard_error,
        confidence_level=input_data.confidence_level,
    )


def build_confidence_interval_for_mean_unknown_variance(input_data: MeanUnknownVarianceInput) -> MeanConfidenceInterval:
    tail = (1.0 - input_data.confidence_level) / 2.0
    degrees_of_freedom = input_data.sample_size - 1
    critical_value = float(stats.t(df=degrees_of_freedom).isf(tail))
    standard_error = input_data.sample_standard_deviation / math.sqrt(input_data.sample_size)
    margin_of_error = critical_value * standard_error
    return MeanConfidenceInterval(
        point_estimate=input_data.sample_mean,
        lower_bound=input_data.sample_mean - margin_of_error,
        upper_bound=input_data.sample_mean + margin_of_error,
        margin_of_error=margin_of_error,
        critical_value=critical_value,
        standard_error=standard_error,
        confidence_level=input_data.confidence_level,
    )
