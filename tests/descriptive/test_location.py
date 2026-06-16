import math

import pandas as pd
from pandera.typing import DataFrame

from core import Observations
from descriptive import compute_location


def test_compute_location_known_values(small_observations: DataFrame[Observations]) -> None:
    statistics = compute_location(small_observations)
    assert math.isclose(statistics.mean, 5.0)
    assert math.isclose(statistics.median, 4.5)
    assert math.isclose(statistics.minimum, 2.0)
    assert math.isclose(statistics.maximum, 9.0)
    assert statistics.sample_size == 8


def test_compute_location_quartiles_known_sample() -> None:
    observations = Observations.validate(pd.DataFrame({"value": [1.0, 2.0, 3.0, 4.0, 5.0]}))
    statistics = compute_location(observations)
    assert math.isclose(statistics.first_quartile, 2.0)
    assert math.isclose(statistics.third_quartile, 4.0)
