import altair as alt
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from core import CategoricalFrequencyTable, DiscreteFrequencyTable, Settings, TabularData
from descriptive import (
    CategoricalFrequencyTableInput,
    DiscreteFrequencyTableInput,
    build_categorical_frequency_table,
    build_discrete_frequency_table,
)
from visualization.theme import apply_theme

_ARBITRARY = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class CategoricalBarChartInput(BaseModel):
    model_config = _ARBITRARY

    frequency_table: DataFrame[CategoricalFrequencyTable]
    title: str = "Frecuencias por categoría"
    category_title: str = "Categoría"
    settings: Settings = Settings()


def chart_categorical_bars(input_data: CategoricalBarChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    chart = (
        alt.Chart(input_data.frequency_table)
        .mark_bar(color=theme.palette.primary, opacity=theme.bar_opacity)
        .encode(
            x=alt.X("category:N", sort=None, title=input_data.category_title),
            y=alt.Y("absolute_frequency:Q", title="Frecuencia"),
            tooltip=["category", "absolute_frequency", "relative_frequency"],
        )
        .properties(title=input_data.title, width="container", height=theme.height)
    )
    return apply_theme(chart, input_data.settings, set_size=False)


class CategoricalBarFromDataChartInput(BaseModel):
    model_config = _ARBITRARY

    data: DataFrame[TabularData]
    category_column: str
    category_order: tuple[str, ...] | None = None
    title: str = "Frecuencias por categoría"
    category_title: str = "Categoría"
    settings: Settings = Settings()


def _categorical_table_from_data(
    data: DataFrame[TabularData],
    category_column: str,
    category_order: tuple[str, ...] | None,
    *,
    sort_descending: bool = False,
    exclude_categories: tuple[str, ...] = (),
) -> DataFrame[CategoricalFrequencyTable]:
    values = data[category_column]
    if exclude_categories:
        values = values[~values.isin(exclude_categories)]
    counts = values.value_counts(sort=False)
    if category_order is not None:
        ordered_categories = tuple(category for category in category_order if category not in exclude_categories)
        counts = counts.reindex(ordered_categories, fill_value=0)
    return build_categorical_frequency_table(
        CategoricalFrequencyTableInput(
            categories=tuple(str(category) for category in counts.index),
            absolute_frequencies=tuple(int(frequency) for frequency in counts),
            sort_descending=sort_descending,
        )
    )


def chart_categorical_bars_from_data(input_data: CategoricalBarFromDataChartInput) -> alt.Chart:
    frequency_table = _categorical_table_from_data(
        input_data.data,
        input_data.category_column,
        input_data.category_order,
    )
    return chart_categorical_bars(
        CategoricalBarChartInput(
            frequency_table=frequency_table,
            title=input_data.title,
            category_title=input_data.category_title,
            settings=input_data.settings,
        )
    )


class ParetoChartInput(BaseModel):
    model_config = _ARBITRARY

    frequency_table: DataFrame[CategoricalFrequencyTable]
    title: str = "Diagrama de Pareto"
    category_title: str = "Categoría"
    settings: Settings = Settings()


def chart_pareto(input_data: ParetoChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    y_axis = alt.Y(
        "relative_frequency:Q",
        axis=alt.Axis(format="%"),
        title="Frecuencia relativa",
    )
    bars = (
        alt.Chart(input_data.frequency_table)
        .mark_bar(color=theme.palette.primary, opacity=theme.bar_opacity)
        .encode(
            x=alt.X("category:N", sort=None, title=input_data.category_title),
            y=y_axis,
            tooltip=["category", "absolute_frequency", "relative_frequency"],
        )
    )
    cumulative_line = (
        alt.Chart(input_data.frequency_table)
        .mark_line(
            point=True,
            color=theme.palette.secondary,
            strokeWidth=theme.line_stroke_width,
        )
        .encode(
            x=alt.X("category:N", sort=None),
            y=alt.Y(
                "cumulative_relative_frequency:Q",
                axis=alt.Axis(format="%"),
                title="Frecuencia relativa",
            ),
        )
    )
    chart = alt.layer(bars, cumulative_line).properties(
        title=input_data.title,
        width="container",
        height=theme.height,
    )
    return apply_theme(chart, input_data.settings, set_size=False)


class ParetoFromDataChartInput(BaseModel):
    model_config = _ARBITRARY

    data: DataFrame[TabularData]
    category_column: str
    category_order: tuple[str, ...] | None = None
    exclude_categories: tuple[str, ...] = ()
    title: str = "Diagrama de Pareto"
    category_title: str = "Categoría"
    settings: Settings = Settings()


def chart_pareto_from_data(input_data: ParetoFromDataChartInput) -> alt.Chart:
    frequency_table = _categorical_table_from_data(
        input_data.data,
        input_data.category_column,
        input_data.category_order,
        sort_descending=True,
        exclude_categories=input_data.exclude_categories,
    )
    return chart_pareto(
        ParetoChartInput(
            frequency_table=frequency_table,
            title=input_data.title,
            category_title=input_data.category_title,
            settings=input_data.settings,
        )
    )


class DiscreteStickChartInput(BaseModel):
    model_config = _ARBITRARY

    frequency_table: DataFrame[DiscreteFrequencyTable]
    title: str = "Gráfico de bastones"
    value_title: str = "Valor"
    settings: Settings = Settings()


def chart_discrete_sticks(input_data: DiscreteStickChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    chart = (
        alt.Chart(input_data.frequency_table)
        .mark_bar(color=theme.palette.primary, opacity=theme.bar_opacity, size=12)
        .encode(
            x=alt.X("value:O", sort=None, title=input_data.value_title),
            y=alt.Y(
                "relative_frequency:Q",
                axis=alt.Axis(format="%"),
                title="Frecuencia relativa",
            ),
            tooltip=["value", "absolute_frequency", "relative_frequency"],
        )
        .properties(
            title=input_data.title,
            width="container",
            height=theme.height,
        )
    )
    return apply_theme(chart, input_data.settings, set_size=False)


class DiscreteStickFromDataChartInput(BaseModel):
    model_config = _ARBITRARY

    data: DataFrame[TabularData]
    value_column: str
    exact_values: tuple[int, ...] | None = None
    title: str = "Gráfico de bastones"
    value_title: str = "Valor"
    settings: Settings = Settings()


def chart_discrete_sticks_from_data(input_data: DiscreteStickFromDataChartInput) -> alt.Chart:
    values = input_data.data[input_data.value_column]
    counts = values.value_counts(sort=False)
    exact_values = input_data.exact_values
    if exact_values is None:
        exact_values = tuple(int(value) for value in sorted(counts.index))
    counts = counts.reindex(exact_values, fill_value=0)
    frequency_table = build_discrete_frequency_table(
        DiscreteFrequencyTableInput(
            exact_values=exact_values,
            absolute_frequencies=tuple(int(frequency) for frequency in counts),
        )
    )
    return chart_discrete_sticks(
        DiscreteStickChartInput(
            frequency_table=frequency_table,
            title=input_data.title,
            value_title=input_data.value_title,
            settings=input_data.settings,
        )
    )
