import altair as alt
import pandas as pd
from pandera.typing import DataFrame

from core import Observations, Settings
from descriptive import FrequencyTableInput, build_frequency_table, summarize_observations
from visualization import (
    BoxplotExampleChartInput,
    BoxplotShapeComparisonChartInput,
    DescriptiveSummaryChartInput,
    ObservationsOverviewInput,
    TypicalValuesComparisonChartInput,
    apply_theme,
    chart_boxplot_example,
    chart_boxplot_shape_comparison,
    chart_descriptive_summary,
    chart_observations_overview,
    chart_typical_values_comparison,
)


def test_chart_descriptive_summary(normal_observations: DataFrame[Observations], fixed_settings: Settings) -> None:
    statistics = summarize_observations(normal_observations)
    chart = chart_descriptive_summary(
        DescriptiveSummaryChartInput(
            observations=normal_observations,
            statistics=statistics,
            settings=fixed_settings,
        )
    )
    assert chart.to_dict()


def test_chart_descriptive_summary_without_theme_can_vconcat(
    normal_observations: DataFrame[Observations], fixed_settings: Settings
) -> None:
    statistics = summarize_observations(normal_observations)
    chart_input = DescriptiveSummaryChartInput(
        observations=normal_observations,
        statistics=statistics,
        settings=fixed_settings,
        apply_theme=False,
    )
    composed = alt.vconcat(
        chart_descriptive_summary(chart_input),
        chart_descriptive_summary(chart_input.model_copy(update={"title": "Comparación"})),
        spacing=10,
    ).resolve_scale(x="shared")
    chart = apply_theme(composed, fixed_settings, set_size=False)
    spec = chart.to_dict()
    assert spec["vconcat"], "expected vconcat with two stacked panels"
    assert len(spec["vconcat"]) == 2
    assert spec["resolve"]["scale"]["x"] == "shared"
    assert "config" in spec


def test_chart_boxplot_example_builds_from_values(fixed_settings: Settings) -> None:
    chart = chart_boxplot_example(
        BoxplotExampleChartInput(
            values=(2.0, 3.0, 4.0, 5.0, 6.0),
            settings=fixed_settings,
            apply_theme=False,
        )
    )

    spec = chart.to_dict()
    assert spec["layer"][0]["mark"]["type"] == "boxplot"


def test_chart_typical_values_comparison_shows_extreme_observation_shift(
    small_observations: DataFrame[Observations], fixed_settings: Settings
) -> None:
    observations_with_extreme = pd.concat(
        [small_observations, pd.DataFrame({"value": [120.0]})], ignore_index=True
    ).pipe(DataFrame[Observations])
    original_statistics = summarize_observations(small_observations)
    comparison_statistics = summarize_observations(observations_with_extreme)
    chart = chart_typical_values_comparison(
        TypicalValuesComparisonChartInput(
            original_statistics=original_statistics,
            comparison_statistics=comparison_statistics,
            original_label="Original",
            comparison_label="Con extremo",
            settings=fixed_settings,
        )
    )
    expected_rows = [
        {"scenario": "Original", "measure": "Media", "value": original_statistics.location.mean},
        {"scenario": "Original", "measure": "Mediana", "value": original_statistics.location.median},
        {"scenario": "Con extremo", "measure": "Media", "value": comparison_statistics.location.mean},
        {"scenario": "Con extremo", "measure": "Mediana", "value": comparison_statistics.location.median},
    ]
    datasets = list(chart.to_dict()["datasets"].values())
    assert expected_rows in datasets


def test_chart_boxplot_shape_comparison_stacks_three_panels(
    normal_observations: DataFrame[Observations], fixed_settings: Settings
) -> None:
    second_sample = pd.DataFrame(
        {"value": normal_observations["value"].to_numpy() + 5.0}
    ).pipe(DataFrame[Observations])
    chart = chart_boxplot_shape_comparison(
        BoxplotShapeComparisonChartInput(
            first_sample=normal_observations,
            second_sample=second_sample,
            first_label="A",
            second_label="B",
            settings=fixed_settings,
        )
    )
    spec = chart.to_dict()
    assert len(spec["vconcat"]) == 3
    assert spec["resolve"]["scale"]["x"] == "shared"


def test_chart_observations_overview_shares_x_axis(
    normal_observations: DataFrame[Observations], fixed_settings: Settings
) -> None:
    statistics = summarize_observations(normal_observations)
    table = build_frequency_table(FrequencyTableInput(observations=normal_observations))
    chart = chart_observations_overview(
        ObservationsOverviewInput(
            observations=normal_observations,
            frequency_table=table,
            statistics=statistics,
            settings=fixed_settings,
        )
    )
    spec = chart.to_dict()
    assert spec["vconcat"], "expected vconcat with two stacked panels"
    assert len(spec["vconcat"]) == 2
    assert spec["resolve"]["scale"]["x"] == "shared"
