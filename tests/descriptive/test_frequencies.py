import math

import pandas as pd
import pytest
from pandera.typing import DataFrame
from pydantic import ValidationError

from core import Observations
from descriptive import FrequencyTableInput, build_frequency_table, sturges_bin_count


def test_sturges_formula_minimum_is_one() -> None:
    assert sturges_bin_count(1) == 1


def test_sturges_formula_grows_with_size() -> None:
    assert sturges_bin_count(10) < sturges_bin_count(1_000)


def test_build_frequency_table_uses_default_bin_count(normal_observations: DataFrame[Observations]) -> None:
    table = build_frequency_table(FrequencyTableInput(observations=normal_observations))
    assert table["absolute_frequency"].sum() == len(normal_observations)
    assert math.isclose(table["relative_frequency"].sum(), 1.0)


def test_build_frequency_table_with_explicit_bin_count(small_observations: DataFrame[Observations]) -> None:
    table = build_frequency_table(FrequencyTableInput(observations=small_observations, bin_count=4))
    assert len(table) == 4
    assert math.isclose(table["cumulative_relative_frequency"].iloc[-1], 1.0)


def test_build_frequency_table_rejects_empty() -> None:
    empty = pd.DataFrame({"value": pd.Series([], dtype=float)}).pipe(DataFrame[Observations])
    with pytest.raises(ValidationError):
        FrequencyTableInput(observations=empty)
