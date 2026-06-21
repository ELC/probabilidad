import altair as alt
import pandas as pd
from pydantic import BaseModel, ConfigDict

from core import Settings
from distributions.evaluations import DensityGrid, ProbabilityMassTable
from visualization.theme import apply_theme

_ARBITRARY = ConfigDict(arbitrary_types_allowed=True, frozen=True)


class DensityChartInput(BaseModel):
    model_config = _ARBITRARY

    density_grid: DensityGrid
    title: str | None = None
    settings: Settings = Settings()


def chart_density(input_data: DensityChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    data = pd.DataFrame({"x": input_data.density_grid.grid, "density": input_data.density_grid.density})
    title = input_data.title or f"Densidad — {input_data.density_grid.distribution_name}"
    chart = (
        alt
        .Chart(data)
        .mark_line(color=theme.palette.primary, strokeWidth=theme.line_stroke_width)
        .encode(
            x=alt.X("x:Q", title="x"),
            y=alt.Y("density:Q", title="f(x)"),
        )
        .properties(title=title)
    )
    return apply_theme(chart, input_data.settings)


class ProbabilityMassChartInput(BaseModel):
    model_config = _ARBITRARY

    probability_mass: ProbabilityMassTable
    title: str | None = None
    settings: Settings = Settings()


def chart_probability_mass(input_data: ProbabilityMassChartInput) -> alt.Chart:
    theme = input_data.settings.chart_theme
    title = input_data.title or f"Masa de probabilidad — {input_data.probability_mass.distribution_name}"
    chart = (
        alt
        .Chart(input_data.probability_mass.table)
        .mark_bar(opacity=theme.bar_opacity, color=theme.palette.primary)
        .encode(
            x=alt.X("outcome:O", title="Resultado"),
            y=alt.Y("probability:Q", title="P(X = x)"),
            tooltip=["outcome", "probability"],
        )
        .properties(title=title)
    )
    return apply_theme(chart, input_data.settings)
