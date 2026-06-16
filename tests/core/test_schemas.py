import pandas as pd
import pytest
from pandera.errors import SchemaError

from core import BivariateObservations, FrequencyTable, Observations, PMFTable


def test_observations_accepts_valid_dataframe() -> None:
    Observations.validate(pd.DataFrame({"value": [1.0, 2.0, 3.0]}))


def test_observations_rejects_nulls() -> None:
    with pytest.raises(SchemaError):
        Observations.validate(pd.DataFrame({"value": [1.0, None, 3.0]}))


def test_bivariate_observations_validates_columns() -> None:
    BivariateObservations.validate(pd.DataFrame({"x": [1.0, 2.0], "y": [3.0, 4.0]}))


def test_frequency_table_rejects_out_of_range_probability() -> None:
    invalid = pd.DataFrame(
        {
            "interval_start": [0.0],
            "interval_end": [1.0],
            "midpoint": [0.5],
            "absolute_frequency": [3],
            "relative_frequency": [2.0],
            "cumulative_relative_frequency": [2.0],
        }
    )
    with pytest.raises(SchemaError):
        FrequencyTable.validate(invalid)


def test_pmf_table_rejects_negative_probability() -> None:
    invalid = pd.DataFrame({"outcome": [0.0, 1.0], "probability": [-0.1, 1.1]})
    with pytest.raises(SchemaError):
        PMFTable.validate(invalid)
