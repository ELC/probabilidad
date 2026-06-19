---
title: Práctica — Inferencia
short_title: Práctica
kernelspec:
  name: python3
  display_name: Python 3
---

# Práctica — Inferencia

Esta sección reúne ejercicios para fijar los conceptos del capítulo de
[Inferencia](inference.md): intervalos de confianza para la media
(σ conocido y desconocido), para una proporción y para la varianza;
tests de hipótesis, conexión IC-test y cálculo de tamaño muestral. Cada enunciado
incluye una **solución** plegada con el paso a paso, una visualización
y la verificación correspondiente.

```{code-cell} python
:tags: [hide-input]
import math

import numpy as np
import pandas as pd
from scipy import stats

from core import NormalParams, Observations, Settings
from distributions import make_normal
from exercises import (
    BooleanAnswerInput,
    IntervalContainsInput,
    NumericAnswerInput,
    verify_boolean_answer,
    verify_interval_contains,
    verify_numeric_answer,
)
from inference import (
    MeanKnownVarianceInput,
    MeanUnknownVarianceInput,
    OneSampleMeanTestInput,
    ProportionInput,
    SampleSizeForMeanInput,
    VarianceInput,
    build_confidence_interval_for_mean_known_variance,
    build_confidence_interval_for_mean_unknown_variance,
    build_confidence_interval_for_proportion,
    build_confidence_interval_for_variance,
    sample_size_for_mean,
    test_one_sample_mean,
)
from inference.hypothesis_tests import Alternative

settings = Settings()
```

## Ejercicio 1 — IC para la media con σ conocido

Un torno produce piezas cuya longitud sigue $X \sim \mathcal{N}(\mu, \sigma^{2})$
con $\sigma = 0{,}10$ cm conocido del proceso histórico. En una muestra
de $n = 25$ piezas se obtuvo $\bar{x} = 5{,}04$ cm. Construí un
intervalo de **95 %** de confianza para $\mu$ y decidí si el valor
nominal $\mu_0 = 5{,}00$ cm queda **adentro** del intervalo.

:::{admonition} Solución
:class: dropdown

### Planteo

Como $\sigma$ es conocido, el pivote es el de
[](inference.md#eq-z-pivot) y el IC tiene la forma de
[](inference.md#eq-ci-mean-known):

$$
\bar{x} \;\pm\; z_{1 - \alpha/2}\,\frac{\sigma}{\sqrt{n}}.
$$

### Derivación

Con $\alpha = 0{,}05$, $z_{0{,}975} \approx 1{,}96$. El error estándar
es $\sigma/\sqrt{n} = 0{,}10/5 = 0{,}02$. El margen de error es
$1{,}96 \cdot 0{,}02 = 0{,}0392$, así que el IC es
$5{,}04 \pm 0{,}0392 = (5{,}0008,\ 5{,}0792)$.

El valor $\mu_0 = 5{,}00$ **no** cae dentro del intervalo: la muestra
es compatible con que el torno esté **desajustado** un poco hacia
arriba.

### Verificación

```{code-cell} python
length_ci = build_confidence_interval_for_mean_known_variance(
    MeanKnownVarianceInput(
        sample_mean=5.04,
        population_standard_deviation=0.10,
        sample_size=25,
        confidence_level=0.95,
    ),
)
length_ci
```

```{code-cell} python
verify_interval_contains(
    IntervalContainsInput(
        lower_bound=length_ci.lower_bound,
        upper_bound=length_ci.upper_bound,
        target_value=5.00,
    )
)
```

:::

## Ejercicio 2 — IC para la media con σ desconocido (t de Student)

Para validar una nueva regulación, se cronometra el tiempo (en minutos)
hasta que un paciente entra al consultorio en una guardia. En una
muestra de $n = 12$ pacientes se observó $\bar{x} = 13{,}2$ minutos y
$s = 3{,}1$ minutos. Construí un IC del **95 %** y mostrá si el valor
de referencia $\mu_0 = 12$ minutos **cae adentro**.

:::{admonition} Solución
:class: dropdown

### Planteo

Como $\sigma$ no se conoce, el pivote es el de Student
[](inference.md#eq-t-pivot) y el IC sigue la forma análoga a
[](inference.md#eq-ci-mean-known) reemplazando $z$ por $t_{n-1}$:

$$
\bar{x} \;\pm\; t_{n - 1,\ 1 - \alpha/2}\,\frac{s}{\sqrt{n}}.
$$

### Derivación

Con $\alpha = 0{,}05$ y $n - 1 = 11$ grados de libertad,
$t_{11,\ 0{,}975} \approx 2{,}201$. El error estándar muestral es
$s/\sqrt{n} = 3{,}1/\sqrt{12} \approx 0{,}895$.

Margen de error: $2{,}201 \cdot 0{,}895 \approx 1{,}970$. El IC es
$13{,}2 \pm 1{,}970 \approx (11{,}23,\ 15{,}17)$.

El valor $12$ **sí** está dentro, así que la muestra **no permite
rechazar** la hipótesis de que la media poblacional sea $12$.

### Verificación

```{code-cell} python
wait_ci = build_confidence_interval_for_mean_unknown_variance(
    MeanUnknownVarianceInput(
        sample_mean=13.2,
        sample_standard_deviation=3.1,
        sample_size=12,
        confidence_level=0.95,
    ),
)
wait_ci
```

```{code-cell} python
verify_interval_contains(
    IntervalContainsInput(
        lower_bound=wait_ci.lower_bound,
        upper_bound=wait_ci.upper_bound,
        target_value=12.0,
    )
)
```

:::

## Ejercicio 3 — IC para una proporción

En una encuesta a $n = 500$ votantes, $x = 215$ declararon que apoyan
al partido oficialista. Construí un IC del **95 %** para la proporción
real de apoyo $p$, y decidí si la afirmación «más del 50 % apoya al
oficialismo» es **compatible** con los datos.

:::{admonition} Solución
:class: dropdown

### Planteo

Por la aproximación Normal a la Binomial
([](inference.md#eq-ci-prop)),

$$
\hat{p} \;\pm\; z_{1 - \alpha/2}\,\sqrt{\frac{\hat{p}(1 - \hat{p})}{n}},
\qquad \hat{p} = x / n.
$$

### Derivación

$\hat{p} = 215/500 = 0{,}43$. El error estándar es
$\sqrt{0{,}43 \cdot 0{,}57 / 500} \approx 0{,}02214$. El margen es
$1{,}96 \cdot 0{,}02214 \approx 0{,}0434$. IC:
$(0{,}3866,\ 0{,}4734)$.

El valor $0{,}50$ **no** está dentro del intervalo. Más aún, todo el
intervalo está por **debajo** de $0{,}50$. Los datos contradicen la
afirmación de mayoría.

### Verificación

```{code-cell} python
support_ci = build_confidence_interval_for_proportion(
    ProportionInput(successes=215, sample_size=500, confidence_level=0.95),
)
support_ci
```

```{code-cell} python
verify_interval_contains(
    IntervalContainsInput(
        lower_bound=support_ci.lower_bound,
        upper_bound=support_ci.upper_bound,
        target_value=0.50,
    )
)
```

:::

## Ejercicio 4 — IC para la varianza

En una línea de envasado se controla la masa neta (en gramos) de las
unidades. Una muestra de $n = 16$ unidades arrojó varianza muestral
$s^{2} = 6{,}25\ \mathrm{g}^{2}$. Construí un IC del **95 %** para
$\sigma^{2}$, y decidí si la varianza objetivo $\sigma_{0}^{2} = 4$ está
**dentro**.

:::{admonition} Solución
:class: dropdown

### Planteo

Por el pivote $\chi^{2}_{n-1}$ ([](inference.md#eq-chi-pivot)), el IC
es ([](inference.md#eq-ci-var))

$$
\left(\frac{(n - 1)\,s^{2}}{\chi^{2}_{n-1,\,1-\alpha/2}},
       \frac{(n - 1)\,s^{2}}{\chi^{2}_{n-1,\,\alpha/2}}\right).
$$

### Derivación

Con $n - 1 = 15$ y $\alpha = 0{,}05$:
$\chi^{2}_{15,\,0{,}975} \approx 27{,}488$,
$\chi^{2}_{15,\,0{,}025} \approx 6{,}262$.

Numerador: $(n - 1)\,s^{2} = 15 \cdot 6{,}25 = 93{,}75$.

IC:

$$
\left(\frac{93{,}75}{27{,}488},\ \frac{93{,}75}{6{,}262}\right)
\approx (3{,}41,\ 14{,}97).
$$

El valor objetivo $4$ **sí** está adentro: con esta muestra **no podemos
rechazar** que la varianza poblacional sea $4$.

### Verificación

```{code-cell} python
variance_ci = build_confidence_interval_for_variance(
    VarianceInput(sample_variance=6.25, sample_size=16, confidence_level=0.95),
)
variance_ci
```

```{code-cell} python
verify_interval_contains(
    IntervalContainsInput(
        lower_bound=variance_ci.lower_bound,
        upper_bound=variance_ci.upper_bound,
        target_value=4.0,
    )
)
```

:::

## Ejercicio 5 — Tamaño muestral para un margen de error

Volvé al escenario del [Ejercicio 1](#ejercicio-1-ic-para-la-media-con-conocido)
con $\sigma = 0{,}10$ cm. ¿Cuántas piezas hay que medir para obtener un
margen de error de $\pm 0{,}02$ cm con **99 %** de confianza?

:::{admonition} Solución
:class: dropdown

### Planteo

Despejando $n$ de la mitad del ancho de
[](inference.md#eq-ci-mean-known):

$$
n = \left(\frac{z_{1 - \alpha/2}\,\sigma}{E}\right)^{2}.
$$

### Derivación

Con $z_{0{,}995} \approx 2{,}576$, $\sigma = 0{,}10$ y $E = 0{,}02$:

$$
n = \left(\frac{2{,}576 \cdot 0{,}10}{0{,}02}\right)^{2}
= (12{,}88)^{2} = 165{,}9\dots
$$

Redondeamos hacia arriba: **$n = 166$** piezas.

### Verificación

```{code-cell} python
required_size = sample_size_for_mean(
    SampleSizeForMeanInput(
        population_standard_deviation=0.10,
        margin_of_error=0.02,
        confidence_level=0.99,
    ),
).required_sample_size

verify_numeric_answer(
    NumericAnswerInput(
        student_answer=166.0,
        expected_answer=float(required_size),
    )
)
```

:::

## Ejercicio 6 — Test t de una muestra (¿rechazamos $H_0$?)

Volvé a los $n = 12$ pacientes del [Ejercicio 2](#ejercicio-2-ic-para-la-media-con-desconocido-t-de-student)
con $\bar{x} = 13{,}2$ minutos y $s = 3{,}1$ minutos. Planteamos las
hipótesis

$$
H_0: \mu = 12,\qquad H_1: \mu \ne 12,
$$

con nivel de significancia $\alpha = 0{,}05$. ¿**Se rechaza $H_0$**?

:::{admonition} Solución
:class: dropdown

### Planteo

Por el pivote $T = (\bar{X} - \mu_0)/(s/\sqrt{n}) \sim t_{n - 1}$
bajo $H_0$, calculamos el $p$-valor a dos colas
([](inference.md#sec-inf-test)) y comparamos con
$\alpha$.

### Derivación

$T_{\text{obs}} = (13{,}2 - 12) / (3{,}1/\sqrt{12}) \approx
1{,}2 / 0{,}895 \approx 1{,}341$. Con $n - 1 = 11$ g.l., el
$p$-valor a dos colas es $\approx 2 \cdot 0{,}1034 = 0{,}207$, muy por
encima de $0{,}05$.

**Conclusión:** $p \gg \alpha$ → **no rechazamos $H_0$**. Coincide
con la conexión IC-test de [](inference.md#sec-inf-test): el valor $12$
caía adentro del intervalo del Ejercicio 2.

### Verificación

```{code-cell} python
test_result = test_one_sample_mean(
    OneSampleMeanTestInput(
        sample_mean=13.2,
        sample_standard_deviation=3.1,
        sample_size=12,
        null_mean=12.0,
        alternative=Alternative.TWO_SIDED,
        significance_level=0.05,
    ),
)
test_result
```

```{code-cell} python
verify_boolean_answer(
    BooleanAnswerInput(
        student_answer=False,
        expected_answer=test_result.reject_null,
    )
)
```

:::
