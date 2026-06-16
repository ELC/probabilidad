import math
from typing import Self

import numpy as np
import pandas as pd
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict, Field, model_validator

from core import FrequencyTable, Observations


class FrequencyTableInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    observations: DataFrame[Observations]
    bin_count: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def _check_not_empty(self) -> Self:
        if self.observations.empty:
            msg = "observations cannot be empty"
            raise ValueError(msg)
        return self


def sturges_bin_count(sample_size: int) -> int:
    return max(1, math.ceil(1.0 + math.log2(sample_size)))


def build_frequency_table(input_data: FrequencyTableInput) -> DataFrame[FrequencyTable]:
    values = input_data.observations["value"].to_numpy()
    bin_count = input_data.bin_count if input_data.bin_count is not None else sturges_bin_count(values.size)
    edges = np.linspace(values.min(), values.max(), bin_count + 1)
    absolute_frequency, _ = np.histogram(values, bins=edges)
    interval_start = edges[:-1]
    interval_end = edges[1:]
    midpoint = (interval_start + interval_end) / 2.0
    relative_frequency = absolute_frequency / values.size
    cumulative_relative_frequency = np.cumsum(relative_frequency)
    cumulative_relative_frequency[-1] = 1.0
    raw = pd.DataFrame({
        "interval_start": interval_start.astype(float),
        "interval_end": interval_end.astype(float),
        "midpoint": midpoint.astype(float),
        "absolute_frequency": absolute_frequency.astype(int),
        "relative_frequency": relative_frequency.astype(float),
        "cumulative_relative_frequency": cumulative_relative_frequency.astype(float),
    })
    return FrequencyTable.validate(raw)
