import math

from core import ExponentialParams, Settings
from distributions import make_exponential
from sampling import CLTSimulationInput, simulate_clt


def test_simulate_clt_centers_standardized_means(fixed_settings: Settings) -> None:
    distribution = make_exponential(ExponentialParams(rate=1.0))
    result = simulate_clt(
        CLTSimulationInput(
            distribution=distribution,
            sample_size_per_replicate=40,
            replicates=2_000,
            settings=fixed_settings,
        )
    )
    assert math.isclose(result.standardized_means.mean(), 0.0, abs_tol=0.1)
    assert math.isclose(result.standardized_means.std(), 1.0, abs_tol=0.1)
    assert result.sample_size_per_replicate == 40
    assert result.sample_means.size == 2_000
