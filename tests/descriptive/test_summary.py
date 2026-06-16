from pandera.typing import DataFrame

from core import Observations
from descriptive import summarize_observations


def test_summarize_returns_three_blocks(small_observations: DataFrame[Observations]) -> None:
    statistics = summarize_observations(small_observations)
    assert statistics.location.sample_size == 8
    assert statistics.dispersion.sample_variance > 0.0
    assert statistics.outliers.outlier_count >= 0
