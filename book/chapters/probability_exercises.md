---
title: Práctica — Probabilidad
short_title: Práctica
kernelspec:
  name: python3
  display_name: Python 3
---

# Práctica — Probabilidad

Esta sección reúne ejercicios para fijar los conceptos del capítulo de
[Probabilidad](probability.md). Cada problema tiene un enunciado breve
y una **solución** plegada que se abre con un clic, con el paso a paso
de la fórmula, una visualización y el verificador correspondiente. Antes
de abrir, intentá el cálculo en papel.

```{code-cell} python
:tags: [hide-input]
import math

from core import Settings
from exercises import (
    BooleanAnswerInput,
    NumericAnswerInput,
    verify_boolean_answer,
    verify_numeric_answer,
)
from visualization import (
    PartitionDiagramInput,
    ProbabilityTreeInput,
    VennTwoSetsInput,
    chart_partition_diagram,
    chart_probability_tree,
    chart_venn_two_sets,
)

settings = Settings()
```

## Ejercicio 1 — Regla aditiva

En una sala de espera, llevamos registro de dos hábitos de los pacientes
mientras esperan: $A$ = «usa el celular», $B$ = «lee una revista». En
una muestra grande se observó:

- $P(A) = 0{,}45$,
- $P(B) = 0{,}30$,
- $P(A \cap B) = 0{,}12$.

¿Cuál es $P(A \cup B)$? ¿Cuál es la probabilidad de que un paciente
**no haga ninguna** de las dos cosas?

:::{admonition} Solución
:class: dropdown

### Planteo

Por la regla aditiva ([](probability.md#eq-union-prob)),

$$
P(A \cup B) = P(A) + P(B) - P(A \cap B).
$$

El complemento $\overline{A \cup B}$ se calcula como $1 - P(A \cup B)$
por la regla de [](probability.md#eq-complement-prob).

### Derivación

$$
P(A \cup B) = 0{,}45 + 0{,}30 - 0{,}12 = 0{,}63.
$$

$$
P(\overline{A \cup B}) = 1 - 0{,}63 = 0{,}37.
$$

### Visual

```{code-cell} python
chart_venn_two_sets(
    VennTwoSetsInput(
        probability_a=0.45,
        probability_b=0.30,
        probability_intersection=0.12,
        set_a_label="Celular (A)",
        set_b_label="Revista (B)",
        settings=settings,
    )
)
```

### Verificación

```{code-cell} python
expected_union = 0.45 + 0.30 - 0.12
verify_numeric_answer(
    NumericAnswerInput(
        student_answer=0.63,
        expected_answer=expected_union,
    )
)
```

```{code-cell} python
expected_neither = 1.0 - expected_union
verify_numeric_answer(
    NumericAnswerInput(
        student_answer=0.37,
        expected_answer=expected_neither,
    )
)
```

:::

## Ejercicio 2 — Probabilidad condicional en una tabla

En una encuesta a 200 votantes se cruzó la intención de voto con el grupo
etario:

| | Apoya (S) | No apoya ($\bar{S}$) |
|---|---|---|
| Jóvenes (J) | 48 | 32 |
| Mayores ($\bar{J}$) | 60 | 60 |

Calculá $P(S \mid J)$ — la probabilidad de que un votante elegido al azar
**apoye**, sabiendo que es **joven**.

:::{admonition} Solución
:class: dropdown

### Planteo

Por la definición de probabilidad condicional
[](probability.md#eq-cond-prob),

$$
P(S \mid J) = \frac{P(S \cap J)}{P(J)}.
$$

Cuando trabajamos con conteos podemos pasar directamente a cocientes de
conteos:

$$
P(S \mid J) = \frac{n(S \cap J)}{n(J)}.
$$

### Derivación

$$
n(S \cap J) = 48,\qquad n(J) = 48 + 32 = 80.
$$

$$
P(S \mid J) = \frac{48}{80} = 0{,}60.
$$

### Verificación

```{code-cell} python
expected_conditional = 48 / 80
verify_numeric_answer(
    NumericAnswerInput(
        student_answer=0.60,
        expected_answer=expected_conditional,
    )
)
```

:::

## Ejercicio 3 — Probabilidad total

Una línea de producción usa dos máquinas, $M_1$ y $M_2$. $M_1$ fabrica
el 60 % de las piezas y produce un 2 % de defectuosas; $M_2$ fabrica el
40 % restante y produce un 5 % de defectuosas. Se elige una pieza al
azar del lote total.

¿Cuál es la probabilidad de que **sea defectuosa** ($D$)?

:::{admonition} Solución
:class: dropdown

### Planteo

Las máquinas $M_1$ y $M_2$ forman una partición del espacio muestral.
Por la regla de probabilidad total
([](probability.md#eq-total-prob)),

$$
P(D) = P(D \mid M_1)\,P(M_1) + P(D \mid M_2)\,P(M_2).
$$

### Derivación

$$
P(D) = 0{,}02 \cdot 0{,}60 + 0{,}05 \cdot 0{,}40
     = 0{,}012 + 0{,}020 = 0{,}032.
$$

Es decir, el lote total tiene **3,2 %** de piezas defectuosas.

### Visual

```{code-cell} python
chart_partition_diagram(
    PartitionDiagramInput(
        partition_labels=("M₁", "M₂"),
        partition_weights=(0.60, 0.40),
        overlay_label="Defectuosas (D)",
        overlay_fractions=(0.02, 0.05),
        title="Partición por máquina con defectuosos resaltados",
        settings=settings,
    )
)
```

### Verificación

```{code-cell} python
expected_defective = 0.02 * 0.60 + 0.05 * 0.40
verify_numeric_answer(
    NumericAnswerInput(
        student_answer=0.032,
        expected_answer=expected_defective,
    )
)
```

:::

## Ejercicio 4 — Bayes en una prueba diagnóstica

Una clínica usa un test rápido para una enfermedad con **prevalencia**
$P(E) = 0{,}01$. El test tiene sensibilidad $P(+ \mid E) = 0{,}98$ y
especificidad $P(- \mid \bar{E}) = 0{,}95$.

Si un paciente da **positivo**, ¿cuál es la probabilidad de que
**realmente esté enfermo**?

:::{admonition} Solución
:class: dropdown

### Planteo

Queremos $P(E \mid +)$. Aplicamos Bayes
([](probability.md#eq-bayes)) con denominador armado por
probabilidad total ([](probability.md#eq-total-prob)):

$$
P(E \mid +) = \frac{P(+ \mid E)\,P(E)}
{P(+ \mid E)\,P(E) + P(+ \mid \bar{E})\,P(\bar{E})}.
$$

Notar que $P(+ \mid \bar{E}) = 1 - P(- \mid \bar{E}) = 0{,}05$.

### Derivación

**Numerador.** $P(+ \mid E)\,P(E) = 0{,}98 \cdot 0{,}01 = 0{,}0098$.

**Denominador.** $0{,}0098 + 0{,}05 \cdot 0{,}99 = 0{,}0098 + 0{,}0495 = 0{,}0593$.

$$
P(E \mid +) = \frac{0{,}0098}{0{,}0593} \approx 0{,}165.
$$

Aun con un test que parece muy bueno, **solo el 16,5 %** de los
positivos corresponden a enfermos reales. La prevalencia baja domina.

### Visual

```{code-cell} python
chart_probability_tree(
    ProbabilityTreeInput(
        branch_labels=("E", "Ē"),
        branch_probabilities=(0.01, 0.99),
        leaf_labels=("+", "−"),
        conditional_probabilities=((0.98, 0.02), (0.05, 0.95)),
        title="Árbol enfermedad / test",
        settings=settings,
    )
)
```

### Verificación

```{code-cell} python
prior = 0.01
sensitivity = 0.98
false_positive = 1.0 - 0.95
numerator = sensitivity * prior
denominator = numerator + false_positive * (1.0 - prior)
expected_posterior = numerator / denominator

verify_numeric_answer(
    NumericAnswerInput(
        student_answer=0.165,
        expected_answer=expected_posterior,
        absolute_tolerance=0.005,
    )
)
```

:::

## Ejercicio 5 — ¿Son independientes?

Volvé a la tabla del [Ejercicio 2](#ejercicio-2-probabilidad-condicional-en-una-tabla).
Calculá $P(S)$ marginal y compará con $P(S \mid J)$.

¿Los eventos $S$ y $J$ son **independientes**?

:::{admonition} Solución
:class: dropdown

### Planteo

$S$ y $J$ son independientes si $P(S \mid J) = P(S)$ (o
equivalentemente $P(S \cap J) = P(S)\,P(J)$, ver
[](probability.md#sec-prob-independence)).

### Derivación

- $P(S) = (48 + 60) / 200 = 108 / 200 = 0{,}54$.
- $P(S \mid J) = 48 / 80 = 0{,}60$ (del Ejercicio 2).

Como $0{,}60 \ne 0{,}54$, **no son independientes**: ser joven cambia
la probabilidad de apoyar.

### Verificación

```{code-cell} python
probability_support = 108 / 200
probability_support_given_young = 48 / 80
expected_independent = math.isclose(
    probability_support, probability_support_given_young, abs_tol=1e-6
)

verify_boolean_answer(
    BooleanAnswerInput(
        student_answer=False,
        expected_answer=expected_independent,
    )
)
```

:::

## Ejercicio 6 — Bayes inverso en producción

Volvé al [Ejercicio 3](#ejercicio-3-probabilidad-total). Se elige una pieza
del lote y resulta ser **defectuosa**.

¿Cuál es la probabilidad de que la haya fabricado la **máquina $M_2$**?

:::{admonition} Solución
:class: dropdown

### Planteo

Aplicamos Bayes ([](probability.md#eq-bayes)) con denominador igual al
$P(D)$ ya calculado en el Ejercicio 3:

$$
P(M_2 \mid D) = \frac{P(D \mid M_2)\,P(M_2)}{P(D)}.
$$

### Derivación

$$
P(M_2 \mid D) = \frac{0{,}05 \cdot 0{,}40}{0{,}032}
              = \frac{0{,}020}{0{,}032} = 0{,}625.
$$

Aunque $M_2$ fabrica menos piezas que $M_1$ (40 % vs. 60 %), produce más
defectos, así que **dada una pieza defectuosa**, lo más probable es que
venga de $M_2$.

### Verificación

```{code-cell} python
probability_machine_two = 0.40
defect_rate_machine_two = 0.05
total_defect_probability = 0.032
expected_posterior = (defect_rate_machine_two * probability_machine_two) / total_defect_probability

verify_numeric_answer(
    NumericAnswerInput(
        student_answer=0.625,
        expected_answer=expected_posterior,
    )
)
```

:::
