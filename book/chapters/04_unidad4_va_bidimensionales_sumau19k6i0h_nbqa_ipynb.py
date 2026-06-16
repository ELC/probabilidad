# %%NBQA-CELL-SEP2b5a54
from core import BinomialParams, ExponentialParams, Settings
from distributions import make_binomial, make_exponential
from exercises import NumericAnswerInput, verify_numeric_answer
from sampling import (
    CLTSimulationInput,
    GaltonBoardInput,
    LLNSimulationInput,
    simulate_clt,
    simulate_galton_board,
    simulate_lln,
)
from visualization import (
    CLTComparisonChartInput,
    LLNChartInput,
    chart_clt_comparison,
    chart_lln_running_mean,
)
from widgets import (
    CLTExplorerInput,
    LLNExplorerInput,
    build_clt_explorer,
    build_lln_explorer,
)


# %%NBQA-CELL-SEP2b5a54
settings = Settings()


# %%NBQA-CELL-SEP2b5a54
bernoulli = make_binomial(BinomialParams(trials=1, success_probability=0.3))
lln_result = simulate_lln(LLNSimulationInput(distribution=bernoulli, horizon=4_000, settings=settings))
chart_lln_running_mean(LLNChartInput(lln_result=lln_result, settings=settings))


# %%NBQA-CELL-SEP2b5a54
build_lln_explorer(LLNExplorerInput(settings=settings))


# %%NBQA-CELL-SEP2b5a54
import altair as alt
import pandas as pd

galton_result = simulate_galton_board(GaltonBoardInput(rows=24, balls=8_000, settings=settings))
galton_table = pd.DataFrame({
    "posición": galton_result.bin_positions,
    "frecuencia": galton_result.bin_counts,
})
alt.Chart(galton_table).mark_bar(opacity=0.75, color="#1f77b4").encode(
    x=alt.X("posición:O", title="Casilla"),
    y=alt.Y("frecuencia:Q", title="Bolas"),
).properties(width=520, height=320, title="Tablero de Galton — suma de 24 pasos ±1")


# %%NBQA-CELL-SEP2b5a54
exponential_distribution = make_exponential(ExponentialParams(rate=1.0))
clt_result = simulate_clt(
    CLTSimulationInput(
        distribution=exponential_distribution,
        sample_size_per_replicate=30,
        replicates=5_000,
        settings=settings,
    )
)
chart_clt_comparison(CLTComparisonChartInput(clt_result=clt_result, settings=settings))


# %%NBQA-CELL-SEP2b5a54
build_clt_explorer(CLTExplorerInput(settings=settings))


# %%NBQA-CELL-SEP2b5a54
import math

expected_standard_error = 10.0 / math.sqrt(25)
student_answer = 2.0
verify_numeric_answer(NumericAnswerInput(student_answer=student_answer, expected_answer=expected_standard_error))


# %%NBQA-CELL-SEP2b5a54
from core import NormalParams
from distributions import make_normal, tail_probability_of_continuous
from distributions.evaluations import TailProbabilityInput

normal_approximation = make_normal(NormalParams(mean=40.0, standard_deviation=math.sqrt(24.0)))
expected_probability = tail_probability_of_continuous(
    TailProbabilityInput(distribution=normal_approximation, upper_bound=45.0)
).probability

student_answer = 0.846
verify_numeric_answer(
    NumericAnswerInput(
        student_answer=student_answer,
        expected_answer=expected_probability,
        absolute_tolerance=5e-3,
    )
)
