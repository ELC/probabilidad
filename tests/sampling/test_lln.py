import math

import numpy as np

from core import NormalParams, Settings
from distributions import make_normal
from sampling import (
    LLNMultipleTrajectoriesInput,
    LLNSimulationInput,
    simulate_lln,
    simulate_lln_multiple_trajectories,
)


def test_simulate_lln_converges_to_mean(fixed_settings: Settings) -> None:
    distribution = make_normal(NormalParams(mean=3.0, standard_deviation=1.0))
    result = simulate_lln(LLNSimulationInput(distribution=distribution, horizon=4_000, settings=fixed_settings))
    assert math.isclose(result.running_mean[-1], 3.0, abs_tol=0.05)
    assert result.step.size == 4_000
    assert math.isclose(result.underlying_mean, 3.0)


def test_simulate_lln_multiple_trajectories_shape_matches_input(fixed_settings: Settings) -> None:
    distribution = make_normal(NormalParams(mean=3.0, standard_deviation=1.0))
    result = simulate_lln_multiple_trajectories(
        LLNMultipleTrajectoriesInput(
            distribution=distribution,
            horizon=500,
            trajectory_count=12,
            settings=fixed_settings,
        )
    )
    assert result.running_means.shape == (12, 500)
    assert result.step.size == 500
    assert math.isclose(result.underlying_mean, 3.0)


def test_simulate_lln_multiple_trajectories_all_converge_to_mean(fixed_settings: Settings) -> None:
    distribution = make_normal(NormalParams(mean=3.0, standard_deviation=1.0))
    result = simulate_lln_multiple_trajectories(
        LLNMultipleTrajectoriesInput(
            distribution=distribution,
            horizon=4_000,
            trajectory_count=10,
            settings=fixed_settings,
        )
    )
    final_means = result.running_means[:, -1]
    assert np.all(np.abs(final_means - 3.0) < 0.1)


def test_simulate_lln_multiple_trajectories_initial_means_are_independent(fixed_settings: Settings) -> None:
    distribution = make_normal(NormalParams(mean=3.0, standard_deviation=1.0))
    result = simulate_lln_multiple_trajectories(
        LLNMultipleTrajectoriesInput(
            distribution=distribution,
            horizon=300,
            trajectory_count=8,
            settings=fixed_settings,
        )
    )
    initial_means = result.running_means[:, 0]
    assert len(np.unique(initial_means)) == 8
