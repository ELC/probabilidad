import math

from pandera.typing import DataFrame

from core import Observations
from descriptive import standardize_observations


def test_standardize_has_zero_mean_unit_variance(small_observations: DataFrame[Observations]) -> None:
    standardized = standardize_observations(small_observations)
    assert math.isclose(standardized.z_scores.mean(), 0.0, abs_tol=1e-12)
    assert math.isclose(standardized.z_scores.std(ddof=1), 1.0, abs_tol=1e-10)


def test_standardize_constant_returns_zero(constant_observations: DataFrame[Observations]) -> None:
    standardized = standardize_observations(constant_observations)
    assert all(value == 0.0 for value in standardized.z_scores)
