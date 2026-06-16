import pytest
from pydantic import ValidationError

from core import Settings
from core.theme import ChartTheme


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.random_seed > 0
    assert settings.monte_carlo_replicates > 0
    assert settings.bootstrap_replicates > 0
    assert settings.grid_resolution > 0
    assert isinstance(settings.chart_theme, ChartTheme)


def test_settings_frozen_disallows_mutation() -> None:
    settings = Settings()
    with pytest.raises(ValidationError):
        settings.random_seed = 123
