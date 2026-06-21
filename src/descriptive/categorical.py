from typing import Self

import pandas as pd
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict, model_validator

from core import CategoricalFrequencyTable


class CategoricalFrequencyTableInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    categories: tuple[str, ...]
    absolute_frequencies: tuple[int, ...]
    sort_descending: bool = False

    @model_validator(mode="after")
    def _check_inputs(self) -> Self:
        if len(self.categories) == 0:
            msg = "categories cannot be empty"
            raise ValueError(msg)
        if len(self.categories) != len(self.absolute_frequencies):
            msg = "categories and absolute_frequencies must have the same length"
            raise ValueError(msg)
        if any(frequency < 0 for frequency in self.absolute_frequencies):
            msg = "absolute_frequencies must be non-negative"
            raise ValueError(msg)
        if sum(self.absolute_frequencies) <= 0:
            msg = "absolute_frequencies must contain at least one positive value"
            raise ValueError(msg)
        return self


def build_categorical_frequency_table(
    input_data: CategoricalFrequencyTableInput,
) -> DataFrame[CategoricalFrequencyTable]:
    raw = pd.DataFrame({
        "category": input_data.categories,
        "absolute_frequency": input_data.absolute_frequencies,
    })
    if input_data.sort_descending:
        raw = raw.sort_values(
            "absolute_frequency",
            ascending=False,
            kind="stable",
            ignore_index=True,
        )
    total = raw["absolute_frequency"].sum()
    relative_frequency = raw["absolute_frequency"] / total
    cumulative_relative_frequency = relative_frequency.cumsum()
    cumulative_relative_frequency.iloc[-1] = 1.0
    table = raw.assign(
        relative_frequency=relative_frequency,
        cumulative_relative_frequency=cumulative_relative_frequency,
    )
    return table.pipe(DataFrame[CategoricalFrequencyTable])
