from typing import cast

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from pandas.io.formats.style import Styler
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict, Field

from core import (
    CategoricalFrequencyTable,
    DiscreteFrequencyTable,
    FrequencyTable,
    Observations,
    Settings,
    TabularData,
)
from descriptive.categorical import CategoricalFrequencyTableInput, build_categorical_frequency_table
from descriptive.frequencies import (
    DiscreteFrequencyTableInput,
    FrequencyTableInput,
    build_discrete_frequency_table,
    build_frequency_table,
)

_AREA_CATEGORIES = ("Guardia", "Clínica médica", "Laboratorio", "Pediatría", "Traumatología")
_AREA_WEIGHTS = np.array([22, 32, 4, 14, 8])
_DELAY_REASON_CATEGORIES = (
    "Ninguna",
    "Admisión administrativa lenta",
    "Consulta anterior extendida",
    "Autorización de cobertura",
    "Laboratorio previo demorado",
    "Llegada fuera de horario",
    "Derivación entre áreas",
)
_DELAY_REASON_WEIGHTS = np.array([25, 18, 15, 9, 6, 4, 3])
_PEOPLE_AHEAD_VALUES = (0, 1, 2, 3, 4, 5, 6, 7)
_PEOPLE_AHEAD_WEIGHTS = np.array([5, 9, 13, 18, 16, 10, 6, 3])


class ClinicSampleInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    settings: Settings = Settings()
    sample_size: int = Field(default=80, ge=1)
    waiting_time_mean: float = 4.0
    waiting_time_standard_deviation: float = Field(default=1.2, gt=0.0)
    waiting_time_bin_width: float = Field(default=1.0, gt=0.0)


class ClinicSample(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    clinic_data: DataFrame[TabularData]
    clinic_display_table: DataFrame[TabularData]
    waiting_times: DataFrame[Observations]
    frequency_table: DataFrame[FrequencyTable]
    area_frequency_table: DataFrame[CategoricalFrequencyTable]
    delay_reason_frequency_table: DataFrame[CategoricalFrequencyTable]
    people_ahead_frequency_table: DataFrame[DiscreteFrequencyTable]
    area_display_table: DataFrame[TabularData]
    delay_reason_display_table: DataFrame[TabularData]
    people_ahead_display_table: DataFrame[TabularData]
    frequency_display_table: DataFrame[TabularData]
    area_categories: tuple[str, ...]
    delay_reason_categories: tuple[str, ...]
    people_ahead_values: tuple[int, ...]


def _probabilities(weights: NDArray[np.int_]) -> NDArray[np.float64]:
    return cast("NDArray[np.float64]", weights / weights.sum())


def _categorical_display_table(
    frequency_table: DataFrame[CategoricalFrequencyTable],
    *,
    category_label: str,
    include_cumulative: bool = False,
) -> DataFrame[TabularData]:
    columns = {
        category_label: frequency_table["category"],
        "$n_k$": frequency_table["absolute_frequency"],
        "$f_k$": frequency_table["relative_frequency"].round(2),
    }
    if include_cumulative:
        columns["$F_k$"] = frequency_table["cumulative_relative_frequency"].round(2)
    return pd.DataFrame(columns).pipe(DataFrame[TabularData])


def _discrete_display_table(frequency_table: DataFrame[DiscreteFrequencyTable]) -> DataFrame[TabularData]:
    return pd.DataFrame({
        "$x_k$": frequency_table["value"],
        "$n_k$": frequency_table["absolute_frequency"],
        "$f_k$": frequency_table["relative_frequency"].round(2),
        "$N_k$": frequency_table["cumulative_absolute_frequency"],
        "$F_k$": frequency_table["cumulative_relative_frequency"].round(2),
    }).pipe(DataFrame[TabularData])


def _continuous_display_table(frequency_table: DataFrame[FrequencyTable]) -> DataFrame[TabularData]:
    return pd.DataFrame({
        "Intervalo": frequency_table["interval"],
        "$x_k$": frequency_table["midpoint"].round(2),
        "$n_k$": frequency_table["absolute_frequency"],
        "$f_k$": frequency_table["relative_frequency"].round(2),
        "$N_k$": frequency_table["cumulative_absolute_frequency"],
        "$F_k$": frequency_table["cumulative_relative_frequency"].round(2),
    }).pipe(DataFrame[TabularData])


def _clinic_display_table(clinic_data: DataFrame[TabularData]) -> DataFrame[TabularData]:
    return pd.DataFrame({
        "Minutos de espera": clinic_data["value"].round(2),
        "Área de atención": clinic_data["area"],
        "Motivo de demora": clinic_data["delay_reason"],
        "Personas adelante": clinic_data["people_ahead"],
    }).pipe(DataFrame[TabularData])


def _first_column_min_width(table: pd.DataFrame) -> str:
    longest_label = int(table.iloc[:, 0].astype(str).str.len().max())
    return f"{max(280, longest_label * 10 + 24)}px"


def style_display_table(table: pd.DataFrame) -> Styler:
    float_columns = list(table.select_dtypes(include=[float]).columns)
    styler = table.style.hide(axis="index")
    if float_columns:
        styler = styler.format("{:.2f}", subset=float_columns)
    first_column_min_width = _first_column_min_width(table)
    first_column_styles = [
        ("min-width", first_column_min_width),
        ("white-space", "nowrap"),
        ("text-align", "right !important"),
    ]
    table_styles = [
        {"selector": "th.col0", "props": first_column_styles},
        {"selector": "td.col0", "props": first_column_styles},
    ]
    for column_index in range(1, table.shape[1]):
        centered = [("text-align", "center !important")]
        table_styles.extend([
            {"selector": f"th.col{column_index}", "props": centered},
            {"selector": f"td.col{column_index}", "props": centered},
        ])
    return styler.set_table_styles(table_styles)


def generate_clinic_sample(input_data: ClinicSampleInput) -> ClinicSample:
    rng_clinic = np.random.default_rng(input_data.settings.random_seed)
    raw_waiting_times = rng_clinic.normal(
        loc=input_data.waiting_time_mean,
        scale=input_data.waiting_time_standard_deviation,
        size=input_data.sample_size,
    ).clip(min=0.0)
    area_absolute_frequencies = tuple(rng_clinic.multinomial(input_data.sample_size, _probabilities(_AREA_WEIGHTS)))
    delay_reason_absolute_frequencies = tuple(
        rng_clinic.multinomial(input_data.sample_size, _probabilities(_DELAY_REASON_WEIGHTS))
    )
    people_ahead_absolute_frequencies = tuple(
        rng_clinic.multinomial(input_data.sample_size, _probabilities(_PEOPLE_AHEAD_WEIGHTS))
    )
    clinic_data = pd.DataFrame({
        "value": raw_waiting_times,
        "area": rng_clinic.permutation(np.repeat(_AREA_CATEGORIES, area_absolute_frequencies)),
        "delay_reason": rng_clinic.permutation(np.repeat(_DELAY_REASON_CATEGORIES, delay_reason_absolute_frequencies)),
        "people_ahead": rng_clinic.permutation(np.repeat(_PEOPLE_AHEAD_VALUES, people_ahead_absolute_frequencies)),
    }).pipe(DataFrame[TabularData])
    waiting_times = clinic_data[["value"]].pipe(DataFrame[Observations])
    frequency_table = build_frequency_table(
        FrequencyTableInput(
            observations=waiting_times,
            bin_width=input_data.waiting_time_bin_width,
        )
    )
    area_counts = clinic_data["area"].value_counts(sort=False).reindex(_AREA_CATEGORIES)
    area_frequency_table = build_categorical_frequency_table(
        CategoricalFrequencyTableInput(
            categories=_AREA_CATEGORIES,
            absolute_frequencies=tuple(area_counts.astype(int)),
        )
    )
    delay_reason_counts = clinic_data["delay_reason"].value_counts(sort=False).reindex(_DELAY_REASON_CATEGORIES)
    pareto_delay_reason_counts = delay_reason_counts.drop("Ninguna")
    delay_reason_frequency_table = build_categorical_frequency_table(
        CategoricalFrequencyTableInput(
            categories=tuple(pareto_delay_reason_counts.index),
            absolute_frequencies=tuple(pareto_delay_reason_counts.astype(int)),
            sort_descending=True,
        )
    )
    people_ahead_counts = clinic_data["people_ahead"].value_counts(sort=False).reindex(_PEOPLE_AHEAD_VALUES)
    people_ahead_frequency_table = build_discrete_frequency_table(
        DiscreteFrequencyTableInput(
            exact_values=_PEOPLE_AHEAD_VALUES,
            absolute_frequencies=tuple(people_ahead_counts.astype(int)),
        )
    )
    return ClinicSample(
        clinic_data=clinic_data,
        clinic_display_table=_clinic_display_table(clinic_data),
        waiting_times=waiting_times,
        frequency_table=frequency_table,
        area_frequency_table=area_frequency_table,
        delay_reason_frequency_table=delay_reason_frequency_table,
        people_ahead_frequency_table=people_ahead_frequency_table,
        area_display_table=_categorical_display_table(
            area_frequency_table,
            category_label="Clase $k$",
        ),
        delay_reason_display_table=_categorical_display_table(
            delay_reason_frequency_table,
            category_label="Causa $k$",
            include_cumulative=True,
        ),
        people_ahead_display_table=_discrete_display_table(people_ahead_frequency_table),
        frequency_display_table=_continuous_display_table(frequency_table),
        area_categories=_AREA_CATEGORIES,
        delay_reason_categories=_DELAY_REASON_CATEGORIES,
        people_ahead_values=_PEOPLE_AHEAD_VALUES,
    )
