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


def test_build_frequency_table_with_explicit_bin_width(small_observations: DataFrame[Observations]) -> None:
    table = build_frequency_table(FrequencyTableInput(observations=small_observations, bin_width=2.0))
    assert table["interval_start"].to_list() == [2.0, 4.0, 6.0, 8.0]
    assert table["interval_end"].to_list() == [4.0, 6.0, 8.0, 10.0]
    assert table["midpoint"].to_list() == [3.0, 5.0, 7.0, 9.0]
    assert table["absolute_frequency"].to_list() == [1, 5, 1, 1]


def test_build_frequency_table_with_bin_width_for_constant_edge_values() -> None:
    constant_observations = pd.DataFrame({"value": [4.0, 4.0, 4.0, 4.0]}).pipe(DataFrame[Observations])
    table = build_frequency_table(FrequencyTableInput(observations=constant_observations, bin_width=2.0))
    assert table["interval_start"].to_list() == [4.0]
    assert table["interval_end"].to_list() == [6.0]
    assert table["midpoint"].to_list() == [5.0]
    assert table["absolute_frequency"].to_list() == [4]


def test_build_frequency_table_rejects_bin_count_with_bin_width(
    small_observations: DataFrame[Observations],
) -> None:
    with pytest.raises(ValidationError):
        FrequencyTableInput(observations=small_observations, bin_count=4, bin_width=2.0)


def test_build_frequency_table_rejects_empty() -> None:
    empty = pd.DataFrame({"value": pd.Series([], dtype=float)}).pipe(DataFrame[Observations])
    with pytest.raises(ValidationError):
        FrequencyTableInput(observations=empty)
