---
title: Inferencia estadística
short_title: Inferencia
kernelspec:
  name: python3
  display_name: Python 3
---

Hasta este capítulo el flujo siempre fue el mismo: dados los
parámetros — una tasa, una proporción real, un desvío estándar —,
calcular probabilidades sobre las observaciones. La práctica casi
siempre invierte el sentido. Lo que se tiene son los datos: el turno
que cronometramos, las cuatrocientas respuestas, los conteos de la
jornada. Lo que se quiere saber son los parámetros que los generaron,
justamente esos parámetros que **nunca** se observan directamente.

¿Cuál es el rango plausible para la verdadera espera media de la
clínica si solo pudimos medir un turno?, ¿qué tan cerca está la
proporción que dio la encuesta de la del barrio entero, y cuánta gente
más hace falta consultar para apretar esa precisión?, cuando la línea
de producción reporta defectos cerca del límite contractual, ¿alcanza
para afirmar que el proceso se salió de control o todavía cabe el
azar?

La pregunta no es solo matemática: alguien tiene que decidir si actúa,
si espera más datos o si comunica una conclusión con incertidumbre
explícita. Lucía no puede decir simplemente “el promedio observado fue
12”; tiene que decidir si ese número justifica reorganizar el servicio
y cómo explicarlo sin prometer una certeza que los datos no dan.

**Antes de seguir.** Recuperá el hilo del capítulo anterior: por qué un
promedio muestral fluctúa, qué papel cumple el error estándar y por qué
el TCL permite pasar de datos observados a rangos plausibles.

Esas preguntas tienen nombre propio: **inferencia estadística**, y son
el oficio que sostiene buena parte de la estadística aplicada.

> **Situación de decisión.** Lucía no necesita una fórmula aislada en un
> informe: necesita decidir si actúa, mide más o comunica incertidumbre. La
> inferencia será útil solo si separa evidencia, supuesto y recomendación sin
> convertir una muestra limitada en certeza.
> Al final del capítulo vas a poder construir rangos plausibles, leer tests sin
> exagerar sus conclusiones y escribir una recomendación que distinga evidencia,
> impacto operativo y duda residual.

```{code-cell} python
:tags: [hide-input]
import numpy as np
import pandas as pd
from pandera.typing import DataFrame

from core import Observations, Settings
from core import ChiSquareParams, NormalParams, StudentTParams
from distributions import (
    DensityGridInput,
    evaluate_density_grid,
    make_chi_square,
    make_normal,
    make_student_t,
)
from exercises import (
    IntervalContainsInput,
    NumericAnswerInput,
    verify_interval_contains,
    verify_numeric_answer,
)
from inference import (
    MeanKnownVarianceInput,
    MeanUnknownVarianceInput,
    OneSampleMeanTestInput,
    ProportionInput,
    SampleSizeForMeanInput,
    SampleSizeForProportionInput,
    VarianceInput,
    build_confidence_interval_for_mean_known_variance,
    build_confidence_interval_for_mean_unknown_variance,
    build_confidence_interval_for_proportion,
    build_confidence_interval_for_variance,
    sample_size_for_mean,
    sample_size_for_proportion,
    test_one_sample_mean,
)
from inference.hypothesis_tests import Alternative
from sampling import BootstrapInput, bootstrap_mean
from visualization import (
    BootstrapDistributionChartInput,
    DensityChartInput,
    chart_bootstrap_distribution,
    chart_density,
)
from widgets import (
    MeanCIExplorerInput,
    PivotInversionExplorerInput,
    build_mean_ci_explorer,
    build_pivot_inversion_explorer,
)
```

```{code-cell} python
:tags: [remove-cell]
settings = Settings()
```

(sec-inf-mean-known)=
## IC para la espera media con $\sigma$ conocido

### Intuición operativa

Tenemos $n = 36$ esperas con $\bar{x} = 12$ y, por datos históricos,
$\sigma = 3$. Buscamos un IC al 95%.

**Antes de calcular.** La responsable de operaciones no necesita un único
número puntual: necesita un rango defendible. Si duplicáramos $n$ manteniendo
la misma variabilidad histórica, ¿esperás que ese rango se ensanche o se
achique?

El intervalo no intenta adivinar el valor exacto de $\mu$. Construye una zona
razonable alrededor de lo observado, más ancha cuando hay más variabilidad o
menos datos, y más angosta cuando la muestra trae más información.

### Forma matemática

**Paso 1 — pivot.** Por la ecuación [](#eq-clt) sabemos que el
promedio estandarizado tiende a Normal estándar:

$$ Z = \frac{\bar{X} - \mu}{\sigma/\sqrt{n}} \sim \mathcal{N}(0, 1) $$ (eq-z-pivot)

Cuando reemplazamos las mayúsculas por los datos observados y por
$\mu_0$ de $H_0$, obtenemos un valor numérico $z_{\text{obs}}$; ese número
es el **$z$-statistic** del contraste (no un $z$-score descriptivo).

**Paso 2 — intervalo.** Despejamos $\mu$ usando el cuantil
$z_{1 - \alpha/2}$ definido en [](#eq-quantile):

$$ \bar{x} \;\pm\; z_{1 - \alpha/2}\,\frac{\sigma}{\sqrt{n}} $$ (eq-ci-mean-known)

**Paso 3 — números.** Con $z_{0{,}975} = 1{,}96$, $\sigma = 3$, $n = 36$:

$$ 12 \;\pm\; 1{,}96 \cdot \frac{3}{6} = 12 \;\pm\; 0{,}98 = (11{,}02,\ 12{,}98) $$

> **Contrato del modelo.** Este IC resume un procedimiento, no una certeza sobre
> un intervalo aislado. Necesita una muestra representativa, independencia y una
> distribución del promedio bien aproximada por la Normal; acá además asumimos
> $\sigma$ conocido. Si la muestra está sesgada, el intervalo puede ser preciso y
> aun así apuntar al lugar equivocado.

```{code-cell} python
clinic_known_input = MeanKnownVarianceInput(
    sample_mean=12.0,
    population_standard_deviation=3.0,
    sample_size=36,
)
clinic_known_interval = build_confidence_interval_for_mean_known_variance(clinic_known_input)
clinic_known_interval
```

### Qué quiere decir «95% de confianza»

### Intuición operativa

**No** es «el verdadero $\mu$ está con probabilidad 0,95 en este intervalo».
El verdadero $\mu$ es una constante. Lo aleatorio es la muestra y, por lo
tanto, el intervalo. La afirmación correcta es:

> Si repitiéramos este procedimiento muchas veces, **el 95% de los
> intervalos generados** contendría a $\mu$.

La exploración de abajo materializa esa idea: cada línea es un intervalo
construido sobre una muestra distinta. Antes de mover controles, anticipá qué
fracción de las líneas debería cubrir al verdadero $\mu$ y qué fracción debería
quedarse afuera. Con muchas réplicas el resultado debería acercarse al 95%
prometido por la construcción.

**Trampa común.** Después de ver un intervalo concreto, no decimos “hay 95% de
probabilidad de que $\mu$ esté adentro”. Decimos que el procedimiento que lo
produjo cubre a $\mu$ en el 95% de repeticiones comparables.

**Idea para retener.** La confianza vive en el procedimiento que genera
intervalos, no en una probabilidad subjetiva sobre un intervalo ya observado.

**No confundas.** Un intervalo de confianza frecuentista no es una probabilidad
posterior sobre $\mu$. Si querés decir “hay 95% de probabilidad de que el
parámetro esté en este rango”, necesitás un marco bayesiano con una distribución
previa. En este capítulo, el 95% pertenece al procedimiento repetido.

```{code-cell} python
ci_explorer_input = MeanCIExplorerInput(settings=settings)
build_mean_ci_explorer(ci_explorer_input)
```

(sec-inf-mean-unknown)=
## IC con $\sigma$ desconocido — la $t$ de Student

En la práctica casi nunca conocemos $\sigma$. Lo estimamos con el desvío
estándar muestral $s$ definido en [](#eq-std), y el pivote cambia: deja
de ser Normal.

La incertidumbre extra se ve mejor con una muestra chica. Si medimos pocas
esperas, $s$ también fluctúa de muestra a muestra; por eso la referencia debe
tener colas más pesadas que la Normal. La distribución $t$ de Student cumple ese
papel: se parece a una campana centrada en cero, pero deja más probabilidad en
valores extremos.

```{code-cell} python
standard_normal = make_normal(NormalParams())
student_reference = make_student_t(StudentTParams(degrees_of_freedom=11))

normal_density = evaluate_density_grid(DensityGridInput(distribution=standard_normal, settings=settings))
student_density = evaluate_density_grid(DensityGridInput(distribution=student_reference, settings=settings))

normal_chart_input = DensityChartInput(
    density_grid=normal_density,
    title="Normal estándar",
    settings=settings,
)
student_chart_input = DensityChartInput(
    density_grid=student_density,
    title="t de Student (11 g.l.)",
    settings=settings,
)
chart_density(normal_chart_input) | chart_density(student_chart_input)
```

**Paso 1.** Si las observaciones son Normales, vale:

$$ T = \frac{\bar{X} - \mu}{s/\sqrt{n}} \sim t_{n-1} $$ (eq-t-pivot)

**Paso 2.** Reemplazamos $z_{1 - \alpha/2}$ por $t_{n-1,\,1 - \alpha/2}$ en
[](#eq-ci-mean-known). Para $n$ grande la $t$ converge a la Normal y los dos IC coinciden.

El subíndice $n-1$ son los **grados de libertad**. La muestra tiene $n$
desvíos respecto de $\bar{x}$, pero esos desvíos deben sumar cero: una vez
conocidos $n-1$, el último queda forzado. Esa libertad perdida es el precio de
estimar $\sigma$ con $s$.

```{code-cell} python
clinic_unknown_input = MeanUnknownVarianceInput(
    sample_mean=12.0,
    sample_standard_deviation=3.0,
    sample_size=36,
)
clinic_unknown_interval = build_confidence_interval_for_mean_unknown_variance(clinic_unknown_input)
clinic_unknown_interval
```

(sec-inf-proportion)=
## IC para una proporción

En la encuesta, 200 de 400 dicen «sí». La proporción observada es
$\hat{p} = 0{,}5$. La analista que prepara el informe público sabe que
un titular con “50%” puede sonar definitivo, aunque la muestra todavía
tenga incertidumbre.

**Antes de calcular.** Si el analista quiere comunicar el resultado al barrio,
¿alcanza decir “ganó el sí por 50%” o hace falta decir cuánta incertidumbre
queda alrededor de ese 50%?

**Paso 1:** la Binomial subyacente [](#eq-binomial-pmf) tiene varianza
$np(1-p)$.

**Paso 2:** por el TCL [](#eq-clt-bin), $\hat{p}$ es aproximadamente Normal.

**Paso 3:** IC de Wald al $1 - \alpha$:

$$ \hat{p} \;\pm\; z_{1 - \alpha/2}\,\sqrt{\frac{\hat{p}(1 - \hat{p})}{n}} $$ (eq-ci-prop)

Este intervalo se llama **Wald**. Es rápido y funciona razonablemente cuando
$n$ es grande y $\hat p$ no queda demasiado cerca de 0 o 1. Si una encuesta
observa 3 éxitos en 100 casos, la aproximación Normal alrededor de $\hat p$ se
vuelve torpe: puede producir límites imposibles o demasiado optimistas. En esos
bordes conviene usar alternativas como Wilson; acá conservamos Wald porque
alcanza para mostrar el puente entre Binomial, TCL e intervalos.

```{code-cell} python
poll_input = ProportionInput(
    successes=200,
    sample_size=400,
)
poll_interval = build_confidence_interval_for_proportion(poll_input)
poll_interval
```

(sec-inf-variance)=
## IC para la varianza — la $\chi^2$

### Intuición operativa

Hasta acá todos los IC fueron sobre la **media**. Una pregunta muy
diferente —pero igual de operativa— pesa sobre la **dispersión**: la
clínica observó un desvío muestral de $3$ minutos sobre $36$ esperas.
¿Cuán lejos puede estar ese $s = 3$ del verdadero $\sigma$? La forma
del problema es la misma de antes —tomar un estimador, ver cómo
fluctúa muestra a muestra, invertir—, pero el estimador ahora es
$S^2$ y su distribución no es Normal.

**Antes de mirar.** Imaginá dos procesos con la misma media de espera:
uno casi siempre ronda los 12 minutos y otro alterna mañanas tranquilas
con demoras largas. Para Lucía, el segundo es más difícil de planificar.
Antes de escribir la fórmula, anticipá algo: ¿esperás un intervalo
simétrico alrededor de $s^2$ o uno deformado por la posibilidad de colas
largas?

La referencia que reemplaza a la Normal es la $\chi^2$. A diferencia de la $t$,
no está centrada en cero ni es simétrica: vive en valores positivos y se estira
hacia la derecha, justo lo que esperamos de una cantidad basada en cuadrados.

```{code-cell} python
chi_square_reference = make_chi_square(ChiSquareParams(degrees_of_freedom=35))
chi_square_density = evaluate_density_grid(
    DensityGridInput(distribution=chi_square_reference, settings=settings)
)
chi_square_chart_input = DensityChartInput(
    density_grid=chi_square_density,
    title="Referencia chi-cuadrado (35 g.l.)",
    settings=settings,
)
chart_density(chi_square_chart_input)
```

### Forma matemática

El resultado clave es que, para $X_i$ Normales con varianza
$\sigma^2$, la cantidad escalada

$$ \frac{(n-1)\,S^2}{\sigma^2} \sim \chi^2_{n-1} $$ (eq-chi-pivot)

sigue una distribución **chi-cuadrado** con $n - 1$ grados de
libertad — asimétrica y con cola pesada a derecha, muy distinta de la
Normal. Despejando $\sigma^2$ usando los cuantiles
$\chi^2_{n-1,\,\alpha/2}$ y $\chi^2_{n-1,\,1 - \alpha/2}$ obtenemos el
intervalo,

$$ \left(\frac{(n-1)\,s^2}{\chi^2_{n-1,\,1 - \alpha/2}},\ \frac{(n-1)\,s^2}{\chi^2_{n-1,\,\alpha/2}}\right) $$ (eq-ci-var)

que, por la asimetría de la $\chi^2$, ya **no** queda centrado en
$s^2$.

**En una frase.** Para la media preguntamos dónde está el centro; para la
varianza preguntamos cuán irregular puede ser el proceso, y esa incertidumbre
no crece igual hacia ambos lados.

Aplicado a la clínica con $s^2 = 9$ y $n = 36$:

```{code-cell} python
clinic_variance_input = VarianceInput(
    sample_variance=9.0,
    sample_size=36,
)
clinic_variance_interval = build_confidence_interval_for_variance(clinic_variance_input)
clinic_variance_interval
```

(sec-inf-pivot)=
## El método del pivote — por qué todos los IC tienen la misma forma

### Intuición operativa

Los tres intervalos anteriores parecen tres recetas distintas. La de la
Normal y la de la $t$ se escriben como **estadístico ± percentil × dispersión**;
la de la $\chi^2$ no — es un cociente con dos cuantiles distintos en el
numerador y el denominador. La pregunta natural es si hay una sola
construcción detrás de las tres, o si simplemente fueron apareciendo por
historia. La respuesta es la primera: hay una sola receta, llamada **método
del pivote**, y la forma "± percentil × dispersión" es lo que ocurre en un
caso particular.

La intuición es simple: buscamos una cantidad cuya distribución conozcamos aun
cuando el parámetro sea desconocido; después preguntamos para qué valores del
parámetro los datos observados caen en la zona central esperada.

### Forma matemática

### 1. Cantidad pivote

Una **cantidad pivote** es una función $Q(X_1, \dots, X_n;\,\theta)$ de los
datos y del parámetro de interés cuya distribución **no depende** de
$\theta$ ni de ningún otro parámetro desconocido. Es un concepto distinto
del de *estadístico*: un estadístico depende solo de los datos, mientras
que un pivote mezcla datos y parámetro pero su distribución vive en una
familia conocida — una $\mathcal{N}(0,1)$, una $t_{n-1}$, una $\chi^2_{n-1}$.

### 2. Construcción genérica

Como la distribución de $Q$ no depende de $\theta$, podemos elegir dos
cuantiles $a < b$ tales que

$$ P\!\left(a \le Q(\mathbf{X};\,\theta) \le b\right) = 1 - \alpha $$ (eq-pivot-mass)

para todo valor real del parámetro. Si para los datos observados
$\mathbf{x}$ la función $\theta \mapsto Q(\mathbf{x};\,\theta)$ es
estrictamente monótona, el conjunto

$$ \{\theta : a \le Q(\mathbf{x};\,\theta) \le b\} $$ (eq-pivot-set)

es un intervalo. Por construcción, ese intervalo (aleatorio antes de
mirar los datos) cubre a $\theta$ con probabilidad $1-\alpha$. Esa es la
definición de **intervalo de confianza al $1-\alpha$**.

> **Lema de inversión monótona.** Si $g(\theta) = Q(\mathbf{x};\,\theta)$
> es estrictamente decreciente en $\theta$, entonces
> $a \le g(\theta) \le b \iff g^{-1}(b) \le \theta \le g^{-1}(a)$, así que
> el intervalo en $\theta$ existe y la masa $1-\alpha$ se preserva. El
> caso creciente es simétrico. La monotonía es lo único que se le pide al
> pivote para que la receta funcione.

### 3. Caso lineal: de dónde sale "± percentil × dispersión"

Supongamos que el pivote tiene la forma especial

$$ Q(\mathbf{X};\,\theta) = \frac{\hat\theta - \theta}{\widehat{SE}} $$ (eq-pivot-linear)

con $\hat\theta$ un estimador puntual y $\widehat{SE}$ una estimación de
su error estándar (ambos funciones solo de los datos). Esa $Q$ es lineal
en $\theta$, así que despejarla de $a \le Q \le b$ es inmediato:

$$ \hat\theta - b\,\widehat{SE} \;\le\; \theta \;\le\; \hat\theta - a\,\widehat{SE} $$ (eq-pivot-linear-bounds)

Si además la distribución de referencia es **simétrica alrededor de cero**,
los cuantiles cumplen $a = -q_{1-\alpha/2}$ y $b = q_{1-\alpha/2}$, y el
intervalo colapsa en

$$ \hat\theta \;\pm\; q_{1-\alpha/2}\,\widehat{SE} $$ (eq-pivot-symmetric)

Esa es la forma **estadístico ± percentil × dispersión**. No es una ley
estadística — es la consecuencia algebraica de combinar dos supuestos:
*pivote afín en $\theta$* y *referencia simétrica*. Cualquier pivote que
cumpla las dos condiciones produce esa forma.

### 4. Las tres recetas, una sola construcción

| Caso | Pivote $Q$ | ¿Lineal en θ? | Referencia | ¿Simétrica? | Forma del IC |
| --- | --- | --- | --- | --- | --- |
| Normal con $\sigma$ conocido [](#eq-z-pivot) | $\dfrac{\bar X - \mu}{\sigma/\sqrt n}$ | Sí | $\mathcal{N}(0,1)$ | Sí | $\bar x \pm z_{1-\alpha/2}\,\sigma/\sqrt n$ |
| $t$ de Student [](#eq-t-pivot) | $\dfrac{\bar X - \mu}{s/\sqrt n}$ | Sí | $t_{n-1}$ | Sí | $\bar x \pm t_{n-1,\,1-\alpha/2}\,s/\sqrt n$ |
| Wald para proporción [](#eq-ci-prop) | $\dfrac{\hat p - p}{\sqrt{\hat p(1-\hat p)/n}}$ | Sí (asintóticamente) | $\mathcal{N}(0,1)$ | Sí | $\hat p \pm z_{1-\alpha/2}\sqrt{\hat p(1-\hat p)/n}$ |
| $\chi^2$ para varianza [](#eq-chi-pivot) | $\dfrac{(n-1)S^2}{\sigma^2}$ | **No**: $\sigma^2$ está en el denominador | $\chi^2_{n-1}$ | **No**: asimétrica | $\bigl((n-1)s^2/\chi^2_{n-1,\,1-\alpha/2},\ (n-1)s^2/\chi^2_{n-1,\,\alpha/2}\bigr)$ |

Las primeras tres filas comparten la misma plantilla porque comparten los
dos supuestos. La $\chi^2$ rompe **ambos**: el pivote es monótono pero no
afín en $\sigma^2$, y la referencia no es simétrica. Aplicar la receta
genérica [](#eq-pivot-mass)–[](#eq-pivot-set) sigue siendo legal, pero la
inversión es multiplicativa, no aditiva: $a \le (n-1)s^2/\sigma^2 \le b$
equivale a $(n-1)s^2/b \le \sigma^2 \le (n-1)s^2/a$. De ahí la asimetría
del intervalo respecto de $s^2$.

### 5. La intuición en una frase

Toda la familia de IC vistos es la misma receta — encontrar un pivote,
fijar dos cuantiles, despejar el parámetro — vista a través de tres
casos. La forma "± percentil × dispersión" no es la regla general; es lo
que pasa cuando el pivote es afín en $\theta$ y la distribución de
referencia es simétrica. Cuando esos dos supuestos fallan, como en la
$\chi^2$, la misma receta sigue funcionando pero produce un intervalo
asimétrico.

**Idea para retener.** Un pivote convierte “no conozco el parámetro” en “sí
conozco la distribución de esta cantidad”, y esa es la palanca para despejar un
intervalo.

**Punto de control.** Cuando aparezca un IC nuevo, preguntá tres cosas antes de
memorizar la receta: cuál es el estimador, cuál es el pivote y qué supuesto hace
conocida su distribución. Si podés responder eso, la fórmula deja de ser una
plantilla suelta.

**Antes de mirar.** En el explorador de abajo, antes de mover los controles
anticipá: si subo $1-\alpha$ del 80% al 99%, ¿qué pasa con los cuantiles
$a, b$ y, en consecuencia, con el ancho del IC? ¿Y si cambio de Normal a
$\chi^2$ manteniendo $1-\alpha$ y $n$ fijos: cuál panel se queda igual y
cuál cambia de forma?

> **Trampa común.** El nivel $1-\alpha$ vive en el procedimiento, no en un
> intervalo concreto. La receta garantiza que la probabilidad asignada al
> pivote sea $1-\alpha$; lo que el intervalo concreto haga con esa masa una
> vez que vimos los datos depende de la muestra que tocó.

```{code-cell} python
pivot_explorer_input = PivotInversionExplorerInput(
    settings=settings,
    sample_mean=12.0,
    sample_standard_deviation=3.0,
)
build_pivot_inversion_explorer(pivot_explorer_input)
```

(sec-inf-test)=
## Test de hipótesis sobre la espera media

### Intuición operativa

El manual de operaciones afirma que la espera media en la línea de
inspección debería ser 11 minutos. Observamos $\bar{x} = 12$, $s = 3$,
$n = 36$.

**Antes de calcular.** Una diferencia de un minuto puede ser operativamente
importante o irrelevante según el proceso. Separá dos preguntas: ¿hay evidencia
estadística contra el valor de control? y ¿la diferencia importa en la práctica?

Un test no decide por sí solo qué hacer. Ordena una pregunta más acotada: si el
valor de control fuera cierto, ¿sería raro ver una muestra tan alejada como la
que observamos?

### Forma matemática

$$ H_0: \mu = 11 \qquad H_1: \mu \neq 11 \qquad \alpha = 0{,}05 $$

Antes de calcular, fijamos la dirección de la alternativa. Si cualquier cambio
respecto de 11 minutos importa, usamos un test **bilateral**: reparte la región
rara entre las dos colas. Si solo preocupa que la espera aumente, usamos un test
**unilateral**: concentra la región rara en la cola derecha. Elegir la dirección
después de mirar los datos rompe el acuerdo del test.

**Paso 1.** Estadístico de prueba (mismo pivote [](#eq-t-pivot)):

$$ T = \frac{\bar{X} - \mu_0}{s/\sqrt{n}} $$ (eq-t-test)

Acá el nombre correcto es **$t$-statistic** porque usamos $s$ y la
referencia es la distribución $t$. El nombre **$z$-statistic** se reserva
para contrastes cuyo estadístico sigue la Normal estándar bajo $H_0$.

**Paso 2.** Calculamos el $p$-valor en la $t_{n-1}$ y rechazamos si es
menor a $\alpha$. El $p$-valor es un área de cola: mide qué tan raro sería ver
un estadístico tan extremo como el observado, o más, si $H_0$ fuera correcto.
En un test bilateral el área aparece en las dos colas; en uno unilateral aparece
solo en la dirección definida por $H_1$.

**En una frase.** Un test pregunta si los datos serían raros si el valor de
control fuera cierto; no mide por sí solo cuánto cuesta el desvío ni qué acción
conviene tomar.

Dos errores acompañan siempre esta decisión:

| Realidad del proceso | Decisión del test | Nombre del error |
| --- | --- | --- |
| $H_0$ era cierta | Rechazamos $H_0$ | Tipo I: falsa alarma |
| $H_0$ era falsa | No rechazamos $H_0$ | Tipo II: no detectar el cambio |

En ingeniería, elegir $\alpha$ es elegir cuánto peso le damos al error tipo I.
Un $\alpha$ más chico exige evidencia más extrema para actuar, pero puede hacer
más fácil pasar por alto cambios reales.

> **Contrato del modelo.** Un test de hipótesis sirve para medir si los datos
> serían raros bajo un valor de control. Necesita que el estadístico de prueba
> tenga la distribución asumida, una alternativa fijada antes de mirar el
> resultado y una muestra representativa del proceso. Rechazar no mide el tamaño
> del problema; no rechazar no prueba que el proceso esté perfecto.

```{code-cell} python
factory_test_input = OneSampleMeanTestInput(
    sample_mean=12.0,
    sample_standard_deviation=3.0,
    sample_size=36,
    null_mean=11.0,
    alternative=Alternative.TWO_SIDED,
)
factory_test_result = test_one_sample_mean(factory_test_input)
factory_test_result
```

### Conexión IC ↔ test

Un test bilateral al nivel $\alpha$ rechaza $H_0: \mu = \mu_0$ **sí y solo
sí** $\mu_0$ no cae dentro del IC al nivel $1 - \alpha$ construido sobre la
misma muestra (ecuaciones [](#eq-ci-mean-known) y [](#eq-t-pivot)). Es el
mismo objeto visto desde dos ángulos.

Visualmente, imaginá el IC como una regla apoyada sobre la recta de valores
posibles para $\mu$. Si el valor de control cae dentro de la regla, los datos
son compatibles con ese valor al nivel elegido. Si queda afuera, el mismo
desplazamiento que lo excluye del intervalo empuja el estadístico hacia la cola
de rechazo.

**Trampa común.** Un $p$-valor chico no mide el tamaño del problema ni la
probabilidad de que $H_0$ sea cierta. Mide cuán raro sería ver un resultado tan
extremo, o más, si el valor de control fuera correcto.

**Idea para retener.** El $p$-valor mide sorpresa bajo una hipótesis, no tamaño
del efecto ni probabilidad de que la hipótesis sea verdadera.

**No confundas.** Significancia estadística y decisión de ingeniería se cruzan,
pero no son lo mismo. Un efecto pequeño puede ser estadísticamente claro y aun
así irrelevante para operar; un efecto grande puede ser importante aunque la
muestra todavía no alcance para demostrarlo con bajo riesgo de error.

(sec-inf-bootstrap)=
## Bootstrap sin supuestos paramétricos

Cuando no queremos asumir Normalidad ni conocer $\sigma$, podemos
**remuestrear**: tomar muchas muestras con reemplazo del conjunto observado
y mirar la distribución de las medias bootstrap. La idea práctica es tratar el
único turno medido como una pequeña población plausible y preguntar qué medias
aparecen al recombinar esos datos muchas veces. El IC sale de los percentiles.

**Antes de mirar.** Si la muestra original tiene mucha dispersión, ¿esperás que
la distribución bootstrap de la media sea angosta o ancha?

El procedimiento es mecánico:

1. Tomar una muestra bootstrap del mismo tamaño que la original, con reemplazo.
2. Calcular su media.
3. Repetir miles de veces.
4. Usar los percentiles 2,5 y 97,5 de esas medias como intervalo al 95%.

> **Contrato del modelo.** El bootstrap usa la muestra observada como sustituto
> de la población. Es útil cuando no querés imponer una forma paramétrica, pero
> depende de que la muestra represente bien al proceso. Si faltan casos raros,
> hay dependencia temporal fuerte o el muestreo original estuvo sesgado, el
> remuestreo repite esos problemas.

```{code-cell} python
rng_bootstrap = np.random.default_rng(settings.random_seed)
synthetic_sample = pd.DataFrame({
    "value": rng_bootstrap.normal(loc=12.0, scale=3.0, size=36)
}).pipe(DataFrame[Observations])
bootstrap_input = BootstrapInput(
    observations=synthetic_sample,
    replicates=3_000,
    settings=settings,
)
bootstrap_result = bootstrap_mean(bootstrap_input)

bootstrap_chart_input = BootstrapDistributionChartInput(
    bootstrap_result=bootstrap_result,
    title="Distribución bootstrap de la media",
    settings=settings,
)
chart_bootstrap_distribution(bootstrap_chart_input)
```

(sec-inf-sample-size)=
## Tamaño muestral para una precisión dada

**Para la media.** La pregunta ahora se invierte: no “qué precisión consigo
con estos datos”, sino “cuántos datos necesito para prometer cierta precisión”.
Antes de despejar, anticipá la dirección: pedir la mitad del margen de error
requiere bastante más que el doble de observaciones.

Despejando $n$ de la fórmula [](#eq-ci-mean-known) con margen de error $E$ y
$z_{1 - \alpha/2}$:

$$ n \ge \left(\frac{z_{1 - \alpha/2}\,\sigma}{E}\right)^2 $$ (eq-n-mean)

Para la clínica con $\sigma = 3$, $E = 1$ y 95%: $n \ge (1{,}96 \cdot 3)^2 \approx 35$.

> **Contrato del modelo.** Una fórmula de tamaño muestral promete precisión bajo
> supuestos: variabilidad razonablemente conocida, muestreo representativo y el
> mismo nivel de confianza que se comunicará después. Si la variabilidad real es
> mayor o la muestra no representa al proceso, el margen de error prometido queda
> demasiado optimista.

**Lectura operativa.** El tamaño muestral no es una meta moral de “más datos
siempre mejor”. Es una negociación explícita entre precisión, costo, plazo y
riesgo de comunicar una conclusión demasiado ajustada.

```{code-cell} python
clinic_sample_size_input = SampleSizeForMeanInput(
    population_standard_deviation=3.0,
    margin_of_error=1.0,
)
clinic_sample_size = sample_size_for_mean(clinic_sample_size_input)
clinic_sample_size
```

**Para una proporción.** Despejando $n$ de [](#eq-ci-prop) con $\hat{p} = 0{,}5$
(peor caso, varianza máxima):

El peor caso no es una superstición: la varianza de una Bernoulli es
$p(1-p)$, y esa parábola alcanza su máximo en $p=0{,}5$. Si no sabemos de
antemano dónde estará la proporción, diseñar con 0,5 produce el tamaño muestral
más conservador.

$$ n \ge \left(\frac{z_{1 - \alpha/2}}{E}\right)^2 \hat{p}(1 - \hat{p}) $$ (eq-n-prop)

```{code-cell} python
poll_sample_size_input = SampleSizeForProportionInput(
    estimated_proportion=0.5,
    margin_of_error=0.03,
)
poll_sample_size = sample_size_for_proportion(poll_sample_size_input)
poll_sample_size
```

## Ejercicio 1 — IC contiene un valor de control

Construí un IC al 95% para $\mu$ con $\bar{x} = 12$, $\sigma = 3$,
$n = 36$. Verificá que contenga el valor de control $\mu_0 = 11{,}5$.

**Predicción.** Estimá primero el margen de error. Si el intervalo queda
centrado en 12, ¿esperás que 11,5 caiga adentro o afuera?

**Cómputo.** Construí el intervalo y ejecutá la verificación.

**Interpretación.** Si el valor de control cae dentro del intervalo, la
decisión prudente no es “probamos que el control es verdadero”, sino “estos
datos no lo descartan al nivel usado”.

**Comunicación.** Escribí una frase para un informe operativo que mencione el
rango, el valor de control y la incertidumbre sin convertir el IC en una certeza.

```{code-cell} python
exercise_known_input = MeanKnownVarianceInput(
    sample_mean=12.0,
    population_standard_deviation=3.0,
    sample_size=36,
)
exercise_interval = build_confidence_interval_for_mean_known_variance(exercise_known_input)
interval_contains_input = IntervalContainsInput(
    lower_bound=exercise_interval.lower_bound,
    upper_bound=exercise_interval.upper_bound,
    target_value=11.5,
)
verify_interval_contains(interval_contains_input)
```

## Ejercicio 2 — Tamaño muestral para una proporción

La encuesta quiere margen de error de ±3% al 95% de confianza, usando
$\hat{p} = 0{,}5$ (peor caso).

**Intentá antes de ejecutar.** Antes de calcular, anticipá el orden de
magnitud: ¿decenas, cientos o más de mil personas? Después aplicá [](#eq-n-prop)
y verificá.

**Decisión de ingeniería.** Si bajar el margen de error exige muchas más
respuestas, la pregunta deja de ser solo estadística: ¿vale el costo adicional
para la decisión que se quiere tomar?

```{code-cell} python
exercise_proportion_input = SampleSizeForProportionInput(
    estimated_proportion=0.5,
    margin_of_error=0.03,
)
expected_size = sample_size_for_proportion(exercise_proportion_input).required_sample_size

student_answer_size = 1067.0
verify_input = NumericAnswerInput(
    student_answer=student_answer_size,
    expected_answer=float(expected_size),
)
verify_numeric_answer(verify_input)
```

## Ejercicio 3 — Intervalo para la variabilidad

Volvé al IC para la varianza de la clínica, construido con $s^2 = 9$ y $n = 36$.

**Predicción.** Antes de mirar el resultado, decidí si el intervalo debería quedar simétrico alrededor de 9 o más estirado hacia uno de los lados.

**Cómputo.** Usá [](#eq-ci-var) o inspeccioná el objeto calculado más arriba.

**Interpretación.** Traducí el intervalo a una frase sobre regularidad del servicio: no estamos preguntando si la espera típica cambió, sino cuán variable puede ser el proceso.

**Decisión de ingeniería.** Si el extremo superior fuera demasiado alto para planificar personal, ¿actuarías sobre la media, sobre la variabilidad o pedirías una muestra más representativa?

```{code-cell} python
clinic_variance_interval
```

## Ejercicio 4 — Test unilateral para una demora

Supongamos que el problema operativo no es cualquier cambio respecto de 11 minutos, sino específicamente que la espera media haya **aumentado**. Con los mismos datos, planteá un test unilateral.

**Predicción.** Antes de ejecutar, decidí si usarías $H_1: \mu > 11$ o $H_1: \mu < 11$. La dirección tiene que salir de la pregunta de ingeniería, no del resultado observado.

**Cómputo.** Ejecutá el test unilateral y comparalo con el bilateral anterior.

**Comunicación.** Escribí una frase que separe evidencia estadística de impacto operativo: incluso si hay evidencia de aumento, Lucía todavía necesita decidir si el aumento justifica cambiar personal o medir más.

```{code-cell} python
one_sided_test_input = OneSampleMeanTestInput(
    sample_mean=12.0,
    sample_standard_deviation=3.0,
    sample_size=36,
    null_mean=11.0,
    alternative=Alternative.GREATER,
)
one_sided_test_result = test_one_sample_mean(one_sided_test_input)
one_sided_test_result
```

(sec-inf-capstone)=
## Capstone — un memo con incertidumbre

Volvé a la sala de espera. Lucía tiene una semana de mediciones, una queja del
equipo médico por demoras en la primera franja de la mañana y presupuesto para
hacer **una** de tres cosas: sumar una persona, rediseñar turnos o medir una
semana más antes de decidir.

Escribí un memo breve, de no más de cinco frases, que combine el recorrido del
libro:

1. **Descripción.** ¿Qué resumen mirarías primero: media, mediana, dispersión u
   outliers? Justificá qué pregunta contesta.
2. **Modelo.** Si querés anticipar esperas futuras, ¿qué familia usarías como
   primera aproximación y qué supuesto revisarías antes de confiar en ella?
3. **Incertidumbre.** ¿Comunicarías un intervalo, un test o un tamaño muestral?
   Explicá qué decisión sostiene.
4. **Recomendación.** Terminá con una frase operativa: actuar ahora, medir más o
   cambiar el proceso, dejando explícito qué incertidumbre queda.

El objetivo no es encontrar “la” respuesta correcta. Es practicar la habilidad
más difícil de la estadística aplicada: convertir un cálculo honesto en una
decisión comunicable.

### Dos cierres posibles para el memo

Una formulación cuidadosa podría decir: “Con los datos disponibles, la espera media parece estar por encima del objetivo y el intervalo sugiere que la diferencia puede ser operativamente relevante; recomiendo reforzar la franja de la mañana mientras medimos una semana adicional para confirmar que el patrón no fue excepcional”.

Una formulación demasiado fuerte sería: “Quedó demostrado que el sistema está mal y hay que contratar más personal”. El problema no es la decisión, sino la certeza excesiva: borra el margen de error, los supuestos de muestreo y la posibilidad de que el proceso haya cambiado solo durante la semana observada.

**Comunicación.** Un buen memo estadístico no evita tomar posición: toma una
posición honesta. Dice qué muestran los datos, qué supuesto sostiene esa lectura
y qué incertidumbre queda viva.

## Cierre del recorrido

**Ahora podemos** recorrer un ciclo completo entre datos y parámetros. La sala
de espera empezó como una muestra de minutos resumida en un boxplot, terminó
modelada como Exponencial, su promedio diario apareció junto al teorema central
del límite y la espera media tuvo, finalmente, un intervalo de confianza. La
encuesta pasó de conteo a Bayes, de Bayes a Binomial, de Binomial a proporción
asintóticamente Normal y de ahí a un IC con tamaño muestral. La línea de
producción pasó de defectos por turno a Bin/Poisson, a aproximación Normal y a
un test de hipótesis.

**Lo que todavía falta** es mirar problemas donde un solo parámetro ya no
alcanza. La espera puede depender de la edad del paciente, la franja horaria o
el día de la semana; las creencias sobre un parámetro pueden actualizarse como
una distribución completa; las observaciones pueden llegar en orden temporal y
hacer que el orden importe.

**Las preguntas que quedan abiertas** empujan a regresión, estadística
bayesiana y series de tiempo. Cada hilo arranca exactamente donde este libro
termina: con un IC, un $p$-valor o un tamaño de muestra como punto de partida,
y con la misma obligación de comunicar incertidumbre sin esconderla.

Si necesitás repasar **símbolos** o **términos**, el [glosario](glossary.md)
tiene tablas con todo lo que apareció. Si querés revisar **cómo está
construido pedagógicamente el libro**, el apéndice de
[enfoque pedagógico](pedagogy.md) explica la progresión que recorrieron las
secciones.
