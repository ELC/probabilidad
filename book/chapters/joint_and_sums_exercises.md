---
title: Práctica — Sumas y promedios
short_title: Práctica
kernelspec:
  name: python3
  display_name: Python 3
---

# Práctica — Sumas y promedios

Esta sección reúne ejercicios para fijar las ideas del capítulo de
[Sumas y promedios](joint_and_sums.md): Ley de los grandes números
(LLN), Teorema central del límite (TCL), aproximación
Binomial → Normal, y suma de variables aleatorias independientes. Cada
enunciado va acompañado de una **solución** plegada con el paso a paso,
una visualización y la verificación.

```{code-cell} python
:tags: [hide-input]
import math

import numpy as np
from scipy import stats

from core import (
    BinomialParams,
    ExponentialParams,
    NormalParams,
    PoissonParams,
    Settings,
)
from distributions import (
    make_binomial,
    make_exponential,
    make_normal,
    make_poisson,
)
from exercises import (
    BooleanAnswerInput,
    NumericAnswerInput,
    verify_boolean_answer,
    verify_numeric_answer,
)
from sampling import (
    CLTSimulationInput,
    LLNSimulationInput,
    simulate_clt,
    simulate_lln,
)
from visualization import (
    CLTComparisonChartInput,
    LLNChartInput,
    chart_clt_comparison,
    chart_lln_running_mean,
)

settings = Settings()
```

## Ejercicio 1 — Desvío del promedio muestral

Una balanza mide con error aleatorio de media $\mu = 0$ y desvío
$\sigma = 0{,}5$ gramos. Si se promedian $n = 25$ pesadas
independientes, ¿cuál es el **desvío estándar del promedio** $\bar{X}_n$?

:::{admonition} Solución
:class: dropdown

### Planteo

Por la varianza del promedio bajo el TCL
([](joint_and_sums.md#eq-clt)),

$$
\mathrm{Var}(\bar{X}_n) = \frac{\sigma^{2}}{n},\qquad
\mathrm{DE}(\bar{X}_n) = \frac{\sigma}{\sqrt{n}}.
$$

### Derivación

$$
\mathrm{DE}(\bar{X}_{25}) = \frac{0{,}5}{\sqrt{25}} = \frac{0{,}5}{5} = 0{,}10\ \mathrm{g}.
$$

El promedio tiene **cinco veces menos** dispersión que una medición
individual.

### Verificación

```{code-cell} python
sigma = 0.5
sample_size = 25
expected_se = sigma / math.sqrt(sample_size)

verify_numeric_answer(
    NumericAnswerInput(
        student_answer=0.10,
        expected_answer=expected_se,
        absolute_tolerance=0.005,
    )
)
```

:::

## Ejercicio 2 — Convergencia visual (LLN)

Simulá la **media acumulada** de una Exponencial con tasa $\lambda = 2$ a
lo largo de $n = 2000$ observaciones y compará el valor final con la
media teórica $1/\lambda = 0{,}5$. ¿La media acumulada cae a menos de
$0{,}05$ del valor teórico al final del horizonte?

:::{admonition} Solución
:class: dropdown

### Planteo

Por la LLN ([](joint_and_sums.md#eq-lln)),

$$
\bar{X}_n \xrightarrow{P} \mu = \frac{1}{\lambda} = 0{,}5
\qquad \text{cuando } n \to \infty.
$$

Con $n = 2000$ esperamos un valor cercano a $0{,}5$, aunque pueden
quedar oscilaciones del orden de $\sigma/\sqrt{n}$.

### Derivación

Para la Exponencial $\sigma = 1/\lambda = 0{,}5$, así que el desvío
del promedio con $n = 2000$ es $\approx 0{,}5/\sqrt{2000} \approx 0{,}011$,
muy por debajo del umbral $0{,}05$. El final de la trayectoria
debería caer en $[0{,}45,\ 0{,}55]$ con altísima probabilidad.

### Visual

```{code-cell} python
lln_distribution = make_exponential(ExponentialParams(rate=2.0))
lln_result = simulate_lln(
    LLNSimulationInput(distribution=lln_distribution, horizon=2000, settings=settings),
)
chart_lln_running_mean(LLNChartInput(lln_result=lln_result, settings=settings))
```

### Verificación

```{code-cell} python
running_mean_final = float(lln_result.running_mean[-1])
expected_within_band = abs(running_mean_final - lln_result.underlying_mean) < 0.05

verify_boolean_answer(
    BooleanAnswerInput(
        student_answer=True,
        expected_answer=expected_within_band,
    )
)
```

:::

## Ejercicio 3 — TCL para un promedio de Exponenciales

Las esperas en la cola de la guardia se modelan como
$T_i \sim \text{Exp}(\lambda = 0{,}25)$ minutos $^{-1}$ (es decir,
media de 4 minutos). Para $n = 36$ pacientes independientes, ¿cuál es
**aproximadamente** la probabilidad de que el **tiempo medio**
$\bar{T}_{36}$ sea **mayor a 4,5 minutos**?

:::{admonition} Solución
:class: dropdown

### Planteo

La Exponencial tiene $\mu = 1/\lambda = 4$ y $\sigma = 1/\lambda = 4$.
Por el TCL ([](joint_and_sums.md#eq-clt)) con $n = 36$,

$$
\bar{T}_{36} \;\dot\sim\; \mathcal{N}\!\left(4,\ \left(\frac{4}{6}\right)^{2}\right)
= \mathcal{N}(4,\ 0{,}444\dots).
$$

### Derivación

Estandarizamos el umbral $4{,}5$:

$$
z = \frac{4{,}5 - 4}{4/6} = \frac{0{,}5}{0{,}6667} \approx 0{,}75.
$$

Buscamos $P(Z > 0{,}75) = 1 - \Phi(0{,}75) \approx 1 - 0{,}7734 \approx 0{,}2266$.

### Visual

```{code-cell} python
wait_distribution = make_exponential(ExponentialParams(rate=0.25))
clt_result = simulate_clt(
    CLTSimulationInput(
        distribution=wait_distribution,
        sample_size_per_replicate=36,
        replicates=5000,
        settings=settings,
    ),
)
chart_clt_comparison(
    CLTComparisonChartInput(clt_result=clt_result, settings=settings),
)
```

### Verificación

```{code-cell} python
underlying_mean = 4.0
underlying_std = 4.0
sample_size = 36
standard_error = underlying_std / math.sqrt(sample_size)
z_value = (4.5 - underlying_mean) / standard_error
expected_tail = 1.0 - float(stats.norm.cdf(z_value))

verify_numeric_answer(
    NumericAnswerInput(
        student_answer=0.227,
        expected_answer=expected_tail,
        absolute_tolerance=0.01,
    )
)
```

:::

## Ejercicio 4 — Aproximación Binomial → Normal

En la línea de producción del [ejercicio 1 de probabilidad](probability_exercises.md)
seguimos con $p = 0{,}04$ defectuosas. Se inspeccionan $n = 400$ piezas.
Aproximá $P(Y \le 12)$, donde $Y$ es la cantidad de defectuosas.

:::{admonition} Solución
:class: dropdown

### Planteo

$Y \sim \text{Bin}(400, 0{,}04)$ con $np = 16$ y $np(1-p) = 15{,}36$,
así que el TCL ([](joint_and_sums.md#eq-clt-bin)) recomienda
aproximar

$$
Y \;\dot\sim\; \mathcal{N}(16,\ 15{,}36).
$$

### Derivación

Estandarizamos el umbral (sin corrección por continuidad para
simplificar):

$$
z = \frac{12 - 16}{\sqrt{15{,}36}} = \frac{-4}{3{,}919} \approx -1{,}021.
$$

$$
P(Y \le 12) \approx \Phi(-1{,}021) \approx 0{,}154.
$$

### Verificación

```{code-cell} python
binomial_distribution = make_binomial(BinomialParams(trials=400, success_probability=0.04))
normal_approximation = make_normal(
    NormalParams(mean=16.0, standard_deviation=math.sqrt(15.36)),
)
expected_tail_normal = float(normal_approximation.frozen_distribution.cdf(12.0))

verify_numeric_answer(
    NumericAnswerInput(
        student_answer=0.154,
        expected_answer=expected_tail_normal,
        absolute_tolerance=0.01,
    )
)
```

:::

## Ejercicio 5 — Suma de Normales independientes

Una caja con productos tiene dos pesos sumados: el contenedor pesa
$X \sim \mathcal{N}(2{,}0;\ 0{,}10^{2})$ kg y el contenido pesa
$Y \sim \mathcal{N}(8{,}0;\ 0{,}40^{2})$ kg, independientes. ¿Cuál es la
probabilidad de que el **peso total** $W = X + Y$ supere los $10{,}5$ kg?

:::{admonition} Solución
:class: dropdown

### Planteo

La suma de Normales independientes es Normal con

$$
E[W] = E[X] + E[Y],\qquad \mathrm{Var}(W) = \mathrm{Var}(X) + \mathrm{Var}(Y).
$$

### Derivación

$$
E[W] = 2{,}0 + 8{,}0 = 10{,}0,\quad
\mathrm{Var}(W) = 0{,}01 + 0{,}16 = 0{,}17,\quad
\mathrm{DE}(W) = \sqrt{0{,}17} \approx 0{,}4123.
$$

$$
z = \frac{10{,}5 - 10{,}0}{0{,}4123} \approx 1{,}213.
$$

$$
P(W > 10{,}5) \approx 1 - \Phi(1{,}213) \approx 0{,}1125.
$$

### Verificación

```{code-cell} python
total_distribution = make_normal(
    NormalParams(mean=10.0, standard_deviation=math.sqrt(0.17)),
)
expected_tail = 1.0 - float(total_distribution.frozen_distribution.cdf(10.5))

verify_numeric_answer(
    NumericAnswerInput(
        student_answer=0.113,
        expected_answer=expected_tail,
        absolute_tolerance=0.005,
    )
)
```

:::

## Ejercicio 6 — ¿El TCL siempre exige Normal en la población?

Indicá si la siguiente afirmación es **Verdadera o Falsa**:

> «Para poder usar la aproximación del TCL al promedio
> $\bar{X}_n$ es necesario que la población **original** sea Normal.»

:::{admonition} Solución
:class: dropdown

### Planteo

El TCL ([](joint_and_sums.md#eq-clt)) dice que **el promedio
estandarizado** converge en distribución a $\mathcal{N}(0,1)$ para
cualquier población con varianza finita, **independientemente de su
forma**, cuando $n$ es grande. La Normalidad en la población original
**no** es un requisito.

### Derivación

En este mismo capítulo armamos un TCL con una **Exponencial** (que es
asimétrica con cola pesada) y vimos que el promedio termina pareciendo
Normal aun así. El resultado es exactamente que el TCL **no** exige
normalidad de la población, sólo varianza finita e independencia. La
afirmación es **Falsa**.

### Verificación

```{code-cell} python
expected_truth = False
verify_boolean_answer(
    BooleanAnswerInput(student_answer=False, expected_answer=expected_truth)
)
```

:::
