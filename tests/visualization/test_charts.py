import json

import matplotlib.pyplot as plt
import pandas as pd
import pytest
from pandera.typing import DataFrame

from core import (
    BinomialParams,
    ExponentialParams,
    NormalParams,
    Observations,
    Settings,
    TabularData,
)
from descriptive import (
    CategoricalFrequencyTableInput,
    DiscreteFrequencyTableInput,
    FrequencyTableInput,
    build_categorical_frequency_table,
    build_discrete_frequency_table,
    build_frequency_table,
    summarize_observations,
)
from distributions import (
    DensityGridInput,
    ProbabilityMassInput,
    evaluate_density_grid,
    evaluate_probability_mass,
    make_binomial,
    make_exponential,
    make_normal,
)
from inference import (
    MeanKnownVarianceInput,
    build_confidence_interval_for_mean_known_variance,
)
from sampling import (
    BootstrapInput,
    CLTSimulationInput,
    LLNMultipleTrajectoriesInput,
    LLNSimulationInput,
    bootstrap_mean,
    simulate_clt,
    simulate_lln,
    simulate_lln_multiple_trajectories,
)
from visualization import (
    BootstrapDistributionChartInput,
    CategoricalBarChartInput,
    CategoricalBarFromDataChartInput,
    CLTComparisonChartInput,
    ConfidenceIntervalChartInput,
    DensityChartInput,
    DescriptiveSummaryChartInput,
    DiscreteStickChartInput,
    DiscreteStickFromDataChartInput,
    FrequencyChartInput,
    FrequencyPolygonChartInput,
    HistogramChartInput,
    LLNChartInput,
    LLNMultipleTrajectoriesChartInput,
    ObservationsOverviewInput,
    ParetoChartInput,
    ParetoFromDataChartInput,
    PartitionDiagramInput,
    ProbabilityMassChartInput,
    ProbabilityTreeInput,
    StemLeafChartInput,
    TypicalValuesComparisonChartInput,
    VennTwoSetsInput,
    chart_bootstrap_distribution,
    chart_categorical_bars,
    chart_categorical_bars_from_data,
    chart_clt_comparison,
    chart_confidence_interval,
    chart_cumulative_frequency_polygon,
    chart_density,
    chart_descriptive_summary,
    chart_discrete_sticks,
    chart_discrete_sticks_from_data,
    chart_frequency_table,
    chart_histogram,
    chart_histogram_with_frequency_polygon,
    chart_lln_multiple_trajectories,
    chart_lln_running_mean,
    chart_observations_overview,
    chart_pareto,
    chart_pareto_from_data,
    chart_partition_diagram,
    chart_probability_mass,
    chart_probability_tree,
    chart_stem_leaf,
    chart_typical_values_comparison,
    chart_venn_two_sets,
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


def test_chart_density_uses_distribution_name(fixed_settings: Settings) -> None:
    distribution = make_normal(NormalParams())
    grid = evaluate_density_grid(DensityGridInput(distribution=distribution, settings=fixed_settings))
    chart = chart_density(DensityChartInput(density_grid=grid, settings=fixed_settings))
    assert chart.to_dict()


def test_chart_density_accepts_custom_title(fixed_settings: Settings) -> None:
    distribution = make_normal(NormalParams())
    grid = evaluate_density_grid(DensityGridInput(distribution=distribution, settings=fixed_settings))
    chart = chart_density(DensityChartInput(density_grid=grid, title="Custom", settings=fixed_settings))
    assert "Custom" in chart.to_dict()["title"]


def test_chart_probability_mass(fixed_settings: Settings) -> None:
    distribution = make_binomial(BinomialParams(trials=8, success_probability=0.5))
    mass = evaluate_probability_mass(ProbabilityMassInput(distribution=distribution, lower_outcome=0, upper_outcome=8))
    chart = chart_probability_mass(ProbabilityMassChartInput(probability_mass=mass, settings=fixed_settings))
    assert chart.to_dict()


def test_chart_probability_mass_accepts_title(fixed_settings: Settings) -> None:
    distribution = make_binomial(BinomialParams(trials=4, success_probability=0.5))
    mass = evaluate_probability_mass(ProbabilityMassInput(distribution=distribution, lower_outcome=0, upper_outcome=4))
    chart = chart_probability_mass(
        ProbabilityMassChartInput(probability_mass=mass, title="Personalizado", settings=fixed_settings)
    )
    assert "Personalizado" in chart.to_dict()["title"]


def test_chart_clt_comparison(fixed_settings: Settings) -> None:
    distribution = make_exponential(ExponentialParams(rate=1.0))
    clt_result = simulate_clt(
        CLTSimulationInput(
            distribution=distribution,
            sample_size_per_replicate=20,
            replicates=500,
            settings=fixed_settings,
        )
    )
    chart = chart_clt_comparison(CLTComparisonChartInput(clt_result=clt_result, settings=fixed_settings))
    assert chart.to_dict()


def test_chart_lln(fixed_settings: Settings) -> None:
    distribution = make_normal(NormalParams())
    lln_result = simulate_lln(LLNSimulationInput(distribution=distribution, horizon=1_000, settings=fixed_settings))
    chart = chart_lln_running_mean(LLNChartInput(lln_result=lln_result, settings=fixed_settings))
    assert chart.to_dict()


def test_chart_lln_multiple_trajectories(fixed_settings: Settings) -> None:
    distribution = make_normal(NormalParams())
    lln_result = simulate_lln_multiple_trajectories(
        LLNMultipleTrajectoriesInput(
            distribution=distribution,
            horizon=400,
            trajectory_count=8,
            settings=fixed_settings,
        )
    )
    chart = chart_lln_multiple_trajectories(
        LLNMultipleTrajectoriesChartInput(lln_result=lln_result, settings=fixed_settings)
    )
    assert chart.to_dict()


def test_chart_lln_multiple_trajectories_handles_large_datasets(fixed_settings: Settings) -> None:
    distribution = make_normal(NormalParams())
    lln_result = simulate_lln_multiple_trajectories(
        LLNMultipleTrajectoriesInput(
            distribution=distribution,
            horizon=4_000,
            trajectory_count=30,
            settings=fixed_settings,
        )
    )
    chart = chart_lln_multiple_trajectories(
        LLNMultipleTrajectoriesChartInput(lln_result=lln_result, settings=fixed_settings)
    )
    assert chart.to_dict()


def test_chart_bootstrap(normal_observations: DataFrame[Observations], fixed_settings: Settings) -> None:
    bootstrap_result = bootstrap_mean(
        BootstrapInput(observations=normal_observations, replicates=500, settings=fixed_settings)
    )
    chart = chart_bootstrap_distribution(
        BootstrapDistributionChartInput(bootstrap_result=bootstrap_result, settings=fixed_settings)
    )
    assert chart.to_dict()


def test_chart_confidence_interval_with_target(fixed_settings: Settings) -> None:
    intervals = tuple(
        build_confidence_interval_for_mean_known_variance(
            MeanKnownVarianceInput(
                sample_mean=mean,
                population_standard_deviation=1.0,
                sample_size=25,
                confidence_level=0.95,
            )
        )
        for mean in (-0.5, 0.0, 0.5)
    )
    chart = chart_confidence_interval(
        ConfidenceIntervalChartInput(intervals=intervals, target_mean=0.0, settings=fixed_settings)
    )
    assert chart.to_dict()


def test_chart_confidence_interval_without_target(fixed_settings: Settings) -> None:
    intervals = (
        build_confidence_interval_for_mean_known_variance(
            MeanKnownVarianceInput(
                sample_mean=0.0,
                population_standard_deviation=1.0,
                sample_size=25,
                confidence_level=0.95,
            )
        ),
    )
    chart = chart_confidence_interval(ConfidenceIntervalChartInput(intervals=intervals, settings=fixed_settings))
    assert chart.to_dict()


def test_chart_confidence_interval_uses_firebrick_for_misses(fixed_settings: Settings) -> None:
    intervals = tuple(
        build_confidence_interval_for_mean_known_variance(
            MeanKnownVarianceInput(
                sample_mean=mean,
                population_standard_deviation=1.0,
                sample_size=25,
                confidence_level=0.95,
            )
        )
        for mean in (-0.5, 0.0, 0.5)
    )
    chart = chart_confidence_interval(
        ConfidenceIntervalChartInput(intervals=intervals, target_mean=0.0, settings=fixed_settings)
    )
    spec_text = json.dumps(chart.to_dict(format="vega"))
    assert "#B22222" in spec_text.upper()


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


def test_chart_venn_two_sets_renders_set_labels(fixed_settings: Settings) -> None:
    figure = chart_venn_two_sets(
        VennTwoSetsInput(
            probability_a=0.5,
            probability_b=0.4,
            probability_intersection=0.2,
            set_a_label="Esperan mucho",
            set_b_label="Llegan tarde",
            settings=fixed_settings,
        )
    )
    assert len(figure.axes) == 1
    axes = figure.axes[0]
    texts = [text.get_text() for text in axes.texts]
    legend = axes.get_legend()
    assert legend is not None
    legend_labels = [text.get_text() for text in legend.get_texts()]
    assert "Esperan mucho" in legend_labels
    assert "Llegan tarde" in legend_labels
    assert "P(Ω) = 1" in texts
    assert "0.2" in texts
    plt.close(figure)


def test_chart_venn_two_sets_accepts_custom_intersection_label(fixed_settings: Settings) -> None:
    figure = chart_venn_two_sets(
        VennTwoSetsInput(
            probability_a=3 / 6,
            probability_b=3 / 6,
            probability_intersection=2 / 6,
            set_a_label="A",
            set_b_label="B",
            intersection_label="A ∩ B = {4, 6}",
            settings=fixed_settings,
        )
    )
    texts = [text.get_text() for text in figure.axes[0].texts]
    assert "A ∩ B = {4, 6}" in texts
    plt.close(figure)


def test_chart_venn_two_sets_handles_nested_subset(fixed_settings: Settings) -> None:
    figure = chart_venn_two_sets(
        VennTwoSetsInput(
            probability_a=0.21,
            probability_b=0.45,
            probability_intersection=0.21,
            set_a_label="T",
            set_b_label="S",
            settings=fixed_settings,
        )
    )
    assert figure.axes
    plt.close(figure)


def test_chart_venn_two_sets_rejects_inconsistent_intersection(fixed_settings: Settings) -> None:
    with pytest.raises(ValueError, match="probability_intersection must not exceed"):
        chart_venn_two_sets(
            VennTwoSetsInput(
                probability_a=0.3,
                probability_b=0.4,
                probability_intersection=0.35,
                settings=fixed_settings,
            )
        )


def test_chart_venn_two_sets_rejects_out_of_range_probability(fixed_settings: Settings) -> None:
    with pytest.raises(ValueError, match="must lie in"):
        chart_venn_two_sets(
            VennTwoSetsInput(
                probability_a=1.2,
                probability_b=0.4,
                probability_intersection=0.1,
                settings=fixed_settings,
            )
        )


def test_chart_partition_diagram_renders_strips(fixed_settings: Settings) -> None:
    chart = chart_partition_diagram(
        PartitionDiagramInput(
            partition_labels=("Caja 1", "Caja 2", "Caja 3"),
            partition_weights=(2.0, 3.0, 1.0),
            settings=fixed_settings,
        )
    )
    assert chart.to_dict()


def test_chart_partition_diagram_renders_overlay(fixed_settings: Settings) -> None:
    chart = chart_partition_diagram(
        PartitionDiagramInput(
            partition_labels=("A_1", "A_2"),
            partition_weights=(1.0, 1.0),
            overlay_label="Evento B",
            overlay_fractions=(0.4, 0.6),
            settings=fixed_settings,
        )
    )
    assert chart.to_dict()


def test_chart_partition_diagram_rejects_mismatched_lengths(fixed_settings: Settings) -> None:
    with pytest.raises(ValueError, match="same length"):
        chart_partition_diagram(
            PartitionDiagramInput(
                partition_labels=("A_1", "A_2"),
                partition_weights=(1.0,),
                settings=fixed_settings,
            )
        )


def test_chart_partition_diagram_rejects_zero_weights(fixed_settings: Settings) -> None:
    with pytest.raises(ValueError, match="positive"):
        chart_partition_diagram(
            PartitionDiagramInput(
                partition_labels=("A_1", "A_2"),
                partition_weights=(0.0, 0.0),
                settings=fixed_settings,
            )
        )


def test_chart_partition_diagram_rejects_overlay_length_mismatch(fixed_settings: Settings) -> None:
    with pytest.raises(ValueError, match="overlay"):
        chart_partition_diagram(
            PartitionDiagramInput(
                partition_labels=("A_1", "A_2"),
                partition_weights=(1.0, 1.0),
                overlay_label="B",
                overlay_fractions=(0.4,),
                settings=fixed_settings,
            )
        )


def test_chart_probability_tree_emits_joint_probabilities(fixed_settings: Settings) -> None:
    chart = chart_probability_tree(
        ProbabilityTreeInput(
            root_label="Ω",
            branch_labels=("Enfermo", "Sano"),
            branch_probabilities=(0.01, 0.99),
            leaf_labels=("Test +", "Test −"),
            conditional_probabilities=((0.99, 0.01), (0.05, 0.95)),
            settings=fixed_settings,
        )
    )
    flattened = str(chart.to_dict(format="vega"))
    assert "Enfermo" in flattened
    assert "Sano" in flattened
    assert "0.01" in flattened
