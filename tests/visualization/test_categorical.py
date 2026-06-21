import pandas as pd
from pandera.typing import DataFrame

from core import Settings, TabularData
from descriptive import (
    CategoricalFrequencyTableInput,
    DiscreteFrequencyTableInput,
    build_categorical_frequency_table,
    build_discrete_frequency_table,
)
from visualization import (
    CategoricalBarChartInput,
    CategoricalBarFromDataChartInput,
    DiscreteStickChartInput,
    DiscreteStickFromDataChartInput,
    ParetoChartInput,
    ParetoFromDataChartInput,
    chart_categorical_bars,
    chart_categorical_bars_from_data,
    chart_discrete_sticks,
    chart_discrete_sticks_from_data,
    chart_pareto,
    chart_pareto_from_data,
)


def test_chart_categorical_bars_preserves_table_order_and_uses_container_width(fixed_settings: Settings) -> None:
    table = build_categorical_frequency_table(
        CategoricalFrequencyTableInput(
            categories=("Guardia", "Clínica médica", "Laboratorio"),
            absolute_frequencies=(22, 32, 4),
        )
    )
    chart = chart_categorical_bars(
        CategoricalBarChartInput(
            frequency_table=table,
            category_title="Área de atención",
            settings=fixed_settings,
        )
    )
    chart_spec = chart.to_dict()
    assert chart_spec["width"] == "container"
    assert chart_spec["encoding"]["x"]["sort"] is None
    assert chart_spec["encoding"]["x"]["title"] == "Área de atención"


def test_chart_categorical_bars_from_data_counts_source_column(fixed_settings: Settings) -> None:
    data = pd.DataFrame({"area": ["Laboratorio", "Guardia", "Guardia", "Clínica médica"]}).pipe(
        DataFrame[TabularData]
    )
    chart = chart_categorical_bars_from_data(
        CategoricalBarFromDataChartInput(
            data=data,
            category_column="area",
            category_order=("Guardia", "Clínica médica", "Laboratorio"),
            settings=fixed_settings,
        )
    )
    chart_data = chart.to_dict()["datasets"]
    rows = next(iter(chart_data.values()))
    assert [row["category"] for row in rows] == ["Guardia", "Clínica médica", "Laboratorio"]
    assert [row["absolute_frequency"] for row in rows] == [2, 1, 1]


def test_chart_pareto_uses_relative_frequencies_and_container_width(fixed_settings: Settings) -> None:
    table = build_categorical_frequency_table(
        CategoricalFrequencyTableInput(
            categories=("A", "B", "C"),
            absolute_frequencies=(2, 5, 3),
            sort_descending=True,
        )
    )
    chart = chart_pareto(ParetoChartInput(frequency_table=table, category_title="Motivo", settings=fixed_settings))
    chart_spec = chart.to_dict()
    bars_layer = chart_spec["layer"][0]
    line_layer = chart_spec["layer"][1]
    assert chart_spec["width"] == "container"
    assert bars_layer["encoding"]["x"]["sort"] is None
    assert bars_layer["encoding"]["x"]["axis"]["labelAngle"] == 30
    assert bars_layer["encoding"]["y"]["field"] == "relative_frequency"
    assert line_layer["encoding"]["y"]["field"] == "cumulative_relative_frequency"
    assert "resolve" not in chart_spec


def test_chart_pareto_from_data_excludes_categories(fixed_settings: Settings) -> None:
    data = pd.DataFrame({
        "delay_reason": ["Ninguna", "Autorización", "Autorización", "Admisión", "Ninguna", "Admisión", "Admisión"]
    }).pipe(DataFrame[TabularData])
    chart = chart_pareto_from_data(
        ParetoFromDataChartInput(
            data=data,
            category_column="delay_reason",
            category_order=("Ninguna", "Admisión", "Autorización"),
            exclude_categories=("Ninguna",),
            settings=fixed_settings,
        )
    )
    chart_data = chart.to_dict()["datasets"]
    rows = next(iter(chart_data.values()))
    assert [row["category"] for row in rows] == ["Admisión", "Autorización"]
    assert [row["absolute_frequency"] for row in rows] == [3, 2]


def test_chart_discrete_sticks_renders_stems_and_points(fixed_settings: Settings) -> None:
    table = build_discrete_frequency_table(
        DiscreteFrequencyTableInput(
            exact_values=(0, 1, 2),
            absolute_frequencies=(2, 3, 5),
        )
    )
    chart = chart_discrete_sticks(
        DiscreteStickChartInput(
            frequency_table=table,
            value_title="Personas esperando antes",
            settings=fixed_settings,
        )
    )
    chart_spec = chart.to_dict()
    assert chart_spec["width"] == "container"
    assert chart_spec["mark"]["type"] == "bar"
    assert chart_spec["mark"]["size"] == 12
    assert chart_spec["encoding"]["x"]["field"] == "value"
    assert chart_spec["encoding"]["x"]["axis"]["labelAngle"] == 0
    assert chart_spec["encoding"]["y"]["field"] == "relative_frequency"


def test_chart_discrete_sticks_from_data_counts_exact_values(fixed_settings: Settings) -> None:
    data = pd.DataFrame({"people_ahead": [2, 0, 2, 1, 2]}).pipe(DataFrame[TabularData])
    chart = chart_discrete_sticks_from_data(
        DiscreteStickFromDataChartInput(
            data=data,
            value_column="people_ahead",
            exact_values=(0, 1, 2, 3),
            settings=fixed_settings,
        )
    )
    chart_data = chart.to_dict()["datasets"]
    rows = next(iter(chart_data.values()))
    assert [row["value"] for row in rows] == [0, 1, 2, 3]
    assert [row["absolute_frequency"] for row in rows] == [1, 1, 3, 0]
