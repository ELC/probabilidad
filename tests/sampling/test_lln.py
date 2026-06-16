import math

from core import NormalParams, Settings
from distributions import make_normal
from sampling import LLNSimulationInput, simulate_lln


def test_simulate_lln_converges_to_mean(fixed_settings: Settings) -> None:
    distribution = make_normal(NormalParams(mean=3.0, standard_deviation=1.0))
    result = simulate_lln(LLNSimulationInput(distribution=distribution, horizon=4_000, settings=fixed_settings))
    assert math.isclose(result.running_mean[-1], 3.0, abs_tol=0.05)
    assert result.step.size == 4_000
    assert math.isclose(result.underlying_mean, 3.0)
