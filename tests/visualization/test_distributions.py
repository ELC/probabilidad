from core import BinomialParams, NormalParams, Settings
from distributions import (
    DensityGridInput,
    ProbabilityMassInput,
    evaluate_density_grid,
    evaluate_probability_mass,
    make_binomial,
    make_normal,
)
from visualization import (
    DensityChartInput,
    ProbabilityMassChartInput,
    chart_density,
    chart_probability_mass,
)


def test_chart_density_uses_distribution_name(fixed_settings: Settings) -> None:
    distribution = make_normal(NormalParams())
    grid = evaluate_density_grid(DensityGridInput(distribution=distribution, settings=fixed_settings))
    chart = chart_density(DensityChartInput(density_grid=grid, settings=fixed_settings))
    assert chart.to_dict()


def test_chart_density_accepts_custom_title(fixed_settings: Settings) -> None:
    distribution = make_normal(NormalParams())
    grid = evaluate_density_grid(DensityGridInput(distribution=distribution, settings=fixed_settings))
    chart = chart_density(DensityChartInput(density_grid=grid, title="Custom", settings=fixed_settings))
    assert "Custom" in chart.to_dict()["title"]


def test_chart_probability_mass(fixed_settings: Settings) -> None:
    distribution = make_binomial(BinomialParams(trials=8, success_probability=0.5))
    mass = evaluate_probability_mass(ProbabilityMassInput(distribution=distribution, lower_outcome=0, upper_outcome=8))
    chart = chart_probability_mass(ProbabilityMassChartInput(probability_mass=mass, settings=fixed_settings))
    assert chart.to_dict()


def test_chart_probability_mass_accepts_title(fixed_settings: Settings) -> None:
    distribution = make_binomial(BinomialParams(trials=4, success_probability=0.5))
    mass = evaluate_probability_mass(ProbabilityMassInput(distribution=distribution, lower_outcome=0, upper_outcome=4))
    chart = chart_probability_mass(
        ProbabilityMassChartInput(probability_mass=mass, title="Personalizado", settings=fixed_settings)
    )
    assert "Personalizado" in chart.to_dict()["title"]
