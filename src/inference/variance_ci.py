from pydantic import BaseModel, ConfigDict, Field
from scipy import stats

from core import RichMarkdownModel

_FROZEN = ConfigDict(frozen=True)


class VarianceInput(BaseModel):
    model_config = _FROZEN

    sample_variance: float = Field(gt=0.0)
    sample_size: int = Field(ge=2)
    confidence_level: float = Field(default=0.95, gt=0.0, lt=1.0)


class VarianceConfidenceInterval(RichMarkdownModel):
    model_config = _FROZEN

    point_estimate: float
    lower_bound: float
    upper_bound: float
    lower_critical_value: float
    upper_critical_value: float
    degrees_of_freedom: int
    confidence_level: float


def build_confidence_interval_for_variance(input_data: VarianceInput) -> VarianceConfidenceInterval:
    degrees_of_freedom = input_data.sample_size - 1
    tail = (1.0 - input_data.confidence_level) / 2.0
    upper_critical_value = float(stats.chi2(df=degrees_of_freedom).isf(tail))
    lower_critical_value = float(stats.chi2(df=degrees_of_freedom).isf(1.0 - tail))
    pivot_numerator = degrees_of_freedom * input_data.sample_variance
    return VarianceConfidenceInterval(
        point_estimate=input_data.sample_variance,
        lower_bound=pivot_numerator / upper_critical_value,
        upper_bound=pivot_numerator / lower_critical_value,
        lower_critical_value=lower_critical_value,
        upper_critical_value=upper_critical_value,
        degrees_of_freedom=degrees_of_freedom,
        confidence_level=input_data.confidence_level,
    )
