import pandera.pandas as pa
from pandera.typing import Series


class Observations(pa.DataFrameModel):
    value: Series[float] = pa.Field(nullable=False)


class BivariateObservations(pa.DataFrameModel):
    x: Series[float] = pa.Field(nullable=False)
    y: Series[float] = pa.Field(nullable=False)


class FrequencyTable(pa.DataFrameModel):
    interval_start: Series[float] = pa.Field(nullable=False)
    interval_end: Series[float] = pa.Field(nullable=False)
    midpoint: Series[float] = pa.Field(nullable=False)
    absolute_frequency: Series[int] = pa.Field(ge=0)
    relative_frequency: Series[float] = pa.Field(ge=0.0, le=1.0)
    cumulative_relative_frequency: Series[float] = pa.Field(ge=0.0, le=1.0)


class PMFTable(pa.DataFrameModel):
    outcome: Series[float] = pa.Field(nullable=False)
    probability: Series[float] = pa.Field(ge=0.0, le=1.0)
