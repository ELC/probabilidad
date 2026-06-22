---
title: Tratamiento de datos
kernelspec:
  name: python3
  display_name: Python 3
---

Imaginate sentado en la recepción de una clínica durante toda una
mañana. Cada vez que un paciente entra al consultorio, anotás los
minutos que estuvo esperando: 4, 6, 3, 2, 12, 5, 4, 7, 5… Al final
del turno tenés ochenta números anotados rápidamente en una hoja.

Si alguien te pregunta «¿cuánto se espera, en general?», recitar la
lista entera no sirve. La persona se aburre antes del tercer paciente
y al final tampoco saca una conclusión. Si te preguntan «¿hoy fue un
día tranquilo o uno raro?», directamente no sabés por dónde empezar.

Para contestar hay que apretar la lista en unos pocos gráficos y unos pocos números que
respondan cosas concretas: qué medida resume la espera, qué tan
**parecidas** fueron las esperas entre sí (¿todos esperaron parecido?,
¿algunos muy poco y otros mucho?) y si hubo alguna **fuera de lo
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
> Al final del capítulo vas a poder decidir qué resumen conviene mirar primero,
> qué forma del gráfico cambia la historia y cuándo una muestra no alcanza para
> hablar de todo el servicio.

```{code-cell} python
:tags: [remove-cell, hide-input]
import altair as alt
import numpy as np
import pandas as pd
from pandera.typing import DataFrame

from core import Observations, Settings
from descriptive import (
    ClinicSampleInput,
    detect_outliers_tukey,
    generate_clinic_sample,
    standardize_observations,
    style_display_table,
    summarize_observations,
)
from visualization import (
    BoxplotExampleChartInput,
    BoxplotShapeComparisonChartInput,
    CategoricalBarFromDataChartInput,
    DescriptiveSummaryChartInput,
    DiscreteStickFromDataChartInput,
    FrequencyPolygonChartInput,
    HistogramChartInput,
    ParetoFromDataChartInput,
    StemLeafChartInput,
    chart_boxplot_example,
    chart_boxplot_shape_comparison,
    chart_categorical_bars_from_data,
    chart_cumulative_frequency_polygon,
    apply_theme,
    chart_descriptive_summary,
    chart_discrete_sticks_from_data,
    chart_histogram,
    chart_histogram_with_frequency_polygon,
    chart_pareto_from_data,
    chart_stem_leaf,
)
from widgets import (
    DescriptiveExplorerInput,
    IntervalWidthExplorerInput,
    SummaryEvolutionExplorerInput,
    build_descriptive_explorer,
    build_iqr_evolution_explorer,
    build_interval_width_explorer,
    build_location_evolution_explorer,
    build_mean_evolution_explorer,
    build_median_evolution_explorer,
    build_mode_evolution_explorer,
    build_range_evolution_explorer,
    build_standard_deviation_evolution_explorer,
)
```

```{code-cell} python
:tags: [remove-cell, hide-input]
settings = Settings()
```

(sec-descriptive-foundations)=
## Estadística en ingeniería: procesos, variabilidad y riesgo

En la sala de espera de la clínica, el proceso no está quieto. Un paciente puede
esperar cuatro minutos y el siguiente doce; una mañana puede fluir sin demoras y otra
puede trabarse por unos pocos casos largos. Esa variabilidad genera incertidumbre:
antes de medir, no sabemos con exactitud qué valor tomará la característica de
interés en el próximo paciente.

Un **proceso** es una secuencia de etapas que transforma una **entrada** en una
**salida**. En la clínica entran pacientes, se ordenan turnos, se asignan recursos y
sale una atención después de cierta espera. En el camino actúan factores que cambian:
demanda, horario, disponibilidad de personal, urgencias, duración de consultas. La
estadística aporta herramientas para plantear el problema, recolectar datos,
organizarlos, resumirlos y decidir con riesgo controlado.

Antes de calcular cualquier resumen hay que formular el problema con precisión. En
la clínica, Lucía no quiere resumir "datos" en abstracto: quiere saber qué pasó con
las esperas sobre las que debe decidir.

Si la decisión es cerrar el informe de la mañana, el universo relevante son los
pacientes atendidos durante ese turno. Si la decisión es rediseñar horarios para todo
el mes, el universo relevante se agranda: son las esperas de todos los días y horarios
que el nuevo esquema debería cubrir. A ese universo de unidades sobre el que
queremos concluir o decidir lo llamamos **población**. Según cómo se formule el
problema, la población de la clínica puede ser finita —por ejemplo, los pacientes
atendidos esta mañana, con tamaño $N$— o infinita/indeterminada —por ejemplo, todas
las esperas que podrían observarse mientras el servicio funcione bajo condiciones
estables—.

Después hay que decir qué cuenta como una observación individual. En esta historia,
puede ser cada paciente atendido o cada espera registrada, según cómo se haya
definido la pregunta. A cada elemento de la población lo llamamos **unidad
elemental** o **unidad de análisis**.

Sobre cada unidad observamos una característica. Para Lucía, la característica central
es el tiempo de espera, pero sobre el mismo paciente también podría observar la hora
de llegada, el tipo de consulta, si tenía turno previo, la cantidad de personas que
esperaban antes o si terminó derivado a otra área. En general, cada característica que
puede cambiar de una unidad a otra se llama **variable** y se simboliza con una letra
mayúscula, por ejemplo $X$: tiempo de espera. Un valor observado se escribe en
minúscula, por ejemplo $x = 4{,}2$ minutos.

En la práctica, muchas veces no observamos toda la población. Observamos una parte:
por ejemplo, las 80 esperas anotadas durante una mañana. A esa parte observada la
llamamos **muestra**, y su tamaño se simboliza con $n$.

La notación cambia según si resumimos toda la población o sólo esa muestra:

- Si Lucía tuviera **todas** las esperas de la población que le importa, el resumen
  sería un **parámetro**. Usamos letras griegas: $\mu$ para la media poblacional,
  $\sigma$ para el desvío estándar poblacional, $\sigma^2$ para la varianza
  poblacional y $\pi$ para una proporción poblacional.
- Si Lucía tiene sólo **una muestra**, el resumen es un **estadístico**. Usamos otra
  notación: $\bar{x}$ para la media muestral, $s$ para el desvío estándar muestral y
  una proporción muestral cuando resumimos respuestas de tipo sí/no.

La misma colección física puede definir poblaciones distintas según el objetivo. Si
Lucía decide sobre la mañana que acaba de terminar, la población puede ser esa
mañana. Si decide turnos para todo el mes, la población son las esperas de todos los
días y horarios relevantes del servicio.

(sec-descriptive-sample)=
## Una muestra de tiempos de espera

Trabajemos con un caso concreto: los 80 minutos de espera que la
enfermera de turno fue anotando paciente a paciente, ordenados en la
secuencia en que llegaron a la guardia.

```{code-cell} python
:tags: [hide-input]
clinic_sample = generate_clinic_sample(ClinicSampleInput(settings=settings, sample_size=80))
summary = summarize_observations(clinic_sample.waiting_times)
style_display_table(clinic_sample.clinic_display_table.head())
```

A partir de esos 80 tiempos vamos a construir un resumen estadístico — guardado en
el objeto `summary` — al que iremos volviendo a lo largo del capítulo. Cada sección
agrega un significado a una de sus filas; al final lo leeremos completo como una
sola tabla de cierre.

```{code-cell} python
:tags: [hide-input]
summary
```

(sec-descriptive-variable-types)=
## Antes de agrupar: qué tipo de variable tenemos

Antes de elegir una tabla o un gráfico hay que nombrar qué característica estamos
observando en cada unidad. Las herramientas cambian según el tipo de variable: no
se organiza igual una categoría, un conteo o una medición.

| Tipo de variable | Qué valores puede tomar | Ejemplos | Presentación usual |
|---|---|---|---|
| **Cualitativa** o **atributo** | Categorías o niveles | tipo de consulta, área de atención, prioridad asignada | tabla de frecuencias, barras, Pareto |
| **Cuantitativa discreta** | Valores contables, finitos o numerables | personas esperando al llegar, reprogramaciones, llamados previos | tabla por valores exactos, gráfico de bastones |
| **Cuantitativa continua** | Intervalos de números reales | tiempo de espera, duración de la consulta, hora de llegada | tallo-hoja, intervalos de clase, histograma |

Con esa clasificación, los minutos de espera de la clínica son una variable
cuantitativa continua: se miden sobre una escala de tiempo y podrían tomar valores
intermedios, como 4,5 minutos o 4,52 minutos si el registro fuera más preciso.

**Punto de control.** Antes de elegir un gráfico, formulá la variable en una
frase: “en cada unidad voy a observar...”. Si la respuesta es una categoría,
contás clases; si es un conteo, respetás valores enteros; si es una medición,
pensás en intervalos.

Un mismo contexto puede producir variables de tipos distintos. En la clínica, por
ejemplo, cada unidad elemental puede ser un paciente atendido durante la mañana.
Según la pregunta, cambia la variable:

| Pregunta sobre cada paciente | Variable | Tipo |
|---|---|---|
| ¿A qué área fue derivado? | guardia, laboratorio, clínica médica | cualitativa |
| ¿Tenía turno previo? | sí/no | cualitativa |
| ¿Qué nivel de prioridad recibió? | baja, media, alta | cualitativa |
| ¿Cuántas personas tenía adelante al llegar? | número de personas | cuantitativa discreta |
| ¿Cuántas veces fue reprogramado? | número de reprogramaciones | cuantitativa discreta |
| ¿Cuántos minutos esperó? | tiempo de espera | cuantitativa continua |
| ¿Cuánto duró la consulta? | duración de la consulta | cuantitativa continua |

La población no alcanza para decidir la herramienta: también importa qué
característica observamos en cada unidad.

(sec-descriptive-attributes)=
### Atributos: clases, porcentajes y Pareto

Cuando la variable es cualitativa, cada categoría define una **clase**. La tabla
cuenta cuántas unidades caen en cada clase y qué proporción representan:

$$
f_k = \frac{n_k}{n}
$$ (eq-relative-frequency)

$$
\sum_k n_k = n
$$ (eq-absolute-frequency-total)

$$
\sum_k f_k = 1
$$ (eq-relative-frequency-total)

El subíndice $k$ identifica una clase concreta de la tabla: por ejemplo, una fila
puede corresponder a "Guardia" y otra a "Pediatría". Así, $n_k$ es la cantidad
observada en esa clase y $f_k$ es su proporción sobre el total.

En la clínica, una tabla por área de atención podría leerse así:

```{code-cell} python
:tags: [hide-input]
style_display_table(clinic_sample.area_display_table)
```

La frecuencia relativa suele expresarse como porcentaje: una proporción de
$0{,}25$, por ejemplo, equivale al 25% de la muestra. Para variables cualitativas
conviene usar **gráficos de barras**, porque facilitan la comparación visual entre
categorías y partes del total. Aunque los gráficos de torta o de sectores son muy
usados, hay estudios y guías de visualización que recomiendan evitarlos cuando el
objetivo es comparar magnitudes con precisión [@few2007visual].

```{code-cell} python
:tags: [hide-input]
chart_categorical_bars_from_data(
    CategoricalBarFromDataChartInput(
        data=clinic_sample.clinic_data,
        category_column="area",
        category_order=clinic_sample.area_categories,
        title="Pacientes por área de atención",
        category_title="Área de atención",
        settings=settings,
    )
)
```

Si ordenamos las barras de mayor a menor frecuencia y sumamos el porcentaje
acumulado, aparece rápido si unas pocas causas explican gran parte de las demoras.
Ese gráfico de barras ordenadas, pensado para priorizar dónde intervenir primero,
se llama **diagrama de Pareto**.

Si Lucía registra el motivo principal de demora en cada atención, algunas filas
pueden quedar como "Ninguna". Para priorizar intervenciones, esa categoría se
separa y el Pareto se construye sólo con las atenciones que sí tuvieron una causa
de demora identificable. Así empieza por las causas más frecuentes, no por las más
raras:

```{code-cell} python
:tags: [hide-input]
style_display_table(clinic_sample.delay_reason_display_table)
```

```{code-cell} python
:tags: [hide-input]
chart_pareto_from_data(
    ParetoFromDataChartInput(
        data=clinic_sample.clinic_data,
        category_column="delay_reason",
        category_order=clinic_sample.delay_reason_categories,
        exclude_categories=("Ninguna",),
        title="Motivos de demora: diagrama de Pareto",
        category_title="Motivo principal",
        settings=settings,
    )
)
```

La pregunta operativa no es sólo "cuál barra es más alta", sino dónde conviene
intervenir primero para reducir más esperas largas con menos acciones.

La línea que sube sobre las barras es una **ojiva**: muestra el porcentaje
acumulado a medida que agregamos causas en orden de importancia. Esa lectura dice,
por ejemplo, cuánta demora queda explicada si Lucía atiende primero las dos o tres
causas principales. En términos operativos, da la información necesaria para hacer
un **triage**: separar lo urgente y más frecuente de lo menos prioritario.

(sec-descriptive-discrete-frequency)=
### Variables discretas: valores exactos y acumulados

Si la variable cuantitativa es discreta, la tabla se arma por cada valor observado
$x_k$. Además de $n_k$ y $f_k$, aparecen dos columnas acumuladas:

$$
N_k = \sum_{r \le k} n_r
$$ (eq-cumulative-absolute-frequency)

$$
F_k = \sum_{r \le k} f_r
$$ (eq-cumulative-relative-frequency)

$N_k$ cuenta cuántas observaciones tienen valores menores o iguales que $x_k$;
$F_k$ da la proporción acumulada. En la clínica, si registramos cuántas personas
tenía cada paciente por delante al llegar, una parte de la tabla podría verse así:

```{code-cell} python
:tags: [hide-input]
style_display_table(clinic_sample.people_ahead_display_table)
```

La fila de $3$ tiene dos lecturas distintas: $f_k$ dice qué proporción de
pacientes tenía exactamente tres personas adelante, y $F_k$ dice qué proporción
tenía tres personas o menos.

La frecuencia relativa acumulada también permite hablar de **puntos de corte**.
Un **percentil** indica el valor hasta el cual se acumula cierto porcentaje de
la muestra: el percentil 25 es el menor valor cuya frecuencia acumulada alcanza
al menos el 25%. Los **deciles** son percentiles definidos en múltiplos de 10%:
$D_1$ alcanza al menos el 10%, $D_2$ al menos el 20%, y así sucesivamente. Los
**cuartiles** son percentiles definidos en múltiplos de 25%: $Q_1$ alcanza al
menos el 25%, $Q_2$ al menos el 50% y $Q_3$ al menos el 75%. El gráfico natural para estos datos es el **gráfico
de bastones**: una barra angosta para cada valor posible, con altura proporcional
a su frecuencia.

```{code-cell} python
:tags: [hide-input]
chart_discrete_sticks_from_data(
    DiscreteStickFromDataChartInput(
        data=clinic_sample.clinic_data,
        value_column="people_ahead",
        exact_values=clinic_sample.people_ahead_values,
        title="Personas esperando antes del paciente",
        value_title="Personas esperando antes",
        settings=settings,
    )
)
```

El gráfico de bastones se parece al gráfico de barras porque en ambos la altura
representa frecuencia. La diferencia está en el significado del eje horizontal:
en barras comparamos categorías separadas, como áreas de atención; en bastones
marcamos valores numéricos exactos de una variable discreta. Por eso el eje
horizontal de un gráfico de bastones debe respetar el orden numérico: $0, 1, 2,
\dots$. Además, puede haber valores sin observaciones, y ese espacio vacío también
informa. En un gráfico de barras no existe un "valor numérico faltante" entre
categorías: reordenar las barras puede ayudar a comparar sin cambiar el significado.
En un gráfico de bastones, en cambio, reordenar las barras angostas puede confundir,
porque el lector espera que el eje avance en orden ascendente.

(sec-descriptive-frequency)=
### Variables continuas: intervalos, tallo-hoja e histogramas

En variables continuas casi nunca conviene contar cada valor exacto. Primero se
puede usar un **diagrama de tallo y hoja**, que conserva los datos individuales pero
los ordena visualmente: si un paciente esperó 4,7 minutos, por ejemplo, el tallo
puede ser 4 y la hoja 7. Es útil en conjuntos pequeños o medianos porque muestra
la forma sin destruir del todo la lista original.

```{code-cell} python
:tags: [hide-input]
chart_stem_leaf(
    StemLeafChartInput(
        observations=clinic_sample.waiting_times,
        title="Tiempos de espera: diagrama de tallo y hoja",
        settings=settings,
    )
)
```

Para una tabla de frecuencias continua se particiona el rango observado en
**intervalos de clase**. Conviene que tengan amplitud similar y que cada dato caiga
en uno y sólo un intervalo; por eso se usan intervalos semiabiertos, como
$(2, 3]$. El **punto medio** de una clase representa al intervalo cuando hacemos
cálculos con datos agrupados.

Elegir la cantidad de intervalos es parte del análisis. Demasiados intervalos dejan
muchas frecuencias pequeñas o nulas; demasiado pocos condensan tanto que ocultan
la forma. Como regla práctica, suelen usarse entre 5 y 20 clases, ajustando según la
cantidad de datos y el objetivo.

En un histograma, la base de cada barra es la amplitud del intervalo y el área de la
barra debe ser proporcional a la frecuencia. Si todas las amplitudes son iguales, la
altura también queda proporcional a la frecuencia; si no lo son, hay que ajustar las
alturas. Al pasar de datos originales a intervalos se pierde información, pero se gana
legibilidad. En muestras pequeñas, cambiar el ancho de clase puede cambiar bastante
la apariencia del histograma. A diferencia del gráfico de bastones, las barras de
un histograma no llevan espacios entre sí: si aparece un hueco, se lee como un
intervalo sin observaciones. En los bastones, en cambio, el espacio entre valores
exactos no representa una probabilidad intermedia.

**Antes de mirar.** Si la mañana fue razonablemente estable, ¿esperás ver muchas
esperas cerca de un valor central o una cola larga de casos lentos? Hacé una
predicción rápida: dónde se va a concentrar el histograma y en qué minuto creés
que la ojiva va a cruzar el 70%.

```{code-cell} python
:tags: [hide-input]
chart_histogram_with_frequency_polygon(
    FrequencyPolygonChartInput(
        frequency_table=clinic_sample.frequency_table,
        title="Tiempos de espera: histograma y polígono de frecuencias",
        settings=settings,
    )
)
```

El **polígono de frecuencias** une los puntos medios superiores de las barras del
histograma. No agrega datos nuevos: traza una línea sobre la misma tabla para leer
mejor la forma general, especialmente si queremos comparar centros, colas o
asimetrías.

```{code-cell} python
:tags: [hide-input]
chart_cumulative_frequency_polygon(
    FrequencyPolygonChartInput(
        frequency_table=clinic_sample.frequency_table,
        title="Tiempos de espera: frecuencias acumuladas y ojiva",
        settings=settings,
    )
)
```

El **polígono de frecuencias acumuladas** une las frecuencias acumuladas. Cuando
esos puntos se ubican en los límites superiores de los intervalos, esa línea es la
**ojiva**: permite leer qué proporción quedó por debajo de un corte dado, como
cinco minutos de espera.

El siguiente control mantiene fijos los mismos 80 tiempos y sólo cambia el ancho
del intervalo. Mirá primero cómo se mueve el histograma de la izquierda: algunas
barras suben, bajan o desaparecen según dónde caigan los cortes. Después mirá la
curva acumulada de la derecha. Aunque también cambia, suele variar menos y conserva
mejor la lectura operativa: qué proporción de pacientes quedó por debajo de cada
tiempo de espera.

```{code-cell} python
:tags: [hide-input]
build_interval_width_explorer(
    IntervalWidthExplorerInput(
        observations=clinic_sample.waiting_times,
        settings=settings,
    )
)
```

En la clínica, si agrupamos los 80 tiempos de espera en intervalos de un minuto,
podríamos obtener una tabla como esta:

```{code-cell} python
:tags: [hide-input]
style_display_table(clinic_sample.frequency_display_table)
```

Cada fila dice dos cosas a la vez: $f_k$ cuenta qué proporción cae dentro de ese
intervalo, y $F_k$ acumula todo lo que queda por debajo de su límite superior. El
punto medio representa a todo el intervalo cuando hacemos cuentas con datos
agrupados; por eso agrupamos para leer mejor, pero aceptamos perder el detalle de
cada espera individual.

Si $n_j$ es la cantidad de observaciones en el intervalo $j$ y $n$ el tamaño total,
la frecuencia relativa de intervalos se calcula como en [](#eq-relative-frequency):
casos de la clase dividido el total. La acumulada se lee con la misma lógica de
[](#eq-cumulative-relative-frequency), pero recorriendo intervalos en lugar de
valores exactos.

Para Lucía, la pregunta operativa puede ser "¿qué porcentaje esperó menos de cinco
minutos?". Esa lectura sale de la distribución acumulada: no mira sólo una barra,
sino todo lo que quedó por debajo del corte que importa para decidir.

(sec-descriptive-time-order)=
### Cuando el tiempo importa

Si las observaciones se registran en el orden en que ocurren, el tiempo puede ser una
fuente central de variabilidad. Una **gráfica de serie de tiempo** pone el valor
observado en el eje vertical y el tiempo en el eje horizontal. Antes de colapsar datos
en una tabla de frecuencias, conviene mirar si aparecen tendencias, ciclos o cambios
de régimen. Si hay un patrón temporal fuerte, analizar frecuencias como si todos los
datos hubieran ocurrido bajo las mismas condiciones puede llevar a conclusiones
engañosas.

En la clínica, esa advertencia tiene una forma concreta: las esperas pueden crecer
hacia el mediodía, caer después de que se libera un consultorio o concentrarse justo
después de una llegada simultánea de pacientes. Si mezclamos todo en una sola tabla
sin mirar el orden temporal, una tendencia o un ciclo puede quedar escondido.

(sec-descriptive-summary)=
## Tres preguntas que resumen la muestra

Volvamos a las tres preguntas que dejó abiertas la introducción: qué medida
resume la espera, qué tan parecidas fueron las esperas entre sí, y si hubo
alguna fuera de lo común. Cada pregunta se contesta con un número distinto, y
vamos a definir uno por uno.

(sec-descriptive-mean)=
### Una medida resumen: el promedio

A los números que condensan una muestra en una lectura breve también los
llamamos **medidas resumen**. La primera candidata es el **promedio**: sumar
todos los minutos y dividir por la cantidad de pacientes. En estadística al
promedio se lo llama **media muestral** y se lo escribe $\bar{x}$ (una equis
con una rayita arriba — es solo una convención). Si anotamos los minutos del
paciente $1$ al paciente $n$ como $x_1, x_2, \dots, x_n$, la fórmula que hace
lo que recién dijimos en palabras es:

$$ \bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i $$ (eq-mean)

El símbolo $\sum$ es solo «sumá todos estos términos», y $x_i$ es el
tiempo del paciente número $i$. El subíndice $i$ recorre los valores
$1, 2, \dots, n$ — así que la fórmula dice exactamente lo mismo que
«sumalos a todos y dividí por la cantidad».

Si los datos ya están agrupados en $r$ clases, usamos el valor de la clase $x_k$
— el valor exacto en datos discretos o el punto medio del intervalo en datos
continuos — y su frecuencia. Como $f_k$ es la frecuencia relativa definida en
[](#eq-relative-frequency), podemos escribir:

$$
\bar{x} = \frac{1}{n}\sum_{k=1}^{r} x_k n_k
$$ (eq-grouped-mean-absolute)

$$
\bar{x} = \sum_{k=1}^{r} x_k \frac{n_k}{n}
$$ (eq-grouped-mean-relative-ratio)

$$
\bar{x} = \sum_{k=1}^{r} x_k f_k
$$ (eq-grouped-mean)

Si el conjunto observado es toda la población, el promedio es un parámetro y se
escribe $\mu$. La media no tiene por qué coincidir con un valor observado: puede
dar 4,36 minutos aunque ningún paciente haya esperado exactamente 4,36 minutos. Como
usa toda la información, también es sensible a valores extremos. Por eso sirve para
comparar distribuciones sólo cuando sus formas son razonablemente semejantes.

**Predicción.** Antes de tocar el control, imaginá qué va a pasar si agregás un
valor extremo, por ejemplo 20 minutos: ¿el promedio se va a mover apenas o va a
saltar? Después agregalo y compará el salto con lo que pasa cuando agregás valores
aleatorios parecidos al resto de la muestra.

```{code-cell} python
:tags: [hide-input]
build_mean_evolution_explorer(
    SummaryEvolutionExplorerInput(
        observations=clinic_sample.waiting_times,
        settings=settings,
    )
)
```

La media que usamos acá es la **media aritmética**. Existen otras medias útiles,
pero responden a preguntas distintas. La **media geométrica** se usa cuando el
fenómeno se compone multiplicando cambios relativos: por ejemplo, si Lucía compara
mejoras porcentuales sucesivas en el tiempo de espera promedio después de varios
ajustes de agenda, la mejora típica no debería promediarse sumando porcentajes sin
más. La **media armónica** se usa para promediar tasas cuando el denominador común
es fijo: por ejemplo, si se comparan ritmos de atención medidos en pacientes por
hora en franjas de igual duración, puede describir mejor el ritmo típico que una
media aritmética simple de tasas. En este libro vamos a trabajar con la media
aritmética; elegir y calcular otras medias queda fuera de alcance.

(sec-descriptive-mode)=
### El valor más frecuente: la moda

Otra medida de posición es la **moda**, escrita $\hat{x}$: el valor o categoría con
mayor frecuencia. En la clínica puede ser el minuto de espera que más se repite, el
área de atención más frecuente o el motivo de demora que aparece más veces.

La moda tiene tres detalles importantes. Algunas muestras no tienen moda clara;
otras tienen dos modas y se llaman **bimodales**; y es la única medida de tendencia
central que puede calcularse para cualquier tipo de variable, incluso cualitativa.
En el control siguiente, para que la idea tenga sentido con tiempos continuos,
la moda se calcula sobre minutos redondeados.

**Predicción.** Antes de agregar un valor extremo, pensá si alcanza con una sola
observación para cambiar la moda. Después probá agregar un valor escrito y varios
valores aleatorios.

```{code-cell} python
:tags: [hide-input]
build_mode_evolution_explorer(
    SummaryEvolutionExplorerInput(
        observations=clinic_sample.waiting_times,
        settings=settings,
    )
)
```

(sec-descriptive-position)=
### Posición dentro de la muestra: percentiles, deciles y cuartiles

Además de resumir con un único centro, a Lucía le interesa ubicar cortes dentro
de la lista ordenada. Si pregunta «¿hasta qué minuto esperó el 75% de los
pacientes?», no busca el promedio: busca un **percentil**.

Un percentil $p$ es un valor que deja aproximadamente el $p\%$ de las
observaciones por debajo. Los **deciles** hacen cortes cada 10%: $D_1$ deja
cerca del 10%, $D_2$ cerca del 20%, y así sucesivamente. Los **cuartiles** hacen
cortes cada 25%: $Q_1$ deja cerca del 25%, $Q_2$ deja cerca del 50% y $Q_3$ deja
cerca del 75%.

Más formalmente, estos cortes son mínimos valores que acumulan al menos cierto
porcentaje de observaciones ordenadas. El segundo cuartil coincide con el
percentil 50:

$$ Q_2 = P_{50} $$ (eq-second-quartile)

Con una tabla de frecuencias acumuladas, se buscan mirando la primera fila cuya
acumulada alcanza el porcentaje pedido.

```{code-cell} python
:tags: [hide-input]
position_summary = pd.DataFrame({
    "corte": ["mínimo", "Q1", "P50 / Q2", "Q3", "máximo"],
    "minutos": [
        summary.location.minimum,
        summary.location.first_quartile,
        summary.location.median,
        summary.location.third_quartile,
        summary.location.maximum,
    ],
})
style_display_table(position_summary)
```

Antes de leer la tabla, pensá en la ojiva: $Q_1$, $P_{50}$ y $Q_3$ son puntos
sobre esa curva acumulada. Si $Q_3$ queda cerca del corte central, la mayor
parte de la mañana fue compacta; si queda lejos, el tramo alto de esperas se
estiró.

(sec-descriptive-median-definition)=
### Otra medida resumen: la mediana

El promedio tiene un punto débil. Si entre los 80 pacientes hubo uno
que esperó dos horas porque al médico se le complicó un caso, ese
único valor extremo arrastra el promedio hacia arriba aunque el
resto de la mañana haya sido normal. Para esos casos viene bien otro
tipo de medida resumen: la **mediana**, que es el número del medio cuando
ordenamos la lista de menor a mayor. La escribimos $\tilde{x}$ (equis
con una eñe encima):

Para escribirla con fórmula, primero **ordenamos** la lista de menor a mayor y
le ponemos un nombre nuevo a esos valores ordenados: $x_{[1]} \le x_{[2]} \le
\dots \le x_{[n]}$. Los corchetes recuerdan que ese subíndice indica posición en
la lista ordenada, no el orden en que llegaron los pacientes. Con esa notación:

$$ \tilde{x} = \begin{cases}
  x_{[(n+1)/2]} & \text{si } n \text{ es impar} \\
  \dfrac{x_{[n/2]} + x_{[n/2 + 1]}}{2} & \text{si } n \text{ es par}
\end{cases} $$ (eq-position)

Si la cantidad de observaciones es par no hay un único «valor del medio», así
que se promedian los dos centrales.

Formalmente, la mediana es el mínimo valor que acumula al menos el 50% de las
observaciones ordenadas. Con la notación anterior, es el percentil 50 y también
el segundo cuartil:

$$ \tilde{x} = P_{50} = Q_2 $$ (eq-median-percentile)

Por eso, cuando tenemos una tabla de frecuencias, puede leerse mirando la primera
fila cuya frecuencia relativa acumulada alcanza o supera 0,50.

**Predicción.** Antes de usar el control, anticipá si una espera extrema debería
mover la mediana tanto como movía el promedio. Probá con 20 minutos y mirá la
evolución.

```{code-cell} python
:tags: [hide-input]
build_median_evolution_explorer(
    SummaryEvolutionExplorerInput(
        observations=clinic_sample.waiting_times,
        settings=settings,
    )
)
```

**No confundas.** La media pregunta por el equilibrio numérico de todos los
valores; la mediana pregunta por la posición que parte la muestra; la moda
pregunta qué valor o categoría aparece más. Las tres pueden coincidir, pero no
cuentan la misma historia. De hecho, cuando no coinciden, esa diferencia aporta
información importante sobre la simetría de los datos: si la media queda bastante
separada de la mediana, suele haber una cola o valores extremos tirando del
equilibrio numérico.

(sec-descriptive-standard-deviation)=
### Qué tan parecidas son las esperas: el desvío estándar

Saber el promedio no alcanza: necesitamos también qué tan **parecidas**
fueron las esperas entre sí. Si todos esperaron alrededor de cuatro
minutos, el promedio cuenta casi toda la historia. Si la mitad esperó
dos minutos y la otra mitad seis, el mismo promedio esconde dos
experiencias muy distintas.

Las medidas de dispersión resumen distancia, amplitud o variabilidad. A
diferencia de las medidas de posición, son siempre no negativas: no existe una
variación de $-2$ minutos. En todos los casos, el valor $0$ significa que los
datos están concentrados en un único valor.

La idea es medir, en promedio, cuánto se aleja cada paciente del
promedio general. Lo armamos en tres pasos.

**Paso 1.** Calculamos $\bar{x}$ con la fórmula [](#eq-mean) para tener el
punto de referencia.

**Paso 2.** Para cada paciente miramos cuánto se desvió del promedio
($x_i - \bar{x}$). Algunas diferencias son positivas (esperaron más),
otras negativas (esperaron menos), y al sumarlas directamente los valores
positivos y negativos pueden compensarse hasta dar cero, aunque haya
variación real. Para evitarlo necesitamos transformar cada desvío en un
número no negativo. Elevar al cuadrado es una forma sencilla de lograrlo:
convierte todos los desvíos en cantidades positivas o nulas antes de
sumarlas.[^squared-deviations] A esa suma la llamamos **suma de cuadrados**
y la escribimos $\text{SS}$ (por *sum of squares*):

$$ \text{SS} = \sum_{i=1}^{n}(x_i - \bar{x})^2 $$

[^squared-deviations]: Otra opción sería usar valores absolutos, como
    $|x_i-\bar{x}|$. El cuadrado se usa con frecuencia porque es una función
    suave y diferenciable, lo que facilita buscar mínimos y derivar
    propiedades algebraicas; además penaliza más los desvíos grandes.

**Paso 3.** Dividimos esa suma por $n-1$. Ese cociente es la **varianza
muestral**:

$$ s^2 = \frac{\text{SS}}{n - 1} $$ (eq-sample-variance)

Con datos agrupados, la misma idea usa la frecuencia de cada clase:

$$ s^2 = \frac{1}{n - 1}\sum_{k=1}^{r} n_k(x_k - \bar{x})^2 $$ (eq-grouped-variance)

El divisor $n-1$ aparece porque usamos los mismos datos para estimar
$\bar{x}$: una vez fijado el promedio, el último desvío ya queda determinado
por los anteriores. No es un detalle cosmético; evita que la dispersión
muestral quede sistemáticamente demasiado chica cuando usamos la muestra para
hablar de un proceso más amplio.[^bessel-correction]

[^bessel-correction]: La corrección de Bessel compensa que $\bar{x}$ se eligió
    a partir de la misma muestra y, en general, no coincide exactamente con la
    media poblacional $\mu$. Como $\bar{x}$ queda atraída hacia los valores
    observados, las distancias $x_i-\bar{x}$ suelen ser menores que las
    distancias que mediríamos contra $\mu$: les falta parte de la distancia
    entre $\bar{x}$ y $\mu$. Al elevar esas diferencias al cuadrado, esa reducción
    también se cuadratiza; por eso $\sum_i(x_i-\bar{x})^2/n$ tiende a subestimar
    la varianza poblacional $\sigma^2$. Dividir por $n-1$ corrige ese sesgo en
    promedio y refleja que, una vez fijada la media muestral, queda un grado de
    libertad menos. Para una explicación visual introductoria, ver
    [@sampleVarianceNMinusOneSimple]; para una explicación desde el álgebra lineal, ver
    [@sampleVarianceNMinusOneAdvanced].

La varianza tiene un problema práctico: como elevamos los desvíos al cuadrado,
también deja las unidades al cuadrado. En este caso hablaríamos de minutos
cuadrados, una unidad difícil de interpretar como espera. Para volver a las
unidades originales (minutos, no minutos al cuadrado), tomamos raíz cuadrada. Lo
que sale es el **desvío estándar muestral**, que escribimos $s$:

$$
s = \sqrt{s^2}
$$ (eq-std)

Como $s^2$ es la varianza muestral definida en [](#eq-sample-variance), también
podemos escribir:

$$
s = \sqrt{\frac{\text{SS}}{n - 1}}
$$ (eq-std-ss)

En palabras: $s$ es la distancia típica entre una observación
cualquiera y el promedio. Cuanto más chico es $s$, más parecidas son
las esperas entre sí.

**Predicción.** Agregá mentalmente un valor extremo: si entra una espera de 20
minutos, ¿el desvío estándar va a moverse poco o mucho? Usá el control para
compararlo con valores aleatorios cercanos al resto de la muestra.

```{code-cell} python
:tags: [hide-input]
build_standard_deviation_evolution_explorer(
    SummaryEvolutionExplorerInput(
        observations=clinic_sample.waiting_times,
        settings=settings,
    )
)
```

Si los datos corresponden a toda la población, usamos la media poblacional $\mu$,
el tamaño poblacional $N$ y el denominador $N$. La varianza poblacional se
escribe $\sigma^2$ y el desvío estándar poblacional se escribe $\sigma$:

$$
\sigma^2 = \frac{1}{N}\sum_{i=1}^{N}(x_i - \mu)^2
$$ (eq-population-variance)

$$
\sigma = \sqrt{\sigma^2}
$$ (eq-population-std)

Otra medida de dispersión, más simple y más sensible a extremos, es el
**rango**. Si miramos la observación más chica y la más grande de la muestra,
el rango muestral es $R = \max_i x_i - \min_i x_i$. Resume la amplitud total
observada: cuánto separa al caso más bajo del caso más alto. A diferencia de
$s$, que usa todas las observaciones, $R$ depende sólo de los dos extremos; por
eso crece mucho cuando aparece un valor atípico.

```{code-cell} python
:tags: [hide-input]
build_range_evolution_explorer(
    SummaryEvolutionExplorerInput(
        observations=clinic_sample.waiting_times,
        settings=settings,
    )
)
```

Como vimos al hablar de frecuencias acumuladas, $Q_1$ y $Q_3$ son los cuartiles
cuya frecuencia acumulada alcanza al menos el 25% y el 75%, respectivamente. El **rango
intercuartil** o **recorrido intercuartílico** resume la variación del 50%
central:

$$ \text{IQR} = Q_3 - Q_1 $$ (eq-iqr)

Como usa cuartiles, no cambia demasiado por un único valor extremo. Si las medidas
de dispersión son altas decimos que el conjunto es heterogéneo o muy variable. La
varianza queda en unidades al cuadrado y por eso se usa mucho para propiedades
matemáticas; el desvío estándar vuelve a la unidad original y suele ser más fácil de
interpretar en contexto.

```{code-cell} python
:tags: [hide-input]
build_iqr_evolution_explorer(
    SummaryEvolutionExplorerInput(
        observations=clinic_sample.waiting_times,
        settings=settings,
    )
)
```

```{code-cell} python
:tags: [hide-input]
summary
```

La tabla de arriba contesta las tres preguntas a la vez. La **media**
y la **mediana** dan dos formas distintas de resumir la espera; el
**desvío estándar** y el **rango** dicen qué tan parecidas
fueron las esperas entre sí, pero con sensibilidades distintas. Por ahora,
concentrémonos en esas filas: más
adelante vamos a construir una regla para separar lo habitual de lo
raro. Pasá la vista por la tabla y fijate qué te dice cada número antes
de seguir.

**Trampa común.** Una única medida resumen no decide si la operación
funcionó bien. Dos mañanas pueden tener la misma media y experiencias
muy distintas si una fue estable y la otra alternó esperas mínimas con
esperas extremas.

**Decisión de ingeniería.** Antes de seguir, elegí qué mirarías si
tuvieras que justificar una acción: ¿la media para estimar capacidad,
la mediana como medida resumen más resistente, o la dispersión para medir
estabilidad?

**Idea para retener.** La medida resumen cuenta una historia central; la
dispersión y los atípicos dicen cuánta confianza merece esa historia.

(sec-descriptive-median)=
## Por qué la mediana resiste lo que la media no

Cuando la distribución es **simétrica**, $\bar{x}$ y $\tilde{x}$ están casi
pegados. Cuando aparecen valores muy altos (un paciente con espera anormal) la
**media se mueve** hacia ese punto; la **mediana se queda quieta** porque sólo
depende del orden.

Probemos esa idea con un control interactivo. No estamos cambiando los datos
reales: incorporamos valores al explorador para comparar qué pasa con cada
medida resumen cuando aparece un valor extremo.

```{code-cell} python
:tags: [hide-input]
build_location_evolution_explorer(
    SummaryEvolutionExplorerInput(
        observations=clinic_sample.waiting_times,
        settings=settings,
    )
)
```

Usá los controles anteriores como un laboratorio pequeño. Antes de presionar cada
botón, anticipá qué curva debería moverse y después compará tu predicción con el
gráfico:

- Si agregás una espera extrema alta, por ejemplo 20 minutos, la **media** puede
  desplazarse hacia arriba porque ese valor entra directamente en la suma. Ese
  efecto puede compensarse con un valor igual de extremo en sentido contrario:
  si la muestra tuviera esperas alrededor de 4 minutos, una espera de 20 empuja
  la media hacia arriba y una espera de 0 empuja en dirección opuesta.
- Si agregás una espera exactamente igual a la media muestral actual, la
  **media** no cambia: sumar un valor igual al equilibrio anterior mantiene el
  mismo equilibrio. En la clínica, si el promedio actual fuera 4,3 minutos y
  entra otro paciente con 4,3 minutos de espera, la media queda igual.
- La **mediana** puede moverse, pero lo hace saltando de un valor ordenado a
  otro. Por eso sus saltos suelen ser pequeños; sólo serían grandes si hubiera
  huecos grandes entre valores consecutivos. Se mueve hacia el lado donde se
  agregan más observaciones, extremas o no. Si entran varias esperas altas, la
  posición central se desplaza hacia arriba; si luego entran esperas bajas, ese
  efecto puede compensarse.
- El **desvío estándar** disminuye cuando agregás datos cerca de la media
  muestral: si la mañana venía con esperas alrededor de 4 minutos y agregás más
  pacientes cerca de 4, la nube se vuelve más compacta respecto de su centro.
- El **desvío estándar** crece mucho con datos extremos. Una espera de 20
  minutos agrega una distancia grande al promedio; para compensar ese efecto no
  alcanza con un único valor simétrico, porque ambos extremos suman distancia:
  hace falta incorporar muchos más datos cerca del comportamiento habitual.
- El **rango** es monótonamente creciente: no puede achicarse al agregar datos,
  porque depende sólo del mínimo y del máximo. Aumenta tanto con una espera
  extremadamente alta como con una espera extremadamente baja.
- El **IQR** puede disminuir cuando agregás muchos valores muy cercanos a la
  media muestral, porque el 50% central se concentra más. En cambio, tiende a
  permanecer estable cuando agregás valores parecidos a toda la muestra original:
  si los nuevos pacientes reproducen la misma mezcla de esperas bajas, medias y
  altas, los cuartiles cambian poco.

## Exploración interactiva

Probá esa intuición moviendo $\sigma$ con el control de abajo. Antes de tocar
el control, anticipá dos cosas: qué debería pasar con la dispersión visual de
las esperas y qué debería quedarse casi quieto. Después mové un parámetro por
vez y verificá si tu predicción se cumple.

**Chequeo rápido.** Si el centro queda parecido pero el tramo central se
ensancha, ¿qué le dirías a Lucía: cambió la medida resumen o cambió la
regularidad del servicio?

```{code-cell} python
:tags: [hide-input]
explorer_input = DescriptiveExplorerInput(settings=settings)
build_descriptive_explorer(explorer_input)
```

(sec-descriptive-boxplot)=
## Cómo leer un boxplot

Un **boxplot** — o diagrama de caja y bigotes — comprime la distribución en
cinco referencias visuales. En la versión introductoria, esas referencias son mínimo,
$Q_1$, mediana, $Q_3$ y máximo. En la versión de Tukey, que usamos en el gráfico,
los extremos visuales son el mínimo no atípico y el máximo no atípico. En ambos
casos, es la tabla de posiciones convertida en dibujo.

Cuando los bigotes llegan al mínimo y al máximo observados, la longitud total del
diagrama es el rango y la longitud de la caja es el rango intercuartil. En Tukey, los
bigotes llegan sólo hasta valores no atípicos y los puntos externos se muestran
aparte. Conviene reconocer ambas convenciones antes de comparar gráficos de
distintas fuentes.

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
:tags: [hide-input]
summary_chart_input = DescriptiveSummaryChartInput(
    observations=clinic_sample.waiting_times,
    statistics=summary,
    settings=settings,
)
chart_descriptive_summary(summary_chart_input)
```

Un boxplot clásico no suele incluir la media. En este gráfico la agregamos como
línea punteada para compararla visualmente con la mediana y reforzar cómo los
valores extremos pueden mover el promedio.

### Cuando el boxplot esconde la forma

El boxplot es compacto, pero justamente por eso puede ser engañoso. Dos muestras
pueden tener centro, cuartiles y rango muy parecidos, y aun así contar historias
operativas distintas. En una clínica, una sola campana alrededor de cuatro minutos
podría indicar un flujo regular; dos grupos separados podrían indicar dos circuitos
distintos de atención mezclados en el mismo resumen.

En el ejemplo siguiente, la muestra bimodal se genera como la combinación de dos
grupos con forma de campana: pacientes atendidos casi sin demora y pacientes que
entran en un circuito más lento. El boxplot central resume ambas muestras con una
lectura muy parecida; los histogramas, alineados en el mismo eje x, muestran que las
formas son muy diferentes.

```{code-cell} python
:tags: [hide-input]
rng_boxplot = np.random.default_rng(20260303)
unimodal_waits = pd.DataFrame({
    "value": rng_boxplot.normal(4.0, 0.75, 320).clip(1.5, 6.5)
}).pipe(DataFrame[Observations])
bimodal_waits = pd.DataFrame({
    "value": np.concatenate([
        rng_boxplot.normal(3.35, 0.35, 160),
        rng_boxplot.normal(4.65, 0.35, 160),
    ])
}).pipe(DataFrame[Observations])
```

```{code-cell} python
:tags: [hide-input]
chart_boxplot_shape_comparison(
    BoxplotShapeComparisonChartInput(
        first_sample=unimodal_waits,
        second_sample=bimodal_waits,
        first_label="Unimodal",
        second_label="Bimodal",
        first_title="Muestra unimodal",
        second_title="Muestra bimodal",
        value_title="Minutos de espera",
        settings=settings,
    )
)
```

La enseñanza no es que el boxplot sea inútil, sino que no alcanza solo. Si el resumen
visual sugiere una mañana razonable pero el histograma muestra dos grupos, Lucía no
debería promediar todo sin preguntar qué separa a esos grupos: área de atención,
horario de llegada, derivación o disponibilidad de consultorios.

(sec-descriptive-tukey)=
## Detección de outliers — la regla de Tukey

Un **outlier** — o dato atípico — es una observación tan alejada del resto
que conviene mirarla aparte: puede ser un error de carga, un caso excepcional
o una señal importante que no queremos esconder dentro del promedio.

Para detectarlos vamos a reutilizar los cuartiles del boxplot. La distancia
entre $Q_1$ y $Q_3$ resume el tramo central de la muestra.

**Paso 1.** Ordenamos los datos y ubicamos $Q_1$ y $Q_3$.

**Paso 2.** Calculamos el rango intercuartil definido en [](#eq-iqr) y marcamos
como **outlier** cualquier observación que caiga fuera del intervalo:

$$ \bigl[Q_1 - 1{,}5\,\text{IQR},\ Q_3 + 1{,}5\,\text{IQR}\bigr] $$ (eq-iqr-fence)

Es la misma regla que define hasta dónde llegan los bigotes del boxplot: por
eso ese gráfico es buen detector visual.

Cuando aparece un valor atípico, antes de descartarlo conviene preguntar de dónde
salió. En la práctica suele deberse a una de tres causas: se registró mal, proviene de
una población distinta, o está bien medido pero representa un suceso poco común.

```{code-cell} python
:tags: [hide-input]
outlier_report = detect_outliers_tukey(clinic_sample.waiting_times)
outlier_report
```

En la muestra de la clínica, `outlier_report` separa el tramo habitual de espera de
los casos que quedan más allá de los límites de Tukey. Si el reporte marca pocas
esperas altas, la lectura operativa no es "borrarlas", sino revisarlas: pueden ser
pacientes derivados, autorizaciones demoradas o consultas anteriores que trabaron el
flujo. Para Lucía, esos casos no invalidan el resumen general, pero sí dicen dónde
conviene mirar antes de cambiar turnos para todo el servicio.

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

La dirección del sesgo la marca la **cola**, no la parte más alta del gráfico. En una
distribución simétrica y con una sola moda, media, mediana y moda quedan cerca:
$\bar{x} \approx \tilde{x} \approx \hat{x}$. Si la cola se estira a la derecha,
la media suele quedar hacia ese lado y aparece el orden
$\hat{x} < \tilde{x} < \bar{x}$. Si la cola se estira a la izquierda, el orden
típico se invierte: $\bar{x} < \tilde{x} < \hat{x}$.

### Preguntas para leer formas típicas

Antes de abrir cada respuesta, imaginá el boxplot y traducí su forma a una
frase sobre los datos.

En estos boxplots horizontales, la **izquierda** corresponde a valores menores
y la **derecha** a valores mayores. Por eso cada pregunta describe no sólo la
forma, sino también hacia qué lado de la escala se ubican los datos.

**Pregunta 1.** La caja está centrada, la mediana cae casi en el medio y los dos
bigotes tienen longitudes parecidas hacia la izquierda y hacia la derecha. ¿Qué
sugiere sobre la distribución?

```{code-cell} python
:tags: [hide-input]

chart_boxplot_example(
    BoxplotExampleChartInput(
        values=(2.0, 2.5, 3.0, 3.5, 3.8, 4.0, 4.2, 4.5, 5.0, 5.5, 6.0),
        settings=settings,
    )
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
    BoxplotExampleChartInput(
        values=(1.0, 1.0, 1.1, 1.2, 1.3, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0),
        settings=settings,
    )
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
    BoxplotExampleChartInput(
        values=(3.8, 3.9, 4.0, 4.0, 4.1, 4.1, 4.2, 4.2, 4.3, 4.3, 7.0, 8.5, 9.0),
        settings=settings,
    )
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
aislados.
::::

**Pregunta 4.** Dos grupos tienen medianas parecidas, ubicadas cerca del mismo
valor central. En el grupo A la caja se extiende poco hacia la izquierda
y hacia la derecha; en el grupo B la caja se extiende mucho más hacia ambos
lados. ¿Qué diferencia hay entre los grupos?

```{code-cell} python
:tags: [hide-input]

apply_theme(
    alt.vconcat(
        chart_boxplot_example(BoxplotExampleChartInput(
            values=(3.6, 3.8, 3.9, 4.0, 4.1, 4.2, 4.4),
            settings=settings,
            apply_theme=False,
        )).properties(width=settings.chart_theme.width, height=settings.chart_theme.height),
        chart_boxplot_example(BoxplotExampleChartInput(
            values=(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0),
            settings=settings,
            apply_theme=False,
        )).properties(width=settings.chart_theme.width, height=settings.chart_theme.height),
        spacing=10,
    ).resolve_scale(x="shared"),
    settings,
    set_size=False,
)
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
    BoxplotExampleChartInput(
        values=(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 6.5, 6.7, 6.8, 6.9, 7.0, 7.0),
        settings=settings,
    )
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

(sec-descriptive-empirical-rule)=
## Regla empírica: media más desvíos

Cuando un histograma es aproximadamente simétrico, con un solo centro claro y una
forma de campana, el desvío estándar se interpreta junto con la media usando la
**regla empírica**:

$$
\bar{x} \pm s \approx 68\%, \qquad
\bar{x} \pm 2s \approx 95\%, \qquad
\bar{x} \pm 3s \approx \text{casi todos los datos}
$$ (eq-empirical-rule)

La regla es descriptiva y depende de la forma. Si el histograma no tiene esa forma
de campana, esos porcentajes pueden cambiar mucho. También evita una confusión
común: $\bar{x} \pm s$ no es el rango de variación; en muchas formas cubre sólo una
parte central de los datos.

Veamos una verificación concreta con los minutos de espera. Si su forma fuera
razonablemente campanular, los intervalos $\bar{x} \pm ks$ deberían cubrir
aproximadamente 68%, 95% y casi todas las observaciones para $k = 1, 2, 3$.

```{code-cell} python
:tags: [hide-input]
waiting_summary = summarize_observations(clinic_sample.waiting_times)
waiting_mean = waiting_summary.location.mean
waiting_std = waiting_summary.dispersion.sample_standard_deviation

style_display_table(pd.DataFrame({
    "k": [1, 2, 3],
    "intervalo": [
        f"{waiting_mean - k * waiting_std:.3f} a {waiting_mean + k * waiting_std:.3f}"
        for k in [1, 2, 3]
    ],
    "proporción esperada": ["68%", "95%", "casi todos"],
    "proporción observada": [
        ((clinic_sample.waiting_times["value"] >= waiting_mean - k * waiting_std)
         & (clinic_sample.waiting_times["value"] <= waiting_mean + k * waiting_std)).mean()
        for k in [1, 2, 3]
    ],
}))
```

Si los porcentajes observados se parecen bastante a la regla, eso no prueba una
ley matemática especial; sólo dice que, para esta descripción rápida, media y
desvío resumen razonablemente el centro y la dispersión. Si se alejan mucho, la
forma pide otro gráfico y probablemente otro resumen.

(sec-descriptive-zscore)=
## Posición relativa: el $z$-score

El $z$-score (*standard score*) traduce una observación a la pregunta «¿a cuántos desvíos del
promedio está?».

**Paso 1:** partimos de las fórmulas [](#eq-mean) y [](#eq-std) para tener
$\bar{x}$ y $s$.

**Paso 2:** centramos restando el promedio y reescalamos dividiendo por $s$:

$$ z_i = \frac{x_i - \bar{x}}{s} $$ (eq-zscore)

Si estuviéramos describiendo una población completa, usaríamos los parámetros
poblacionales:

$$ z = \frac{x - \mu}{\sigma} $$ (eq-population-zscore)

Un $z_i$ positivo dice «este paciente esperó más que el promedio»; un
$z_i$ negativo, «menos que el promedio». Y la magnitud cuenta cuántos
$s$ separan la observación del centro: $z_i = 2$ significa dos desvíos
estándar arriba, sin importar las unidades originales.

La regla empírica sugiere un criterio simple para valores muy extremos: si
$|z_i| > 3$, la observación está a más de tres desvíos de la media y merece revisión.
No es una sentencia automática de error; en algunos procesos un valor así puede ser
real y relevante.

La regla de Tukey usa otra escala, basada en cuartiles. En una forma campanular
simétrica, sus límites $Q_1 - 1{,}5\,\text{IQR}$ y $Q_3 + 1{,}5\,\text{IQR}$
quedan aproximadamente a $2{,}7$ desvíos estándar del centro. Por eso, en datos con
esa forma, Tukey y el criterio $|z_i| > 3$ suelen señalar casos parecidos, aunque
no idénticos: Tukey es un poco más sensible y además funciona sin usar la media.

En este capítulo usamos $z_i$ solo como resumen descriptivo: compara cada
observación con el promedio del mismo conjunto de datos. Ayuda a ver qué
valores están cerca del centro y cuáles quedan relativamente lejos.

```{code-cell} python
:tags: [hide-input]
standardized = standardize_observations(clinic_sample.waiting_times)
standardized
```

(sec-descriptive-people-ahead)=
## Personas por delante al llegar

Sigamos en la clínica, pero cambiemos la variable. Además de los minutos de
espera, Lucía registró cuántas personas tenía cada paciente por delante al llegar.
Ya no estamos midiendo tiempo continuo: ahora contamos personas. Un paciente puede
llegar con 0 personas delante, otro con 3, otro con 7.

La pregunta vuelve a sonar conocida: ¿qué medida resume el conteo?, ¿qué tan
estable fue la fila?, ¿apareció una llegada suficientemente cargada como para
revisar qué pasó? Cambiamos de unidad — de minutos a personas —, pero seguimos
haciendo estadística descriptiva sobre observaciones de la misma mañana.

```{code-cell} python
:tags: [hide-input]
people_ahead_observations = pd.DataFrame({
    "value": clinic_sample.clinic_data["people_ahead"].astype(float)
}).pipe(DataFrame[Observations])

people_ahead_histogram_input = HistogramChartInput(
    observations=people_ahead_observations,
    bin_count=12,
    title="Personas por delante al llegar",
    settings=settings,
)
chart_histogram(people_ahead_histogram_input)
```

```{code-cell} python
:tags: [hide-input]
people_ahead_summary = summarize_observations(people_ahead_observations)
people_ahead_summary
```

(sec-descriptive-cv)=
## Comparar dispersión en escalas distintas

Las dos variables viven en escalas distintas — minutos contra personas en fila — y
con magnitudes muy distintas. Comparar sus medias en crudo dice poco: 4 minutos
no es ni mejor ni peor que 3 personas por delante. Lo mismo pasa con los desvíos:
un minuto y una persona no comparten unidad.

Cuando la comparación se vuelve incómoda hay que salir de las unidades
originales. Los $z$-scores (*standard scores*), que ya introdujimos, comparan
observaciones dentro de su propia muestra. Para comparar la **dispersión
relativa** de dos variables usamos el **coeficiente de variación**:

$$ CV = \frac{s}{\bar{x}} $$ (eq-coefficient-variation)

El cociente no tiene unidades: mide qué tan grande es el desvío típico en
relación con la media del mismo proceso. Muchas veces se informa como porcentaje,
$100 \cdot CV$. Sirve para comparar distribuciones con unidades distintas y también
distribuciones con la misma unidad pero promedios muy diferentes.

El $CV$ sólo tiene una lectura clara cuando la media es positiva y está razonablemente
lejos de cero. Si $\bar{x}$ queda cerca de cero, dividir por un número tan chico puede
inflar el cociente y hacer que una variación moderada parezca enorme. El caso límite
es $\bar{x}=0$: ahí el $CV$ ni siquiera está definido, porque no se puede dividir por
cero. Si la media es negativa, la idea de "variar cierto porcentaje respecto del
promedio" también deja de ser una comparación útil. Por eso tiene sentido para tiempos
de espera o cantidades positivas, pero no conviene usarlo automáticamente con variables
que pueden cruzar el cero, como saldos, temperaturas en grados Celsius o cambios con
signo.

Antes de mirar la tabla, anticipá: ¿los tiempos de espera o la cantidad de personas por
delante parecen más irregulares respecto de su propio centro?

```{code-cell} python
:tags: [hide-input]
cv_comparison = pd.DataFrame({
    "muestra": ["Clínica: minutos de espera", "Clínica: personas por delante"],
    "media": [summary.location.mean, people_ahead_summary.location.mean],
    "desvío estándar": [
        summary.dispersion.sample_standard_deviation,
        people_ahead_summary.dispersion.sample_standard_deviation,
    ],
    "coeficiente de variación": [
        summary.dispersion.coefficient_of_variation,
        people_ahead_summary.dispersion.coefficient_of_variation,
    ],
})
style_display_table(cv_comparison)
```

La muestra con mayor $CV$ no es necesariamente la que tiene mayor desvío en
unidades originales; es la que varía más **relativo a su propio nivel típico**.
Esa es la comparación justa cuando cambiamos de minutos a personas por delante.

Leyendo la tabla, las dos variables tienen desvíos estándar parecidos en valor
absoluto, pero viven en escalas muy distintas: un minuto y una persona no
pesan lo mismo respecto del promedio. El $CV$ pone ese desbalance en evidencia
y dice cuál de las dos series es más **inestable respecto de su propio centro**.
Si para Lucía la cantidad de personas por delante tiene un $CV$ más alto que los
minutos de espera, la fila varía más de lo que su promedio sugiere: dos llegadas
de aspecto parecido pueden encontrar congestiones muy distintas, incluso cuando
los tiempos medios entre pacientes se parecen. Si fuera al revés, los minutos
serían el lado más irregular del proceso. En cualquiera de los dos casos, la
lectura operativa es la misma: el promedio solo alcanza para describir bien la
mañana si el $CV$ es chico; cuanto más grande, más conviene mirar la dispersión
antes de tomar decisiones.

Veamos ahora un contraejemplo con datos generados al azar. Lucía compara dos
indicadores: cuántos pacientes se atienden por bloque de tiempo y cuánto cambia la
fila en esos mismos bloques. El primer indicador es positivo y queda lejos de cero; el
segundo tiene valores negativos y positivos, aunque su media queda por encima de 1.

```{code-cell} python
:tags: [hide-input]
cv_counterexample_size = 80
rng_cv_counterexample = np.random.default_rng(20260622)
attended_blocks = rng_cv_counterexample.normal(
    loc=10.0,
    scale=1.2,
    size=cv_counterexample_size,
).clip(min=0.0)
queue_changes = rng_cv_counterexample.normal(
    loc=1.2,
    scale=1.4,
    size=cv_counterexample_size,
)

cv_counterexample_data = pd.DataFrame({
    "indicador": np.repeat(
        ["Pacientes atendidos", "Cambio neto en fila"],
        [len(attended_blocks), len(queue_changes)],
    ),
    "valor": np.concatenate([attended_blocks, queue_changes]),
})
```

```{code-cell} python
:tags: [hide-input]
apply_theme(
    alt.Chart(cv_counterexample_data).mark_boxplot(extent=1.5, size=42).encode(
        x=alt.X("valor:Q", title="Valor observado"),
        y=alt.Y(
            "indicador:N",
            title=None,
            sort=["Pacientes atendidos", "Cambio neto en fila"],
        ),
    ).properties(title="Contraejemplo: valores negativos anticipan problemas", height=150),
    settings,
)
```

El boxplot ya da una pista: aunque el cambio neto en fila tiene media positiva, sus
valores cruzan el cero. En ese caso, comparar "porcentaje respecto del promedio" no
tiene una interpretación estable.

```{code-cell} python
:tags: [hide-input]
cv_counterexample_summary = cv_counterexample_data.groupby("indicador", sort=False)["valor"].agg(
    media="mean",
    **{"desvío estándar": "std"},
).reset_index().assign(CV=lambda data: data["desvío estándar"] / data["media"])
style_display_table(cv_counterexample_summary)
```

Si miráramos sólo el $CV$, concluiríamos que el cambio neto en fila es
desproporcionadamente más irregular. Esa lectura es engañosa: el desvío estándar no
es enorme en unidades originales, pero el indicador mezcla valores negativos y
positivos. La forma del boxplot permitía anticiparlo antes de calcular la tabla:
cuando una variable cruza el cero, el $CV$ deja de ser una buena brújula aunque la
media sea positiva.

:::::{admonition} Nota técnica: CV y escala logarítmica
:class: dropdown

El $CV$ resume dispersión relativa: pregunta cuán grande es el desvío típico en
relación con el nivel medio. Esa lectura se parece a mirar cambios multiplicativos,
como cuando se comparan datos en escala logarítmica. La conexión aparece paso a paso.

Primero llamemos $s_i$ al desvío de la observación $i$ respecto de la media. En esta
nota, $s_i$ no es el desvío estándar muestral $s$, sino un desvío individual:

$$
s_i = x_i - \bar{x}
$$

Entonces cada observación puede escribirse como la media más ese desvío:

$$
x_i = \bar{x} + s_i
$$

Si reemplazamos $s_i$ por su definición:

$$
x_i = \bar{x} + (x_i - \bar{x})
$$

Después sacamos factor común $\bar{x}$. Para poder hacerlo necesitamos
$\bar{x}\ne0$:

$$
x_i = \bar{x}\left(1 + \frac{s_i}{\bar{x}}\right)
= \bar{x}\left(1 + \frac{x_i - \bar{x}}{\bar{x}}\right)
$$

El término

$$
r_i = \frac{s_i}{\bar{x}} = \frac{x_i - \bar{x}}{\bar{x}}
$$

es el desvío relativo de la observación $i$: no dice cuántas unidades se alejó de la
media, sino qué fracción de la media representa ese alejamiento. Con esa abreviatura:

$$
x_i = \bar{x}(1+r_i)
$$

Si dividimos por $\bar{x}$:

$$
\frac{x_i}{\bar{x}} = 1+r_i
$$

Ahora aparece una razón multiplicativa: $x_i/\bar{x}$ compara la observación con el
nivel medio. Si tomamos logaritmos a ambos lados:

$$
\log\left(\frac{x_i}{\bar{x}}\right) = \log(1+r_i)
$$

Y por la propiedad $\log(a/b)=\log(a)-\log(b)$:

$$
\log(x_i) - \log(\bar{x}) = \log(1+r_i)
$$

Cuando el desvío relativo es chico, usamos la aproximación
$\log(1+r) \approx r$. Entonces:

$$
\log(x_i) - \log(\bar{x}) \approx r_i
= \frac{x_i - \bar{x}}{\bar{x}}
$$

Es decir: la dispersión de los logaritmos se parece a la dispersión de los datos
medidos como proporción de la media. Por eso, cuando el $CV = s/\bar{x}$ es chico y
los datos son positivos, puede leerse aproximadamente como una dispersión en escala
logarítmica.

El problema aparece cuando $\bar{x}$ se acerca a cero: el término
$(x_i-\bar{x})/\bar{x}$ se vuelve inestable, porque divide por un número muy chico.
Además, la escala logarítmica sólo existe para números positivos: no se puede calcular
$\log(0)$ ni $\log(x)$ para $x<0$ dentro de los números reales.

Por eso, si una variable puede valer cero o tomar valores negativos, la comparación
relativa deja de tener una base clara. Además, si bastara con sumar una constante para
que todos los valores fueran positivos, el $CV$ cambiaría aunque la dispersión en
unidades originales no cambiara. Ese problema de escala es parte de la discusión
estadística sobre cuándo el coeficiente de variación deja de ser una medida adecuada;
ver esta discusión en
[Cross Validated](https://stats.stackexchange.com/questions/56399/why-is-the-coefficient-of-variation-not-valid-when-using-data-with-positive-and).

:::::

(sec-descriptive-sampling)=
## Antes de inferir: cómo se juntaron los datos

Un resumen descriptivo puede ser exacto y aun así engañar. Si las 80 esperas de la
clínica fueron tomadas durante varias mañanas típicas, con pacientes habituales y sin
cambios de proceso, la muestra habla bastante bien del servicio. Si todas salieron de
un lunes después de un feriado o de la franja más congestionada, el promedio y el
desvío describen esa situación especial, no necesariamente la clínica. Lo mismo pasa
si sólo registramos pacientes de guardia, o si medimos justo después de un cambio
excepcional en la agenda de consultorios.

Si observamos todas las unidades de la población hacemos un **censo** o estudio
exhaustivo. En ese caso el análisis descriptivo alcanza para responder sobre esa
población finita porque tenemos todos los datos y podemos calcular los parámetros de
interés. Pero muchas veces un censo no es posible: la población puede ser infinita,
los ensayos pueden ser destructivos o costosos, o el proceso puede tardar demasiado.

Cuando observamos sólo un subconjunto hacemos un **estudio por muestreo**. La
**muestra** tiene tamaño $n$ y produce estadísticos, no parámetros. Para extender sus
conclusiones a la población necesitamos herramientas que midan cuánta incertidumbre
queda al pasar de lo observado a lo no observado; esas herramientas empiezan en el
capítulo siguiente.

Tres palabras conviene tener presentes desde ahora:

- **Representatividad.** La muestra debe parecerse al proceso sobre el que queremos decidir.
- **Sesgo.** Un patrón de recolección puede empujar todos los datos en una misma dirección.
- **Independencia.** Una observación no debería arrastrar mecánicamente a la siguiente; si una demora inicial retrasa a todos los pacientes posteriores, las esperas quedan encadenadas.

Una muestra **aleatoria** o **probabilística** da a cada unidad de la población una
chance conocida de ser seleccionada. Esa condición es la que permite controlar el
riesgo al generalizar. Una muestra **por conveniencia** incorpora unidades porque son
fáciles de conseguir, porque responden voluntariamente o porque están a mano; puede
ser útil como exploración, pero puede quedar sesgada si no reproduce la variabilidad
de la población. Además del método de selección, importa el tamaño de la muestra:
ambos influyen en la calidad de las conclusiones.

> **Contrato del dato.** Antes de confiar en cualquier modelo, preguntá cómo nació la muestra. ¿Cubre horarios y días relevantes? ¿Evita elegir solo casos fáciles de medir? ¿Hubo cambios de política, demanda o personal durante la medición? Una muestra sesgada puede producir gráficos prolijos y fórmulas correctas apuntando a una conclusión equivocada.

**Lectura operativa.** Si el objetivo es describir la mañana observada, alcanza
con resumir esos datos. Si el objetivo es rediseñar turnos para el mes, la
pregunta cambia: la muestra debe representar el proceso que se quiere mejorar.

Imaginá dos planes de medición. El primero registra ochenta pacientes el lunes
después de un feriado; el segundo registra veinte pacientes por semana durante
cuatro semanas, mezclando días y horarios. El primer plan puede tener una tabla
impecable, pero representa una situación particular. El segundo suele ser más
útil para decidir turnos porque cubre más partes del proceso.

La independencia también se ve en la historia de recolección. Si una demora
inicial retrasa a todos los pacientes posteriores, las observaciones quedan
encadenadas: cada espera ya no cuenta como una unidad nueva de información del
mismo modo que en una mañana estable. En ese caso el gráfico sigue sirviendo
para describir lo ocurrido, pero no alcanza para inferir cómo funciona el
servicio en general.

**Decisión de ingeniería.** Si Lucía quiere rediseñar turnos para todo el mes, una mañana extrema sirve como alarma, pero no como única evidencia. La pregunta siguiente no es solo “cuál fue la media”, sino “qué proceso generó estos datos y qué población representan”.

## Conclusión: qué sabemos de la mañana

Volvamos a las preguntas del principio. La respuesta operativa no es un único
número: cada medida resumen contesta una pregunta distinta, con una sensibilidad
distinta a los valores extremos. La siguiente tabla condensa el capítulo en un
solo mapa de referencia: cuándo conviene cada medida, qué tipo de variable
acepta, qué tan estable es ante un dato atípico y en qué unidades queda.

| Medida | Pregunta que Lucía puede responder | Tipo de variable | Sensibilidad a outliers | Unidades |
|---|---|---|---|---|
| Media $\bar{x}$ | ¿Cuántos minutos esperó un paciente *en promedio* esta mañana? | cuantitativa | alta | originales |
| Mediana $\tilde{x}$ | ¿Cuánto esperó el paciente del medio, el que parte la mañana en dos mitades? | cuantitativa | baja | originales |
| Moda $\hat{x}$ | ¿Cuál fue el área de atención o el motivo de demora más frecuente? | cualquiera | nula | originales |
| Cuartiles / percentiles | ¿Hasta qué minuto esperó el 25%, el 50% o el 75% de los pacientes? | cuantitativa | baja | originales |
| Rango $R$ | ¿Cuánto separa al paciente que menos esperó del que más esperó? | cuantitativa | máxima | originales |
| IQR | ¿Qué tan ancho fue el tramo central de esperas, ignorando los extremos? | cuantitativa | baja | originales |
| Varianza $s^2$ | ¿Cuánta dispersión total tuvo la mañana, en escala cuadrática para propiedades algebraicas? | cuantitativa | alta | originales al cuadrado |
| Desvío estándar $s$ | ¿Cuántos minutos se aleja, en promedio, una espera del promedio del día? | cuantitativa | alta | originales |
| $CV = s/\bar{x}$ | ¿Qué proceso de la clínica es más irregular respecto de su propio promedio: las esperas en minutos o las personas en fila? | cuantitativa positiva, con media lejos de cero | alta (vía $s$) | adimensional |
| $z_i = (x_i - \bar{x})/s$ | ¿A cuántos desvíos del promedio quedó la espera de un paciente concreto? | cuantitativa | alta (vía $\bar{x}$, $s$) | adimensional |
| Tukey ($Q_1 - 1{,}5\,\text{IQR}$, $Q_3 + 1{,}5\,\text{IQR}$) | ¿Qué pacientes esperaron tanto que conviene revisar el caso aparte? | cuantitativa | baja | originales |

Esa tabla es la guía operativa: para resumir el centro de una mañana, conviene
usar mediana cuando la forma es asimétrica y media cuando es razonablemente
campanular; para describir qué tan regular fue el servicio, IQR resiste lo que
desvío estándar y rango no; para señalar casos que merecen revisión, Tukey y
$z$-scores apuntan a los mismos casos cuando la forma es simétrica, pero
divergen cuando hay sesgo. Si el centro es razonable pero hay outliers, Lucía
puede revisar esos casos antes de cambiar toda la agenda. Si el histograma
muestra dos grupos, conviene preguntar si se mezclaron áreas o circuitos
distintos. Si la muestra salió de una mañana especial, los gráficos describen
esa mañana, no necesariamente todo el servicio.

La práctica del capítulo retoma estos cálculos con ejercicios específicos. Lo que
queda abierto es mirar hacia adelante: si mañana llega otro paciente, ¿qué tan
probable es que espere más de cinco minutos?, ¿cambian las chances si ya lleva un
rato sentado?, ¿cómo se combinan señales parciales para tomar una decisión? Para
responder esas preguntas necesitamos el lenguaje del próximo capítulo:
**probabilidad**.
