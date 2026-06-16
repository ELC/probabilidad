import math

from pydantic import BaseModel, ConfigDict, Field
from scipy import stats

_FROZEN = ConfigDict(frozen=True)


class ProportionInput(BaseModel):
    model_config = _FROZEN

    successes: int = Field(ge=0)
    sample_size: int = Field(ge=1)
    confidence_level: float = Field(default=0.95, gt=0.0, lt=1.0)


class ProportionConfidenceInterval(BaseModel):
    model_config = _FROZEN

    point_estimate: float
    lower_bound: float
    upper_bound: float
    margin_of_error: float
    critical_value: float
    standard_error: float
    confidence_level: float


def build_confidence_interval_for_proportion(input_data: ProportionInput) -> ProportionConfidenceInterval:
    if input_data.successes > input_data.sample_size:
        msg = "successes cannot exceed sample_size"
        raise ValueError(msg)
    point_estimate = input_data.successes / input_data.sample_size
    standard_error = math.sqrt(point_estimate * (1.0 - point_estimate) / input_data.sample_size)
    tail = (1.0 - input_data.confidence_level) / 2.0
    critical_value = float(stats.norm.isf(tail))
    margin_of_error = critical_value * standard_error
    return ProportionConfidenceInterval(
        point_estimate=point_estimate,
        lower_bound=max(0.0, point_estimate - margin_of_error),
        upper_bound=min(1.0, point_estimate + margin_of_error),
        margin_of_error=margin_of_error,
        critical_value=critical_value,
        standard_error=standard_error,
        confidence_level=input_data.confidence_level,
    )
