import pandas as pd
import pytest
from pandera.typing import DataFrame
from pydantic import ValidationError

from core import Observations, Settings
from sampling import BootstrapInput, bootstrap_mean


def test_bootstrap_mean_contains_sample_mean(
    normal_observations: DataFrame[Observations], fixed_settings: Settings
) -> None:
    result = bootstrap_mean(BootstrapInput(observations=normal_observations, replicates=500, settings=fixed_settings))
    assert result.lower_quantile < result.point_estimate < result.upper_quantile
    assert result.bootstrap_means.size == 500


def test_bootstrap_rejects_empty_observations() -> None:
    empty = pd.DataFrame({"value": pd.Series([], dtype=float)}).pipe(DataFrame[Observations])
    with pytest.raises(ValidationError):
        BootstrapInput(observations=empty)
