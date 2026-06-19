---
title: Promedios, estabilidad y el teorema central del límite
short_title: Sumas y promedios
kernelspec:
  name: python3
  display_name: Python 3
---

Cada distribución del capítulo anterior describía **una observación a
la vez**: la espera de un paciente, la respuesta de una persona en la
encuesta, el conteo de defectos de una sola pieza. Pero ningún día de
la clínica se decide con un solo paciente, ninguna encuesta se publica
con una sola respuesta, ningún turno de la línea de producción se
resume en un único conteo. Lo que termina importando es el
**promedio** o el **total** sobre muchas observaciones, y apenas damos
ese paso aparecen tres preguntas que insisten una y otra vez.

Este capítulo se concentra en sumas, promedios y aproximaciones. Las
distribuciones conjuntas quedan fuera del recorrido inicial; acá la
pregunta es qué pasa cuando repetimos muchas veces una misma medición
bajo condiciones comparables.

¿A qué tiende el promedio diario de esperas a medida que la muestra
crece, y por qué tantas mañanas distintas dan números cada vez más
parecidos?, ¿cómo se distribuye ese promedio alrededor de su valor
central cuando todavía solo medimos un puñado de pacientes?, ¿por qué
la suma de muchos efectos pequeños — una respuesta de la encuesta
tras otra, un defecto tras otro — termina pareciéndose a una campana
incluso cuando ninguna observación individual lo hace?

La decisión práctica es conocida para cualquier equipo de ingeniería:
cuántas observaciones hacen falta para confiar en un promedio, una
proporción o un total antes de cambiar turnos, publicar una encuesta o
parar una línea. Esa decisión convierte una fórmula en una pregunta de
costo, riesgo y comunicación.

**Antes de seguir.** Traé de vuelta tres piezas: qué representa una
esperanza, qué representa una varianza y cómo cambia una distribución
cuando deja de describir una observación para describir un promedio.

Las tres preguntas comparten respuesta y caen, finalmente, sobre el
**teorema central del límite**.

```{code-cell} python
:tags: [hide-input]
import math

import altair as alt
import pandas as pd

from core import (
    BinomialParams,
    ExponentialParams,
    NormalParams,
    Settings,
)
from distributions import (
    make_binomial,
    make_exponential,
    make_normal,
    tail_probability_of_continuous,
)
from distributions.evaluations import TailProbabilityInput
from exercises import NumericAnswerInput, verify_numeric_answer
from sampling import (
    CLTSimulationInput,
    GaltonBoardInput,
    LLNMultipleTrajectoriesInput,
    LLNSimulationInput,
    simulate_clt,
    simulate_galton_board,
    simulate_lln,
    simulate_lln_multiple_trajectories,
)
from visualization import (
    CLTComparisonChartInput,
    LLNChartInput,
    LLNMultipleTrajectoriesChartInput,
    chart_clt_comparison,
    chart_lln_multiple_trajectories,
    chart_lln_running_mean,
)
from visualization.theme import apply_theme
from widgets import (
    CLTExplorerInput,
    LLNExplorerInput,
    build_clt_explorer,
    build_lln_explorer,
)
```

```{code-cell} python
:tags: [remove-cell]
settings = Settings()
```

## Dónde estamos en las tres historias

Antes de entrar al teorema central del límite, vale ordenar el mapa:

- **Clínica.** Ya describimos esperas observadas y las modelamos como tiempos individuales. Ahora queremos entender promedios diarios de muchas esperas.
- **Encuesta.** Ya vimos respuestas «sí/no» como eventos y como variables Binomiales. Ahora nos importa por qué la proporción observada se estabiliza al crecer la muestra.
- **Línea de producción.** Ya contamos defectos con Binomial y Poisson. Ahora vamos a aproximar totales grandes sin revisar barra por barra.

**Antes de seguir.** Elegí una de las tres historias y anticipá qué debería pasar cuando pasamos de una observación aislada a muchas observaciones promediadas.

(sec-sums-lln)=
## La proporción observada se estabiliza

Volvemos a la encuesta. Cada persona responde «sí» con probabilidad
$p$ y «no» con probabilidad $1 - p$. Llevamos un cuaderno y, después
de cada respuesta, anotamos la **proporción acumulada** de «sí» hasta
ese momento: la cantidad de «sí» dividida por la cantidad total de
respuestas. La pregunta concreta es: si fijamos $p = 0{,}55$ (la
verdad oculta de la población) y vamos preguntando una persona tras
otra, ¿qué hace ese cociente a medida que crece $n$?

**Antes de simular.** Imaginá las primeras diez respuestas y después las
primeras cuatro mil. ¿En cuál etapa esperás más saltos bruscos? ¿En cuál
esperás que el promedio acumulado sea más difícil de mover?

```{code-cell} python
bernoulli = make_binomial(BinomialParams(trials=1, success_probability=0.55))
lln_input = LLNSimulationInput(
    distribution=bernoulli,
    horizon=4_000,
    settings=settings,
)
lln_result = simulate_lln(lln_input)

lln_chart_input = LLNChartInput(
    lln_result=lln_result,
    title="Encuesta — proporción observada de «sí» (LLN)",
    settings=settings,
)
chart_lln_running_mean(lln_chart_input)
```

Una sola simulación podría haber bajado en lugar de subir, o haber pasado
más tiempo lejos de $0{,}55$. Para ver que la convergencia no depende de la
suerte de un único experimento, repetimos el mismo procedimiento muchas
veces en paralelo: cada trayectoria es una encuesta distinta hecha en una
ciudad imaginaria diferente, con sus propios «sí» y «no» en otro orden.

```{code-cell} python
lln_multi_input = LLNMultipleTrajectoriesInput(
    distribution=bernoulli,
    horizon=4_000,
    trajectory_count=30,
    settings=settings,
)
lln_multi_result = simulate_lln_multiple_trajectories(lln_multi_input)

lln_multi_chart_input = LLNMultipleTrajectoriesChartInput(
    lln_result=lln_multi_result,
    title="30 encuestas paralelas — todas convergen al mismo valor",
    settings=settings,
)
chart_lln_multiple_trajectories(lln_multi_chart_input)
```

El abanico es ancho al principio: con pocas respuestas, la proporción
observada en cada encuesta puede caer casi en cualquier lado. A medida
que $n$ crece, las treinta líneas se aprietan contra el valor teórico
$0{,}55$ y el ancho de la franja tiende a cero. Esa contracción
simultánea no depende de la suerte de un experimento: ocurre en las
treinta encuestas a la vez.

### El nombre de lo que vimos

Lo que las simulaciones acaban de mostrar tiene un nombre clásico. El
promedio acumulado tras $n$ respuestas es

$$ \bar{X}_n = \frac{1}{n}\sum_{i=1}^{n} X_i $$ (eq-running-mean)

—exactamente la misma definición de promedio de [](#eq-mean), pero
ahora con $X_i$ **variables aleatorias** en lugar de observaciones
fijas. La afirmación que extrajimos del gráfico se conoce como
**ley de los grandes números (LLN)**: si las $X_i$ son
i.i.d. con $E[X_i] = \mu$ y varianza finita,

$$ \bar{X}_n \xrightarrow{P} \mu \quad\text{cuando } n \to \infty $$ (eq-lln)

La flecha es el modo formal de decir lo que el abanico mostró: con
muestras chicas la proporción puede estar lejos del valor verdadero,
con muestras grandes la chance de seguir lejos cae a cero.

> **Contrato del modelo.** La LLN describe promedios de muchas observaciones
> comparables, independientes y con esperanza bien definida. Te permite confiar
> en la estabilidad de un promedio grande, no prometer que una muestra chica va a
> estar cerca ni describir la forma exacta de sus errores.

**Trampa común.** La LLN habla de estabilidad del promedio cuando $n$ crece.
No describe todavía la forma de la distribución de ese promedio alrededor del
valor verdadero; esa será la pregunta del TCL.

```{code-cell} python
lln_explorer_input = LLNExplorerInput(settings=settings)
build_lln_explorer(lln_explorer_input)
```

(sec-sums-galton)=
## El tablero de Galton

Cambiamos por completo de escenario. Imaginá un tablero vertical con
filas de clavos en zigzag. Soltamos una bolita por arriba; cada vez
que choca un clavo, salta a la izquierda o a la derecha con la misma
probabilidad. Después de pasar por $r$ filas, la bolita cae en una
casilla del fondo. Soltamos miles de bolitas, contamos cuántas
terminan en cada casilla, y miramos el histograma de casillas
ocupadas.

**Antes de mirar.** Una bolita sola solo cuenta una historia accidental. Con
miles de bolitas, ¿esperás que todas las casillas reciban cantidades parecidas
o que aparezca una forma reconocible?

Cada caída individual no tiene nada de «normal» — es una secuencia de saltos
discretos $\pm 1$ —, y sin embargo el dibujo colectivo que vamos a ver tiene
una forma sospechosamente familiar.

```{code-cell} python
galton_input = GaltonBoardInput(rows=24, balls=8_000, settings=settings)
galton_result = simulate_galton_board(galton_input)

galton_table = pd.DataFrame({
    "posicion": galton_result.bin_positions,
    "frecuencia": galton_result.bin_counts,
})
galton_chart = (
    alt
    .Chart(galton_table)
    .mark_bar(opacity=0.85)
    .encode(
        x=alt.X("posicion:O", title="Casilla final"),
        y=alt.Y("frecuencia:Q", title="Cantidad de bolas"),
    )
    .properties(title="Tablero de Galton — suma de 24 pasos ±1")
)
apply_theme(galton_chart, settings)
```

(sec-sums-clt)=
## El TCL formal

El histograma del tablero forma una campana centrada, simétrica,
con colas que decaen rápido — la misma silueta que apareció con la
Normal en el capítulo anterior. Pero acá nadie partió de una Normal:
la regla de cada paso era totalmente discreta y uniforme. Lo único
que hicimos fue **sumar muchos pasos independientes**. Ese es,
finalmente, el contenido del **Teorema Central del Límite**: si
promediamos suficientes copias i.i.d. de cualquier variable con
varianza finita, la distribución del promedio se vuelve
aproximadamente Normal.

La forma precisa del enunciado es la siguiente. Tomamos $X_1, X_2, \dots$
i.i.d. con $E[X_i] = \mu$ y $\mathrm{Var}(X_i) = \sigma^2 < \infty$.
Centramos el promedio [](#eq-running-mean) restándole $\mu$ y lo
escalamos por su desvío $\sigma/\sqrt{n}$:

$$ \begin{aligned}
Z_n &= \frac{\bar{X}_n - \mu}{\sigma/\sqrt{n}} \\[4pt]
Z_n &\xrightarrow{d} \mathcal{N}(0, 1)
\end{aligned} $$ (eq-clt)

Conviene retener una sutileza: [](#eq-clt) **no** dice que las $X_i$
tiendan a una Normal. Dice que su **media estandarizada** lo hace —
exactamente lo que acabamos de ver con bolitas que individualmente no
tienen nada de normal.

> **Contrato del modelo.** El TCL es una aproximación para promedios o sumas de
> muchas observaciones i.i.d. con varianza finita. Funciona mejor con muestras
> grandes y distribuciones no demasiado extremas. Si hay dependencia fuerte,
> colas muy pesadas o tamaños chicos, la campana puede llegar tarde o no llegar.

(sec-sums-clt-waits)=
## TCL aplicado a tiempos de espera

Volvamos a la sala de espera. Cada espera individual es Exponencial
([](#eq-exp-pdf)): asimétrica, con cola larga, claramente **no**
Normal. Si tomamos un día completo y registramos $30$ esperas, el
**promedio** del día es un solo número. Repetimos durante $5\,000$
días imaginarios y miramos cómo se distribuyen esos promedios diarios.
El histograma siguiente compara esa distribución empírica con la
Normal estándar después de centrar y escalar:

```{code-cell} python
clinic_distribution = make_exponential(ExponentialParams(rate=0.25))
clt_input = CLTSimulationInput(
    distribution=clinic_distribution,
    sample_size_per_replicate=30,
    replicates=5_000,
    settings=settings,
)
clinic_clt_result = simulate_clt(clt_input)

clt_chart_input = CLTComparisonChartInput(
    clt_result=clinic_clt_result,
    title="Promedio de 30 esperas (clínica) — convergencia a la Normal",
    settings=settings,
)
chart_clt_comparison(clt_chart_input)
```

Las barras estandarizadas se acomodan, día a día, encima de la
campana $\mathcal{N}(0, 1)$ ([](#eq-normal-pdf)). El TCL [](#eq-clt)
**predice** esa coincidencia: no la imponemos artificialmente — sale
del simple hecho de promediar muchas esperas.

**Chequeo rápido.** Si duplicamos el tamaño de cada día simulado, ¿esperás que
los promedios diarios se dispersen más o menos alrededor de $\mu$? Usá el
explorador de abajo para comprobarlo.

```{code-cell} python
clt_explorer_input = CLTExplorerInput(settings=settings)
build_clt_explorer(clt_explorer_input)
```

(sec-sums-binomial-normal)=
## Aproximación Binomial → Normal

Una consecuencia útil del TCL aparece sin esfuerzo en la línea de
producción. Una variable $Y \sim \text{Bin}(n, p)$ no es otra cosa
que la **suma de $n$ Bernoullis i.i.d.** — cada inspección suma uno
si la pieza es defectuosa, cero si no. Tomar la suma de muchas
Bernoullis es exactamente la situación a la que se aplica
[](#eq-clt). Resultado: cuando $n$ es razonable, la Binomial se
aproxima por una Normal con la misma media y varianza,

$$ \begin{aligned}
Y       &\approx \mathcal{N}\!\bigl(np,\ np(1-p)\bigr) \\[4pt]
        &\quad\text{válida si } np \ge 10 \text{ y } n(1-p) \ge 10
\end{aligned} $$ (eq-clt-bin)

**En una frase.** La línea no se controla pieza por pieza sino por totales: el
TCL explica por qué un conteo grande de inspecciones puede tratarse como una
campana alrededor del número esperado de defectos.

Para una jornada con $n = 100$ piezas y proporción de defectos
$p = 0{,}4$, [](#eq-clt-bin) deja calcular probabilidades sin contar
barra por barra:

```{code-cell} python
factory_normal_approx = make_normal(NormalParams(mean=40.0, standard_deviation=math.sqrt(24.0)))
factory_tail_input = TailProbabilityInput(
    distribution=factory_normal_approx,
    upper_bound=45.0,
)
factory_tail_probability = tail_probability_of_continuous(factory_tail_input)
factory_tail_probability
```

## Ejercicio 1 — Desvío del promedio

Si $X_i \sim \mathcal{N}(50, 100)$ (es decir $\sigma = 10$) y tomamos
$n = 25$ observaciones, ¿cuál es el desvío estándar de $\bar{X}_n$?

**Predicción.** Antes de calcular, decidí si el promedio de 25 observaciones
debería variar igual que una observación individual o menos. Esa intuición te
dice si el resultado debe ser menor que 10.

**Cómputo.** Calculá el error estándar y ejecutá la verificación.

**Interpretación.** Explicá por qué promediar 25 mediciones estabiliza el
resultado aunque cada observación individual siga teniendo $\sigma = 10$.

**Decisión de ingeniería.** Si el equipo quiere reducir a la mitad el error estándar, ¿alcanza
con duplicar $n$ o hace falta pensar en el crecimiento cuadrático de la muestra?

**Pista mínima.** Usá el factor de escala que aparece en [](#eq-clt).

```{code-cell} python
expected_standard_error = 10.0 / math.sqrt(25)

student_answer_se = 2.0
verify_input = NumericAnswerInput(
    student_answer=student_answer_se,
    expected_answer=expected_standard_error,
)
verify_numeric_answer(verify_input)
```

## Ejercicio 2 — Aproximar Binomial con Normal

$Y \sim \text{Bin}(100, 0{,}4)$. Aproximá $P(Y \le 45)$ aplicando [](#eq-clt-bin)
(sin corrección por continuidad para simplificar).

**Predicción.** Antes de calcular, ubicá 45 respecto de la media $np$. ¿Está
por debajo, cerca o por encima? Eso debería decirte si la probabilidad buscada
será menor o mayor que 0,5.

**Pista mínima.** Calculá primero $E[Y]$ y $\mathrm{Var}(Y)$, después
estandarizá.

```{code-cell} python
exercise_normal_approx = make_normal(NormalParams(mean=40.0, standard_deviation=math.sqrt(24.0)))
exercise_tail_input = TailProbabilityInput(
    distribution=exercise_normal_approx,
    upper_bound=45.0,
)
expected_probability = tail_probability_of_continuous(exercise_tail_input).probability

student_answer_probability = 0.846
verify_input = NumericAnswerInput(
    student_answer=student_answer_probability,
    expected_answer=expected_probability,
)
verify_numeric_answer(verify_input)
```

Hasta acá el flujo siempre fue el mismo: dados los parámetros — una tasa, una
proporción real, un desvío estándar — calcular probabilidades sobre las
observaciones. Con LLN y TCL también ganamos una regla práctica: más datos
vuelven más estable el promedio y más predecible su fluctuación.

En la práctica, sin embargo, los parámetros casi nunca se conocen; lo que se
tiene son los datos, y la pregunta natural es la **inversa**: dado lo medido,
¿qué se puede afirmar de lo que no vemos? ¿Cuál es el rango plausible para la
verdadera espera media de la clínica?, ¿cuánto se acerca la proporción
observada en la encuesta a la verdadera?, ¿alcanzan los conteos de la línea de
producción para descartar la afirmación de que los defectos están bajo el 5%?
Ese cambio de sentido — de los parámetros a los datos a los parámetros otra
vez — es el oficio de la **inferencia**.
