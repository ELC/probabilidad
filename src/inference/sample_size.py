import math

from pydantic import BaseModel, ConfigDict, Field
from scipy import stats

_FROZEN = ConfigDict(frozen=True)


class SampleSizeForMeanInput(BaseModel):
    model_config = _FROZEN

    population_standard_deviation: float = Field(gt=0.0)
    margin_of_error: float = Field(gt=0.0)
    confidence_level: float = Field(default=0.95, gt=0.0, lt=1.0)


class SampleSizeForProportionInput(BaseModel):
    model_config = _FROZEN

    estimated_proportion: float = Field(default=0.5, gt=0.0, lt=1.0)
    margin_of_error: float = Field(gt=0.0, lt=1.0)
    confidence_level: float = Field(default=0.95, gt=0.0, lt=1.0)


class SampleSizeResult(BaseModel):
    model_config = _FROZEN

    required_sample_size: int = Field(ge=1)
    critical_value: float
    margin_of_error: float
    confidence_level: float


def sample_size_for_mean(input_data: SampleSizeForMeanInput) -> SampleSizeResult:
    tail = (1.0 - input_data.confidence_level) / 2.0
    critical_value = float(stats.norm.isf(tail))
    minimum = (critical_value * input_data.population_standard_deviation / input_data.margin_of_error) ** 2
    return SampleSizeResult(
        required_sample_size=math.ceil(minimum),
        critical_value=critical_value,
        margin_of_error=input_data.margin_of_error,
        confidence_level=input_data.confidence_level,
    )


def sample_size_for_proportion(input_data: SampleSizeForProportionInput) -> SampleSizeResult:
    tail = (1.0 - input_data.confidence_level) / 2.0
    critical_value = float(stats.norm.isf(tail))
    variance_factor = input_data.estimated_proportion * (1.0 - input_data.estimated_proportion)
    minimum = (critical_value ** 2) * variance_factor / (input_data.margin_of_error ** 2)
    return SampleSizeResult(
        required_sample_size=math.ceil(minimum),
        critical_value=critical_value,
        margin_of_error=input_data.margin_of_error,
        confidence_level=input_data.confidence_level,
    )
