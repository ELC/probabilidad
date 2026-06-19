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

Para contestar hay que apretar la lista en unos pocos gráficos y unos pocos números que
respondan cosas concretas: cuál fue una espera **típica**, qué tan
**parecidas** fueron las esperas entre sí (¿todos esperaron parecido?,
¿unos poquísimo y otros muchísimo?) y si hubo alguna **fuera de lo
común** que valga la pena mirar aparte. Lucía, la responsable de
operaciones, tiene una decisión concreta antes del cierre del día:
mantener el esquema de turnos, sumar una persona en la franja crítica o
investigar si hubo un caso excepcional que distorsionó la mañana. Esos
pocos números, y la forma de calcularlos, son lo que vamos a aprender
en este capítulo.

> **Situación de decisión.** Lucía tiene que cerrar la mañana con una
> recomendación concreta: mantener el esquema de turnos, reforzar una franja o
> investigar un caso excepcional. El riesgo no es calcular mal una media; es
> resumir una mañana irregular con un número que esconda justo lo que importa.

```{code-cell} python
:tags: [hide-input]
import numpy as np
import pandas as pd
from pandera.typing import DataFrame

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
    TypicalValuesComparisonChartInput,
    chart_descriptive_summary,
    chart_frequency_table,
    chart_histogram,
    chart_typical_values_comparison,
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
waiting_times = pd.DataFrame({"value": raw_waiting_times}).pipe(DataFrame[Observations])
waiting_times.head()
```

(sec-descriptive-frequency)=
## Agrupar la lista antes de resumir

Antes de cualquier número, **dibujamos**. La primera decisión no es qué fórmula usar, sino
cómo convertir ochenta valores sueltos en una forma legible sin borrar lo importante.

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
frequency_input = FrequencyTableInput(observations=waiting_times, bin_width=2.0)
frequency_table = build_frequency_table(frequency_input)

frequency_chart_input = FrequencyChartInput(
    frequency_table=frequency_table,
    title="Tiempos de espera (clínica) — histograma y ojiva",
    settings=settings,
)
chart_frequency_table(frequency_chart_input)
```

La tabla que alimenta el gráfico tiene tres columnas que conviene distinguir.
La **frecuencia absoluta** cuenta pacientes en cada intervalo; la **frecuencia
relativa** divide esa cuenta por el total; la **frecuencia relativa acumulada**
va sumando las filas anteriores. Si $n_j$ es la cantidad de observaciones en el
intervalo $j$ y $n$ el tamaño total,

$$ f_j = \frac{n_j}{n}, \qquad F_j = \sum_{r \le j} f_r $$ (eq-frequency-table)

El histograma responde «¿dónde se amontonan los datos?». La ojiva responde
«¿qué proporción queda por debajo de cierto corte?». Antes de resumir con una
media o un desvío, esta mirada protege contra una trampa común: pedirle a un
solo número que cuente una forma completa.

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
dos minutos y la otra mitad seis, el mismo promedio esconde dos
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

**Paso 3.** Dividimos esa suma por $n-1$. Ese cociente es la **varianza
muestral**:

$$ s^2 = \frac{\text{SS}}{n - 1} $$ (eq-sample-variance)

El divisor $n-1$ aparece porque usamos los mismos datos para estimar
$\bar{x}$: una vez fijado el promedio, el último desvío ya queda determinado
por los anteriores. No es un detalle cosmético; evita que la dispersión
muestral quede sistemáticamente demasiado chica cuando usamos la muestra para
hablar de un proceso más amplio.

Para volver a las unidades originales (minutos, no minutos al cuadrado),
tomamos raíz cuadrada. Lo que sale es el **desvío estándar muestral**, que
escribimos $s$:

$$ s = \sqrt{\frac{\text{SS}}{n - 1}} $$ (eq-std)

En palabras: $s$ es la distancia típica entre una observación
cualquiera y el promedio. Cuanto más chico es $s$, más parecidas son
las esperas entre sí.

Otra medida de dispersión, más simple y más sensible a extremos, es el
**rango**. Si miramos la observación más chica y la más grande de la muestra,
el rango muestral es $R = \max_i x_i - \min_i x_i$. Resume la amplitud total
observada: cuánto separa al caso más bajo del caso más alto. A diferencia de
$s$, que usa todas las observaciones, $R$ depende sólo de los dos extremos; por
eso crece mucho cuando aparece un valor atípico.

```{code-cell} python
summary = summarize_observations(waiting_times)
summary
```

La tabla de arriba contesta las tres preguntas a la vez. La **media**
y la **mediana** dan dos formas distintas de responder cuál fue una
espera típica; el **desvío estándar** y el **rango** dicen qué tan parecidas
fueron las esperas entre sí, pero con sensibilidades distintas. Por ahora,
concentrémonos en esas filas: más
adelante vamos a construir una regla para separar lo habitual de lo
raro. Pasá la vista por la tabla y fijate qué te dice cada número antes
de seguir.

**Trampa común.** Un único “valor típico” no decide si la operación
funcionó bien. Dos mañanas pueden tener la misma media y experiencias
muy distintas si una fue estable y la otra alternó esperas mínimas con
esperas extremas.

**Decisión de ingeniería.** Antes de seguir, elegí qué mirarías si
tuvieras que justificar una acción: ¿la media para estimar capacidad,
la mediana para describir la experiencia típica, o la dispersión para
medir estabilidad?

**Idea para retener.** El centro cuenta una historia típica; la dispersión y
los atípicos dicen cuánta confianza merece esa historia.

(sec-descriptive-median)=
## Por qué la mediana resiste lo que la media no

Cuando la distribución es **simétrica**, $\bar{x}$ y $\tilde{x}$ están casi
pegados. Cuando aparecen valores muy altos (un paciente con espera anormal) la
**media se mueve** hacia ese punto; la **mediana se queda quieta** porque sólo
depende del orden.

Agreguemos artificialmente una espera de 120 minutos a la misma mañana. No
estamos cambiando los datos reales: armamos una segunda muestra para comparar
qué pasa con cada resumen cuando aparece un valor extremo.

```{code-cell} python
waiting_times_with_extreme = pd.concat(
    [waiting_times, pd.DataFrame({"value": [120.0]})], ignore_index=True
).pipe(DataFrame[Observations])
summary_with_extreme = summarize_observations(waiting_times_with_extreme)
```

```{code-cell} python
typical_values_chart_input = TypicalValuesComparisonChartInput(
    original_statistics=summary,
    comparison_statistics=summary_with_extreme,
    settings=settings,
)
chart_typical_values_comparison(typical_values_chart_input)
```

La línea de la media sube con fuerza porque el valor extremo entra en la suma.
La mediana, en cambio, apenas se mueve: al ordenar 81 valores, el centro sigue
representando una espera habitual, no el caso excepcional.

(sec-descriptive-position)=
## Posición dentro de la muestra: cuartiles y percentiles

La mediana respondió una pregunta de posición: ¿qué valor deja la mitad de los
datos a cada lado? Podemos hacer la misma pregunta con otros cortes. Si Lucía
pregunta «¿hasta qué minuto esperó el 75% de los pacientes?», ya no busca una
espera típica sino un **percentil**.

Un percentil $p$ es el valor que deja aproximadamente el $p\%$ de las
observaciones por debajo. Los **cuartiles** son tres percentiles especiales:
$Q_1$ deja cerca del 25%, $Q_2$ coincide con la mediana y $Q_3$ deja cerca del
75%.

```{code-cell} python
position_summary = pd.DataFrame({
    "corte": ["mínimo", "Q1", "mediana / Q2", "Q3", "máximo"],
    "minutos": [
        summary.location.minimum,
        summary.location.first_quartile,
        summary.location.median,
        summary.location.third_quartile,
        summary.location.maximum,
    ],
})
position_summary
```

Antes de leer la tabla, pensá en la ojiva: $Q_1$, $Q_2$ y $Q_3$ son puntos sobre
esa curva acumulada. Si $Q_3$ queda cerca de la mediana, la mayor parte de la
mañana fue compacta; si queda lejos, el tramo alto de esperas se estiró.

(sec-descriptive-boxplot)=
## Cómo leer un boxplot

Un **boxplot** — o diagrama de caja y bigotes — comprime la distribución en
cinco referencias visuales: mínimo no atípico, $Q_1$, mediana, $Q_3$ y máximo
no atípico. Es la tabla de posiciones convertida en dibujo.

En el gráfico, la línea dentro de la caja es la mediana: la mitad de las
observaciones queda a la izquierda y la otra mitad a la derecha. Los bordes de
la caja son $Q_1$ y $Q_3$, así que la caja contiene el 50% central de los
datos. Si la caja es angosta, ese tramo central fue bastante parecido; si es
ancha, hubo más variación entre valores habituales.

Los **bigotes** se extienden desde la caja hasta los valores más extremos que
todavía no se consideran atípicos. Los puntos que quedan afuera se dibujan
separados: no son errores automáticamente, pero sí observaciones que conviene
mirar antes de resumir todo con un único número.

```{code-cell} python
summary_chart_input = DescriptiveSummaryChartInput(
    observations=waiting_times,
    statistics=summary,
    settings=settings,
)
chart_descriptive_summary(summary_chart_input)
```

Un boxplot clásico no suele incluir la media. En este gráfico la agregamos como
línea punteada para compararla visualmente con la mediana y reforzar cómo los
valores extremos pueden mover el promedio.

(sec-descriptive-shape)=
## Forma, sesgo y colas

Para leerlo, hacé tres preguntas. **Centro:** ¿dónde cae la línea de la
mediana? **Dispersión:** ¿qué tan larga es la caja y qué tan lejos llegan los
bigotes? **Asimetría y rarezas:** ¿un bigote es mucho más largo que el otro o
aparecen puntos aislados? En el caso de la clínica, una caja concentrada cerca
de pocos minutos cuenta una mañana regular; una caja ancha o puntos muy lejos
señalan que algunas experiencias fueron bastante distintas.

Cuando una cola se estira más que la otra decimos que la distribución tiene
**sesgo**. Hay **sesgo hacia la derecha** cuando la cola larga apunta a valores
grandes: unos pocos valores altos tiran de la media y suele pasar que
$\bar{x} > \tilde{x}$. Hay **sesgo hacia la izquierda** cuando la cola larga
apunta a valores chicos: unos pocos valores bajos tiran de la media y suele
pasar que $\bar{x} < \tilde{x}$.

### Preguntas para leer formas típicas

Antes de abrir cada respuesta, imaginá el boxplot y traducí su forma a una
frase sobre los datos. En las respuestas usamos los símbolos del glosario:
$\bar{x}$ para la media muestral, $\tilde{x}$ para la mediana muestral y
$\text{IQR}$ para el rango intercuartil. También usamos $s$ para el desvío
estándar muestral y $R$ para el rango muestral.

En estos boxplots horizontales, la **izquierda** corresponde a valores menores
y la **derecha** a valores mayores. Por eso cada pregunta describe no sólo la
forma, sino también hacia qué lado de la escala se ubican los datos.

```{code-cell} python
:tags: [hide-input]

def chart_boxplot_example(values: list[float], title: str):
    observations = pd.DataFrame({"value": values}).pipe(DataFrame[Observations])
    statistics = summarize_observations(observations)
    chart_input = DescriptiveSummaryChartInput(
        observations=observations, statistics=statistics, title=title, settings=settings
    )
    return chart_descriptive_summary(chart_input)
```

**Pregunta 1.** La caja está centrada, la mediana cae casi en el medio y los dos
bigotes tienen longitudes parecidas hacia la izquierda y hacia la derecha. ¿Qué
sugiere sobre la distribución?

```{code-cell} python
:tags: [hide-input]

chart_boxplot_example(
    [2.0, 2.5, 3.0, 3.5, 3.8, 4.0, 4.2, 4.5, 5.0, 5.5, 6.0],
    "Pregunta 1 — boxplot equilibrado",
)
```

::::{admonition} Respuesta
:class: dropdown

Sugiere una distribución bastante equilibrada: no se ve una asimetría fuerte
hacia la izquierda ni hacia la derecha. Los datos habituales se reparten de
manera parecida a ambos lados de la mediana.

Expresión esperada: $\bar{x} \approx \tilde{x}$; la media y la mediana quedan
cerca del mismo punto central.

Dispersión esperada: $s$ no queda inflado por una cola dominante. El rango
siempre cumple $R > \text{IQR}$, pero en una forma equilibrada no esperamos
$R \gg \text{IQR}$.
::::

**Pregunta 2.** La caja tiene un bigote izquierdo muy corto y un bigote derecho
muy largo. ¿Qué implica?

```{code-cell} python
:tags: [hide-input]

chart_boxplot_example(
    [1.0, 1.0, 1.1, 1.2, 1.3, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
    "Pregunta 2 — sesgo hacia la derecha",
)
```

::::{admonition} Respuesta
:class: dropdown

Implica datos sumamente asimétricos hacia la derecha: la mayoría de los valores
queda concentrada en la zona baja o media, pero algunos valores grandes estiran
la cola derecha.

Expresión esperada: $\bar{x} \gg \tilde{x}$; la media queda más a la derecha
que la mediana por el peso de la cola derecha.

Dispersión esperada: la cola derecha aumenta $s$ y estira mucho el rango, así
que $R \gg \text{IQR}$. El $\text{IQR}$ puede seguir siendo moderado porque
describe sólo el 50% central.
::::

**Pregunta 3.** La caja es muy angosta, pero aparecen varios puntos aislados a
la derecha del gráfico. ¿Cómo conviene leerlo?

```{code-cell} python
:tags: [hide-input]

chart_boxplot_example(
    [3.8, 3.9, 4.0, 4.0, 4.1, 4.1, 4.2, 4.2, 4.3, 4.3, 7.0, 8.5, 9.0],
    "Pregunta 3 — caja estable con valores atípicos altos",
)
```

::::{admonition} Respuesta
:class: dropdown

El 50% central de los datos es muy estable, pero hay observaciones atípicas
hacia la derecha que merecen revisión. El proceso habitual parece concentrado;
las rarezas pueden ser errores, casos excepcionales o señales relevantes.

Expresión esperada: $\text{IQR} \ll R$: la dispersión central es chica frente
a la amplitud total. Si los atípicos están a la derecha, también esperamos
$\bar{x} > \tilde{x}$; la media queda a la derecha de la mediana.

Dispersión esperada: $\text{IQR}$ chico, pero $s$ y $R$ grandes por los puntos
aislados. En símbolos del glosario: $\text{IQR} \ll R$.
::::

**Pregunta 4.** Dos grupos tienen medianas parecidas, ubicadas cerca del mismo
valor central. En el grupo A la caja se extiende poco hacia la izquierda
y hacia la derecha; en el grupo B la caja se extiende mucho más hacia ambos
lados. ¿Qué diferencia hay entre los grupos?

```{code-cell} python
:tags: [hide-input]

(
    chart_boxplot_example([3.6, 3.8, 3.9, 4.0, 4.1, 4.2, 4.4], "Grupo A")
    & chart_boxplot_example([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0], "Grupo B")
).resolve_scale(x="shared")
```

::::{admonition} Respuesta
:class: dropdown

Tienen centros parecidos, pero distinta variabilidad. El grupo B tiene valores
habituales más dispersos hacia la izquierda y hacia la derecha: aunque el
centro sea similar, sus observaciones son menos consistentes.

Expresión esperada: $\tilde{x}_A \approx \tilde{x}_B$, pero
$\text{IQR}_A \ll \text{IQR}_B$; los centros quedan cerca del mismo valor, pero
el grupo B se abre más hacia la izquierda y hacia la derecha.

Dispersión esperada: el grupo B tiene más variabilidad en cualquier resumen de
dispersión: $s_A \ll s_B$, $\text{IQR}_A \ll \text{IQR}_B$ y $R_A \ll R_B$.
::::

**Pregunta 5.** La caja tiene un bigote izquierdo muy largo y un bigote derecho
muy corto. ¿Qué lectura harías?

```{code-cell} python
:tags: [hide-input]

chart_boxplot_example(
    [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 6.5, 6.7, 6.8, 6.9, 7.0, 7.0],
    "Pregunta 5 — sesgo hacia la izquierda",
)
```

::::{admonition} Respuesta
:class: dropdown

Sugiere sesgo hacia la izquierda: la mayoría de los valores queda concentrada
en la zona media o alta, pero algunos valores chicos estiran la cola izquierda.

Expresión esperada: $\bar{x} \ll \tilde{x}$; la media queda más a la izquierda
que la mediana por el peso de la cola izquierda.

Dispersión esperada: la cola izquierda aumenta $s$ y estira el rango hacia
valores chicos, así que $R \gg \text{IQR}$. El $\text{IQR}$ resume la zona
central alta, no toda la cola.
::::

(sec-descriptive-tukey)=
## Detección de outliers — la regla de Tukey

Un **outlier** — o dato atípico — es una observación tan alejada del resto
que conviene mirarla aparte: puede ser un error de carga, un caso excepcional
o una señal importante que no queremos esconder dentro del promedio.

Para detectarlos vamos a reutilizar los cuartiles del boxplot. La distancia
entre $Q_1$ y $Q_3$ resume el tramo central de la muestra.

**Paso 1.** Ordenamos los datos y ubicamos $Q_1$ y $Q_3$.

**Paso 2.** Definimos el rango intercuartil:

$$ \text{IQR} = Q_3 - Q_1 $$

**Paso 3.** Una observación es **outlier** si cae fuera del intervalo:

$$ \bigl[Q_1 - 1{,}5\,\text{IQR},\ Q_3 + 1{,}5\,\text{IQR}\bigr] $$ (eq-iqr-fence)

Es la misma regla que define hasta dónde llegan los bigotes del boxplot: por
eso ese gráfico es buen detector visual.

```{code-cell} python
outlier_report = detect_outliers_tukey(waiting_times)
outlier_report
```

(sec-descriptive-zscore)=
## Posición relativa: el $z$-score

El $z$-score (*standard score*) traduce una observación a la pregunta «¿a cuántos desvíos del
promedio está?».

**Paso 1:** partimos de las fórmulas [](#eq-mean) y [](#eq-std) para tener
$\bar{x}$ y $s$.

**Paso 2:** centramos restando el promedio.

**Paso 3:** reescalamos dividiendo por $s$:

$$ z_i = \frac{x_i - \bar{x}}{s} $$ (eq-zscore)

Un $z_i$ positivo dice «este paciente esperó más que el promedio»; un
$z_i$ negativo, «menos que el promedio». Y la magnitud cuenta cuántos
$s$ separan la observación del centro: $z_i = 2$ significa dos desvíos
estándar arriba, sin importar las unidades originales.

En este capítulo usamos $z_i$ solo como resumen descriptivo: compara cada
observación con el promedio del mismo conjunto de datos. Ayuda a ver qué
valores están cerca del centro y cuáles quedan relativamente lejos.

```{code-cell} python
standardized = standardize_observations(waiting_times)
standardized
```

(sec-descriptive-defects)=
## Piezas defectuosas por turno

Ahora salgamos de la sala de espera y crucemos a otro proceso cotidiano. En
una fábrica, al final de cada turno, la supervisora revisa el parte de
inspección: no le importa cuánto tardó cada pieza, sino cuántas salieron
defectuosas. Un turno puede cerrar con 1 pieza defectuosa, otro con 5, otro
con ninguna.

Después de 60 turnos, la pregunta vuelve a sonar conocida: ¿cuál fue un
conteo típico?, ¿qué tan estable fue la línea?, ¿apareció algún turno
suficientemente raro como para revisar qué pasó? Cambiamos de escala y de
unidad — de minutos a piezas defectuosas —, pero seguimos haciendo
estadística descriptiva sobre una lista de observaciones.

```{code-cell} python
rng_factory = np.random.default_rng(seed=20260202)
raw_defect_counts = rng_factory.poisson(lam=3.5, size=60).astype(float)
defect_counts = pd.DataFrame({"value": raw_defect_counts}).pipe(DataFrame[Observations])

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

(sec-descriptive-cv)=
## Comparar dispersión en escalas distintas

Las dos muestras viven en escalas distintas — minutos contra piezas — y con
magnitudes muy distintas. Comparar sus medias en crudo dice poco: 4 minutos
no es ni mejor ni peor que 3 piezas defectuosas. Lo mismo pasa con los desvíos:
un minuto y una pieza defectuosa no comparten unidad.

Cuando la comparación se vuelve incómoda hay que salir de las unidades
originales. Los $z$-scores (*standard scores*), que ya introdujimos, comparan
observaciones dentro de su propia muestra. Para comparar la **dispersión
relativa** de dos procesos usamos el **coeficiente de variación**:

$$ CV = \frac{s}{\bar{x}} $$ (eq-coefficient-variation)

El cociente no tiene unidades: mide qué tan grande es el desvío típico en
relación con la media del mismo proceso. Antes de mirar la tabla, apostá: ¿la
clínica o la fábrica parece más irregular respecto de su propio centro?

```{code-cell} python
cv_comparison = pd.DataFrame({
    "muestra": ["Clínica: minutos", "Fábrica: defectos"],
    "media": [summary.location.mean, defect_summary.location.mean],
    "desvío estándar": [
        summary.dispersion.sample_standard_deviation,
        defect_summary.dispersion.sample_standard_deviation,
    ],
    "coeficiente de variación": [
        summary.dispersion.coefficient_of_variation,
        defect_summary.dispersion.coefficient_of_variation,
    ],
})
cv_comparison
```

La muestra con mayor $CV$ no es necesariamente la que tiene mayor desvío en
unidades originales; es la que varía más **relativo a su propio nivel típico**.
Esa es la comparación justa cuando cambiamos de minutos a piezas.

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

Imaginá dos planes de medición. El primero registra ochenta pacientes el lunes
después de un feriado; el segundo registra veinte pacientes por semana durante
cuatro semanas, mezclando días y horarios. El primer plan puede tener una tabla
impecable, pero representa una situación particular. El segundo suele ser más
útil para decidir turnos porque cubre más partes del proceso.

La independencia también se ve en la historia de recolección. Si una demora
inicial retrasa a todos los pacientes posteriores, las observaciones quedan
encadenadas: cada espera ya no cuenta como una pieza nueva de información del
mismo modo que en una mañana estable. En ese caso el gráfico sigue sirviendo
para describir lo ocurrido, pero no alcanza para inferir cómo funciona el
servicio en general.

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
exercise_sample = pd.DataFrame({"value": [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]}).pipe(
    DataFrame[Observations]
)
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

**Ahora podemos** separar tres mensajes: cómo fue la espera típica, cuán
estable fue el servicio y si algún caso extremo merece revisión.

**Lo que todavía falta** es salir de lo que ya pasó. Una muestra describe un
puñado de mañanas en la clínica o algunos turnos de la línea, pero no asigna por
sí sola chances al próximo paciente o al próximo lote.

**La pregunta que empuja el capítulo siguiente** aparece apenas entra un
paciente nuevo o llega un turno todavía no inspeccionado: ¿qué tan probable es
que espere más de cinco minutos?, ¿cambian las chances si ya lleva tres minutos
sentado?, ¿qué tan creíble es una respuesta «sí» en la encuesta? Para responder
hay que hablar de futuros posibles — un idioma con su propia gramática, la
**probabilidad**.
