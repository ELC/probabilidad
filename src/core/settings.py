from pydantic_settings import BaseSettings, SettingsConfigDict

from core.theme import ChartTheme


class Settings(BaseSettings):
    model_config = SettingsConfigDict(frozen=True, env_prefix="PROBABILIDAD_")

    random_seed: int = 20260101
    monte_carlo_replicates: int = 20_000
    bootstrap_replicates: int = 5_000
    grid_resolution: int = 401
    chart_theme: ChartTheme = ChartTheme()
