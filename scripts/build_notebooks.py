"""Generates the five Spanish unit notebooks under book/chapters/.

Run with: uv run python scripts/build_notebooks.py
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = REPO_ROOT / "book" / "chapters"

KERNEL_SPEC = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3",
}
LANGUAGE_INFO = {
    "codemirror_mode": {"name": "ipython", "version": 3},
    "file_extension": ".py",
    "mimetype": "text/x-python",
    "name": "python",
    "nbconvert_exporter": "python",
    "pygments_lexer": "ipython3",
    "version": "3.13",
}


def _new_cell_id() -> str:
    return uuid.uuid4().hex[:8]


def markdown_cell(text: str) -> dict:
    return {
        "id": _new_cell_id(),
        "cell_type": "markdown",
        "metadata": {},
        "source": text.splitlines(keepends=True),
    }


def code_cell(text: str) -> dict:
    return {
        "id": _new_cell_id(),
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


def save_notebook(filename: str, cells: list[dict]) -> None:
    notebook = {
        "cells": cells,
        "metadata": {"kernelspec": KERNEL_SPEC, "language_info": LANGUAGE_INFO},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    output_path = CHAPTERS / filename
    output_path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False), encoding="utf-8")


# =============================================================================
# Unidad 1 — Tratamiento de Datos
# =============================================================================

UNIT_1_CELLS = [
    markdown_cell(
        "# Unidad 1 — Tratamiento de datos\n\n"
        "Esta unidad trabaja la **estadística descriptiva**: cómo resumir, ubicar y comunicar\n"
        "una muestra de datos antes de hablar de probabilidad. Trabajamos sobre tres miradas:\n\n"
        "- **Tendencia central** (¿dónde está el centro?): media, mediana.\n"
        "- **Dispersión** (¿qué tan apretados están los datos?): varianza, desvío, IQR.\n"
        "- **Posición y outliers** (¿hay puntos raros?): cuartiles, regla de Tukey.\n\n"
        "El código vive en `src/descriptive/` y `src/visualization/`; este notebook sólo lo orquesta.\n"
    ),
    markdown_cell(
        "## Importaciones\n\n"
        "El paquete `probabilidad` se instala editable al correr `uv sync`. No hay `sys.path`.\n"
    ),
    code_cell(
        "import numpy as np\n"
        "import pandas as pd\n\n"
        "from core import NormalParams, Observations, Settings\n"
        "from descriptive import (\n"
        "    FrequencyTableInput,\n"
        "    build_frequency_table,\n"
        "    detect_outliers_tukey,\n"
        "    standardize_observations,\n"
        "    summarize_observations,\n"
        ")\n"
        "from exercises import NumericAnswerInput, verify_numeric_answer\n"
        "from visualization import (\n"
        "    DescriptiveSummaryChartInput,\n"
        "    FrequencyChartInput,\n"
        "    HistogramChartInput,\n"
        "    chart_descriptive_summary,\n"
        "    chart_frequency_table,\n"
        "    chart_histogram,\n"
        ")\n"
        "from widgets import DescriptiveExplorerInput, build_descriptive_explorer\n"
    ),
    code_cell("settings = Settings()"),
    markdown_cell(
        "## Concreto (C de CPA): una muestra que podemos imaginar\n\n"
        "Pensemos en los **tiempos de espera (minutos) en una caja** durante 80 turnos.\n"
        "La generamos a partir de una Normal para tener un caso prolijo y reproducible.\n"
    ),
    code_cell(
        "rng = np.random.default_rng(settings.random_seed)\n"
        "raw_waiting_times = rng.normal(loc=4.0, scale=1.2, size=80).clip(min=0.0)\n"
        "waiting_times = Observations.validate(pd.DataFrame({'value': raw_waiting_times}))\n"
        "waiting_times.head()"
    ),
    markdown_cell(
        "## Pictórico (P de CPA): histograma con marca de clase y ojiva\n\n"
        "Antes de cualquier número, **dibujamos**. El histograma muestra la *forma* y la ojiva\n"
        "(la frecuencia relativa acumulada) responde \"¿qué porción de datos está por debajo de _x_?\".\n"
    ),
    code_cell(
        "frequency_table = build_frequency_table(\n"
        "    FrequencyTableInput(observations=waiting_times, bin_count=10)\n"
        ")\n"
        "chart_frequency_table(\n"
        "    FrequencyChartInput(frequency_table=frequency_table, settings=settings)\n"
        ")"
    ),
    markdown_cell(
        "## Abstracto (A de CPA): resumen numérico\n\n"
        "El resumen condensa la muestra en un objeto Pydantic — sin tablas sueltas — para que\n"
        "el resto del notebook lo pueda consumir de forma segura.\n"
    ),
    code_cell(
        "summary = summarize_observations(waiting_times)\n"
        "summary"
    ),
    markdown_cell(
        "### Intuición: media vs. mediana\n\n"
        "Cuando la distribución es **simétrica** (como acá), media y mediana están casi pegadas.\n"
        "Cuando hay **cola larga**, la media se mueve hacia la cola y la mediana se queda en el centro.\n"
        "Por eso la **mediana** es el resumen \"robusto\".\n"
    ),
    code_cell(
        "chart_descriptive_summary(\n"
        "    DescriptiveSummaryChartInput(\n"
        "        observations=waiting_times, statistics=summary, settings=settings\n"
        "    )\n"
        ")"
    ),
    markdown_cell(
        "## Detección de outliers (regla de Tukey)\n\n"
        "Un punto es outlier si cae fuera de $[Q_1 - 1{,}5\\,IQR,\\ Q_3 + 1{,}5\\,IQR]$.\n"
        "Es la misma regla que dibuja el *boxplot*: por eso lo usamos para pensar en outliers.\n"
    ),
    code_cell(
        "outlier_report = detect_outliers_tukey(waiting_times)\n"
        "outlier_report"
    ),
    markdown_cell(
        "## Posición: $z$-score\n\n"
        "El $z$-score traduce una observación a la pregunta: **¿a cuántos desvíos del promedio está?**.\n"
        "Es la *moneda común* de la unidad: nos prepara para Unidad 3 (estandarización de la Normal).\n\n"
        "$$ z_i = \\frac{x_i - \\bar{x}}{s} $$\n"
    ),
    code_cell(
        "standardized = standardize_observations(waiting_times)\n"
        "print('media estandarizada:', standardized.z_scores.mean())\n"
        "print('desvío estandarizado:', standardized.z_scores.std(ddof=1))"
    ),
    markdown_cell(
        "## Exploración interactiva\n\n"
        "Movés μ, σ, n y la cantidad de bins. El histograma, la ojiva y el boxplot se recalculan en\n"
        "vivo. Probá empujar σ a valores grandes: ¿qué pasa con el IQR vs. el rango?\n"
    ),
    code_cell(
        "build_descriptive_explorer(DescriptiveExplorerInput(settings=settings))"
    ),
    markdown_cell(
        "## Ejercicio 1 — Media de una muestra\n\n"
        "**Enunciado.** Sea la muestra $\\{2, 4, 4, 4, 5, 5, 7, 9\\}$. Calcular la media muestral.\n\n"
        "**Idea.** Sumar todos los valores y dividir por $n = 8$.\n\n"
        "$$ \\bar{x} = \\frac{2 + 4 + 4 + 4 + 5 + 5 + 7 + 9}{8} = \\frac{40}{8} = 5 $$\n"
    ),
    code_cell(
        "exercise_sample = Observations.validate(\n"
        "    pd.DataFrame({'value': [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]})\n"
        ")\n"
        "expected_mean = summarize_observations(exercise_sample).location.mean\n\n"
        "student_answer = 5.0\n"
        "verify_numeric_answer(\n"
        "    NumericAnswerInput(student_answer=student_answer, expected_answer=expected_mean)\n"
        ")"
    ),
    markdown_cell(
        "## Ejercicio 2 — Desvío estándar muestral\n\n"
        "**Enunciado.** Para la misma muestra, calcular el **desvío estándar muestral** $s$\n"
        "(divisor $n-1$).\n\n"
        "$$ s = \\sqrt{\\frac{1}{n-1}\\sum_{i=1}^{n}(x_i - \\bar{x})^2} $$\n\n"
        "Con $\\bar{x} = 5$:\n\n"
        "$$ s = \\sqrt{\\frac{(2-5)^2 + 3(4-5)^2 + 2(5-5)^2 + (7-5)^2 + (9-5)^2}{7}} = \\sqrt{\\frac{32}{7}} \\approx 2{,}138 $$\n"
    ),
    code_cell(
        "expected_standard_deviation = summarize_observations(exercise_sample).dispersion.sample_standard_deviation\n"
        "student_answer = 2.138\n"
        "verify_numeric_answer(\n"
        "    NumericAnswerInput(\n"
        "        student_answer=student_answer,\n"
        "        expected_answer=expected_standard_deviation,\n"
        "        absolute_tolerance=1e-2,\n"
        "        relative_tolerance=1e-2,\n"
        "    )\n"
        ")"
    ),
    markdown_cell(
        "## Para llevarse\n\n"
        "- **Resumir = ubicar + dispersar + posicionar**. No alcanza con uno solo.\n"
        "- La **mediana** y el **IQR** son robustos a outliers; la **media** y $s$ no.\n"
        "- El $z$-score es la **misma idea** que vamos a usar para la Normal estándar en Unidad 3.\n"
    ),
]


# =============================================================================
# Unidad 2 — Probabilidad
# =============================================================================

UNIT_2_CELLS = [
    markdown_cell(
        "# Unidad 2 — Probabilidad\n\n"
        "En esta unidad pasamos de **describir datos** a **modelar incertidumbre**. Las preguntas\n"
        "guía son:\n\n"
        "- ¿Cómo combinamos eventos? (uniones, intersecciones, complementos)\n"
        "- ¿Qué cambia cuando _ya sabemos_ algo? (probabilidad condicional)\n"
        "- ¿Cómo le damos vuelta a una pregunta? (Bayes)\n\n"
        "Las fórmulas viven en `src/symbolic/theorems.py`; los cálculos numéricos en\n"
        "`src/probability/`. Las visualizaciones interactivas en `src/widgets/bayes_explorer.py`.\n"
    ),
    markdown_cell("## Importaciones"),
    code_cell(
        "from core import Settings\n"
        "from exercises import NumericAnswerInput, verify_numeric_answer\n"
        "from probability import (\n"
        "    BayesInput,\n"
        "    ConditionalInput,\n"
        "    JointEventInput,\n"
        "    SetOperationInput,\n"
        "    evaluate_bayes,\n"
        "    evaluate_conditional_probability,\n"
        "    evaluate_set_operations,\n"
        "    joint_event_probabilities,\n"
        ")\n"
        "from probability.total_probability import TotalProbabilityBranch\n"
        "from symbolic import bayes_theorem, total_probability_theorem\n"
        "from widgets import BayesExplorerInput, build_bayes_explorer\n"
    ),
    code_cell("settings = Settings()"),
    markdown_cell(
        "## Concreto: un experimento con dado\n\n"
        "Tiramos un dado equilibrado. Definimos:\n\n"
        "- $A$ = \"sale par\" = $\\{2, 4, 6\\}$.\n"
        "- $B$ = \"sale mayor o igual que 4\" = $\\{4, 5, 6\\}$.\n\n"
        "Las operaciones de conjuntos son la **maquinaria mecánica** detrás de toda la unidad.\n"
    ),
    code_cell(
        "universe = frozenset({'1', '2', '3', '4', '5', '6'})\n"
        "event_even = frozenset({'2', '4', '6'})\n"
        "event_at_least_four = frozenset({'4', '5', '6'})\n\n"
        "set_result = evaluate_set_operations(\n"
        "    SetOperationInput(\n"
        "        universe=universe,\n"
        "        event_a=event_even,\n"
        "        event_b=event_at_least_four,\n"
        "    )\n"
        ")\n"
        "set_result"
    ),
    markdown_cell(
        "### Pictórico: diagrama de Venn mental\n\n"
        "Imaginá dos círculos solapados: $A \\cap B = \\{4, 6\\}$. La unión $A \\cup B$ es todo lo\n"
        "que cae en alguno de los dos. La **intuición Singapur** es esta:\n\n"
        "$$ |A \\cup B| = |A| + |B| - |A \\cap B| $$\n\n"
        "Si los sumás directamente, **contás dos veces** la intersección. Por eso se la resta.\n"
    ),
    markdown_cell(
        "## Abstracto: la regla aditiva en términos de probabilidad\n\n"
        "Dividiendo cardinalidades por $|\\Omega| = 6$ obtenemos la **regla aditiva**:\n\n"
        "$$ P(A \\cup B) = P(A) + P(B) - P(A \\cap B) $$\n"
    ),
    code_cell(
        "joint = joint_event_probabilities(\n"
        "    JointEventInput(\n"
        "        probability_a=3 / 6,\n"
        "        probability_b=3 / 6,\n"
        "        probability_intersection=2 / 6,\n"
        "    )\n"
        ")\n"
        "joint"
    ),
    markdown_cell(
        "## Probabilidad condicional\n\n"
        "$$ P(A \\mid B) = \\frac{P(A \\cap B)}{P(B)} $$\n\n"
        "**Intuición Singapur:** _restringir el universo_ a $B$. Dentro de ese universo nuevo\n"
        "preguntamos qué fracción cae también en $A$.\n"
    ),
    code_cell(
        "conditional = evaluate_conditional_probability(\n"
        "    ConditionalInput(\n"
        "        probability_intersection=2 / 6,\n"
        "        probability_conditioning_event=3 / 6,\n"
        "    )\n"
        ")\n"
        "conditional"
    ),
    markdown_cell(
        "## Teorema de Bayes (forma simbólica)\n\n"
        "Antes de calcular, miramos la fórmula simbólica viviendo en `src/symbolic/theorems.py`.\n"
        "Esta es la única vez que escribimos la fórmula a mano: el resto de la unidad la _reutiliza_.\n"
    ),
    code_cell(
        "bayes_theorem().formula"
    ),
    markdown_cell(
        "## Bayes con datos: prueba diagnóstica\n\n"
        "**Concreto.** Una enfermedad tiene prevalencia $P(D) = 1\\%$. El test tiene sensibilidad\n"
        "$99\\%$ y especificidad $95\\%$. Si el test da positivo, ¿cuál es $P(D \\mid +)$?\n\n"
        "**Intuición Singapur (pictórica).** Pensá en 10.000 personas. 100 tienen la enfermedad\n"
        "y 99 de ellas dan positivo. De las 9.900 sanas, 495 dan positivo de todas formas\n"
        "(falsos positivos). En total hay $99 + 495 = 594$ positivos; el porcentaje de \"verdaderos\n"
        "enfermos dentro de los positivos\" es $99 / 594 \\approx 16{,}7\\%$.\n\n"
        "**Abstracto:**\n\n"
        "$$ P(D \\mid +) = \\frac{P(+ \\mid D)\\,P(D)}{P(+ \\mid D)\\,P(D) + P(+ \\mid \\bar{D})\\,P(\\bar{D})} $$\n"
    ),
    code_cell(
        "branches = (\n"
        "    TotalProbabilityBranch(label='Enfermo', prior=0.01, likelihood=0.99),\n"
        "    TotalProbabilityBranch(label='Sano', prior=0.99, likelihood=0.05),\n"
        ")\n"
        "posteriors = evaluate_bayes(BayesInput(branches=branches))\n"
        "for posterior in posteriors:\n"
        "    print(posterior.label, posterior.posterior)"
    ),
    markdown_cell(
        "### Por qué la intuición duele\n\n"
        "Aunque el test es buenísimo (sensibilidad 99%), un positivo apenas mueve la creencia del\n"
        "$1\\%$ al $16{,}7\\%$. La culpa es de la **tasa base**: como casi nadie está enfermo, los\n"
        "falsos positivos pesan mucho. Movés los sliders y ves cómo la posterior reacciona.\n"
    ),
    code_cell(
        "build_bayes_explorer(BayesExplorerInput(settings=settings))"
    ),
    markdown_cell(
        "## Probabilidad total (forma simbólica)\n\n"
        "Si $\\{A_1, \\dots, A_k\\}$ es una partición del universo:\n\n"
        "$$ P(B) = \\sum_{i=1}^{k} P(B \\mid A_i)\\,P(A_i) $$\n"
    ),
    code_cell(
        "total_probability_theorem(partition_size=3).formula"
    ),
    markdown_cell(
        "## Ejercicio 1 — Regla aditiva\n\n"
        "Sea $P(A) = 0{,}6$, $P(B) = 0{,}5$, $P(A \\cap B) = 0{,}2$. Calcular $P(A \\cup B)$.\n\n"
        "**Idea.** Aplicar $P(A \\cup B) = P(A) + P(B) - P(A \\cap B) = 0{,}6 + 0{,}5 - 0{,}2 = 0{,}9$.\n"
    ),
    code_cell(
        "expected_union = joint_event_probabilities(\n"
        "    JointEventInput(probability_a=0.6, probability_b=0.5, probability_intersection=0.2)\n"
        ").union\n\n"
        "student_answer = 0.9\n"
        "verify_numeric_answer(\n"
        "    NumericAnswerInput(student_answer=student_answer, expected_answer=expected_union)\n"
        ")"
    ),
    markdown_cell(
        "## Ejercicio 2 — Bayes \"a mano\"\n\n"
        "Una caja $C_1$ tiene 3 bolas rojas y 7 blancas; la caja $C_2$ tiene 6 rojas y 4 blancas.\n"
        "Se elige una caja al azar (probabilidad $1/2$ cada una) y se saca una bola. Resulta roja.\n"
        "¿Cuál es $P(C_1 \\mid \\text{roja})$?\n\n"
        "**Idea.**\n\n"
        "$$ P(C_1 \\mid R) = \\frac{P(R \\mid C_1)\\,P(C_1)}{P(R \\mid C_1)\\,P(C_1) + P(R \\mid C_2)\\,P(C_2)}\n"
        " = \\frac{0{,}3 \\cdot 0{,}5}{0{,}3 \\cdot 0{,}5 + 0{,}6 \\cdot 0{,}5} = \\frac{0{,}15}{0{,}45} = \\frac{1}{3} $$\n"
    ),
    code_cell(
        "box_branches = (\n"
        "    TotalProbabilityBranch(label='C1', prior=0.5, likelihood=0.3),\n"
        "    TotalProbabilityBranch(label='C2', prior=0.5, likelihood=0.6),\n"
        ")\n"
        "expected_posterior = evaluate_bayes(BayesInput(branches=box_branches))[0].posterior\n\n"
        "student_answer = 1 / 3\n"
        "verify_numeric_answer(\n"
        "    NumericAnswerInput(student_answer=student_answer, expected_answer=expected_posterior)\n"
        ")"
    ),
    markdown_cell(
        "## Para llevarse\n\n"
        "- La regla aditiva existe **para no contar dos veces** la intersección.\n"
        "- Condicionar = **restringir el universo**.\n"
        "- Bayes invierte el sentido del condicionamiento usando la probabilidad total como denominador.\n"
        "- La tasa base manda más de lo que la intuición sugiere.\n"
    ),
]


# =============================================================================
# Unidad 3 — Variables Aleatorias
# =============================================================================

UNIT_3_CELLS = [
    markdown_cell(
        "# Unidad 3 — Variables aleatorias\n\n"
        "Una **variable aleatoria** es una función $X: \\Omega \\to \\mathbb{R}$ que le pone un\n"
        "número a cada resultado del experimento. Eso nos deja:\n\n"
        "- Hablar de **distribuciones** (la \"forma\" de probabilidades sobre los valores).\n"
        "- Definir **esperanza** y **varianza** como números.\n"
        "- Pasar de modelos discretos a continuos sin cambiar de lenguaje.\n\n"
        "Las distribuciones simbólicas viven en `src/symbolic/moments.py`; las numéricas en\n"
        "`src/distributions/`.\n"
    ),
    markdown_cell("## Importaciones"),
    code_cell(
        "from core import (\n"
        "    BinomialParams,\n"
        "    ContinuousUniformParams,\n"
        "    ExponentialParams,\n"
        "    NormalParams,\n"
        "    PoissonParams,\n"
        "    Settings,\n"
        ")\n"
        "from distributions import (\n"
        "    DensityGridInput,\n"
        "    MomentsInput,\n"
        "    ProbabilityMassInput,\n"
        "    QuantileInput,\n"
        "    TailProbabilityInput,\n"
        "    compute_numeric_moments,\n"
        "    evaluate_density_grid,\n"
        "    evaluate_probability_mass,\n"
        "    make_binomial,\n"
        "    make_exponential,\n"
        "    make_normal,\n"
        "    make_poisson,\n"
        "    quantile_of_continuous,\n"
        "    tail_probability_of_continuous,\n"
        ")\n"
        "from exercises import NumericAnswerInput, verify_numeric_answer\n"
        "from symbolic import (\n"
        "    compute_binomial_moments,\n"
        "    compute_normal_moments,\n"
        "    compute_poisson_moments,\n"
        "    standardize_normal,\n"
        ")\n"
        "from visualization import (\n"
        "    DensityChartInput,\n"
        "    ProbabilityMassChartInput,\n"
        "    chart_density,\n"
        "    chart_probability_mass,\n"
        ")\n"
        "from widgets import (\n"
        "    ContinuousDistributionExplorerInput,\n"
        "    DiscreteDistributionExplorerInput,\n"
        "    build_continuous_distribution_explorer,\n"
        "    build_discrete_distribution_explorer,\n"
        ")\n"
    ),
    code_cell("settings = Settings()"),
    markdown_cell(
        "## Concreto (discreto): Binomial(10, 0.3)\n\n"
        "Tiramos una moneda sesgada 10 veces. $X$ cuenta cuántas caras salen.\n"
        "$X \\sim \\text{Bin}(n=10, p=0{,}3)$.\n\n"
        "**Intuición Singapur.** $E[X] = np = 3$ es el \"centro de gravedad\" si dibujamos las\n"
        "barras del PMF. Movés $p$ y el centro se mueve linealmente.\n"
    ),
    code_cell(
        "binomial_distribution = make_binomial(BinomialParams(trials=10, success_probability=0.3))\n"
        "probability_mass = evaluate_probability_mass(\n"
        "    ProbabilityMassInput(distribution=binomial_distribution)\n"
        ")\n"
        "chart_probability_mass(\n"
        "    ProbabilityMassChartInput(probability_mass=probability_mass, settings=settings)\n"
        ")"
    ),
    markdown_cell(
        "### Momentos simbólicos\n\n"
        "Los mismos momentos pero como expresiones simbólicas — útiles para *demostrar* las\n"
        "fórmulas \"$np$\" y \"$np(1-p)$\" en clase sin escribirlas dos veces.\n"
    ),
    code_cell(
        "binomial_moments_symbolic = compute_binomial_moments(\n"
        "    BinomialParams(trials=10, success_probability=0.3)\n"
        ")\n"
        "print('E[X] =', binomial_moments_symbolic.expectation)\n"
        "print('Var[X] =', binomial_moments_symbolic.variance)\n\n"
        "binomial_moments_numeric = compute_numeric_moments(\n"
        "    MomentsInput(distribution=binomial_distribution)\n"
        ")\n"
        "binomial_moments_numeric"
    ),
    markdown_cell(
        "## Concreto (continuo): Normal(0, 1)\n\n"
        "Pasamos del PMF (barras) al PDF (curva). La **probabilidad ya no vive en los puntos**:\n"
        "vive en el **área debajo de la curva**.\n\n"
        "$$ P(a \\le X \\le b) = \\int_a^b f_X(x)\\,dx $$\n"
    ),
    code_cell(
        "standard_normal_distribution = make_normal(NormalParams(mean=0.0, standard_deviation=1.0))\n"
        "density = evaluate_density_grid(\n"
        "    DensityGridInput(distribution=standard_normal_distribution, settings=settings)\n"
        ")\n"
        "chart_density(DensityChartInput(density_grid=density, settings=settings))"
    ),
    markdown_cell(
        "### Estandarización\n\n"
        "Cualquier Normal $X \\sim \\mathcal{N}(\\mu, \\sigma^2)$ se convierte en\n"
        "$Z \\sim \\mathcal{N}(0, 1)$ con un cambio de variable lineal:\n"
    ),
    code_cell(
        "standardize_normal(NormalParams(mean=170.0, standard_deviation=8.0)).formula"
    ),
    markdown_cell(
        "Es la **misma transformación** que usamos en Unidad 1 con el $z$-score. La diferencia\n"
        "es que ahora sabemos qué distribución tiene el resultado: $\\mathcal{N}(0, 1)$.\n"
    ),
    markdown_cell(
        "## Pictórico: probabilidades como áreas\n\n"
        "Pregunta concreta: si las alturas en una población se distribuyen $\\mathcal{N}(170, 8^2)$,\n"
        "¿cuál es la probabilidad de medir entre 165 y 180 cm?\n"
    ),
    code_cell(
        "heights_distribution = make_normal(NormalParams(mean=170.0, standard_deviation=8.0))\n"
        "probability_between = tail_probability_of_continuous(\n"
        "    TailProbabilityInput(\n"
        "        distribution=heights_distribution, lower_bound=165.0, upper_bound=180.0\n"
        "    )\n"
        ")\n"
        "probability_between"
    ),
    markdown_cell(
        "## Cuantiles: invertir la pregunta\n\n"
        "En lugar de fijar $x$ y leer probabilidad, fijamos probabilidad y leemos $x$. El\n"
        "**percentil 90** es \"el valor por debajo del cual queda el 90% de la población\".\n"
    ),
    code_cell(
        "percentile_ninety = quantile_of_continuous(\n"
        "    QuantileInput(distribution=heights_distribution, probability=0.90)\n"
        ")\n"
        "percentile_ninety"
    ),
    markdown_cell(
        "## Exploración interactiva — distribuciones continuas\n\n"
        "Cambiamos familia, parámetros y un intervalo $[x_{\\min}, x_{\\max}]$. La probabilidad\n"
        "se actualiza en vivo.\n"
    ),
    code_cell(
        "build_continuous_distribution_explorer(\n"
        "    ContinuousDistributionExplorerInput(settings=settings)\n"
        ")"
    ),
    markdown_cell(
        "## Exploración interactiva — distribuciones discretas\n\n"
        "Pasamos de Binomial a Poisson moviendo el dropdown. **Intuición:** cuando $n$ es grande y\n"
        "$p$ es chico (con $np = \\lambda$ moderado), Binomial $\\approx$ Poisson.\n"
    ),
    code_cell(
        "build_discrete_distribution_explorer(\n"
        "    DiscreteDistributionExplorerInput(settings=settings)\n"
        ")"
    ),
    markdown_cell(
        "## Poisson para eventos raros\n\n"
        "Un call center recibe en promedio $\\lambda = 4$ llamadas por minuto. ¿Probabilidad de\n"
        "recibir exactamente 6 en un minuto?\n\n"
        "$$ P(K = 6) = \\frac{\\lambda^6 e^{-\\lambda}}{6!} $$\n"
    ),
    code_cell(
        "poisson_distribution = make_poisson(PoissonParams(rate=4.0))\n"
        "poisson_mass = evaluate_probability_mass(\n"
        "    ProbabilityMassInput(\n"
        "        distribution=poisson_distribution, lower_outcome=0, upper_outcome=12\n"
        "    )\n"
        ")\n"
        "chart_probability_mass(\n"
        "    ProbabilityMassChartInput(probability_mass=poisson_mass, settings=settings)\n"
        ")"
    ),
    markdown_cell(
        "## Ejercicio 1 — Estandarización\n\n"
        "$X \\sim \\mathcal{N}(170, 8^2)$. Calcular $P(X \\le 178)$ usando $Z = (X - 170)/8$.\n\n"
        "$$ P(X \\le 178) = P(Z \\le 1) \\approx 0{,}8413 $$\n"
    ),
    code_cell(
        "expected_probability = tail_probability_of_continuous(\n"
        "    TailProbabilityInput(distribution=heights_distribution, upper_bound=178.0)\n"
        ").probability\n\n"
        "student_answer = 0.8413\n"
        "verify_numeric_answer(\n"
        "    NumericAnswerInput(\n"
        "        student_answer=student_answer,\n"
        "        expected_answer=expected_probability,\n"
        "        absolute_tolerance=1e-3,\n"
        "    )\n"
        ")"
    ),
    markdown_cell(
        "## Ejercicio 2 — Esperanza de una Poisson\n\n"
        "Si $K \\sim \\text{Poisson}(\\lambda = 3{,}5)$, ¿cuál es $E[K]$?\n\n"
        "**Idea.** $E[K] = \\lambda = 3{,}5$. La Poisson **es** su tasa.\n"
    ),
    code_cell(
        "expected_expectation = compute_poisson_moments(PoissonParams(rate=3.5)).expectation\n\n"
        "student_answer = 3.5\n"
        "verify_numeric_answer(\n"
        "    NumericAnswerInput(student_answer=student_answer, expected_answer=float(expected_expectation))\n"
        ")"
    ),
    markdown_cell(
        "## Para llevarse\n\n"
        "- **PMF (discreto) ↔ PDF (continuo)**: la probabilidad pasa de \"barras\" a \"áreas\".\n"
        "- Estandarizar = trasladar y reescalar para hablar todos el mismo idioma.\n"
        "- La Normal estándar **no** describe a la población; es la unidad de medida con la que la describimos.\n"
        "- Bin($n$ grande, $p$ chico) $\\to$ Poisson($\\lambda = np$): el discreto colapsa al \"raro\".\n"
    ),
]


# =============================================================================
# Unidad 4 — VA bidimensionales y sumas
# =============================================================================

UNIT_4_CELLS = [
    markdown_cell(
        "# Unidad 4 — VA bidimensionales y suma de variables\n\n"
        "Cuando trabajamos con **varias variables a la vez** aparecen dos preguntas centrales:\n\n"
        "1. ¿Cómo se distribuye la **suma** $S_n = X_1 + \\dots + X_n$?\n"
        "2. ¿Qué pasa con la **media muestral** $\\bar{X}_n$ cuando $n$ crece?\n\n"
        "Las dos respuestas son **el corazón estadístico de la materia**:\n\n"
        "- **LLN (Ley de los grandes números):** $\\bar{X}_n \\to \\mu$ casi seguramente.\n"
        "- **TCL (Teorema central del límite):** $\\sqrt{n}\\,(\\bar{X}_n - \\mu) \\to \\mathcal{N}(0, \\sigma^2)$.\n"
    ),
    markdown_cell("## Importaciones"),
    code_cell(
        "from core import BinomialParams, ContinuousUniformParams, ExponentialParams, Settings\n"
        "from distributions import make_binomial, make_continuous_uniform, make_exponential\n"
        "from exercises import NumericAnswerInput, verify_numeric_answer\n"
        "from sampling import (\n"
        "    CLTSimulationInput,\n"
        "    GaltonBoardInput,\n"
        "    LLNSimulationInput,\n"
        "    simulate_clt,\n"
        "    simulate_galton_board,\n"
        "    simulate_lln,\n"
        ")\n"
        "from visualization import (\n"
        "    CLTComparisonChartInput,\n"
        "    LLNChartInput,\n"
        "    chart_clt_comparison,\n"
        "    chart_lln_running_mean,\n"
        ")\n"
        "from widgets import (\n"
        "    CLTExplorerInput,\n"
        "    LLNExplorerInput,\n"
        "    build_clt_explorer,\n"
        "    build_lln_explorer,\n"
        ")\n"
    ),
    code_cell("settings = Settings()"),
    markdown_cell(
        "## Concreto: tirar una moneda y promediar\n\n"
        "Sea $X_i$ una Bernoulli($p = 0{,}3$): cara=1, ceca=0. La media muestral $\\bar{X}_n$ es\n"
        "**la proporción observada de caras** después de $n$ tiradas.\n\n"
        "Si $p$ es la \"verdad\", la LLN promete que $\\bar{X}_n \\to 0{,}3$ cuando $n \\to \\infty$.\n"
    ),
    code_cell(
        "bernoulli = make_binomial(BinomialParams(trials=1, success_probability=0.3))\n"
        "lln_result = simulate_lln(\n"
        "    LLNSimulationInput(distribution=bernoulli, horizon=4_000, settings=settings)\n"
        ")\n"
        "chart_lln_running_mean(LLNChartInput(lln_result=lln_result, settings=settings))"
    ),
    markdown_cell(
        "### Intuición Singapur — \"se estabiliza\"\n\n"
        "Los datos al principio rebotan mucho. **No** porque las primeras tiradas sean diferentes,\n"
        "sino porque al promediar pocos datos cada nueva observación pesa mucho. Después de unos\n"
        "miles, una tirada extra cambia la media en un orden de magnitud despreciable.\n"
    ),
    code_cell(
        "build_lln_explorer(LLNExplorerInput(settings=settings))"
    ),
    markdown_cell(
        "## Concreto: tablero de Galton\n\n"
        "El **tablero de Galton** es la metáfora pictórica del TCL. Cada bola toma 20 decisiones\n"
        "independientes izquierda/derecha. La **posición final** es una **suma** de 20 ±1, y se\n"
        "distribuye aproximadamente como una Normal — aunque cada paso individual es uniforme.\n"
    ),
    code_cell(
        "import altair as alt\n"
        "import pandas as pd\n\n"
        "galton_result = simulate_galton_board(\n"
        "    GaltonBoardInput(rows=24, balls=8_000, settings=settings)\n"
        ")\n"
        "galton_table = pd.DataFrame(\n"
        "    {\n"
        "        'posición': galton_result.bin_positions,\n"
        "        'frecuencia': galton_result.bin_counts,\n"
        "    }\n"
        ")\n"
        "alt.Chart(galton_table).mark_bar(opacity=0.75, color='#1f77b4').encode(\n"
        "    x=alt.X('posición:O', title='Casilla'),\n"
        "    y=alt.Y('frecuencia:Q', title='Bolas'),\n"
        ").properties(width=520, height=320, title='Tablero de Galton — suma de 24 pasos ±1')"
    ),
    markdown_cell(
        "## Pictórico: el TCL en acción\n\n"
        "Tomamos $n$ muestras de una **Exponencial** (que está muy lejos de ser Normal: tiene\n"
        "cola larga y es asimétrica). Calculamos la media. **Repetimos miles de veces** y dibujamos\n"
        "la distribución de las **medias estandarizadas**. La cosa converge a $\\mathcal{N}(0, 1)$\n"
        "incluso aunque la fuente sea \"fea\".\n"
    ),
    code_cell(
        "exponential_distribution = make_exponential(ExponentialParams(rate=1.0))\n"
        "clt_result = simulate_clt(\n"
        "    CLTSimulationInput(\n"
        "        distribution=exponential_distribution,\n"
        "        sample_size_per_replicate=30,\n"
        "        replicates=5_000,\n"
        "        settings=settings,\n"
        "    )\n"
        ")\n"
        "chart_clt_comparison(\n"
        "    CLTComparisonChartInput(clt_result=clt_result, settings=settings)\n"
        ")"
    ),
    markdown_cell(
        "### Intuición Singapur — \"promediar limpia la asimetría\"\n\n"
        "Cada exponencial tiene una cola larga a la derecha. Pero al **promediar 30 exponenciales**,\n"
        "las colas se cancelan parcialmente: las muestras altas y bajas se compensan. Cuanto más\n"
        "grande es $n$, menos se nota el origen de las muestras.\n"
    ),
    code_cell(
        "build_clt_explorer(CLTExplorerInput(settings=settings))"
    ),
    markdown_cell(
        "## Abstracto: qué dice exactamente el TCL\n\n"
        "Sean $X_1, X_2, \\dots$ i.i.d. con $E[X_i] = \\mu$ y $\\mathrm{Var}(X_i) = \\sigma^2 < \\infty$.\n"
        "Entonces:\n\n"
        "$$ Z_n = \\frac{\\bar{X}_n - \\mu}{\\sigma / \\sqrt{n}} \\xrightarrow{d} \\mathcal{N}(0, 1). $$\n\n"
        "**Notar.** El TCL **no** dice que $X_i$ tienda a una Normal. Dice que la **media\n"
        "estandarizada** tiende a una Normal. Es la *estructura del promedio* la que se vuelve Normal.\n"
    ),
    markdown_cell(
        "## Aproximación Normal a Binomial\n\n"
        "Como consecuencia: si $Y \\sim \\text{Bin}(n, p)$, entonces $Y \\approx \\mathcal{N}(np, np(1-p))$\n"
        "para $n$ grande (regla práctica: $np \\ge 10$ y $n(1-p) \\ge 10$).\n"
    ),
    markdown_cell(
        "## Ejercicio 1 — Distribución de la media muestral\n\n"
        "Si $X_i \\sim \\mathcal{N}(50, 100)$ (desvío 10) y tomamos $n = 25$ observaciones,\n"
        "¿cuál es el desvío estándar de $\\bar{X}_n$?\n\n"
        "**Idea.** $\\sigma_{\\bar{X}} = \\sigma / \\sqrt{n} = 10 / \\sqrt{25} = 2$.\n"
    ),
    code_cell(
        "import math\n\n"
        "expected_standard_error = 10.0 / math.sqrt(25)\n"
        "student_answer = 2.0\n"
        "verify_numeric_answer(\n"
        "    NumericAnswerInput(student_answer=student_answer, expected_answer=expected_standard_error)\n"
        ")"
    ),
    markdown_cell(
        "## Ejercicio 2 — Aproximación Binomial-Normal\n\n"
        "$Y \\sim \\text{Bin}(n = 100, p = 0{,}4)$. Aproximar $P(Y \\le 45)$ con la Normal\n"
        "(sin corrección por continuidad para simplificar).\n\n"
        "**Idea.** $E[Y] = 40$, $\\mathrm{Var}(Y) = 24$. Estandarizamos:\n"
        "$P(Y \\le 45) \\approx P\\bigl(Z \\le (45 - 40)/\\sqrt{24}\\bigr) \\approx P(Z \\le 1{,}02) \\approx 0{,}846$.\n"
    ),
    code_cell(
        "from distributions import make_normal\n"
        "from core import NormalParams\n"
        "from distributions.evaluations import TailProbabilityInput\n"
        "from distributions import tail_probability_of_continuous\n\n"
        "normal_approximation = make_normal(\n"
        "    NormalParams(mean=40.0, standard_deviation=math.sqrt(24.0))\n"
        ")\n"
        "expected_probability = tail_probability_of_continuous(\n"
        "    TailProbabilityInput(distribution=normal_approximation, upper_bound=45.0)\n"
        ").probability\n\n"
        "student_answer = 0.846\n"
        "verify_numeric_answer(\n"
        "    NumericAnswerInput(\n"
        "        student_answer=student_answer,\n"
        "        expected_answer=expected_probability,\n"
        "        absolute_tolerance=5e-3,\n"
        "    )\n"
        ")"
    ),
    markdown_cell(
        "## Para llevarse\n\n"
        "- LLN: el promedio se *clava* en $\\mu$.\n"
        "- TCL: el promedio **estandarizado** se vuelve Normal, sin importar la fuente.\n"
        "- Esto justifica por qué la **Normal** aparece tan seguido en datos reales: muchos\n"
        "  fenómenos son sumas/promedios de efectos chicos e independientes.\n"
    ),
]


# =============================================================================
# Unidad 5 — Inferencia
# =============================================================================

UNIT_5_CELLS = [
    markdown_cell(
        "# Unidad 5 — Inferencia\n\n"
        "Toda la materia hasta acá nos permitía **calcular probabilidades** dados los parámetros.\n"
        "La inferencia invierte el problema: vemos **una muestra** y queremos hacer afirmaciones\n"
        "sobre los **parámetros** que la generaron.\n\n"
        "Tres herramientas centrales:\n\n"
        "- **Intervalos de confianza** (IC) — rango plausible para $\\mu$, $p$ o $\\sigma^2$.\n"
        "- **Pruebas de hipótesis** — decisión binaria con control del error tipo I.\n"
        "- **Tamaño muestral** — cuánto necesitamos para una precisión dada.\n"
    ),
    markdown_cell("## Importaciones"),
    code_cell(
        "import numpy as np\n"
        "import pandas as pd\n\n"
        "from core import NormalParams, Observations, Settings\n"
        "from exercises import (\n"
        "    IntervalContainsInput,\n"
        "    NumericAnswerInput,\n"
        "    verify_interval_contains,\n"
        "    verify_numeric_answer,\n"
        ")\n"
        "from inference import (\n"
        "    MeanKnownVarianceInput,\n"
        "    MeanUnknownVarianceInput,\n"
        "    OneSampleMeanTestInput,\n"
        "    ProportionInput,\n"
        "    SampleSizeForMeanInput,\n"
        "    SampleSizeForProportionInput,\n"
        "    VarianceInput,\n"
        "    build_confidence_interval_for_mean_known_variance,\n"
        "    build_confidence_interval_for_mean_unknown_variance,\n"
        "    build_confidence_interval_for_proportion,\n"
        "    build_confidence_interval_for_variance,\n"
        "    sample_size_for_mean,\n"
        "    sample_size_for_proportion,\n"
        "    test_one_sample_mean,\n"
        ")\n"
        "from inference.hypothesis_tests import Alternative\n"
        "from sampling import BootstrapInput, bootstrap_mean\n"
        "from visualization import BootstrapDistributionChartInput, chart_bootstrap_distribution\n"
        "from widgets import MeanCIExplorerInput, build_mean_ci_explorer\n"
    ),
    code_cell("settings = Settings()"),
    markdown_cell(
        "## Concreto: IC para la media con $\\sigma$ conocido\n\n"
        "Suponemos que tenemos $n = 36$ mediciones de tiempo de servicio con $\\bar{x} = 12$ min y\n"
        "sabemos que $\\sigma = 3$ min (info histórica). Queremos un IC al 95%.\n\n"
        "$$ \\bar{x} \\pm z_{1-\\alpha/2}\\,\\frac{\\sigma}{\\sqrt{n}} = 12 \\pm 1{,}96 \\cdot \\frac{3}{6}\n"
        " = 12 \\pm 0{,}98 = (11{,}02,\\ 12{,}98). $$\n"
    ),
    code_cell(
        "confidence_interval = build_confidence_interval_for_mean_known_variance(\n"
        "    MeanKnownVarianceInput(\n"
        "        sample_mean=12.0,\n"
        "        population_standard_deviation=3.0,\n"
        "        sample_size=36,\n"
        "        confidence_level=0.95,\n"
        "    )\n"
        ")\n"
        "confidence_interval"
    ),
    markdown_cell(
        "### Intuición Singapur — \"qué es 95% de confianza\"\n\n"
        "**No** es \"el verdadero $\\mu$ está con probabilidad 0{,}95 en este intervalo\". El verdadero\n"
        "$\\mu$ es una constante (no es aleatorio). Lo aleatorio es la muestra y, por lo tanto, el\n"
        "intervalo. La afirmación correcta es:\n\n"
        "> **\"Si repitiéramos este procedimiento muchas veces, el 95% de los intervalos producidos\n"
        "> contendrían a $\\mu$.\"**\n\n"
        "El widget de abajo lo materializa: cada línea es un intervalo de una muestra distinta.\n"
    ),
    code_cell(
        "build_mean_ci_explorer(MeanCIExplorerInput(settings=settings))"
    ),
    markdown_cell(
        "## IC con $\\sigma$ desconocido — la $t$ de Student\n\n"
        "Cuando no conocemos $\\sigma$ lo estimamos con $s$. Pero entonces el pivote\n"
        "$T = (\\bar{X} - \\mu)/(s/\\sqrt{n})$ tiene **más cola** que la Normal — distribuye como\n"
        "$t_{n-1}$. Para $n$ grande la $t$ converge a la Normal estándar.\n"
    ),
    code_cell(
        "build_confidence_interval_for_mean_unknown_variance(\n"
        "    MeanUnknownVarianceInput(\n"
        "        sample_mean=12.0,\n"
        "        sample_standard_deviation=3.0,\n"
        "        sample_size=36,\n"
        "        confidence_level=0.95,\n"
        "    )\n"
        ")"
    ),
    markdown_cell(
        "## IC para proporción\n\n"
        "En una encuesta de $n = 400$ personas, $200$ dicen \"sí\". $\\hat{p} = 0{,}50$.\n"
        "El IC de Wald al 95% queda:\n\n"
        "$$ \\hat{p} \\pm z\\,\\sqrt{\\frac{\\hat{p}(1-\\hat{p})}{n}}. $$\n"
    ),
    code_cell(
        "build_confidence_interval_for_proportion(\n"
        "    ProportionInput(successes=200, sample_size=400, confidence_level=0.95)\n"
        ")"
    ),
    markdown_cell(
        "## IC para la varianza — la $\\chi^2$\n\n"
        "Si $X_1, \\dots, X_n \\sim \\mathcal{N}(\\mu, \\sigma^2)$, entonces\n"
        "$\\dfrac{(n-1)S^2}{\\sigma^2} \\sim \\chi^2_{n-1}$.\n\n"
        "**Intuición Singapur.** La $\\chi^2$ es una **suma de cuadrados** de normales estándar.\n"
        "Las desviaciones cuadráticas son no negativas: la $\\chi^2$ vive en $[0, \\infty)$.\n"
    ),
    code_cell(
        "build_confidence_interval_for_variance(\n"
        "    VarianceInput(sample_variance=9.0, sample_size=36, confidence_level=0.95)\n"
        ")"
    ),
    markdown_cell(
        "## Test de hipótesis para la media\n\n"
        "Queremos chequear si la media de servicio es realmente 11 minutos (lo que dice el manual).\n"
        "Observamos $\\bar{x} = 12$, $s = 3$, $n = 36$.\n\n"
        "- $H_0: \\mu = 11$\n"
        "- $H_1: \\mu \\ne 11$\n"
        "- $\\alpha = 0{,}05$\n\n"
        "Estadístico: $T = (\\bar{X} - 11)/(s/\\sqrt{n})$.\n"
    ),
    code_cell(
        "mean_test_result = test_one_sample_mean(\n"
        "    OneSampleMeanTestInput(\n"
        "        sample_mean=12.0,\n"
        "        sample_standard_deviation=3.0,\n"
        "        sample_size=36,\n"
        "        null_mean=11.0,\n"
        "        alternative=Alternative.TWO_SIDED,\n"
        "        significance_level=0.05,\n"
        "    )\n"
        ")\n"
        "mean_test_result"
    ),
    markdown_cell(
        "### Conexión IC ↔ Test\n\n"
        "Un test bilateral al nivel $\\alpha$ rechaza $H_0: \\mu = \\mu_0$ **sí y sólo sí** $\\mu_0$\n"
        "**no cae** dentro del IC al nivel $1 - \\alpha$ construido sobre la misma muestra.\n"
        "Es el mismo objeto, visto desde dos ángulos.\n"
    ),
    markdown_cell(
        "## Bootstrap — IC sin supuestos paramétricos\n\n"
        "Cuando no queremos asumir Normalidad ni conocer $\\sigma$, podemos **remuestrear**: tomar\n"
        "muchas muestras con reemplazo del conjunto observado y mirar la distribución de las\n"
        "medias bootstrap. El IC sale de sus percentiles 2{,}5 y 97{,}5.\n"
    ),
    code_cell(
        "rng = np.random.default_rng(settings.random_seed)\n"
        "synthetic_sample = Observations.validate(\n"
        "    pd.DataFrame({'value': rng.normal(loc=12.0, scale=3.0, size=36)})\n"
        ")\n"
        "bootstrap_result = bootstrap_mean(\n"
        "    BootstrapInput(observations=synthetic_sample, replicates=3_000, settings=settings)\n"
        ")\n"
        "chart_bootstrap_distribution(\n"
        "    BootstrapDistributionChartInput(bootstrap_result=bootstrap_result, settings=settings)\n"
        ")"
    ),
    markdown_cell(
        "## Tamaño muestral para una precisión dada\n\n"
        "Si queremos un margen de error $\\le 1$ minuto con $95\\%$ de confianza y sabemos que\n"
        "$\\sigma = 3$:\n\n"
        "$$ n \\ge \\left(\\frac{z\\,\\sigma}{E}\\right)^2 = (1{,}96 \\cdot 3 / 1)^2 \\approx 35 $$\n"
    ),
    code_cell(
        "sample_size_for_mean(\n"
        "    SampleSizeForMeanInput(\n"
        "        population_standard_deviation=3.0,\n"
        "        margin_of_error=1.0,\n"
        "        confidence_level=0.95,\n"
        "    )\n"
        ")"
    ),
    markdown_cell(
        "## Ejercicio 1 — IC contiene el verdadero $\\mu$\n\n"
        "Construir un IC al 95% para $\\mu$ con $\\bar{x} = 12$, $\\sigma = 3$, $n = 36$, y\n"
        "verificar que contenga el valor de control $\\mu_0 = 11{,}5$.\n"
    ),
    code_cell(
        "interval = build_confidence_interval_for_mean_known_variance(\n"
        "    MeanKnownVarianceInput(\n"
        "        sample_mean=12.0,\n"
        "        population_standard_deviation=3.0,\n"
        "        sample_size=36,\n"
        "        confidence_level=0.95,\n"
        "    )\n"
        ")\n"
        "verify_interval_contains(\n"
        "    IntervalContainsInput(\n"
        "        lower_bound=interval.lower_bound,\n"
        "        upper_bound=interval.upper_bound,\n"
        "        target_value=11.5,\n"
        "    )\n"
        ")"
    ),
    markdown_cell(
        "## Ejercicio 2 — Tamaño muestral para una proporción\n\n"
        "Queremos estimar la intención de voto con un margen de error de $\\pm 3\\%$ al $95\\%$ de\n"
        "confianza. Usamos $\\hat{p} = 0{,}5$ (peor caso).\n\n"
        "$$ n \\ge \\left(\\frac{1{,}96}{0{,}03}\\right)^2 \\cdot 0{,}25 \\approx 1067 $$\n"
    ),
    code_cell(
        "expected_size = sample_size_for_proportion(\n"
        "    SampleSizeForProportionInput(\n"
        "        estimated_proportion=0.5,\n"
        "        margin_of_error=0.03,\n"
        "        confidence_level=0.95,\n"
        "    )\n"
        ").required_sample_size\n\n"
        "student_answer = 1067.0\n"
        "verify_numeric_answer(\n"
        "    NumericAnswerInput(\n"
        "        student_answer=student_answer,\n"
        "        expected_answer=float(expected_size),\n"
        "        absolute_tolerance=1.0,\n"
        "    )\n"
        ")"
    ),
    markdown_cell(
        "## Para llevarse\n\n"
        "- Un IC describe el **procedimiento**, no la muestra particular.\n"
        "- $\\sigma$ desconocido → $t$ de Student → colas más anchas que la Normal.\n"
        "- Test e IC son **dual**: rechazar $H_0$ equivale a que $\\mu_0$ caiga fuera del IC.\n"
        "- Bootstrap evita la mayoría de los supuestos y se apoya en la **misma muestra observada**.\n"
        "- El tamaño muestral crece como $1/E^2$: para reducir el margen a la mitad, hace falta $4\\times$ más datos.\n"
    ),
]


# =============================================================================
# Build
# =============================================================================

NOTEBOOKS = {
    "01_unidad1_tratamiento_datos.ipynb": UNIT_1_CELLS,
    "02_unidad2_probabilidad.ipynb": UNIT_2_CELLS,
    "03_unidad3_variables_aleatorias.ipynb": UNIT_3_CELLS,
    "04_unidad4_va_bidimensionales_suma.ipynb": UNIT_4_CELLS,
    "05_unidad5_inferencia.ipynb": UNIT_5_CELLS,
}


def main() -> None:
    CHAPTERS.mkdir(parents=True, exist_ok=True)
    for filename, cells in NOTEBOOKS.items():
        save_notebook(filename, cells)
        print(f"wrote {filename}")


if __name__ == "__main__":
    main()
