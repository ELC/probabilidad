---
title: Práctica — Variables aleatorias
short_title: Práctica
kernelspec:
  name: python3
  display_name: Python 3
---

# Práctica — Variables aleatorias

Esta sección reúne ejercicios para fijar los modelos del capítulo de
[Variables aleatorias](random_variables.md): Bernoulli, Binomial, Geométrica,
Normal, Exponencial y Poisson. Cada enunciado lleva debajo una
**solución** plegada con el paso a paso, una visualización y la
verificación. Antes de abrirla, intentá el cálculo a mano.

```{code-cell} python
:tags: [hide-input]
import numpy as np

from core import (
    BinomialParams,
    ExponentialParams,
    GeometricParams,
    NormalParams,
    PoissonParams,
    Settings,
)
from distributions import (
    DensityGridInput,
    MomentsInput,
    ProbabilityMassInput,
    QuantileInput,
    SurvivalInput,
    TailProbabilityInput,
    compute_numeric_moments,
    evaluate_density_grid,
    evaluate_probability_mass,
    make_binomial,
    make_exponential,
    make_geometric,
    make_normal,
    make_poisson,
    quantile_of_continuous,
    survival_of_continuous,
    tail_probability_of_continuous,
)
from exercises import (
    BooleanAnswerInput,
    DistributionMatchInput,
    NumericAnswerInput,
    verify_boolean_answer,
    verify_distribution_match,
    verify_numeric_answer,
)
from visualization import (
    DensityChartInput,
    ProbabilityMassChartInput,
    chart_density,
    chart_probability_mass,
)

settings = Settings()
```

## Ejercicio 1 — PMF Binomial

En una línea de producción el 4 % de las piezas salen defectuosas. Se
inspeccionan 20 piezas elegidas al azar. ¿Cuál es la probabilidad de
que **exactamente 2** resulten defectuosas?

:::{admonition} Solución
:class: dropdown

### Planteo

Sea $X$ = cantidad de defectuosas en 20 piezas. Como cada pieza es
independiente y tiene la misma probabilidad de defecto,
$X \sim \text{Bin}(n = 20,\ p = 0{,}04)$.

### Derivación

Por la PMF Binomial ([](random_variables.md#eq-binomial-pmf)),

$$
P(X = 2) = \binom{20}{2}(0{,}04)^{2}(0{,}96)^{18}.
$$

Numéricamente,

$$
P(X = 2) = 190 \cdot 0{,}0016 \cdot 0{,}4796 \approx 0{,}146.
$$

### Visual

```{code-cell} python
defect_distribution = make_binomial(BinomialParams(trials=20, success_probability=0.04))
chart_probability_mass(
    ProbabilityMassChartInput(
        probability_mass=evaluate_probability_mass(
            ProbabilityMassInput(distribution=defect_distribution, lower_outcome=0, upper_outcome=6),
        ),
        settings=settings,
    )
)
```

### Verificación

```{code-cell} python
expected_mass = float(defect_distribution.frozen_distribution.pmf(2))

verify_numeric_answer(
    NumericAnswerInput(
        student_answer=0.146,
        expected_answer=expected_mass,
        absolute_tolerance=0.005,
    )
)
```

:::

## Ejercicio 2 — Poisson en un período corto

A una guardia llegan en promedio **6 pacientes por hora**, siguiendo un
proceso de Poisson. ¿Cuál es la probabilidad de que en **20 minutos**
no llegue **nadie**?

:::{admonition} Solución
:class: dropdown

### Planteo

Reescalamos la tasa al período de interés: en 20 minutos = 1/3 de hora
esperamos en promedio $\lambda = 6 \cdot (1/3) = 2$ pacientes. Sea
$Y$ = cantidad de pacientes en 20 minutos, $Y \sim \text{Poisson}(2)$.

### Derivación

Por la PMF Poisson ([](random_variables.md#eq-poisson-pmf)),

$$
P(Y = 0) = \frac{2^{0} e^{-2}}{0!} = e^{-2} \approx 0{,}1353.
$$

### Visual

```{code-cell} python
arrival_distribution = make_poisson(PoissonParams(rate=2.0))
chart_probability_mass(
    ProbabilityMassChartInput(
        probability_mass=evaluate_probability_mass(
            ProbabilityMassInput(distribution=arrival_distribution, lower_outcome=0, upper_outcome=10),
        ),
        settings=settings,
    )
)
```

### Verificación

```{code-cell} python
expected_zero = float(arrival_distribution.frozen_distribution.pmf(0))

verify_numeric_answer(
    NumericAnswerInput(
        student_answer=0.135,
        expected_answer=expected_zero,
        absolute_tolerance=0.002,
    )
)
```

:::

## Ejercicio 3 — Cola de una Exponencial

El tiempo entre llegadas a la guardia, en el escenario del Ejercicio 2,
se modela como **Exponencial** con tasa $\lambda = 6$ pacientes por
hora. ¿Cuál es la probabilidad de que **pasen más de 15 minutos** sin
que llegue nadie?

:::{admonition} Solución
:class: dropdown

### Planteo

Sea $T$ = tiempo (en horas) hasta el próximo paciente. Por la conexión
entre Poisson y Exponencial ([](random_variables.md#sec-rv-exponential)),
$T \sim \text{Exp}(\lambda = 6)$. Pasamos 15 minutos a horas:
$t = 0{,}25$.

### Derivación

La función de supervivencia de la Exponencial es

$$
P(T > t) = e^{-\lambda t}.
$$

Aplicando con $\lambda = 6$ y $t = 0{,}25$,

$$
P(T > 0{,}25) = e^{-1{,}5} \approx 0{,}2231.
$$

### Visual

```{code-cell} python
inter_arrival_distribution = make_exponential(ExponentialParams(rate=6.0))
chart_density(
    DensityChartInput(
        density_grid=evaluate_density_grid(
            DensityGridInput(distribution=inter_arrival_distribution, settings=settings),
        ),
        title="Tiempo entre llegadas — Exp(λ=6)",
        settings=settings,
    )
)
```

### Verificación

```{code-cell} python
expected_tail = survival_of_continuous(
    SurvivalInput(distribution=inter_arrival_distribution, threshold=0.25),
).survival_probability

verify_numeric_answer(
    NumericAnswerInput(
        student_answer=0.223,
        expected_answer=expected_tail,
        absolute_tolerance=0.005,
    )
)
```

:::

## Ejercicio 4 — Probabilidad Normal por estandarización

Las alturas de adultos en una población se modelan como $X \sim \mathcal{N}(170, 8^{2})$
(en cm). ¿Cuál es la probabilidad de que una persona elegida al azar
mida **entre 165 y 180** cm?

:::{admonition} Solución
:class: dropdown

### Planteo

Estandarizamos con [](random_variables.md#eq-zscore-rv):

$$
Z = \frac{X - \mu}{\sigma},\qquad \mu = 170,\ \sigma = 8.
$$

### Derivación

**Paso 1.** Convertimos los límites:

$$
z_1 = \frac{165 - 170}{8} = -0{,}625,\qquad
z_2 = \frac{180 - 170}{8} = 1{,}25.
$$

**Paso 2.** Buscamos en la Normal estándar:

$$
P(-0{,}625 \le Z \le 1{,}25) = \Phi(1{,}25) - \Phi(-0{,}625)
\approx 0{,}8944 - 0{,}2660 \approx 0{,}6284.
$$

### Visual

```{code-cell} python
height_distribution = make_normal(NormalParams(mean=170.0, standard_deviation=8.0))
chart_density(
    DensityChartInput(
        density_grid=evaluate_density_grid(
            DensityGridInput(distribution=height_distribution, settings=settings),
        ),
        title="Alturas — N(170, 8²)",
        settings=settings,
    )
)
```

### Verificación

```{code-cell} python
expected_band = tail_probability_of_continuous(
    TailProbabilityInput(distribution=height_distribution, lower_bound=165.0, upper_bound=180.0),
).probability

verify_numeric_answer(
    NumericAnswerInput(
        student_answer=0.628,
        expected_answer=expected_band,
        absolute_tolerance=0.005,
    )
)
```

:::

## Ejercicio 5 — Cuantil de una Normal

Con la misma distribución de alturas del Ejercicio 4, encontrá el valor
$x_{0{,}95}$ tal que el **95 %** de las personas mide menos que $x_{0{,}95}$.

:::{admonition} Solución
:class: dropdown

### Planteo

Por la definición de cuantil ([](random_variables.md#eq-quantile)),
buscamos $x$ tal que $F_X(x) = 0{,}95$. Equivalentemente, en la Normal
estándar buscamos $z_{0{,}95}$ y desestandarizamos.

### Derivación

**Paso 1.** $z_{0{,}95} \approx 1{,}6449$ (tabla).

**Paso 2.** Desestandarizamos invirtiendo
[](random_variables.md#eq-zscore-rv):

$$
x_{0{,}95} = \mu + z_{0{,}95}\,\sigma = 170 + 1{,}6449 \cdot 8 \approx 183{,}2.
$$

### Verificación

```{code-cell} python
expected_quantile = quantile_of_continuous(
    QuantileInput(distribution=height_distribution, probability=0.95),
).quantile

verify_numeric_answer(
    NumericAnswerInput(
        student_answer=183.16,
        expected_answer=expected_quantile,
        absolute_tolerance=0.2,
    )
)
```

:::

## Ejercicio 6 — Geométrica: primera llamada exitosa

Un encuestador llama a número aleatorios; cada llamada tiene
probabilidad $p = 0{,}30$ de obtener respuesta. ¿Cuál es la
**probabilidad de que la primera respuesta llegue en el tercer intento**?

:::{admonition} Solución
:class: dropdown

### Planteo

Sea $G$ = número del intento en el que se obtiene la primera respuesta.
Entonces $G \sim \text{Geom}(p = 0{,}30)$, en la convención «número de
intentos hasta el primer éxito» (soporte $\{1, 2, 3, \dots\}$). Su PMF
es la de [](random_variables.md#eq-geometric-pmf):

$$
P(G = k) = (1 - p)^{k - 1}\,p,\qquad k = 1, 2, \dots
$$

### Derivación

$$
P(G = 3) = (0{,}70)^{2} \cdot 0{,}30 = 0{,}49 \cdot 0{,}30 = 0{,}147.
$$

### Visual

```{code-cell} python
call_distribution = make_geometric(GeometricParams(success_probability=0.30))
chart_probability_mass(
    ProbabilityMassChartInput(
        probability_mass=evaluate_probability_mass(
            ProbabilityMassInput(distribution=call_distribution, lower_outcome=1, upper_outcome=12),
        ),
        settings=settings,
    )
)
```

### Verificación

```{code-cell} python
expected_third = float(call_distribution.frozen_distribution.pmf(3))

verify_numeric_answer(
    NumericAnswerInput(
        student_answer=0.147,
        expected_answer=expected_third,
        absolute_tolerance=0.002,
    )
)
```

:::

## Ejercicio 7 — Simulación que sigue la distribución teórica

Generá $n = 1000$ muestras desde una Poisson con $\lambda = 4$ usando el
generador del `Settings`. ¿La muestra se comporta como una
$\text{Poisson}(4)$? Verificalo con un test de bondad de ajuste.

:::{admonition} Solución
:class: dropdown

### Planteo

El verificador `verify_distribution_match` aplica $\chi^{2}$ contra los
conteos esperados de la PMF Poisson. Si el $p$-valor supera el nivel de
significancia ($0{,}05$ por defecto), no rechazamos $H_0$: la muestra
es **consistente** con la distribución hipotética.

### Verificación

```{code-cell} python
rng = np.random.default_rng(settings.random_seed)
samples = rng.poisson(lam=4.0, size=1000)
arrival_distribution_per_hour = make_poisson(PoissonParams(rate=4.0))

verify_distribution_match(
    DistributionMatchInput(
        student_samples=samples,
        expected_distribution=arrival_distribution_per_hour,
    )
)
```

:::

## Ejercicio 8 — ¿Es la esperanza el valor más probable?

Indicá si la siguiente afirmación es **Verdadera o Falsa**:

> «Si $X$ es discreta, entonces $E[X]$ siempre coincide con el valor
> $k$ que maximiza $P(X = k)$ (es decir, con la **moda**).»

:::{admonition} Solución
:class: dropdown

### Planteo

La esperanza es un promedio ponderado; la moda es el valor con mayor
probabilidad. Son dos resúmenes distintos de la distribución.

### Derivación

Contraejemplo: $X \sim \text{Bin}(10,\ 0{,}3)$ tiene esperanza
$E[X] = 10 \cdot 0{,}3 = 3{,}0$ y moda en $k = 3$, así que en este
caso particular coinciden. Pero $X \sim \text{Bin}(10,\ 0{,}35)$ tiene
$E[X] = 3{,}5$ y la PMF está maximizada en $k = 3$ (la esperanza no es
ni siquiera un valor del soporte). En general $E[X]$ y la moda **no
coinciden**, así que la afirmación es **Falsa**.

### Visual

```{code-cell} python
example_distribution = make_binomial(BinomialParams(trials=10, success_probability=0.35))
chart_probability_mass(
    ProbabilityMassChartInput(
        probability_mass=evaluate_probability_mass(
            ProbabilityMassInput(distribution=example_distribution, lower_outcome=0, upper_outcome=10),
        ),
        settings=settings,
    )
)
```

### Verificación

```{code-cell} python
moments = compute_numeric_moments(MomentsInput(distribution=example_distribution))
mass_table = evaluate_probability_mass(
    ProbabilityMassInput(distribution=example_distribution, lower_outcome=0, upper_outcome=10),
).table
mode_value = float(mass_table.loc[mass_table["probability"].idxmax(), "outcome"])
expected_truth = float(moments.mean) == mode_value

verify_boolean_answer(
    BooleanAnswerInput(
        student_answer=False,
        expected_answer=expected_truth,
    )
)
```

:::
