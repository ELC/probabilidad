from pandera.typing import DataFrame

from core import Observations, Settings
from descriptive import FrequencyTableInput, build_frequency_table
from visualization import (
    FrequencyChartInput,
    FrequencyPolygonChartInput,
    HistogramChartInput,
    StemLeafChartInput,
    chart_cumulative_frequency_polygon,
    chart_frequency_table,
    chart_histogram,
    chart_histogram_with_frequency_polygon,
    chart_stem_leaf,
)


def test_chart_histogram(normal_observations: DataFrame[Observations], fixed_settings: Settings) -> None:
    chart = chart_histogram(HistogramChartInput(observations=normal_observations, settings=fixed_settings))
    assert chart.to_dict()
    assert chart.to_dict()["mark"]["binSpacing"] == 0


def test_chart_frequency_table(normal_observations: DataFrame[Observations], fixed_settings: Settings) -> None:
    table = build_frequency_table(FrequencyTableInput(observations=normal_observations))
    chart = chart_frequency_table(FrequencyChartInput(frequency_table=table, settings=fixed_settings))
    chart_spec = chart.to_dict()
    bars_layer = chart_spec["layer"][0]
    ogive_layer = chart_spec["layer"][1]
    assert bars_layer["mark"]["type"] == "rect"
    assert bars_layer["encoding"]["x"]["field"] == "interval_start"
    assert bars_layer["encoding"]["x2"]["field"] == "interval_end"
    assert bars_layer["encoding"]["y2"]["field"] == "baseline"
    assert ogive_layer["encoding"]["x"]["field"] == "midpoint"


def test_chart_stem_leaf(normal_observations: DataFrame[Observations], fixed_settings: Settings) -> None:
    chart = chart_stem_leaf(StemLeafChartInput(observations=normal_observations, settings=fixed_settings))
    chart_spec = chart.to_dict()
    assert chart_spec["mark"]["type"] == "text"
    assert chart_spec["encoding"]["text"]["field"] == "leaf"
    assert chart_spec["width"] == "container"


def test_chart_histogram_with_frequency_polygon(
    normal_observations: DataFrame[Observations], fixed_settings: Settings
) -> None:
    table = build_frequency_table(FrequencyTableInput(observations=normal_observations, bin_count=6))
    chart = chart_histogram_with_frequency_polygon(
        FrequencyPolygonChartInput(frequency_table=table, settings=fixed_settings)
    )
    chart_spec = chart.to_dict()
    assert chart_spec["layer"][0]["mark"]["type"] == "rect"
    assert chart_spec["layer"][1]["mark"]["type"] == "line"
    assert chart_spec["layer"][1]["encoding"]["x"]["field"] == "midpoint"


def test_chart_histogram_with_frequency_polygon_accepts_fixed_domains(
    normal_observations: DataFrame[Observations], fixed_settings: Settings
) -> None:
    table = build_frequency_table(FrequencyTableInput(observations=normal_observations, bin_count=6))
    chart = chart_histogram_with_frequency_polygon(
        FrequencyPolygonChartInput(
            frequency_table=table,
            settings=fixed_settings,
            x_domain=(0.0, 10.0),
            y_domain=(0.0, 0.5),
        )
    )
    chart_spec = chart.to_dict()
    assert chart_spec["layer"][0]["encoding"]["x"]["scale"]["domain"] == [0.0, 10.0]
    assert chart_spec["layer"][0]["encoding"]["y"]["scale"]["domain"] == [0.0, 0.5]


def test_chart_cumulative_frequency_polygon(
    normal_observations: DataFrame[Observations], fixed_settings: Settings
) -> None:
    table = build_frequency_table(FrequencyTableInput(observations=normal_observations, bin_count=6))
    chart = chart_cumulative_frequency_polygon(
        FrequencyPolygonChartInput(frequency_table=table, settings=fixed_settings)
    )
    chart_spec = chart.to_dict()
    assert chart_spec["layer"][0]["encoding"]["y"]["field"] == "relative_frequency"
    assert chart_spec["layer"][1]["encoding"]["x"]["field"] == "midpoint"
