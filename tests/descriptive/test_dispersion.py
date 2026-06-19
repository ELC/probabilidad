import math

import pandas as pd
from pandera.typing import DataFrame

from core import Observations
from descriptive import compute_dispersion


def test_compute_dispersion_known_values(small_observations: DataFrame[Observations]) -> None:
    statistics = compute_dispersion(small_observations)
    assert math.isclose(statistics.sample_variance, 32 / 7)
    assert math.isclose(statistics.sample_standard_deviation, math.sqrt(32 / 7))
    assert math.isclose(statistics.range_width, 7.0)
    assert math.isclose(statistics.interquartile_range, 1.5)


def test_coefficient_of_variation_is_nan_for_zero_mean() -> None:
    observations = pd.DataFrame({"value": [-1.0, 1.0]}).pipe(DataFrame[Observations])
    statistics = compute_dispersion(observations)
    assert math.isnan(statistics.coefficient_of_variation)
