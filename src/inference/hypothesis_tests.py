import math
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field
from scipy import stats

_FROZEN = ConfigDict(frozen=True)


class Alternative(StrEnum):
    TWO_SIDED = "two_sided"
    GREATER = "greater"
    LESS = "less"


class OneSampleMeanTestInput(BaseModel):
    model_config = _FROZEN

    sample_mean: float
    sample_standard_deviation: float = Field(gt=0.0)
    sample_size: int = Field(ge=2)
    null_mean: float
    alternative: Alternative = Alternative.TWO_SIDED
    significance_level: float = Field(default=0.05, gt=0.0, lt=1.0)


class OneSampleMeanTestResult(BaseModel):
    model_config = _FROZEN

    test_statistic: float
    degrees_of_freedom: int
    p_value: float = Field(ge=0.0, le=1.0)
    reject_null: bool
    alternative: Alternative


def _p_value_from_t(test_statistic: float, degrees_of_freedom: int, alternative: Alternative) -> float:
    distribution = stats.t(df=degrees_of_freedom)
    if alternative is Alternative.TWO_SIDED:
        return float(2.0 * distribution.sf(abs(test_statistic)))
    if alternative is Alternative.GREATER:
        return float(distribution.sf(test_statistic))
    return float(distribution.cdf(test_statistic))


def test_one_sample_mean(input_data: OneSampleMeanTestInput) -> OneSampleMeanTestResult:
    standard_error = input_data.sample_standard_deviation / math.sqrt(input_data.sample_size)
    test_statistic = (input_data.sample_mean - input_data.null_mean) / standard_error
    degrees_of_freedom = input_data.sample_size - 1
    p_value = _p_value_from_t(test_statistic, degrees_of_freedom, input_data.alternative)
    return OneSampleMeanTestResult(
        test_statistic=test_statistic,
        degrees_of_freedom=degrees_of_freedom,
        p_value=p_value,
        reject_null=p_value < input_data.significance_level,
        alternative=input_data.alternative,
    )


class OneSampleProportionTestInput(BaseModel):
    model_config = _FROZEN

    successes: int = Field(ge=0)
    sample_size: int = Field(ge=1)
    null_proportion: float = Field(gt=0.0, lt=1.0)
    alternative: Alternative = Alternative.TWO_SIDED
    significance_level: float = Field(default=0.05, gt=0.0, lt=1.0)


class OneSampleProportionTestResult(BaseModel):
    model_config = _FROZEN

    test_statistic: float
    p_value: float = Field(ge=0.0, le=1.0)
    reject_null: bool
    alternative: Alternative


def _p_value_from_z(test_statistic: float, alternative: Alternative) -> float:
    if alternative is Alternative.TWO_SIDED:
        return float(2.0 * stats.norm.sf(abs(test_statistic)))
    if alternative is Alternative.GREATER:
        return float(stats.norm.sf(test_statistic))
    return float(stats.norm.cdf(test_statistic))


def test_one_sample_proportion(input_data: OneSampleProportionTestInput) -> OneSampleProportionTestResult:
    if input_data.successes > input_data.sample_size:
        msg = "successes cannot exceed sample_size"
        raise ValueError(msg)
    point_estimate = input_data.successes / input_data.sample_size
    null_variance = input_data.null_proportion * (1.0 - input_data.null_proportion) / input_data.sample_size
    test_statistic = (point_estimate - input_data.null_proportion) / math.sqrt(null_variance)
    p_value = _p_value_from_z(test_statistic, input_data.alternative)
    return OneSampleProportionTestResult(
        test_statistic=test_statistic,
        p_value=p_value,
        reject_null=p_value < input_data.significance_level,
        alternative=input_data.alternative,
    )
