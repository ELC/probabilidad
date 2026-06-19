---
title: Tratamiento de datos
kernelspec:
  name: python3
  display_name: Python 3
---

Imaginate sentado en la recepción de una clínica durante toda una
mañana. Cada vez que un paciente entra al consultorio, anotás los
minutos que estuvo esperando: 4, 6, 3, 2, 12, 5, 4, 7, 5… Al final
del turno tenés ochenta números garabateados en una hoja.

Si alguien te pregunta «¿cuánto se espera, en general?», recitar la
lista entera no sirve. La persona se aburre antes del tercer paciente
y al final tampoco saca una conclusión. Si te preguntan «¿hoy fue un
día tranquilo o uno raro?», directamente no sabés por dónde empezar.

Para contestar hay que apretar la lista en unos pocos números que
respondan cosas concretas: cuál fue una espera **típica**, qué tan
**parecidas** fueron las esperas entre sí (¿todos esperaron parecido?,
¿unos poquísimo y otros muchísimo?) y si hubo alguna **fuera de lo
común** que valga la pena mirar aparte. Lucía, la responsable de
operaciones, tiene una decisión concreta antes del cierre del día:
mantener el esquema de turnos, sumar una persona en la franja crítica o
investigar si hubo un caso excepcional que distorsionó la mañana. Esos
pocos números, y la forma de calcularlos, son lo que vamos a aprender
en este capítulo.

## Cómo leer este libro

Este libro no está pensado como una lista de recetas. Cada capítulo sigue un ciclo parecido: primero aparece una situación concreta, después una imagen o simulación, luego la fórmula y finalmente una decisión o una frase de comunicación.

Cuando veas **Antes de mirar** o **Intentá antes de ejecutar**, detenete unos segundos y hacé una predicción. Ese pequeño compromiso mental ayuda a recordar mejor el resultado, incluso si la predicción sale mal. Cuando aparezca un **Contrato del modelo**, leelo como una lista de chequeo: qué supuesto permite usar la herramienta, qué la puede romper y qué conclusión autoriza.

Si querés ver el diseño completo del recorrido, tené cerca el [enfoque pedagógico](pedagogy.md). Para símbolos y términos que reaparecen entre capítulos, usá el [glosario](glossary.md).

```{code-cell} python
:tags: [hide-input]
import numpy as np
import pandas as pd

from core import Observations, Settings
from descriptive import (
    FrequencyTableInput,
    build_frequency_table,
    detect_outliers_tukey,
    standardize_observations,
    summarize_observations,
)
from exercises import NumericAnswerInput, verify_numeric_answer
from visualization import (
    DescriptiveSummaryChartInput,
    FrequencyChartInput,
    HistogramChartInput,
    chart_descriptive_summary,
    chart_frequency_table,
    chart_histogram,
)
from widgets import DescriptiveExplorerInput, build_descriptive_explorer
```

```{code-cell} python
:tags: [remove-cell]
settings = Settings()
```

(sec-descriptive-sample)=
## Una muestra de tiempos de espera

Trabajemos con un caso concreto: los 80 minutos de espera que la
enfermera de turno fue anotando paciente a paciente, ordenados en la
secuencia en que llegaron a la guardia.

```{code-cell} python
rng_clinic = np.random.default_rng(settings.random_seed)
raw_waiting_times = rng_clinic.normal(loc=4.0, scale=1.2, size=80).clip(min=0.0)
waiting_times = Observations.validate(pd.DataFrame({"value": raw_waiting_times}))
waiting_times.head()
```

Antes de cualquier número, **dibujamos**.

La forma más directa de mirar una lista de minutos es agruparla en
intervalos — por ejemplo, 0 a 2 minutos, 2 a 4, 4 a 6 — y contar
cuántos pacientes cayeron en cada grupo. Esa cuenta por intervalo es
lo que se llama una **tabla de frecuencias**. Si la dibujamos con
barras (más alta donde se amontonaron muchas esperas, más bajita donde
casi no hubo), sale un **histograma**: un gráfico que muestra dónde se
concentran los datos y si aparecen colas o valores poco frecuentes. Y
si encima trazamos una línea que va sumando, paso a paso, el porcentaje
**acumulado** de pacientes hasta cada minuto, esa línea — la **ojiva** —
nos deja leer de un vistazo cosas como «el 70% esperó menos de cinco
minutos».

**Antes de mirar.** Si la mañana fue razonablemente estable, ¿esperás
ver muchas esperas cerca de un valor central o una cola larga de casos
lentos? Hacé una predicción rápida: dónde se va a concentrar el
histograma y en qué minuto creés que la ojiva va a cruzar el 70%.

```{code-cell} python
frequency_input = FrequencyTableInput(observations=waiting_times, bin_count=10)
frequency_table = build_frequency_table(frequency_input)

frequency_chart_input = FrequencyChartInput(
    frequency_table=frequency_table,
    title="Tiempos de espera (clínica) — histograma y ojiva",
    settings=settings,
)
chart_frequency_table(frequency_chart_input)
```

(sec-descriptive-summary)=
## Tres preguntas que resumen la muestra

Volvamos a las tres preguntas que dejó abiertas la introducción: cuál
fue una espera típica, qué tan parecidas fueron las esperas entre sí,
y si hubo alguna fuera de lo común. Cada pregunta se contesta con un
número distinto, y vamos a definir uno por uno.

### Una espera típica: el promedio

El primer candidato a «valor típico» es el **promedio**: sumar todos
los minutos y dividir por la cantidad de pacientes. En estadística al
promedio se lo llama **media muestral** y se lo escribe $\bar{x}$
(una equis con una rayita arriba — es solo una convención). Si
anotamos los minutos del paciente $1$ al paciente $n$ como
$x_1, x_2, \dots, x_n$, la fórmula que hace lo que recién dijimos en
palabras es:

$$ \bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i $$ (eq-mean)

El símbolo $\sum$ es solo «sumá todos estos términos», y $x_i$ es el
tiempo del paciente número $i$. El subíndice $i$ recorre los valores
$1, 2, \dots, n$ — así que la fórmula dice exactamente lo mismo que
«sumalos a todos y dividí por la cantidad».

### Otra espera típica: la mediana

El promedio tiene un punto débil. Si entre los 80 pacientes hubo uno
que esperó dos horas porque al médico se le complicó un caso, ese
único valor extremo arrastra el promedio hacia arriba aunque el
resto de la mañana haya sido normal. Para esos casos viene bien otro
valor típico: la **mediana**, que es el número del medio cuando
ordenamos la lista de menor a mayor. La escribimos $\tilde{x}$ (equis
con una eñe encima):

$$ \tilde{x} = \begin{cases}
  x_{((n+1)/2)} & \text{si } n \text{ es impar} \\
  \dfrac{x_{(n/2)} + x_{(n/2+1)}}{2} & \text{si } n \text{ es par}
\end{cases} $$ (eq-position)

(Si la cantidad de observaciones es par no hay un único «valor del
medio», así que se promedian los dos centrales.)

### Qué tan parecidas son las esperas: el desvío estándar

Saber el promedio no alcanza: necesitamos también qué tan **parecidas**
fueron las esperas entre sí. Si todos esperaron alrededor de cuatro
minutos, el promedio cuenta casi toda la historia. Si la mitad esperó
dos minutos y la otra mitad ocho, el mismo promedio esconde dos
experiencias muy distintas.

La idea es medir, en promedio, cuánto se aleja cada paciente del
promedio general. Lo armamos en tres pasos.

**Paso 1.** Calculamos $\bar{x}$ con la fórmula [](#eq-mean) para tener el
punto de referencia:

$$ \bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i $$

**Paso 2.** Para cada paciente miramos cuánto se desvió del promedio
($x_i - \bar{x}$). Algunas diferencias son positivas (esperaron más),
otras negativas (esperaron menos), y si las sumáramos así nomás los
signos se cancelarían. Para que eso no pase, las elevamos al cuadrado
antes de sumarlas. A esa suma la llamamos **suma de cuadrados** y la
escribimos $\text{SS}$ (por *sum of squares*):

$$ \text{SS} = \sum_{i=1}^{n}(x_i - \bar{x})^2 $$

**Paso 3.** Dividimos esa suma por $n-1$ y tomamos raíz cuadrada para
volver a las unidades originales (minutos, no minutos al cuadrado). Lo
que sale es el **desvío estándar muestral**, que escribimos $s$:

$$ s = \sqrt{\frac{\text{SS}}{n - 1}} $$ (eq-std)

En palabras: $s$ es la distancia típica entre una observación
cualquiera y el promedio. Cuanto más chico es $s$, más parecidas son
las esperas entre sí.

```{code-cell} python
summary = summarize_observations(waiting_times)
summary
```

La tabla de arriba contesta las tres preguntas a la vez. La **media**
y la **mediana** dan dos formas distintas de responder cuál fue una
espera típica; el **desvío estándar** dice qué tan parecidas fueron
las esperas entre sí; y el **rango intercuartil** y las cotas inferior
y superior — que aparecen un poco más abajo, cuando las definamos —
marcan la frontera entre lo habitual y lo raro. Pasá la vista por las
filas y fijate qué te dice cada número antes de seguir.

**Trampa común.** Un único “valor típico” no decide si la operación
funcionó bien. Dos mañanas pueden tener la misma media y experiencias
muy distintas si una fue estable y la otra alternó esperas mínimas con
esperas extremas.

**Decisión de ingeniería.** Antes de seguir, elegí qué mirarías si
tuvieras que justificar una acción: ¿la media para estimar capacidad,
la mediana para describir la experiencia típica, o la dispersión para
medir estabilidad?

(sec-descriptive-median)=
## Por qué la mediana resiste lo que la media no

Cuando la distribución es **simétrica**, $\bar{x}$ y $\tilde{x}$ están casi
pegados. Cuando aparecen valores muy altos (un paciente con espera anormal) la
**media se mueve** hacia ese punto; la **mediana se queda quieta** porque sólo
depende del orden.

Lo materializamos con un boxplot que marca, además, la media muestral con una
línea punteada: cuando hay cola, las dos referencias se separan.

```{code-cell} python
descriptive_chart_input = DescriptiveSummaryChartInput(
    observations=waiting_times,
    statistics=summary,
    title="Tiempos de espera — boxplot con media muestral",
    settings=settings,
)
chart_descriptive_summary(descriptive_chart_input)
```

(sec-descriptive-tukey)=
## Detección de outliers — la regla de Tukey

**Paso 1:** partimos de los cuartiles $Q_1$ y $Q_3$ que ya calculó la fórmula
[](#eq-position) en su versión generalizada. **Paso 2:** definimos el rango intercuartil
$\text{IQR} = Q_3 - Q_1$. **Paso 3:** una observación es **outlier** si cae
fuera del intervalo:

$$ \bigl[Q_1 - 1{,}5\,\text{IQR},\ Q_3 + 1{,}5\,\text{IQR}\bigr] $$ (eq-iqr-fence)

Es la misma regla que usa la caja del boxplot: por eso ese gráfico es buen
detector visual.

```{code-cell} python
outlier_report = detect_outliers_tukey(waiting_times)
outlier_report
```

(sec-descriptive-zscore)=
## Posición relativa: el $z$-score

El $z$-score (*standard score*) traduce una observación a la pregunta «¿a cuántos desvíos del
promedio está?». **Paso 1:** partimos de las fórmulas [](#eq-mean) y [](#eq-std) para tener
$\bar{x}$ y $s$. **Paso 2:** centramos restando el promedio. **Paso 3:**
reescalamos dividiendo por $s$:

$$ z_i = \frac{x_i - \bar{x}}{s} $$ (eq-zscore)

Un $z_i$ positivo dice «este paciente esperó más que el promedio»; un
$z_i$ negativo, «menos que el promedio». Y la magnitud cuenta cuántos
$s$ separan la observación del centro: $z_i = 2$ significa dos desvíos
estándar arriba, sin importar las unidades originales.

Acá $z_i$ es una medida descriptiva de posición relativa. No es un
estadístico de prueba: ese papel aparece en inferencia como $z$-statistic
($z_{\text{obs}}$) cuando se contrasta una hipótesis nula.

```{code-cell} python
standardized = standardize_observations(waiting_times)
standardized
```

(sec-descriptive-defects)=
## Piezas defectuosas por turno

Cambiamos de escala y de unidad. La línea de producción registra, en cada uno
de los últimos 60 turnos, cuántas piezas resultaron defectuosas tras la
inspección. Acá no estamos midiendo en minutos: estamos contando.

```{code-cell} python
rng_factory = np.random.default_rng(seed=20260202)
raw_defect_counts = rng_factory.poisson(lam=3.5, size=60).astype(float)
defect_counts = Observations.validate(pd.DataFrame({"value": raw_defect_counts}))

defect_histogram_input = HistogramChartInput(
    observations=defect_counts,
    bin_count=12,
    title="Piezas defectuosas por turno (60 turnos)",
    settings=settings,
)
chart_histogram(defect_histogram_input)
```

```{code-cell} python
defect_summary = summarize_observations(defect_counts)
defect_summary
```

Las dos muestras viven en escalas distintas — minutos contra piezas — y con
magnitudes muy distintas. Comparar sus medias en crudo dice poco: 4 minutos
no es ni mejor ni peor que 3 piezas defectuosas. Cuando la comparación se
vuelve incómoda hay que salir de las unidades originales: los $z$-scores
(*standard scores*), que ya introdujimos, y el **coeficiente de variación**
$s/\bar{x}$ son adimensionales y permiten comparar sin trampas. ¿Cuál de las dos muestras
tiene, relativo a su propia media, más dispersión?

## Exploración interactiva

Probá esa intuición moviendo $\sigma$ con el control de abajo. Antes de tocar
el control, anticipá dos cosas: qué debería pasar con la caja del boxplot y qué
debería quedarse casi quieto. Después mové un parámetro por vez y verificá si
tu predicción se cumple.

**Chequeo rápido.** Si la mediana queda igual pero la caja se ensancha, ¿qué
le dirías a la responsable de operaciones: cambió la espera típica o cambió la
regularidad del servicio?

```{code-cell} python
explorer_input = DescriptiveExplorerInput(settings=settings)
build_descriptive_explorer(explorer_input)
```

(sec-descriptive-sampling)=
## Antes de inferir: cómo se juntaron los datos

Un resumen descriptivo puede ser exacto y aun así engañar. Si las 80 esperas de la clínica fueron tomadas durante varias mañanas típicas, con pacientes habituales y sin cambios de proceso, la muestra habla bastante bien del servicio. Si todas salieron de un lunes después de un feriado, de una semana con un sistema caído o de la franja más congestionada, el promedio y el desvío describen esa situación especial, no necesariamente la clínica.

Tres palabras conviene tener presentes desde ahora:

- **Representatividad.** La muestra debe parecerse al proceso sobre el que queremos decidir.
- **Sesgo.** Un patrón de recolección puede empujar todos los datos en una misma dirección.
- **Independencia.** Una observación no debería arrastrar mecánicamente a la siguiente; si una demora inicial retrasa a todos los pacientes posteriores, las esperas quedan encadenadas.

> **Contrato del dato.** Antes de confiar en cualquier modelo, preguntá cómo nació la muestra. ¿Cubre horarios y días relevantes? ¿Evita elegir solo casos fáciles de medir? ¿Hubo cambios de política, demanda o personal durante la medición? Una muestra sesgada puede producir gráficos prolijos y fórmulas correctas apuntando a una conclusión equivocada.

**Decisión de ingeniería.** Si Lucía quiere rediseñar turnos para todo el mes, una mañana extrema sirve como alarma, pero no como única evidencia. La pregunta siguiente no es solo “cuál fue la media”, sino “qué proceso generó estos datos y qué población representan”.

## Ejercicio 1 — Media de una muestra pequeña

Tomá la muestra $\{2, 4, 4, 4, 5, 5, 7, 9\}$ y calculá la media muestral
aplicando la fórmula [](#eq-mean).

**Intentá antes de ejecutar.** Primero estimá mentalmente si la media debería
quedar cerca de 4, de 5 o de 6. Después hacé la cuenta y ejecutá la celda para
comparar tu respuesta con la verificación.

**Interpretación.** Si este número fueran minutos de espera, explicá qué dice
sobre la espera típica y qué no dice sobre la regularidad del servicio.

**Decisión de ingeniería.** Escribí una frase para Lucía: ¿mirarías solo la media antes de
cambiar turnos, o pedirías también dispersión y posibles outliers?

```{code-cell} python
exercise_sample = Observations.validate(pd.DataFrame({"value": [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]}))
expected_mean = summarize_observations(exercise_sample).location.mean

student_answer_mean = 5.0
verify_input_mean = NumericAnswerInput(
    student_answer=student_answer_mean,
    expected_answer=expected_mean,
)
verify_numeric_answer(verify_input_mean)
```

## Ejercicio 2 — Desvío estándar muestral

Para la misma muestra, aplicá la fórmula [](#eq-std). Usá $\bar{x} = 5$ del
ejercicio 1.

**Intentá antes de ejecutar.** Calculá la suma de cuadrados, dividí por $n-1$
y recién entonces tomá raíz. Antes de verificar, respondé: ¿un desvío cercano
a 2 minutos te parece mucha o poca dispersión para una media de 5?

**Pista mínima.** Los valores 2 y 9 son los que más empujan la dispersión.

```{code-cell} python
expected_std = summarize_observations(exercise_sample).dispersion.sample_standard_deviation

student_answer_std = 2.138
verify_input_std = NumericAnswerInput(
    student_answer=student_answer_std,
    expected_answer=expected_std,
)
verify_numeric_answer(verify_input_std)
```

## Ejercicio 3 — ¿Qué representa esta muestra?

Lucía tiene dos opciones para estimar la espera típica del mes:

- medir 80 pacientes de una sola mañana posterior a un feriado;
- medir 20 pacientes por semana durante cuatro semanas, mezclando días y horarios.

**Predicción.** Antes de responder, decidí cuál muestra esperás que sea más estable para planificar turnos de todo el mes.

**Interpretación.** Explicá qué sesgo podría aparecer en la primera opción y qué parte del proceso cubre mejor la segunda.

**Decisión de ingeniería.** Si el presupuesto solo permite una medición corta, ¿la usarías para cambiar turnos de inmediato o como señal para medir mejor? Escribí una frase que conserve esa incertidumbre.

Con estos resúmenes, la responsable de operaciones ya puede separar tres
mensajes: cómo fue la espera típica, cuán estable fue el servicio y si algún
caso extremo merece revisión. Esa decisión, sin embargo, mira siempre lo que
**ya pasó**: un puñado de mañanas en la clínica, algunos turnos de la línea de
producción.

Apenas entra un paciente nuevo o llega un turno todavía no inspeccionado, estos
resúmenes dejan de alcanzar: ¿qué tan probable es que el próximo paciente
espere más de cinco minutos?, si ya lleva tres minutos esperando, ¿cambian las
chances?, cuando alguien dice «sí» en la encuesta, ¿qué tan creíble es esa
respuesta dado lo que ya sabemos de la población? Para responder hay que dejar
de mirar muestras y empezar a hablar de futuros posibles — un idioma con su
propia gramática, la **probabilidad**.
