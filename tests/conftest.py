import numpy as np
import pandas as pd
import pytest
from pandera.typing import DataFrame

from core import NormalParams, Observations, Settings


@pytest.fixture
def fixed_settings() -> Settings:
    return Settings(random_seed=20260101)


@pytest.fixture
def normal_observations(fixed_settings: Settings) -> DataFrame[Observations]:
    rng = np.random.default_rng(fixed_settings.random_seed)
    values = rng.normal(loc=10.0, scale=2.0, size=120)
    return pd.DataFrame({"value": values}).pipe(DataFrame[Observations])


@pytest.fixture
def small_observations() -> DataFrame[Observations]:
    return pd.DataFrame({"value": [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]}).pipe(DataFrame[Observations])


@pytest.fixture
def constant_observations() -> DataFrame[Observations]:
    return pd.DataFrame({"value": [3.0, 3.0, 3.0, 3.0]}).pipe(DataFrame[Observations])


@pytest.fixture
def normal_parameters() -> NormalParams:
    return NormalParams(mean=0.0, standard_deviation=1.0)
