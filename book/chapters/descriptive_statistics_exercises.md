---
title: Práctica — Tratamiento de datos
short_title: Práctica
kernelspec:
  name: python3
  display_name: Python 3
---

# Práctica — Tratamiento de datos

Esta sección reúne ejercicios para fijar los conceptos del capítulo de
[Tratamiento de datos](descriptive_statistics.md). Cada ejercicio sigue el
mismo ritmo: un enunciado breve, y debajo una **solución** plegada que se
abre con un clic. La idea es que primero intentes el cálculo en papel (o a
mano alzada) y recién después abras la solución para comparar pasos,
visualizar el resultado y correr la verificación.

```{code-cell} python
:tags: [hide-input]
import numpy as np
import pandas as pd

from core import Observations, Settings
from descriptive import (
    build_frequency_table,
    compute_dispersion,
    compute_location,
    detect_outliers_tukey,
    summarize_observations,
)
from descriptive.frequencies import FrequencyTableInput
from exercises import (
    BooleanAnswerInput,
    CategoricalChoiceInput,
    NumericAnswerInput,
    verify_boolean_answer,
    verify_categorical_choice,
    verify_numeric_answer,
)
from visualization import (
    DescriptiveSummaryChartInput,
    HistogramChartInput,
    ObservationsOverviewInput,
    chart_descriptive_summary,
    chart_histogram,
    chart_observations_overview,
)

settings = Settings()
```

## Ejercicio 1 — Clasificar la variable

En la guardia de una clínica se anota, para cada paciente que llega, **el
tiempo de espera en minutos** hasta que lo atiende un médico. La variable
de estudio es ese tiempo. Clasificala:

- ¿Es **cualitativa** o **cuantitativa**?
- Si es cuantitativa, ¿es **discreta** o **continua**?

:::{admonition} Solución
:class: dropdown

### Planteo

La variable toma valores numéricos que pueden caer en cualquier punto de un
intervalo (no solo enteros): un paciente puede esperar 7 minutos, otro
7,3 minutos, otro 7,28. No estamos contando ocurrencias, estamos midiendo
una duración.

### Derivación

Por la definición del capítulo
([](descriptive_statistics.md#sec-descriptive-sample)):

- **Cualitativa** ↔ los valores son categorías (Sí/No, tipos de defecto).
- **Cuantitativa discreta** ↔ los valores son números enteros que cuentan
  algo (cantidad de pacientes, cantidad de defectos).
- **Cuantitativa continua** ↔ los valores son mediciones que pueden tomar
  cualquier valor real dentro de un intervalo (tiempo, peso, longitud).

El tiempo de espera es una **medición** sobre un eje continuo, por lo
tanto es **cuantitativa continua**.

### Verificación

```{code-cell} python
verify_categorical_choice(
    CategoricalChoiceInput(
        student_choice="cuantitativa continua",
        expected_choice="cuantitativa continua",
        allowed_choices=frozenset({
            "cualitativa",
            "cuantitativa discreta",
            "cuantitativa continua",
        }),
    )
)
```

:::

## Ejercicio 2 — Tabla de frecuencias y forma de la distribución

Se registraron los tiempos de espera (en minutos) de 30 pacientes
consecutivos en la guardia:

$$
\begin{aligned}
&5{,}2;\ 6{,}8;\ 7{,}1;\ 5{,}9;\ 8{,}3;\ 6{,}5;\ 7{,}9;\ 9{,}2;\ 5{,}5;\ 6{,}3;\\
&7{,}4;\ 8{,}8;\ 6{,}1;\ 7{,}7;\ 5{,}0;\ 9{,}6;\ 6{,}4;\ 8{,}1;\ 7{,}0;\ 5{,}8;\\
&8{,}5;\ 6{,}9;\ 7{,}3;\ 6{,}6;\ 8{,}0;\ 7{,}2;\ 6{,}0;\ 7{,}6;\ 9{,}1;\ 6{,}7.
\end{aligned}
$$

Construí una tabla de frecuencias con 5 intervalos. ¿Cuál es la
**frecuencia relativa** de la clase que contiene a 7 minutos?

:::{admonition} Solución
:class: dropdown

### Planteo

Pasamos los 30 valores a una `Observations` y dejamos que
`build_frequency_table` arme la tabla con cinco intervalos. La frecuencia
relativa de una clase es

$$
f_i = \frac{n_i}{n},
$$

con $n_i$ el conteo absoluto del intervalo $i$ y $n = 30$.

### Derivación

El intervalo que contiene a 7 minutos depende del corte que hagamos. Con
5 intervalos uniformes entre el mínimo y el máximo, el rango total es
$9{,}6 - 5{,}0 = 4{,}6$, así que cada clase mide $4{,}6 / 5 = 0{,}92$
minutos. El punto 7 cae en la **tercera** clase, $[6{,}84;\ 7{,}76)$.
Contando a mano: hay 7 valores en esa clase, así que
$f_3 = 7/30 \approx 0{,}233$.

### Visual

```{code-cell} python
waiting_values = np.array([
    5.2, 6.8, 7.1, 5.9, 8.3, 6.5, 7.9, 9.2, 5.5, 6.3,
    7.4, 8.8, 6.1, 7.7, 5.0, 9.6, 6.4, 8.1, 7.0, 5.8,
    8.5, 6.9, 7.3, 6.6, 8.0, 7.2, 6.0, 7.6, 9.1, 6.7,
])
waiting_observations = Observations.validate(pd.DataFrame({"value": waiting_values}))
frequency_table = build_frequency_table(
    FrequencyTableInput(observations=waiting_observations, bin_count=5)
)
chart_observations_overview(
    ObservationsOverviewInput(
        observations=waiting_observations,
        frequency_table=frequency_table,
        statistics=summarize_observations(waiting_observations),
        settings=settings,
    )
)
```

### Verificación

```{code-cell} python
target_class = frequency_table[
    (frequency_table["interval_start"] <= 7.0)
    & (frequency_table["interval_end"] > 7.0)
].iloc[0]
expected_relative = float(target_class["relative_frequency"])

verify_numeric_answer(
    NumericAnswerInput(
        student_answer=0.233,
        expected_answer=expected_relative,
        absolute_tolerance=0.01,
    )
)
```

:::

## Ejercicio 3 — Media y desvío estándar

Con la misma muestra del ejercicio anterior, calculá la **media** y el
**desvío estándar muestral** (divisor $n - 1$).

:::{admonition} Solución
:class: dropdown

### Planteo

La media muestral viene de la ecuación
[](descriptive_statistics.md#eq-mean):

$$
\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i,
$$

y el desvío muestral viene de [](descriptive_statistics.md#eq-std):

$$
s = \sqrt{\frac{1}{n - 1} \sum_{i=1}^{n} (x_i - \bar{x})^2}.
$$

### Derivación

**Paso 1** — sumamos los 30 valores y dividimos por 30 para obtener
$\bar{x}$. Da aproximadamente 7,18 minutos.

**Paso 2** — restamos la media a cada valor, elevamos al cuadrado, sumamos
y dividimos por $n - 1 = 29$. Tomamos raíz cuadrada y obtenemos
aproximadamente $s \approx 1{,}19$ minutos.

### Visual

```{code-cell} python
chart_descriptive_summary(
    DescriptiveSummaryChartInput(
        observations=waiting_observations,
        statistics=summarize_observations(waiting_observations),
        settings=settings,
    )
)
```

### Verificación

```{code-cell} python
expected_summary = summarize_observations(waiting_observations)
expected_mean = expected_summary.location.mean
expected_std = expected_summary.dispersion.sample_standard_deviation

verify_numeric_answer(
    NumericAnswerInput(
        student_answer=7.18,
        expected_answer=expected_mean,
        absolute_tolerance=0.05,
    )
)
```

```{code-cell} python
verify_numeric_answer(
    NumericAnswerInput(
        student_answer=1.19,
        expected_answer=expected_std,
        absolute_tolerance=0.05,
    )
)
```

:::

## Ejercicio 4 — Outlier por la regla de Tukey

A los 30 tiempos de espera anteriores agregamos un día anómalo en el que
un paciente esperó **18 minutos** porque hubo una emergencia
simultánea. ¿Ese valor cuenta como **outlier** según la regla de Tukey
con factor 1,5?

:::{admonition} Solución
:class: dropdown

### Planteo

Por [](descriptive_statistics.md#sec-descriptive-tukey), un valor es
outlier cuando cae fuera del intervalo

$$
\bigl[Q_1 - 1{,}5\,\text{IQR},\ Q_3 + 1{,}5\,\text{IQR}\bigr].
$$

### Derivación

**Paso 1** — calculamos $Q_1$, $Q_3$ y $\text{IQR} = Q_3 - Q_1$ sobre la
muestra extendida (31 valores).

**Paso 2** — armamos el rango admisible y miramos si 18 cae adentro o
afuera. Con $Q_1 \approx 6{,}3$, $Q_3 \approx 8{,}05$ e
$\text{IQR} \approx 1{,}75$, el límite superior queda en
$8{,}05 + 1{,}5 \cdot 1{,}75 \approx 10{,}7$, así que 18 está claramente
por encima → es outlier.

### Visual

```{code-cell} python
extended_values = np.append(waiting_values, 18.0)
extended_observations = Observations.validate(pd.DataFrame({"value": extended_values}))
chart_descriptive_summary(
    DescriptiveSummaryChartInput(
        observations=extended_observations,
        statistics=summarize_observations(extended_observations),
        settings=settings,
    )
)
```

### Verificación

```{code-cell} python
report = detect_outliers_tukey(extended_observations)
expected_is_outlier = bool(18.0 > report.upper_fence)

verify_boolean_answer(
    BooleanAnswerInput(
        student_answer=True,
        expected_answer=expected_is_outlier,
    )
)
```

:::

## Ejercicio 5 — Coeficiente de variación para comparar muestras

Dos turnos de la línea de producción miden el **tiempo entre llegadas
de piezas defectuosas**. El turno A tiene
$\bar{x}_A = 12$ minutos y $s_A = 3$ minutos. El turno B tiene
$\bar{x}_B = 45$ minutos y $s_B = 6$ minutos.

¿En qué turno la variabilidad relativa es **mayor**?

:::{admonition} Solución
:class: dropdown

### Planteo

El coeficiente de variación

$$
\text{CV} = \frac{s}{\bar{x}}
$$

(ver [glosario](glossary.md)) es adimensional, así que sirve para
comparar dispersión entre muestras con medias muy distintas. Cuanto
mayor el CV, mayor la variabilidad relativa.

### Derivación

- $\text{CV}_A = 3 / 12 = 0{,}25$.
- $\text{CV}_B = 6 / 45 \approx 0{,}133$.

Como $0{,}25 > 0{,}133$, **el turno A** tiene variabilidad relativa
mayor a pesar de que el desvío absoluto del turno B (6 min) sea más
grande que el del A (3 min).

### Verificación

```{code-cell} python
cv_a = 3.0 / 12.0
cv_b = 6.0 / 45.0

verify_categorical_choice(
    CategoricalChoiceInput(
        student_choice="A",
        expected_choice="A" if cv_a > cv_b else "B",
        allowed_choices=frozenset({"A", "B"}),
    )
)
```

:::

## Ejercicio 6 — Lectura de un histograma sesgado

Para una variable de tiempos de espera en una sala se construyó un
histograma claramente **asimétrico a la derecha**: la moda está cerca de
los valores bajos y la cola se estira hacia valores altos.

Indicá si la siguiente afirmación es **Verdadera o Falsa**:

> «En este histograma, la **media** es menor que la **mediana**.»

:::{admonition} Solución
:class: dropdown

### Planteo

En una distribución asimétrica a la derecha la cola larga del lado alto
arrastra la media hacia valores grandes, pero **no** mueve a la mediana
con la misma intensidad — la mediana solo necesita el orden de los datos,
no su magnitud (ver [](descriptive_statistics.md#sec-descriptive-median)).

### Derivación

Para una distribución con cola larga a la derecha vale el orden

$$
\tilde{x} \le \bar{x},
$$

es decir, **la media es mayor o igual que la mediana**, no menor. La
afirmación es **Falsa**.

### Visual

```{code-cell} python
right_skewed = np.concatenate([
    np.random.default_rng(settings.random_seed).gamma(shape=2.0, scale=2.0, size=200),
    np.array([12.0, 13.5, 15.0, 18.0]),
])
right_observations = Observations.validate(pd.DataFrame({"value": right_skewed}))
chart_histogram(
    HistogramChartInput(
        observations=right_observations,
        bin_count=20,
        title="Sesgo a la derecha — media > mediana",
        settings=settings,
    )
)
```

### Verificación

```{code-cell} python
location = compute_location(right_observations)
expected_truth = location.mean < location.median

verify_boolean_answer(
    BooleanAnswerInput(
        student_answer=False,
        expected_answer=expected_truth,
    )
)
```

:::
