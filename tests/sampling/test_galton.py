import math

from core import Settings
from sampling import GaltonBoardInput, simulate_galton_board


def test_galton_board_counts_match_balls(fixed_settings: Settings) -> None:
    result = simulate_galton_board(
        GaltonBoardInput(rows=10, balls=1_000, right_probability=0.5, settings=fixed_settings)
    )
    assert int(result.bin_counts.sum()) == 1_000
    assert result.bin_positions.size == 11
    assert math.isclose(result.normal_approximation_mean, 5.0)
    assert math.isclose(result.normal_approximation_standard_deviation, math.sqrt(2.5))
