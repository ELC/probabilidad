from core import NormalParams, Settings
from distributions import make_normal
from sampling import MonteCarloInput, run_monte_carlo


def test_monte_carlo_size_matches_request(fixed_settings: Settings) -> None:
    distribution = make_normal(NormalParams())
    result = run_monte_carlo(MonteCarloInput(distribution=distribution, sample_size=200, settings=fixed_settings))
    assert result.samples.size == 200
    assert result.sample_size == 200


def test_monte_carlo_is_reproducible(fixed_settings: Settings) -> None:
    distribution = make_normal(NormalParams())
    first = run_monte_carlo(MonteCarloInput(distribution=distribution, sample_size=50, settings=fixed_settings))
    second = run_monte_carlo(MonteCarloInput(distribution=distribution, sample_size=50, settings=fixed_settings))
    assert (first.samples == second.samples).all()
