---
title: Variables aleatorias
kernelspec:
  name: python3
  display_name: Python 3
---

La maquinaria del capítulo anterior repartía probabilidad entre
resultados que se podían enumerar uno por uno: una caja con bolas,
un test que da positivo o negativo, una cara del dado. Pero ningún
paciente espera exactamente «uno» o «dos» minutos — espera $3{,}71$,
espera $2{,}089$, espera lo que mida el cronómetro. Y si preguntamos
«¿qué tan probable es que el próximo espere exactamente $4{,}2$
minutos?», la respuesta técnica es cero: cada valor puntual de una
espera real tiene probabilidad cero, y sin embargo claramente algunos
minutos son más esperables que otros.

¿Cómo se le asigna probabilidad a una espera cualquiera sin listar los
infinitos minutos posibles?, ¿qué objeto matemático modela «cantidad
de defectos por turno» o «respuestas afirmativas en una tanda» de
manera que ya traiga incorporados un promedio y un desvío?, ¿por qué
tantos fenómenos disímiles terminan compartiendo una misma forma
acampanada? Para un equipo de ingeniería, la decisión no es elegir la
fórmula más cómoda: es elegir un modelo que represente bien el fenómeno
antes de calcular riesgos, capacidades o promesas de servicio.

**Antes de seguir.** Recordá qué era un evento, qué significa
condicionar sobre información nueva y por qué en una variable continua
la pregunta “exactamente este valor” va a necesitar una idea distinta.

Las respuestas viven en la noción de **variable aleatoria** y en su
**distribución** — un peldaño más arriba de la probabilidad sobre
eventos sueltos, donde la cuenta pasa a hacerse sobre intervalos
enteros.

> **Situación de decisión.** El equipo ya no pregunta solo si un evento ocurre:
> necesita elegir un modelo para esperas, defectos o respuestas antes de
> prometer tiempos, estimar riesgos o definir umbrales de alerta. Elegir mal la
> distribución puede hacer que una decisión parezca precisa cuando solo estaba
> apoyada en un modelo conveniente.
> Al final del capítulo vas a poder elegir entre modelos discretos y continuos,
> leer probabilidades como barras o áreas, y explicar qué resumen del modelo
> sirve para una decisión sin confundir valor esperado con resultado más probable.

```{code-cell} python
:tags: [hide-input]
from core import (
    BinomialParams,
    ExponentialParams,
    GeometricParams,
    NormalParams,
    PoissonParams,
    Settings,
)
from distributions import (
    DensityGridInput,
    MomentsInput,
    ProbabilityMassInput,
    QuantileInput,
    TailProbabilityInput,
    compute_numeric_moments,
    evaluate_density_grid,
    evaluate_probability_mass,
    make_binomial,
    make_exponential,
    make_geometric,
    make_normal,
    make_poisson,
    quantile_of_continuous,
    tail_probability_of_continuous,
)
from exercises import NumericAnswerInput, verify_numeric_answer
from symbolic import (
    compute_binomial_moments,
    compute_poisson_moments,
    standardize_normal,
)
from visualization import (
    DensityChartInput,
    ProbabilityMassChartInput,
    chart_density,
    chart_probability_mass,
)
from widgets import (
    ContinuousDistributionExplorerInput,
    DiscreteDistributionExplorerInput,
    build_continuous_distribution_explorer,
    build_discrete_distribution_explorer,
)
```

```{code-cell} python
:tags: [remove-cell]
settings = Settings()
```

(sec-rv-distribution)=
## De eventos sueltos a distribuciones

Una **variable aleatoria** traduce resultados posibles a números. La respuesta
de una persona puede codificarse como $1$ si dice «sí» y $0$ si dice «no»; el
conteo de defectos de un turno puede ser $0,1,2,\dots$; una espera puede tomar
cualquier valor real no negativo.

La **distribución** de esa variable dice cómo se reparte la probabilidad sobre
esos números. Si la variable es discreta, usamos una PMF (*probability mass
function*): cada barra tiene una probabilidad concreta, como $P(X=k)$. Si la
variable es continua, usamos una PDF o densidad: la curva no da probabilidades
puntuales, sino áreas sobre intervalos.

Hay una tercera mirada que aparece todo el tiempo: la CDF o función de
distribución acumulada,

$$ F_X(x) = P(X \le x) $$ (eq-cdf)

La CDF responde «¿qué proporción queda hasta acá?», igual que una ojiva pero en
lenguaje probabilístico. Su complemento,

$$ S_X(x) = P(X > x) = 1 - F_X(x) $$ (eq-survival)

se llama **función de supervivencia** o cola derecha. En esperas, $S_X(5)$
pregunta qué chance queda de superar cinco minutos.

**Idea para retener.** En una discreta sumás barras; en una continua medís
áreas. La CDF traduce ambas historias a “cuánto queda acumulado hasta acá”.

**No confundas.** Una PMF asigna probabilidad a valores puntuales; una PDF
asigna densidad y necesita intervalos para producir probabilidades; una CDF
acumula lo que queda a la izquierda de un corte. Si la pregunta dice
“exactamente”, “entre” o “hasta”, ya te está señalando qué objeto mirar.

(sec-rv-bernoulli)=
## Una respuesta sí/no: Bernoulli

Antes de contar muchos defectos o muchas respuestas afirmativas, miremos una
sola observación. Una persona de la encuesta dice «sí» con probabilidad $p$ y
«no» con probabilidad $1-p$. Si codificamos «sí» como $1$ y «no» como $0$, la
variable $X$ sigue una **Bernoulli**:

$$ P(X=1)=p,\qquad P(X=0)=1-p $$ (eq-bernoulli-pmf)

```{code-cell} python
single_response = make_binomial(BinomialParams(trials=1, success_probability=0.55))
single_response_mass = evaluate_probability_mass(
    ProbabilityMassInput(distribution=single_response, lower_outcome=0, upper_outcome=1)
)

single_response_chart_input = ProbabilityMassChartInput(
    probability_mass=single_response_mass,
    title="Una respuesta de encuesta — Bernoulli(0.55)",
    settings=settings,
)
chart_probability_mass(single_response_chart_input)
```

La Bernoulli es el ladrillo básico: suma muchas Bernoullis independientes con
la misma probabilidad $p$ y aparece una Binomial. Esa frase será importante más
adelante, cuando el teorema central del límite explique por qué muchos ladrillos
pequeños terminan pareciendo una campana.

(sec-rv-binomial)=
## Contar defectos con una Binomial

Volvamos a un turno de la línea de producción. Antes de la auditoría
del proveedor, el equipo de calidad necesita saber qué conteos de
defectos serían normales y cuáles justificarían detener el proceso.
Inspeccionamos $n = 50$ piezas, y cada una, **independientemente** de
las demás, tiene una chance de $p = 0{,}05$ de salir defectuosa. La
cantidad de piezas defectuosas que vamos a encontrar al final del turno
la llamamos $X$. Es un número entero entre 0 y 50, y a cada valor
posible le corresponde alguna probabilidad: ¿cuál es la chance de
encontrar exactamente cero?, ¿de encontrar tres?, ¿de encontrar diez?
La respuesta entera es una **distribución de probabilidad** — una tabla
que dice, para cada $k$ posible, cuán probable es ese resultado.

**Antes de mirar.** Con $50$ piezas y una probabilidad de defecto de apenas
$0{,}05$, ¿dónde esperás que estén las barras más altas: cerca de cero,
cerca de veinticinco o hacia el extremo derecho? Hacé esa predicción antes de
ver la distribución.

Antes de escribir cualquier fórmula, miremos cómo se ve.

```{code-cell} python
factory_distribution = make_binomial(BinomialParams(trials=50, success_probability=0.05))
factory_mass_input = ProbabilityMassInput(
    distribution=factory_distribution,
    lower_outcome=0,
    upper_outcome=12,
)
factory_mass = evaluate_probability_mass(factory_mass_input)

factory_chart_input = ProbabilityMassChartInput(
    probability_mass=factory_mass,
    title="Defectos en 50 inspecciones — Bin(50, 0.05)",
    settings=settings,
)
chart_probability_mass(factory_chart_input)
```

Tres lecturas saltan de la imagen. La barra más alta se para en $k = 2$
o $k = 3$ defectos: ese es el resultado más probable de un turno
típico. Cero defectos sigue siendo raro pero no imposible. Y a partir
de unos siete u ocho defectos las barras se vuelven prácticamente
invisibles — encontrar más de diez sería un turno excepcional. El gráfico
adelanta lo que el promedio teórico va a confirmar:
$50 \cdot 0{,}05 = 2{,}5$ defectos esperados por turno.

Pongamos un número más a esa intuición: ¿qué probabilidad hay de
encontrar **a lo sumo 5** defectos?

```{code-cell} python
factory_at_most_five = float(factory_distribution.frozen_distribution.cdf(5))
factory_at_most_five
```

Casi $97\,\%$ de los turnos tienen cinco o menos defectos. La cola
derecha de la distribución pesa muy poco: llegar a diez defectos sería
un turno excepcional.

### El motor detrás del gráfico

Cada barra del gráfico es un número concreto: la probabilidad de que
$X$ sea exactamente $k$. ¿De dónde sale ese número? Para que ocurran
exactamente $k$ defectos, hace falta que **algunas $k$ piezas** salgan
defectuosas y las **otras $n - k$** salgan buenas. Probabilidad de un
patrón concreto: $p^{k}(1 - p)^{n - k}$. Pero hay $\binom{n}{k}$
patrones distintos que dan ese mismo total de defectos (todas las
formas de elegir cuáles $k$ piezas son las defectuosas), así que la
probabilidad total de ver $k$ defectos es la suma de todos esos
patrones equivalentes:

$$ P(X = k) = \binom{n}{k}\,p^{k}\,(1 - p)^{n - k},\quad k = 0, 1, \dots, n $$ (eq-binomial-pmf)

Cuando el gráfico tira la barra de $k = 3$, la altura concreta sale
de evaluar [](#eq-binomial-pmf): $\binom{50}{3}(0{,}05)^{3}(0{,}95)^{47}$
$\approx 0{,}22$. Cada barra del gráfico es exactamente ese cálculo.

> **Contrato del modelo.** La Binomial aplica cuando contás éxitos en un número
> fijo de intentos, con la misma probabilidad $p$ en cada intento y resultados
> independientes. Si la probabilidad cambia durante el turno, o las piezas se
> afectan entre sí, el conteo puede parecer Binomial pero contar otra historia.

### Esperanza y varianza

La esperanza y la varianza de la Binomial tienen formas
particularmente limpias: $E[X] = np$ (los $2{,}5$ defectos esperados
que ya leímos del gráfico) y $\mathrm{Var}(X) = np(1-p)$. Conviene
verlas calculadas una vez tanto en su forma simbólica como evaluadas
sobre los parámetros concretos de la fábrica:

```{code-cell} python
factory_moments_symbolic = compute_binomial_moments(BinomialParams(trials=50, success_probability=0.05))
factory_moments_symbolic
```

```{code-cell} python
factory_moments_input = MomentsInput(distribution=factory_distribution)
factory_moments_numeric = compute_numeric_moments(factory_moments_input)
factory_moments_numeric
```

La barra más alta de una PMF se llama **moda**: es el valor individual más
probable. La esperanza, en cambio, es un promedio de largo plazo. En una
distribución simétrica pueden estar cerca; en distribuciones asimétricas o
discretas no tienen por qué coincidir. En la fábrica esperamos $2{,}5$
defectos, aunque ningún turno pueda tener medio defecto.

**Punto de control.** Si tenés que planificar capacidad, preguntá por la
esperanza; si tenés que anticipar el caso individual más común, mirá la moda; si
tenés que fijar un umbral de alerta, mirá una cola o un cuantil.

(sec-rv-geometric)=
## Esperar hasta el primer éxito: Geométrica

La Binomial fija de antemano la cantidad de intentos y pregunta cuántos éxitos
aparecen. Otra pregunta común invierte el reloj: si cada llamada tiene
probabilidad $p$ de lograr una respuesta válida, ¿cuántas llamadas hacen falta
hasta conseguir la primera?

Esa variable sigue una **Geométrica**. Si $G$ cuenta el número de intento en el
que aparece el primer éxito,

$$ P(G=k) = (1-p)^{k-1}p,\quad k=1,2,\dots $$ (eq-geometric-pmf)

```{code-cell} python
call_distribution = make_geometric(GeometricParams(success_probability=0.20))
call_mass = evaluate_probability_mass(
    ProbabilityMassInput(distribution=call_distribution, lower_outcome=1, upper_outcome=15)
)

call_chart_input = ProbabilityMassChartInput(
    probability_mass=call_mass,
    title="Llamadas hasta la primera respuesta — Geométrica(0.20)",
    settings=settings,
)
chart_probability_mass(call_chart_input)
```

Antes de mirar la fórmula, la forma ya dice bastante: el primer intento es el
más probable, pero la cola derecha recuerda que a veces se encadenan varios
fracasos. La Geométrica es a intentos discretos lo que la Exponencial será a
tiempos continuos de espera.

(sec-rv-normal)=
## Alturas con la Normal

Cambiamos de escenario para encontrarnos con la distribución más
famosa de la estadística. Pensemos en la **altura adulta** de una
población medida en centímetros: la mayoría de la gente cae en torno
a un valor central, alturas muy bajas y muy altas son cada vez más
raras a medida que nos alejamos de ese centro, y la dispersión
alrededor del centro se siente bastante simétrica. Tomemos como
referencia un promedio de $170$ cm y un desvío de $8$ cm. Antes de
ponerle nombre formal al modelo, dibujemos cuánta densidad de gente
se concentra en cada altura posible.

```{code-cell} python
heights_distribution = make_normal(NormalParams(mean=170.0, standard_deviation=8.0))
heights_density_input = DensityGridInput(
    distribution=heights_distribution,
    settings=settings,
)
heights_density = evaluate_density_grid(heights_density_input)

heights_chart_input = DensityChartInput(
    density_grid=heights_density,
    title="Altura adulta — Normal(170, 8²)",
    settings=settings,
)
chart_density(heights_chart_input)
```

La curva tiene la forma de campana que reconocemos a primera vista: el
pico justo en $170$, casi total simetría a izquierda y derecha, y
colas que se vuelven prácticamente cero antes de los $145$ y de los
$195$ cm. Notar un detalle importante: como ahora estamos sobre una
variable continua, **la altura del gráfico no es una probabilidad**.
Lo que tiene interpretación probabilística es el **área bajo la
curva** sobre un intervalo: la probabilidad de que una persona mida
entre $a$ y $b$ centímetros es exactamente esa área.

**Trampa común.** En variables continuas, una curva más alta no significa “esa
altura exacta tiene esa probabilidad”. La probabilidad aparece cuando juntamos
un intervalo y medimos área.

Pongámosle un número concreto: ¿qué fracción de la población mide entre $165$
y $180$ cm?

```{code-cell} python
heights_interval_input = TailProbabilityInput(
    distribution=heights_distribution,
    lower_bound=165.0,
    upper_bound=180.0,
)
heights_interval_probability = tail_probability_of_continuous(heights_interval_input)
heights_interval_probability
```

Cerca de dos tercios de la población cae en esa franja. Ese número
salió de calcular el área bajo la campana entre $165$ y $180$.

### El motor detrás de la campana

Esa curva tiene una expresión cerrada. Una variable $X$ se llama
**Normal** con media $\mu$ y desvío $\sigma$, y se anota
$X \sim \mathcal{N}(\mu, \sigma^2)$, cuando su densidad de
probabilidad es:

$$ f_X(x) = \frac{1}{\sigma\sqrt{2\pi}}\,\exp\!\left(-\frac{(x - \mu)^2}{2\sigma^2}\right) $$ (eq-normal-pdf)

Tres piezas de la fórmula explican lo que vimos en el gráfico. El
factor $-(x - \mu)^2$ en el exponente impone simetría alrededor de
$\mu$ y hace que la densidad caiga rapidísimo a medida que $x$ se
aleja del centro. La división por $\sigma$ adentro del exponente
controla el ancho de la campana: $\sigma$ chico aprieta todo cerca de
$\mu$, $\sigma$ grande lo desparrama. Y la constante en frente está
elegida exactamente para que el área total bajo la curva dé uno —
como tiene que ser para una distribución de probabilidad.

La probabilidad de cualquier intervalo se obtiene integrando esa
densidad sobre el intervalo:

$$ P(a \le X \le b) = \int_a^b f_X(x)\,dx $$ (eq-density-integral)

El número que recién vimos, esa fracción cercana a $0{,}66$ entre
$165$ y $180$, es exactamente esa integral con $\mu = 170$ y
$\sigma = 8$.

> **Contrato del modelo.** La Normal es una buena candidata cuando la variación
> es aproximadamente simétrica alrededor de un centro y los extremos se vuelven
> raros de forma gradual. No la uses por costumbre: colas muy pesadas, límites
> naturales duros o asimetrías fuertes piden revisar el modelo antes de calcular.

Los dos parámetros de la Normal se leen directamente como momentos:
$E[X]=\mu$ y $\mathrm{Var}(X)=\sigma^2$. Para las alturas del ejemplo, el centro
teórico es 170 cm y la varianza es $8^2=64$.

```{code-cell} python
heights_moments = compute_numeric_moments(MomentsInput(distribution=heights_distribution))
heights_moments
```

(sec-rv-standardize)=
## Estandarización: borrar la escala

Volvamos a las alturas. Si nos dicen que alguien mide $186$ cm, ¿es
una altura extrema? Depende de la población: en una de promedio $170$
y desvío $8$, esos $186$ cm están a dos desvíos del centro y son
claramente altos. En una de promedio $185$, los mismos $186$ cm están
casi pegados a la media. La pregunta «¿qué tan extremo es esto?» pide
una transformación que **borre la escala original** y deje todo en
unidades comparables.

Esa transformación es exactamente la del $z$-score (*standard score*) que
aplicamos en [](#eq-zscore) sobre una muestra. Ahora la usamos sobre la variable
directamente: a partir de $X \sim \mathcal{N}(\mu, \sigma^2)$
definimos

$$ Z = \frac{X - \mu}{\sigma} $$ (eq-zscore-rv)

y se demuestra que $Z \sim \mathcal{N}(0, 1)$. La diferencia con
[](#eq-zscore) es que ahora **conocemos** la distribución del
resultado, no sólo el resumen de una muestra. Cualquier altura
concreta, traducida por [](#eq-zscore-rv), nos dice en cuántos desvíos
se aleja del centro de la población.

Ese valor estandarizado sigue siendo un $z$-score (posición relativa).
En cambio, en inferencia un $z$-statistic es el valor observado de un
estadístico de prueba construido bajo $H_0$.

```{code-cell} python
standardize_normal(NormalParams(mean=170.0, standard_deviation=8.0)).formula
```

(sec-rv-quantiles)=
## Cuantiles: invertir la pregunta

Hasta ahora preguntamos: «¿qué fracción de la población mide menos
que $x$?». Empecemos a darle vuelta al guion. Una marca de ropa
necesita decidir hasta qué altura cubrir con su talle más grande para
alcanzar al $90\,\%$ de la población. Lo que conocen es la fracción
($0{,}90$); lo que necesitan es el corte en centímetros. Ese
corte se llama **percentil 90** y, más en general, el **percentil
$\alpha$** es el valor $x_\alpha$ tal que $P(X \le x_\alpha) =
\alpha$. Visto en el gráfico de la campana, es la altura concreta
que deja el $\alpha$ del área a su izquierda. Formalmente es la
inversa del CDF:

$$ x_\alpha = F_X^{-1}(\alpha) $$ (eq-quantile)

```{code-cell} python
heights_quantile_input = QuantileInput(
    distribution=heights_distribution,
    probability=0.90,
)
heights_percentile_ninety = quantile_of_continuous(heights_quantile_input)
heights_percentile_ninety
```

(sec-rv-exponential)=
## El tiempo de espera como Exponencial

Volvamos a la sala de espera. Lo que queremos modelar ahora es el
tiempo $T$ que un paciente cualquiera pasa esperando hasta que lo
atienden. A diferencia de la altura, $T$ no es simétrico: hay un
montón de esperas cortas y unas pocas larguísimas. Y tiene una
propiedad curiosa que conviene retener — si el paciente ya lleva tres
minutos sentado, el resto de la espera se siente, en términos de
promedio, igual que la espera de cualquier paciente recién llegado: el
tiempo «no recuerda» cuánto se llevaba acumulado.

**Antes de mirar.** Si las esperas cortas dominan pero algunas se alargan
mucho, ¿esperás una curva simétrica como la Normal o una curva con cola hacia
la derecha?

Trabajemos con una espera promedio de $4$ minutos. ¿Qué forma tiene la
distribución de los tiempos posibles?

```{code-cell} python
clinic_distribution = make_exponential(ExponentialParams(rate=0.25))
clinic_density_input = DensityGridInput(
    distribution=clinic_distribution,
    settings=settings,
)
clinic_density = evaluate_density_grid(clinic_density_input)

clinic_density_chart_input = DensityChartInput(
    density_grid=clinic_density,
    title="Tiempo de espera — Exponencial(λ = 0,25)",
    settings=settings,
)
chart_density(clinic_density_chart_input)
```

Lo que muestra la curva es contundente: la mayor densidad está
**pegada al cero**, y a partir de ahí cae monótonamente hacia la
derecha. Esperas cortas son lo más probable, esperas largas se vuelven
exponencialmente raras a medida que aumentan los minutos. La cola
tarda en llegar a cero pero baja cada vez más rápido.

Pongámosle un número de prueba a esa cola: ¿qué probabilidad hay de
que un paciente espere **más de cinco minutos**?

```{code-cell} python
clinic_tail_input = TailProbabilityInput(
    distribution=clinic_distribution,
    lower_bound=5.0,
)
clinic_tail_probability = tail_probability_of_continuous(clinic_tail_input)
clinic_tail_probability
```

Cerca del $29\,\%$ de los pacientes esperan más de cinco minutos. La
cola pesa, pero claramente menos que la zona compacta cerca del cero.

### El motor detrás de la cola

Esa curva que cae exponencialmente tiene una expresión cerrada que
captura la intuición de «sin memoria»:

$$ f_T(t) = \lambda\,e^{-\lambda t},\quad t \ge 0 $$ (eq-exp-pdf)

El parámetro $\lambda$ es la **tasa**: cuántos eventos se esperan por
unidad de tiempo. Si $\lambda = 0{,}25$ pacientes por minuto, eso
equivale a una espera promedio $E[T] = 1/\lambda = 4$ minutos. La
constante adelante hace que el área total dé uno, y el factor
$e^{-\lambda t}$ explica la cola exponencial.

La integral de [](#eq-exp-pdf) tiene forma cerrada y da la regla
compacta de supervivencia $S_T(t)=P(T > t) = e^{-\lambda t}$. Para $t = 5$:

$$ \begin{aligned}
P(T > 5) &= e^{-0{,}25 \cdot 5} \\[4pt]
         &= e^{-1{,}25} \\[4pt]
         &\approx 0{,}287
\end{aligned} $$

Que es exactamente el número que la simulación nos arrojó.

La esperanza y la varianza también quedan determinadas por la tasa:

$$ E[T] = \frac{1}{\lambda}, \qquad \mathrm{Var}(T) = \frac{1}{\lambda^2} $$ (eq-exp-moments)

```{code-cell} python
clinic_moments = compute_numeric_moments(MomentsInput(distribution=clinic_distribution))
clinic_moments
```

> **Contrato del modelo.** La Exponencial modela tiempos de espera entre eventos
> cuando la tasa se mantiene estable y el tiempo restante no depende de cuánto
> ya se esperó. Si hay turnos, prioridades, saturación o aprendizaje del sistema,
> la propiedad “sin memoria” puede romperse.

## Exploración interactiva — distribuciones continuas

Cambiamos familia, parámetros y un intervalo $[x_{\min}, x_{\max}]$. La
probabilidad se actualiza en vivo.

**Predicción guiada.** Mové un solo parámetro por vez. Antes de cambiar
$\sigma$ en la Normal, anticipá si el área de un intervalo fijo va a crecer o
achicarse. Antes de cambiar la tasa de la Exponencial, anticipá si la cola
$P(T > t)$ se vuelve más pesada o más liviana. Después verificá con el widget.

```{code-cell} python
continuous_explorer_input = ContinuousDistributionExplorerInput(
    settings=settings,
)
build_continuous_distribution_explorer(continuous_explorer_input)
```

(sec-rv-poll)=
## Cuántas personas dicen «sí»

Una encuesta toma una tanda de $n = 30$ personas. Si la verdadera proporción
de «sí» en la población es $p = 0{,}55$, la cantidad $Y$ de respuestas «sí»
en la tanda sigue $Y \sim \text{Bin}(30, 0{,}55)$. Es la suma de 30 respuestas
Bernoulli como la de [](#eq-bernoulli-pmf), una por persona. Reusamos
[](#eq-binomial-pmf):

```{code-cell} python
poll_distribution = make_binomial(BinomialParams(trials=30, success_probability=0.55))
poll_mass_input = ProbabilityMassInput(
    distribution=poll_distribution,
    lower_outcome=0,
    upper_outcome=30,
)
poll_mass = evaluate_probability_mass(poll_mass_input)

poll_chart_input = ProbabilityMassChartInput(
    probability_mass=poll_mass,
    title="Encuesta de 30 personas — Bin(30, 0.55)",
    settings=settings,
)
chart_probability_mass(poll_chart_input)
```

(sec-rv-poisson)=
## Poisson: contar eventos raros

Cambiamos un poco la situación de la fábrica. En lugar de inspeccionar
$n = 50$ piezas con $p = 0{,}05$, imaginá que durante un turno entero
pasan miles de piezas y el porcentaje de defectos es bajo. Lo que
nos interesa contar ya no son cuáles de las 50 inspecciones fallan,
sino **cuántos defectos en total aparecen en el turno**. Lo único que
vamos a fijar es el **promedio** esperado: digamos $\lambda = 4$
defectos por turno. ¿Qué forma tiene la distribución de esa cuenta
diaria?

**Antes de mirar.** Si el promedio esperado es $\lambda = 4$, ¿dónde debería
estar el centro de la distribución? ¿Esperás simetría perfecta o una cola algo
más larga hacia la derecha?

Antes de mirar la fórmula, miremos las barras.

```{code-cell} python
poisson_distribution = make_poisson(PoissonParams(rate=4.0))
poisson_mass_input = ProbabilityMassInput(
    distribution=poisson_distribution,
    lower_outcome=0,
    upper_outcome=12,
)
poisson_mass = evaluate_probability_mass(poisson_mass_input)

poisson_chart_input = ProbabilityMassChartInput(
    probability_mass=poisson_mass,
    title="Defectos por turno — Poisson(4)",
    settings=settings,
)
chart_probability_mass(poisson_chart_input)
```

El pico está en $k = 3$ y $k = 4$ defectos, justo donde el promedio
$\lambda = 4$ nos hizo mirar. La forma se parece mucho a la de
la Binomial que vimos al principio del capítulo — y no es
coincidencia. Si tomamos una Binomial con $n$ muy grande y $p$ muy
chico, manteniendo $\lambda = np$ fijo, las dos distribuciones se
vuelven prácticamente indistinguibles. Eso explica por qué la Poisson
aparece tan seguido en problemas de eventos raros: no se pierde casi
nada al usarla como aproximación cuando contar uno por uno es
incómodo.

### El motor detrás del conteo

La probabilidad de cada barra del gráfico viene dada por:

$$ P(K = k) = \frac{\lambda^{k}\,e^{-\lambda}}{k!} $$ (eq-poisson-pmf)

El factor $\lambda^{k}/k!$ pondera cuán probable es ver exactamente
$k$ eventos cuando el promedio es $\lambda$, y $e^{-\lambda}$ es la
constante de normalización que asegura que las probabilidades sumen
uno. Como ejercicio mental, evaluar [](#eq-poisson-pmf) con
$\lambda = 4$ y $k = 3$ devuelve la altura exacta de una de las barras
más altas del gráfico.

En una Poisson, el parámetro $\lambda$ hace doble trabajo:

$$ E[K] = \lambda, \qquad \mathrm{Var}(K) = \lambda $$ (eq-poisson-moments)

```{code-cell} python
poisson_moments_symbolic = compute_poisson_moments(PoissonParams(rate=4.0))
poisson_moments_symbolic
```

(sec-rv-binomial-poisson)=
### Cuando la Binomial se vuelve Poisson

La similitud con la Binomial no es casual. Si tomamos una Binomial con $n$ muy
grande y $p$ muy chico, manteniendo $\lambda = np$ fijo, las barras se acercan a
las de una Poisson:

$$ \text{Bin}(n,p) \approx \text{Poisson}(\lambda) \quad\text{cuando } n\text{ es grande},\ p\text{ chico},\ \lambda=np $$ (eq-binomial-poisson)

Pensá en una fábrica con miles de piezas y una chance mínima de defecto por
pieza. Contar cada intento como Bernoulli sería correcto, pero poco práctico. La
Poisson conserva lo esencial —la tasa promedio de eventos— y simplifica el
modelo.

> **Contrato del modelo.** La Poisson aplica cuando contás eventos raros en una
> ventana fija y una tasa promedio razonablemente estable. Es potente para
> defectos, llegadas o fallas, pero se debilita si los eventos aparecen en
> racimos, si la tasa cambia por hora o si hay un máximo físico muy cercano.

(sec-rv-poisson-exponential)=
## Conteos y esperas: dos caras de la misma tasa

La misma tasa $\lambda$ puede mirar un proceso desde dos ángulos. En una ventana
de longitud $t$, la Poisson cuenta cuántos eventos aparecen:

$$ N(t) \sim \text{Poisson}(\lambda t) $$ (eq-poisson-window)

Entre dos eventos consecutivos, la Exponencial mide cuánto tiempo esperamos:

$$ T \sim \text{Exp}(\lambda) $$

Si llegan 6 pacientes por hora, en 20 minutos esperamos
$\lambda t = 6 \cdot (20/60) = 2$ llegadas. La pregunta «¿cuántos llegan en 20
minutos?» usa Poisson(2); la pregunta «¿cuánto falta hasta el próximo?» usa una
Exponencial con tasa 6 por hora. Elegir una u otra no cambia el fenómeno: cambia
la pregunta.

**Lectura operativa.** Poisson sirve para dimensionar carga en una ventana fija:
cuántas llegadas, fallas o defectos esperamos. Exponencial sirve para hablar del
tiempo hasta el próximo evento. La tasa puede ser la misma; la decisión que
querés tomar no.

## Exploración interactiva — discretas

Pasamos de Binomial a Poisson moviendo el dropdown. Antes de cambiar de
familia, formulá una regla de decisión: ¿usarías Binomial, Poisson, Normal o
Exponencial si el fenómeno cuenta éxitos, cuenta eventos raros, mide alturas o
mide esperas?

Cuando $n$ es grande y $p$ es chico la PMF Binomial casi se superpone con la
Poisson de tasa $np$.

**Chequeo rápido.** Si dos modelos dibujan curvas parecidas, ¿eso significa
que cuentan exactamente la misma historia o que uno puede aproximar al otro en
ciertas condiciones?

```{code-cell} python
discrete_explorer_input = DiscreteDistributionExplorerInput(settings=settings)
build_discrete_distribution_explorer(discrete_explorer_input)
```

## Ejercicio 1 — Estandarizar y leer en la Normal estándar

$X \sim \mathcal{N}(170, 8^2)$. Calculá $P(X \le 178)$.

**Predicción.** Primero traducí 178 cm a unidades de desvío: ¿está a 0, 1 o 2
desvíos por encima de la media? Después usá esa lectura para anticipar si la
probabilidad acumulada debería estar cerca de 50%, 84% o 97%.

**Cómputo.** Calculá la probabilidad y ejecutá la verificación.

**Interpretación.** Traducí el resultado a una frase: “aproximadamente qué
proporción de la población mide hasta 178 cm”.

**Decisión de ingeniería.** Si fueras una marca que define talles, ¿este percentil alcanza
para decidir un corte o pedirías además costos, stock y población objetivo?

**Pista mínima.** Reducí el problema a una probabilidad sobre $Z$.

```{code-cell} python
exercise_tail_input = TailProbabilityInput(
    distribution=heights_distribution,
    upper_bound=178.0,
)
expected_probability = tail_probability_of_continuous(exercise_tail_input).probability

student_answer_probability = 0.8413
verify_input = NumericAnswerInput(
    student_answer=student_answer_probability,
    expected_answer=expected_probability,
)
verify_numeric_answer(verify_input)
```

## Ejercicio 2 — Cola de una espera Exponencial

Para la sala de espera, mantené $T \sim \text{Exp}(0{,}25)$. Calculá $P(T > 8)$.

**Predicción.** Antes de calcular, compará 8 minutos con la espera promedio de 4 minutos. ¿La probabilidad debería ser menor o mayor que la de esperar más de 5 minutos?

**Cómputo.** Usá la regla $P(T > t) = e^{-\lambda t}$ o la celda de verificación.

**Comunicación.** Escribí una frase para Lucía: una espera de 8 minutos no es imposible, pero pertenece a la cola que conviene monitorear.

**Pista mínima.** Con $\lambda = 0{,}25$, el exponente es $-2$.

```{code-cell} python
exercise_exponential_tail_input = TailProbabilityInput(
    distribution=clinic_distribution,
    lower_bound=8.0,
)
expected_exponential_tail = tail_probability_of_continuous(exercise_exponential_tail_input).probability

student_answer_exponential_tail = 0.1353
verify_input = NumericAnswerInput(
    student_answer=student_answer_exponential_tail,
    expected_answer=expected_exponential_tail,
)
verify_numeric_answer(verify_input)
```

## Ejercicio 3 — Esperanza de una Poisson

Si $K \sim \text{Poisson}(3{,}5)$, ¿cuál es $E[K]$?

**Intentá antes de ejecutar.** Recordá qué representa $\lambda$ en una Poisson:
no es solo un parámetro algebraico, es el promedio esperado de eventos por
unidad observada.

**Comunicación.** Si fueran defectos por turno, explicá en una frase qué
significa esperar $3{,}5$ defectos aunque nunca observemos “medio defecto”.

```{code-cell} python
expected_expectation = compute_poisson_moments(PoissonParams(rate=3.5)).expectation

student_answer_expectation = 3.5
verify_input = NumericAnswerInput(
    student_answer=student_answer_expectation,
    expected_answer=float(expected_expectation),
)
verify_numeric_answer(verify_input)
```

**Ahora podemos** elegir modelos distintos según la situación: una Binomial
para éxitos en una tanda, una Poisson para eventos raros, una Normal para
variación simétrica y una Exponencial para esperas sin memoria.

**Lo que todavía falta** es pasar de una observación a muchas. Ningún día de la
clínica se decide con un solo paciente, ninguna encuesta se publica con una sola
respuesta y ninguna jornada de la línea se resume en un único conteo.

**La pregunta que empuja el capítulo siguiente** es qué pasa con promedios y
totales: ¿cómo se distribuye el promedio de treinta esperas?, ¿por qué una
encuesta gana estabilidad cuando crece la muestra?, ¿por qué tantos fenómenos
terminan pareciendo Normales aunque la fuente no lo sea? Las tres respuestas
comparten el mismo teorema.
