import pandas as pd

from core import Observations
from descriptive import detect_outliers_tukey


def test_detect_outliers_flags_extremes() -> None:
    observations = Observations.validate(pd.DataFrame({"value": [float(value) for value in range(10)] + [100.0]}))
    report = detect_outliers_tukey(observations)
    assert report.outlier_count == 1
    assert 100.0 in report.outlier_values


def test_detect_outliers_returns_empty_for_uniform_sample() -> None:
    observations = Observations.validate(pd.DataFrame({"value": [float(value) for value in range(10)]}))
    report = detect_outliers_tukey(observations)
    assert report.outlier_count == 0
