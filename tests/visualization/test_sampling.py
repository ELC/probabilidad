from pandera.typing import DataFrame

from core import ExponentialParams, NormalParams, Observations, Settings
from distributions import make_exponential, make_normal
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
    LLNChartInput,
    LLNMultipleTrajectoriesChartInput,
    chart_bootstrap_distribution,
    chart_clt_comparison,
    chart_lln_multiple_trajectories,
    chart_lln_running_mean,
)


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
