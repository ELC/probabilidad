import math
from typing import Self

import numpy as np
import pandas as pd
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict, Field, model_validator

from core import DiscreteFrequencyTable, FrequencyTable, Observations


class FrequencyTableInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    observations: DataFrame[Observations]
    bin_count: int | None = Field(default=None, ge=1)
    bin_width: float | None = Field(default=None, gt=0.0)

    @model_validator(mode="after")
    def _check_inputs(self) -> Self:
        if self.observations.empty:
            msg = "observations cannot be empty"
            raise ValueError(msg)
        if self.bin_count is not None and self.bin_width is not None:
            msg = "bin_count and bin_width cannot be used together"
            raise ValueError(msg)
        return self


class DiscreteFrequencyTableInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    exact_values: tuple[int, ...]
    absolute_frequencies: tuple[int, ...]

    @model_validator(mode="after")
    def _check_inputs(self) -> Self:
        if len(self.exact_values) == 0:
            msg = "exact_values cannot be empty"
            raise ValueError(msg)
        if len(self.exact_values) != len(self.absolute_frequencies):
            msg = "exact_values and absolute_frequencies must have the same length"
            raise ValueError(msg)
        if any(frequency < 0 for frequency in self.absolute_frequencies):
            msg = "absolute_frequencies must be non-negative"
            raise ValueError(msg)
        if sum(self.absolute_frequencies) <= 0:
            msg = "absolute_frequencies must contain at least one positive value"
            raise ValueError(msg)
        return self


def sturges_bin_count(sample_size: int) -> int:
    return max(1, math.ceil(1.0 + math.log2(sample_size)))


def _build_equal_width_edges(values: np.ndarray, bin_width: float) -> np.ndarray:
    interval_start = math.floor(float(values.min()) / bin_width) * bin_width
    interval_end = math.ceil(float(values.max()) / bin_width) * bin_width
    if math.isclose(interval_start, interval_end):
        interval_end = interval_start + bin_width
    edges = np.arange(interval_start, interval_end + bin_width, bin_width, dtype=float)
    edges[-1] = interval_end
    return edges


def build_frequency_table(input_data: FrequencyTableInput) -> DataFrame[FrequencyTable]:
    values = input_data.observations["value"].to_numpy()
    if input_data.bin_width is not None:
        edges = _build_equal_width_edges(values, input_data.bin_width)
    else:
        bin_count = input_data.bin_count if input_data.bin_count is not None else sturges_bin_count(values.size)
        edges = np.linspace(values.min(), values.max(), bin_count + 1)
    absolute_frequency, _ = np.histogram(values, bins=edges)
    interval_start = edges[:-1]
    interval_end = edges[1:]
    midpoint = (interval_start + interval_end) / 2.0
    relative_frequency = absolute_frequency / values.size
    cumulative_absolute_frequency = np.cumsum(absolute_frequency)
    cumulative_relative_frequency = np.cumsum(relative_frequency)
    cumulative_relative_frequency[-1] = 1.0
    raw = pd.DataFrame({
        "interval": [
            f"${start:.2f} \\lt x \\le {end:.2f}$"
            for start, end in zip(interval_start, interval_end, strict=True)
        ],
        "interval_start": interval_start.astype(float),
        "interval_end": interval_end.astype(float),
        "midpoint": midpoint.astype(float),
        "absolute_frequency": absolute_frequency.astype(int),
        "relative_frequency": relative_frequency.astype(float),
        "cumulative_absolute_frequency": cumulative_absolute_frequency.astype(int),
        "cumulative_relative_frequency": cumulative_relative_frequency.astype(float),
    })
    return raw.pipe(DataFrame[FrequencyTable])


def build_discrete_frequency_table(
    input_data: DiscreteFrequencyTableInput,
) -> DataFrame[DiscreteFrequencyTable]:
    raw = pd.DataFrame({
        "value": input_data.exact_values,
        "absolute_frequency": input_data.absolute_frequencies,
    })
    total = raw["absolute_frequency"].sum()
    relative_frequency = raw["absolute_frequency"] / total
    cumulative_relative_frequency = relative_frequency.cumsum()
    cumulative_relative_frequency.iloc[-1] = 1.0
    table = raw.assign(
        relative_frequency=relative_frequency,
        cumulative_absolute_frequency=raw["absolute_frequency"].cumsum(),
        cumulative_relative_frequency=cumulative_relative_frequency,
    )
    return table.pipe(DataFrame[DiscreteFrequencyTable])
