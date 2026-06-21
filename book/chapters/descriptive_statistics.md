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
respondan cosas concretas: cuál fue una espera **típica**, qué tan
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
:tags: [hide-input]
import numpy as np
import pandas as pd
from pandera.typing import DataFrame

from core import Observations, Settings
from descriptive import (
    ClinicSampleInput,
    detect_outliers_tukey,
    generate_clinic_sample,
    standardize_observations,
    summarize_observations,
)
from exercises import NumericAnswerInput, verify_numeric_answer
from visualization import (
    CategoricalBarFromDataChartInput,
    DescriptiveSummaryChartInput,
    DiscreteStickFromDataChartInput,
    FrequencyChartInput,
    HistogramChartInput,
    ParetoFromDataChartInput,
    TypicalValuesComparisonChartInput,
    chart_categorical_bars_from_data,
    chart_descriptive_summary,
    chart_discrete_sticks_from_data,
    chart_frequency_table,
    chart_histogram,
    chart_pareto_from_data,
    chart_typical_values_comparison,
)
from widgets import DescriptiveExplorerInput, build_descriptive_explorer
```

```{code-cell} python
:tags: [remove-cell]
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
clinic_sample = generate_clinic_sample(ClinicSampleInput(settings=settings, sample_size=80))
clinic_sample.clinic_data.head()
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
clinic_sample.area_frequency_table
```

```{code-cell} python
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

La frecuencia relativa suele expresarse como porcentaje: una proporción de
$0{,}25$, por ejemplo, equivale al 25% de la muestra. Para variables cualitativas
conviene usar **gráficos de barras**, porque facilitan la comparación visual entre
categorías y partes del total. Aunque los gráficos de torta o de sectores son muy
usados, hay estudios y guías de visualización que recomiendan evitarlos cuando el
objetivo es comparar magnitudes con precisión [@few2007visual].

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
clinic_sample.delay_reason_frequency_table
```

```{code-cell} python
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
clinic_sample.people_ahead_frequency_table
```

La fila de $3$ tiene dos lecturas distintas: $f_k$ dice qué proporción de
pacientes tenía exactamente tres personas adelante, y $F_k$ dice qué proporción
tenía tres personas o menos. El gráfico natural para estos datos es el **gráfico
de bastones**: un segmento vertical para cada valor posible, con altura
proporcional a su frecuencia.

```{code-cell} python
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
En un gráfico de bastones, en cambio, reordenar los segmentos puede confundir,
porque el lector espera que el eje avance en orden ascendente.

### Variables continuas: intervalos, tallo-hoja e histogramas

En variables continuas casi nunca conviene contar cada valor exacto. Primero se
puede usar un **diagrama de tallo y hoja**, que conserva los datos individuales pero
los ordena visualmente: si un paciente esperó 4,7 minutos, por ejemplo, el tallo
puede ser 4 y la hoja 7. Es útil en conjuntos pequeños o medianos porque muestra
la forma sin destruir del todo la lista original.

Para una tabla de frecuencias continua se particiona el rango observado en
**intervalos de clase**. Conviene que tengan amplitud similar y que cada dato caiga
en uno y sólo un intervalo; por eso se usan intervalos semiabiertos, como
$(2, 4]$. El **punto medio** de una clase representa al intervalo cuando hacemos
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
la apariencia del histograma.

En la clínica, si agrupamos los 80 tiempos de espera en intervalos de dos minutos,
podríamos obtener una tabla como esta:

```{code-cell} python
clinic_sample.frequency_table
```

Cada fila dice dos cosas a la vez: `relative_frequency` cuenta qué proporción cae
dentro de ese intervalo, y `cumulative_relative_frequency` acumula todo lo que
queda por debajo de su límite superior. El punto medio representa a todo el
intervalo cuando hacemos cuentas con datos agrupados; por eso agrupamos para leer
mejor, pero aceptamos perder el detalle de cada espera individual.

También se puede sumar un **polígono de frecuencias**, uniendo los puntos medios
superiores de las barras, y un **polígono de frecuencias acumuladas**, que une las
frecuencias acumuladas. La ojiva que usamos más abajo es una versión de ese gráfico
acumulado.

Para Lucía, la pregunta operativa puede ser "¿qué porcentaje esperó menos de cinco
minutos?". Esa lectura sale de la distribución acumulada: no mira sólo una barra,
sino todo lo que quedó por debajo del corte que importa para decidir.

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
frequency_chart_input = FrequencyChartInput(
    frequency_table=clinic_sample.frequency_table,
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

Si los datos ya están agrupados en $r$ clases, usamos el valor de la clase $x_k$
— el valor exacto en datos discretos o el punto medio del intervalo en datos
continuos — y su frecuencia:

$$ \bar{x} = \frac{1}{n}\sum_{k=1}^{r} x_k n_k = \sum_{k=1}^{r} x_k f_k $$ (eq-grouped-mean)

Si el conjunto observado es toda la población, el promedio es un parámetro y se
escribe $\mu$. La media no tiene por qué coincidir con un valor observado: puede
dar 4,36 minutos aunque ningún paciente haya esperado exactamente 4,36 minutos. Como
usa toda la información, también es sensible a valores extremos. Por eso sirve para
comparar distribuciones sólo cuando sus formas son razonablemente semejantes.

### El valor más frecuente: la moda

Otra medida de posición es la **moda**, escrita $\hat{x}$: el valor o categoría con
mayor frecuencia. En una muestra de esperas puede ser el minuto que más se repite;
en una encuesta puede ser la respuesta más elegida; en la fábrica puede ser la causa
de defecto más frecuente.

La moda tiene tres detalles importantes. Algunas muestras no tienen moda clara;
otras tienen dos modas y se llaman **bimodales**; y es la única medida de tendencia
central que puede calcularse para cualquier tipo de variable, incluso cualitativa.

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

Formalmente, la mediana es el mínimo valor que acumula al menos el 50% de las
observaciones ordenadas. Por eso, cuando tenemos una tabla de frecuencias, puede
leerse mirando la primera fila cuya frecuencia relativa acumulada alcanza o supera
0,50.

**No confundas.** La media pregunta por el equilibrio numérico de todos los
valores; la mediana pregunta por la posición que parte la muestra; la moda
pregunta qué valor o categoría aparece más. Las tres pueden coincidir, pero no
cuentan la misma historia.

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
otras negativas (esperaron menos), y si las sumáramos directamente los
signos se cancelarían. Para que eso no pase, las elevamos al cuadrado
antes de sumarlas. A esa suma la llamamos **suma de cuadrados** y la
escribimos $\text{SS}$ (por *sum of squares*):

$$ \text{SS} = \sum_{i=1}^{n}(x_i - \bar{x})^2 $$

**Paso 3.** Dividimos esa suma por $n-1$. Ese cociente es la **varianza
muestral**:

$$ s^2 = \frac{\text{SS}}{n - 1} $$ (eq-sample-variance)

Con datos agrupados, la misma idea usa la frecuencia de cada clase:

$$ s^2 = \frac{1}{n - 1}\sum_{k=1}^{r} n_k(x_k - \bar{x})^2 $$ (eq-grouped-variance)

El divisor $n-1$ aparece porque usamos los mismos datos para estimar
$\bar{x}$: una vez fijado el promedio, el último desvío ya queda determinado
por los anteriores. No es un detalle cosmético; evita que la dispersión
muestral quede sistemáticamente demasiado chica cuando usamos la muestra para
hablar de un proceso más amplio.

Si los datos corresponden a toda la población, usamos la media poblacional $\mu$,
el tamaño poblacional $N$ y el denominador $N$:

$$ \sigma^2 = \frac{1}{N}\sum_{i=1}^{N}(x_i - \mu)^2, \qquad
\sigma = \sqrt{\sigma^2} $$ (eq-population-variance)

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

El **rango intercuartil** o **recorrido intercuartílico** resume la variación del
50% central:

$$ \text{IQR} = Q_3 - Q_1 $$ (eq-iqr)

Como usa cuartiles, no cambia demasiado por un único valor extremo. Si las medidas
de dispersión son altas decimos que el conjunto es heterogéneo o muy variable. La
varianza queda en unidades al cuadrado y por eso se usa mucho para propiedades
matemáticas; el desvío estándar vuelve a la unidad original y suele ser más fácil de
interpretar en contexto.

```{code-cell} python
summary = summarize_observations(clinic_sample.waiting_times)
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
    [clinic_sample.waiting_times, pd.DataFrame({"value": [120.0]})], ignore_index=True
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

Más formalmente, los cuartiles y percentiles son mínimos valores que acumulan al
menos cierto porcentaje de observaciones ordenadas. Así, $Q_1$ acumula al menos
25%, $Q_2$ acumula al menos 50% y $Q_3$ acumula al menos 75%. El segundo cuartil
coincide con la mediana y con el percentil 50:

$$ Q_2 = \tilde{x} = P_{50} $$ (eq-second-quartile)

Con una tabla de frecuencias acumuladas, se buscan de la misma manera que la
mediana: la primera fila cuya acumulada alcanza el porcentaje pedido.

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
    "Clínica — esperas equilibradas",
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
    "Clínica — esperas con cola derecha",
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
    "Clínica — caja estable con esperas atípicas altas",
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
    chart_boxplot_example([3.6, 3.8, 3.9, 4.0, 4.1, 4.2, 4.4], "Clínica A")
    & chart_boxplot_example([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0], "Clínica B")
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
    "Línea de producción — mediciones con cola izquierda",
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

Cuando aparece un valor atípico, antes de descartarlo conviene preguntar de dónde
salió. En la práctica suele deberse a una de tres causas: se registró mal, proviene de
una población distinta, o está bien medido pero representa un suceso poco común.

```{code-cell} python
outlier_report = detect_outliers_tukey(clinic_sample.waiting_times)
outlier_report
```

(sec-descriptive-empirical-rule)=
## Regla empírica: media más desvíos

Cuando una distribución es aproximadamente simétrica y campanular, como una forma
Normal, el desvío estándar se interpreta junto con la media usando la **regla
empírica**:

$$
\bar{x} \pm s \approx 68\%, \qquad
\bar{x} \pm 2s \approx 95\%, \qquad
\bar{x} \pm 3s \approx \text{casi todos los datos}
$$ (eq-empirical-rule)

La regla es descriptiva y depende de la forma. Si la distribución no es simétrica y
campanular, esos porcentajes pueden cambiar mucho. También evita una confusión
común: $\bar{x} \pm s$ no es el rango de variación; en muchas formas cubre sólo una
parte central de los datos.

Veamos una verificación concreta con la línea de producción. Tomemos 30 longitudes
de piezas medidas durante una inspección. Si su forma fuera razonablemente
campanular, los intervalos $\bar{x} \pm ks$ deberían cubrir aproximadamente 68%,
95% y casi todas las observaciones para $k = 1, 2, 3$.

```{code-cell} python
piece_lengths = pd.DataFrame({
    "value": [
        85.0,
        117.0,
        92.0,
        120.0,
        94.0,
        110.0,
        151.0,
        90.0,
        80.0,
        116.0,
        95.0,
        102.0,
        100.0,
        113.0,
        118.0,
        140.0,
        133.0,
        108.0,
        115.0,
        148.0,
        110.0,
        130.0,
        100.0,
        120.0,
        108.0,
        125.0,
        105.0,
        130.0,
        112.0,
        150.0,
    ]
}).pipe(DataFrame[Observations])

piece_length_summary = summarize_observations(piece_lengths)
piece_mean = piece_length_summary.location.mean
piece_std = piece_length_summary.dispersion.sample_standard_deviation

pd.DataFrame({
    "k": [1, 2, 3],
    "intervalo": [
        f"{piece_mean - k * piece_std:.3f} a {piece_mean + k * piece_std:.3f}"
        for k in [1, 2, 3]
    ],
    "proporción esperada": ["68%", "95%", "casi todos"],
    "proporción observada": [
        ((piece_lengths["value"] >= piece_mean - k * piece_std)
         & (piece_lengths["value"] <= piece_mean + k * piece_std)).mean()
        for k in [1, 2, 3]
    ],
})
```

Si los porcentajes observados se parecen bastante a la regla, eso no prueba que el
proceso sea Normal; sólo dice que, para esta descripción rápida, media y desvío
resumen razonablemente el centro y la dispersión. Si se alejan mucho, la forma pide
otro gráfico y probablemente otro resumen.

(sec-descriptive-zscore)=
## Posición relativa: el $z$-score

El $z$-score (*standard score*) traduce una observación a la pregunta «¿a cuántos desvíos del
promedio está?».

**Paso 1:** partimos de las fórmulas [](#eq-mean) y [](#eq-std) para tener
$\bar{x}$ y $s$.

**Paso 2:** centramos restando el promedio.

**Paso 3:** reescalamos dividiendo por $s$:

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

En este capítulo usamos $z_i$ solo como resumen descriptivo: compara cada
observación con el promedio del mismo conjunto de datos. Ayuda a ver qué
valores están cerca del centro y cuáles quedan relativamente lejos.

**No confundas.** Este $z_i$ es una posición relativa dentro de una muestra. Un
$z$-statistic de inferencia se calcula bajo una hipótesis y sirve para medir
sorpresa frente a un valor de control. Comparten la idea de estandarizar, pero
responden preguntas distintas.

```{code-cell} python
standardized = standardize_observations(clinic_sample.waiting_times)
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
relación con la media del mismo proceso. Muchas veces se informa como porcentaje,
$100 \cdot CV$. Sirve para comparar distribuciones con unidades distintas y también
distribuciones con la misma unidad pero promedios muy diferentes. Antes de mirar la
tabla, anticipá: ¿la clínica o la fábrica parece más irregular respecto de su propio
centro?

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

Un resumen descriptivo puede ser exacto y aun así engañar. Si las 80 esperas de la
clínica fueron tomadas durante varias mañanas típicas, con pacientes habituales y sin
cambios de proceso, la muestra habla bastante bien del servicio. Si todas salieron de
un lunes después de un feriado o de la franja más congestionada, el promedio y el
desvío describen esa situación especial, no necesariamente la clínica. Lo mismo pasa
si una encuesta sólo recoge respuestas de personas fáciles de contactar, o si la línea
de producción se mide justo después de un ajuste excepcional de máquina.

Si observamos todas las unidades de la población hacemos un **censo** o estudio
exhaustivo. En ese caso el análisis descriptivo alcanza para responder sobre esa
población finita porque tenemos todos los datos y podemos calcular los parámetros de
interés. Pero muchas veces un censo no es posible: la población puede ser infinita,
los ensayos pueden ser destructivos o costosos, o el proceso puede tardar demasiado.

Cuando observamos sólo un subconjunto hacemos un **estudio por muestreo**. La
**muestra** tiene tamaño $n$ y produce estadísticos, no parámetros. Para extender sus
conclusiones a la población necesitamos análisis inferencial: intervalos de confianza,
pruebas de hipótesis y herramientas apoyadas en probabilidad.

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
