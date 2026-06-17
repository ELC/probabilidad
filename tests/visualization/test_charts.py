from pandera.typing import DataFrame

from core import (
    BinomialParams,
    ExponentialParams,
    NormalParams,
    Observations,
    Settings,
)
from descriptive import (
    FrequencyTableInput,
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
    CLTComparisonChartInput,
    ConfidenceIntervalChartInput,
    DensityChartInput,
    DescriptiveSummaryChartInput,
    FrequencyChartInput,
    HistogramChartInput,
    LLNChartInput,
    LLNMultipleTrajectoriesChartInput,
    PartitionDiagramInput,
    ProbabilityMassChartInput,
    ProbabilityTreeInput,
    VennTwoSetsInput,
    chart_bootstrap_distribution,
    chart_clt_comparison,
    chart_confidence_interval,
    chart_density,
    chart_descriptive_summary,
    chart_frequency_table,
    chart_histogram,
    chart_lln_multiple_trajectories,
    chart_lln_running_mean,
    chart_partition_diagram,
    chart_probability_mass,
    chart_probability_tree,
    chart_venn_two_sets,
)


def test_chart_histogram(normal_observations: DataFrame[Observations], fixed_settings: Settings) -> None:
    chart = chart_histogram(HistogramChartInput(observations=normal_observations, settings=fixed_settings))
    assert chart.to_dict()


def test_chart_frequency_table(normal_observations: DataFrame[Observations], fixed_settings: Settings) -> None:
    table = build_frequency_table(FrequencyTableInput(observations=normal_observations))
    chart = chart_frequency_table(FrequencyChartInput(frequency_table=table, settings=fixed_settings))
    assert chart.to_dict()


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


def test_chart_venn_two_sets_renders_intersection_label(fixed_settings: Settings) -> None:
    chart = chart_venn_two_sets(
        VennTwoSetsInput(set_a_label="Esperan mucho", set_b_label="Llegan tarde", settings=fixed_settings)
    )
    spec = chart.to_dict(format="vega")
    assert "∩" in str(spec)
    assert "Esperan mucho" in str(spec)
    assert "Llegan tarde" in str(spec)


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
    try:
        chart_partition_diagram(
            PartitionDiagramInput(
                partition_labels=("A_1", "A_2"),
                partition_weights=(1.0,),
                settings=fixed_settings,
            )
        )
    except ValueError as error:
        assert "same length" in str(error)
    else:
        msg = "expected ValueError for mismatched lengths"
        raise AssertionError(msg)


def test_chart_partition_diagram_rejects_zero_weights(fixed_settings: Settings) -> None:
    try:
        chart_partition_diagram(
            PartitionDiagramInput(
                partition_labels=("A_1", "A_2"),
                partition_weights=(0.0, 0.0),
                settings=fixed_settings,
            )
        )
    except ValueError as error:
        assert "positive" in str(error)
    else:
        msg = "expected ValueError for zero weights"
        raise AssertionError(msg)


def test_chart_partition_diagram_rejects_overlay_length_mismatch(fixed_settings: Settings) -> None:
    try:
        chart_partition_diagram(
            PartitionDiagramInput(
                partition_labels=("A_1", "A_2"),
                partition_weights=(1.0, 1.0),
                overlay_label="B",
                overlay_fractions=(0.4,),
                settings=fixed_settings,
            )
        )
    except ValueError as error:
        assert "overlay" in str(error)
    else:
        msg = "expected ValueError for overlay length mismatch"
        raise AssertionError(msg)


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
    assert "0.010" in flattened
