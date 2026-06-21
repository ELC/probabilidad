import math

import pandas as pd
import pytest
from pandera.typing import DataFrame
from pydantic import ValidationError

from core import Observations
from descriptive import (
    CategoricalFrequencyTableInput,
    DiscreteFrequencyTableInput,
    FrequencyTableInput,
    build_categorical_frequency_table,
    build_discrete_frequency_table,
    build_frequency_table,
    sturges_bin_count,
)


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
    assert table["interval"].iloc[0] == "2.00 < x <= 3.75"
    assert table["cumulative_absolute_frequency"].iloc[-1] == len(small_observations)
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


def test_build_discrete_frequency_table() -> None:
    table = build_discrete_frequency_table(
        DiscreteFrequencyTableInput(
            exact_values=(0, 1, 2),
            absolute_frequencies=(2, 3, 5),
        )
    )
    assert table["value"].to_list() == [0, 1, 2]
    assert table["relative_frequency"].to_list() == [0.2, 0.3, 0.5]
    assert table["cumulative_absolute_frequency"].to_list() == [2, 5, 10]
    assert math.isclose(table["cumulative_relative_frequency"].iloc[-1], 1.0)


def test_build_discrete_frequency_table_rejects_mismatched_lengths() -> None:
    with pytest.raises(ValidationError):
        DiscreteFrequencyTableInput(exact_values=(0, 1), absolute_frequencies=(1,))


def test_build_discrete_frequency_table_rejects_empty_values() -> None:
    with pytest.raises(ValidationError):
        DiscreteFrequencyTableInput(exact_values=(), absolute_frequencies=())


def test_build_discrete_frequency_table_rejects_negative_frequency() -> None:
    with pytest.raises(ValidationError):
        DiscreteFrequencyTableInput(exact_values=(0, 1), absolute_frequencies=(1, -1))


def test_build_discrete_frequency_table_rejects_zero_total() -> None:
    with pytest.raises(ValidationError):
        DiscreteFrequencyTableInput(exact_values=(0, 1), absolute_frequencies=(0, 0))


def test_build_categorical_frequency_table_preserves_input_order() -> None:
    table = build_categorical_frequency_table(
        CategoricalFrequencyTableInput(
            categories=("Guardia", "Clínica médica", "Laboratorio"),
            absolute_frequencies=(22, 32, 4),
        )
    )
    assert table["category"].to_list() == ["Guardia", "Clínica médica", "Laboratorio"]
    assert table["absolute_frequency"].to_list() == [22, 32, 4]
    assert math.isclose(table["relative_frequency"].sum(), 1.0)
    assert math.isclose(table["cumulative_relative_frequency"].iloc[-1], 1.0)


def test_build_categorical_frequency_table_sorts_for_pareto() -> None:
    table = build_categorical_frequency_table(
        CategoricalFrequencyTableInput(
            categories=("A", "B", "C"),
            absolute_frequencies=(2, 5, 3),
            sort_descending=True,
        )
    )
    assert table["category"].to_list() == ["B", "C", "A"]
    assert table["absolute_frequency"].to_list() == [5, 3, 2]


def test_build_categorical_frequency_table_rejects_mismatched_lengths() -> None:
    with pytest.raises(ValidationError):
        CategoricalFrequencyTableInput(categories=("A", "B"), absolute_frequencies=(1,))


def test_build_categorical_frequency_table_rejects_empty_categories() -> None:
    with pytest.raises(ValidationError):
        CategoricalFrequencyTableInput(categories=(), absolute_frequencies=())


def test_build_categorical_frequency_table_rejects_negative_frequency() -> None:
    with pytest.raises(ValidationError):
        CategoricalFrequencyTableInput(categories=("A", "B"), absolute_frequencies=(1, -1))


def test_build_categorical_frequency_table_rejects_zero_total() -> None:
    with pytest.raises(ValidationError):
        CategoricalFrequencyTableInput(categories=("A", "B"), absolute_frequencies=(0, 0))
