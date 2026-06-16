# %%NBQA-CELL-SEP2b5a54
from core import (
    BinomialParams,
    NormalParams,
    PoissonParams,
    Settings,
)
from distributions import (
    DensityGridInput,
    MomentsInput,
    ProbabilityMassInput,
    QuantileInput,
    TailProbabilityInput,
    compute_numeric_moments,
    evaluate_density_grid,
    evaluate_probability_mass,
    make_binomial,
    make_normal,
    make_poisson,
    quantile_of_continuous,
    tail_probability_of_continuous,
)
from exercises import NumericAnswerInput, verify_numeric_answer
from symbolic import (
    compute_binomial_moments,
    compute_poisson_moments,
    standardize_normal,
)
from visualization import (
    DensityChartInput,
    ProbabilityMassChartInput,
    chart_density,
    chart_probability_mass,
)
from widgets import (
    ContinuousDistributionExplorerInput,
    DiscreteDistributionExplorerInput,
    build_continuous_distribution_explorer,
    build_discrete_distribution_explorer,
)


# %%NBQA-CELL-SEP2b5a54
settings = Settings()


# %%NBQA-CELL-SEP2b5a54
binomial_distribution = make_binomial(BinomialParams(trials=10, success_probability=0.3))
probability_mass = evaluate_probability_mass(ProbabilityMassInput(distribution=binomial_distribution))
chart_probability_mass(ProbabilityMassChartInput(probability_mass=probability_mass, settings=settings))


# %%NBQA-CELL-SEP2b5a54
binomial_moments_symbolic = compute_binomial_moments(BinomialParams(trials=10, success_probability=0.3))

binomial_moments_numeric = compute_numeric_moments(MomentsInput(distribution=binomial_distribution))
binomial_moments_numeric


# %%NBQA-CELL-SEP2b5a54
standard_normal_distribution = make_normal(NormalParams(mean=0.0, standard_deviation=1.0))
density = evaluate_density_grid(DensityGridInput(distribution=standard_normal_distribution, settings=settings))
chart_density(DensityChartInput(density_grid=density, settings=settings))


# %%NBQA-CELL-SEP2b5a54
standardize_normal(NormalParams(mean=170.0, standard_deviation=8.0)).formula


# %%NBQA-CELL-SEP2b5a54
heights_distribution = make_normal(NormalParams(mean=170.0, standard_deviation=8.0))
probability_between = tail_probability_of_continuous(
    TailProbabilityInput(distribution=heights_distribution, lower_bound=165.0, upper_bound=180.0)
)
probability_between


# %%NBQA-CELL-SEP2b5a54
percentile_ninety = quantile_of_continuous(QuantileInput(distribution=heights_distribution, probability=0.90))
percentile_ninety


# %%NBQA-CELL-SEP2b5a54
build_continuous_distribution_explorer(ContinuousDistributionExplorerInput(settings=settings))


# %%NBQA-CELL-SEP2b5a54
build_discrete_distribution_explorer(DiscreteDistributionExplorerInput(settings=settings))


# %%NBQA-CELL-SEP2b5a54
poisson_distribution = make_poisson(PoissonParams(rate=4.0))
poisson_mass = evaluate_probability_mass(
    ProbabilityMassInput(distribution=poisson_distribution, lower_outcome=0, upper_outcome=12)
)
chart_probability_mass(ProbabilityMassChartInput(probability_mass=poisson_mass, settings=settings))


# %%NBQA-CELL-SEP2b5a54
expected_probability = tail_probability_of_continuous(
    TailProbabilityInput(distribution=heights_distribution, upper_bound=178.0)
).probability

student_answer = 0.8413
verify_numeric_answer(
    NumericAnswerInput(
        student_answer=student_answer,
        expected_answer=expected_probability,
        absolute_tolerance=1e-3,
    )
)


# %%NBQA-CELL-SEP2b5a54
expected_expectation = compute_poisson_moments(PoissonParams(rate=3.5)).expectation

student_answer = 3.5
verify_numeric_answer(NumericAnswerInput(student_answer=student_answer, expected_answer=float(expected_expectation)))
