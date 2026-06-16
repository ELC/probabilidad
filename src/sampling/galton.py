import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from core import Settings

_ARBITRARY = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class GaltonBoardInput(BaseModel):
    model_config = _ARBITRARY

    rows: int = Field(default=20, ge=1, le=200)
    balls: int = Field(default=5_000, ge=1)
    right_probability: float = Field(default=0.5, gt=0.0, lt=1.0)
    settings: Settings = Settings()


class GaltonBoardResult(BaseModel):
    model_config = _ARBITRARY

    bin_positions: np.ndarray
    bin_counts: np.ndarray
    normal_approximation_mean: float
    normal_approximation_standard_deviation: float


def simulate_galton_board(input_data: GaltonBoardInput) -> GaltonBoardResult:
    rng = np.random.default_rng(input_data.settings.random_seed)
    right_steps = rng.binomial(n=input_data.rows, p=input_data.right_probability, size=input_data.balls)
    bin_positions = np.arange(input_data.rows + 1)
    bin_counts = np.bincount(right_steps, minlength=input_data.rows + 1)
    mean = input_data.rows * input_data.right_probability
    standard_deviation = np.sqrt(input_data.rows * input_data.right_probability * (1.0 - input_data.right_probability))
    return GaltonBoardResult(
        bin_positions=bin_positions.astype(int),
        bin_counts=bin_counts.astype(int),
        normal_approximation_mean=float(mean),
        normal_approximation_standard_deviation=float(standard_deviation),
    )
