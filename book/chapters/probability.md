---
title: Probabilidad
kernelspec:
  name: python3
  display_name: Python 3
---

Lo que hicimos hasta acá miraba hacia atrás: las esperas de la clínica
que **ya pasaron**, los conteos de defectos del turno **ya
inspeccionado**, las respuestas que la encuesta **ya recogió**.
Apenas el contexto se mueve un poco — un paciente nuevo cruza la
puerta, arranca un turno todavía sin medir, alguien levanta la mano
por primera vez —, los promedios y desvíos del capítulo anterior
dejan de alcanzar.

¿Qué tan probable es que el próximo paciente espere más de cinco
minutos?, si ya lleva tres minutos sentado, ¿cómo se actualizan esas
chances?, cuando alguien dice «sí» en la encuesta, ¿qué tanto pesa esa
respuesta sobre lo que vamos a afirmar del barrio entero? Ahora Lucía
no tiene que describir una mañana cerrada: tiene que decidir mientras
la sala sigue llenándose, con información incompleta y consecuencias
operativas.

**Antes de seguir.** Recuperá tres ideas del capítulo anterior: qué
pregunta contesta la media, qué pregunta contesta la dispersión y por
qué ningún resumen descriptivo alcanza para hablar del próximo caso.

Para responder, vamos a construir tres movimientos simples: combinar
posibilidades, recalcular chances cuando aparece información nueva y
mirar una pregunta desde el lado contrario. Primero los veremos con
situaciones concretas; después les pondremos nombre y fórmula.

> **Situación de decisión.** Lucía ya no mira una mañana cerrada: decide con la
> sala todavía en movimiento. Necesita estimar qué puede pasar con el próximo
> paciente, cuánto cambia la información nueva y cuándo una señal merece
> modificar una acción operativa.
> Al final del capítulo vas a poder combinar eventos sin contar dos veces,
> condicionar sin cambiar de universo por accidente y usar Bayes para convertir
> evidencia imperfecta en una actualización defendible, no en certeza.

```{code-cell} python
:tags: [hide-input]
from core import Settings
from exercises import NumericAnswerInput, verify_numeric_answer
from probability import (
    BayesInput,
    ConditionalInput,
    JointEventInput,
    SetOperationInput,
    evaluate_bayes,
    evaluate_conditional_probability,
    evaluate_set_operations,
    joint_event_probabilities,
)
from probability.total_probability import TotalProbabilityBranch
from symbolic import bayes_theorem, total_probability_theorem
from visualization import (
    PartitionDiagramInput,
    ProbabilityTreeInput,
    VennTwoSetsInput,
    chart_partition_diagram,
    chart_probability_tree,
    chart_venn_two_sets,
)
from widgets import BayesExplorerInput, build_bayes_explorer
```

```{code-cell} python
:tags: [remove-cell]
settings = Settings()
```

(sec-prob-experiment)=
## Un experimento concreto

Antes de hablar de tiempos continuos, fijamos un experimento minimalista: tirar
un dado equilibrado. Definimos dos eventos:

- $A$ = «sale par» = $\{2, 4, 6\}$.
- $B$ = «sale al menos 4» = $\{4, 5, 6\}$.

Sobre este universo de 6 resultados podemos visualizar las operaciones de
conjuntos sin ambigüedad. Después transferimos la idea a eventos sobre
tiempos o resultados de la encuesta.

```{code-cell} python
universe = frozenset({"1", "2", "3", "4", "5", "6"})
event_even = frozenset({"2", "4", "6"})
event_at_least_four = frozenset({"4", "5", "6"})

set_input = SetOperationInput(
    universe=universe,
    event_a=event_even,
    event_b=event_at_least_four,
)
set_result = evaluate_set_operations(set_input)
set_result
```

El conjunto de todos los resultados posibles se llama **espacio muestral** y
lo escribimos $\Omega$. En el dado, $\Omega = \{1,2,3,4,5,6\}$. Un **evento**
es cualquier subconjunto de ese espacio: $A$ y $B$ son eventos porque agrupan
resultados que nos importan.

Como el dado es equilibrado, todos los resultados pesan lo mismo. Entonces la
probabilidad clásica de un evento se calcula contando:

$$ P(A) = \frac{|A|}{|\Omega|} $$ (eq-classical-prob)

Para $A=$ «sale par», $|A|=3$ y $|\Omega|=6$, así que $P(A)=3/6=1/2$.
El **complemento** de $A$, escrito $\bar A$, contiene todo lo que no está en
$A$: salir impar. Como $A$ y $\bar A$ cubren todo sin solaparse,

$$ P(\bar A) = 1 - P(A) $$ (eq-complement-prob)

Antes de combinar eventos, conviene hacer esta lectura simple: ¿qué cuenta el
evento, qué queda afuera y cuál es el universo de referencia?

(sec-prob-additive)=
## La regla aditiva

**Antes de mirar.** Si sumás “sale par” y “sale al menos 4”, ¿qué resultado
creés que se contará dos veces? Identificar ese solapamiento antes de la fórmula
ayuda a que la regla no parezca un truco algebraico.

**Paso 1 — Cardinalidades.** Imaginá dos círculos solapados (Venn): $A \cap B$
vive en la zona compartida. Si sumamos cardinalidades sin corregir el
solapamiento, la zona compartida se cuenta dos veces:

$$ |A \cup B| = |A| + |B| - |A \cap B| $$ (eq-union-card)

**Paso 2 — Probabilidades.** Dividiendo cada cardinalidad por $|\Omega|$
obtenemos la **regla aditiva** sobre probabilidades. Esta es la primera
fórmula propiamente probabilística del libro:

$$ P(A \cup B) = P(A) + P(B) - P(A \cap B) $$ (eq-union-prob)

Volviendo al dado: $P(A) = P(B) = 3/6$, $P(A \cap B) = 2/6$, así que la
ecuación [](#eq-union-prob) da $P(A \cup B) = 3/6 + 3/6 - 2/6 = 4/6$.

```{code-cell} python
joint_input = JointEventInput(
    probability_a=3 / 6,
    probability_b=3 / 6,
    probability_intersection=2 / 6,
)
joint = joint_event_probabilities(joint_input)
joint
```

Para ver por qué la cardinalidad del solapamiento se cuenta dos veces, conviene
tener el diagrama a mano. Cada círculo es un evento, la región compartida es la
intersección $A \cap B$, y la unión es todo lo coloreado.

```{code-cell} python
venn_input = VennTwoSetsInput(
    probability_a=3 / 6,
    probability_b=3 / 6,
    probability_intersection=2 / 6,
    set_a_label="A: sale par",
    set_b_label="B: sale al menos 4",
    intersection_label="A ∩ B = {4, 6}",
    title="Eventos sobre el dado",
    settings=settings,
)
chart_venn_two_sets(venn_input);
```

(sec-prob-conditional)=
## Probabilidad condicional

Probabilidad condicional es **restringir el universo**: dentro del subconjunto
$B$, ¿qué fracción cae también en $A$?

**Paso 1:** retomamos $P(A \cap B)$ que ya definimos junto a [](#eq-union-prob).

**Paso 2:** definimos:

$$ P(A \mid B) = \frac{P(A \cap B)}{P(B)},\quad P(B) > 0 $$ (eq-cond-prob)

Con los datos del dado: $P(A \mid B) = (2/6)/(3/6) = 2/3$. Saber que el
resultado es al menos 4 sube la chance de «par» de $1/2$ a $2/3$.

> **Contrato del modelo.** Usá probabilidad condicional cuando una información
> nueva restringe el universo de casos posibles. Necesitás que el evento que
> condiciona tenga probabilidad positiva. Si cambiás el grupo de referencia sin
> notarlo, la interpretación cambia por completo.

**Trampa común.** $P(A \mid B)$ y $P(B \mid A)$ no cuentan la misma historia:
el universo restringido cambia. Antes de calcular, preguntate siempre “¿dentro
de qué grupo estoy mirando?”.

```{code-cell} python
conditional_input = ConditionalInput(
    probability_intersection=2 / 6,
    probability_conditioning_event=3 / 6,
)
conditional = evaluate_conditional_probability(conditional_input)
conditional
```

Para la condicional $P(A \mid B)$ pensá en quedarte **dentro del círculo $B$**: la fracción de ese
círculo que también cae en $A$ es exactamente $P(A \cap B) / P(B)$. El dibujo muestra esa fracción
de un vistazo.

```{code-cell} python
conditional_venn = VennTwoSetsInput(
    probability_a=3 / 6,
    probability_b=3 / 6,
    probability_intersection=2 / 6,
    set_a_label="A: par",
    set_b_label="B (condiciona)",
    intersection_label="A ∩ B = 2/6",
    title="Universo restringido a B",
    settings=settings,
)
chart_venn_two_sets(conditional_venn);
```

(sec-prob-events-as-waits)=
## Las esperas vistas como eventos

Volvemos a la sala de espera y miramos la fórmula [](#eq-cond-prob) en ese contexto. Tenemos
$T$ = «espera más de 5 minutos» y $S$ = «espera más de 3 minutos». Por
construcción $T \subset S$, así que $P(T \cap S) = P(T)$. La fórmula [](#eq-cond-prob)
queda:

$$ \begin{aligned}
P(T \mid S) &= \frac{P(T \cap S)}{P(S)} \\[4pt]
            &= \frac{P(T)}{P(S)}
\end{aligned} $$

Si en una semana de datos pasados $P(T) = 0{,}21$ y $P(S) = 0{,}45$,
entonces $P(T \mid S) = 0{,}21 / 0{,}45 \approx 0{,}47$. Ya esperar 3 minutos
casi duplica la chance original de cruzar los 5.

```{code-cell} python
clinic_conditional_input = ConditionalInput(
    probability_intersection=0.21,
    probability_conditioning_event=0.45,
)
clinic_conditional = evaluate_conditional_probability(clinic_conditional_input)
clinic_conditional
```

Como $T \subset S$, el círculo de $T$ cae enteramente dentro de $S$: toda espera de más de 5 minutos
también supera los 3. La intersección coincide con $T$ y el denominador condicional es el círculo
mayor $S$.

```{code-cell} python
waits_venn = VennTwoSetsInput(
    probability_a=0.21,
    probability_b=0.45,
    probability_intersection=0.21,
    set_a_label="T (>5 min)",
    set_b_label="S (>3 min)",
    intersection_label="T = T ∩ S",
    title="Esperas: T ⊂ S",
    settings=settings,
)
chart_venn_two_sets(waits_venn);
```

(sec-prob-independence)=
## Cuando saber una cosa no cambia la otra

La probabilidad condicional sube de $1/2$ a $2/3$ en el dado porque saber que
el resultado fue al menos 4 cambia el universo. Pero no toda información nueva
cambia una chance. Si tiramos dos dados, saber que el primero salió par no
debería modificar la probabilidad de que el segundo sea 6.

Dos eventos son **independientes** cuando condicionar por uno deja igual la
probabilidad del otro:

$$ P(A \mid B) = P(A) $$

Usando [](#eq-cond-prob), esa misma idea se escribe como una regla de producto:

$$ P(A \cap B) = P(A)\,P(B) $$ (eq-independence)

La palabra clave es «no informa». Independencia no significa que los eventos no
puedan ocurrir juntos; significa que observar uno no cambia la chance del otro.
En datos operativos esta condición es frágil: dos demoras consecutivas en la
misma guardia pueden estar encadenadas, aunque dos tiradas de dados no lo estén.

(sec-prob-contingency)=
## Tablas de contingencia: contar antes de dividir

Cuando los eventos salen de datos observados, una tabla $2\times2$ suele ser más
clara que una fórmula suelta. Supongamos una inspección de 1.000 piezas:

| | Alarma | Sin alarma | Total |
| --- | ---: | ---: | ---: |
| Defectuosa | 27 | 3 | 30 |
| Sana | 49 | 921 | 970 |
| Total | 76 | 924 | 1.000 |

La tabla permite leer probabilidades conjuntas, marginales y condicionales sin
mezclarlas. Por ejemplo, $27/1000$ es la probabilidad conjunta de «defectuosa y
alarma»; $76/1000$ es la probabilidad marginal de alarma; y $27/76$ es la
probabilidad de defecto **dentro** de las alarmas.

Esa última fracción ya tiene forma bayesiana: invierte la pregunta del test.
No pregunta «si está defectuosa, ¿da alarma?», sino «si dio alarma, ¿qué tan
creíble es que esté defectuosa?».

(sec-prob-bayes-symbolic)=
## Teorema de Bayes (forma simbólica)

**Paso 1.** Escribimos la condicional en los dos sentidos usando [](#eq-cond-prob):

$$ P(A \cap B) = P(A \mid B)\,P(B) = P(B \mid A)\,P(A) $$

**Paso 2.** Igualamos los dos miembros de la derecha y despejamos
$P(A \mid B)$:

$$ P(A \mid B) = \frac{P(B \mid A)\,P(A)}{P(B)} $$ (eq-bayes)

Dejamos también la versión simbólica visible para que la forma sea
inequívoca:

```{code-cell} python
bayes_theorem().formula
```

**No confundas.** Probabilidad condicional calcula una chance dentro de un
universo restringido. Bayes usa dos condicionales y una tasa base para invertir
la dirección de la pregunta. Si ya tenés el grupo de referencia correcto, usás
condicional; si querés pasar de evidencia observada a causa plausible, necesitás
Bayes.

(sec-prob-total)=
## Probabilidad total — armar el denominador

Bayes necesita el denominador $P(B)$: la probabilidad de observar la evidencia
sin importar de qué causa vino. Si $\{A_1, \dots, A_k\}$ es una **partición**
del universo —eventos incompatibles que cubren todo—, sumamos la contribución
de cada parte:

$$ P(B) = \sum_{i=1}^{k} P(B \mid A_i)\,P(A_i) $$ (eq-total-prob)

```{code-cell} python
total_probability_theorem(partition_size=3).formula
```

Una **partición** se ve como una franja $\Omega$ cortada en pedazos disjuntos
$A_1, \dots, A_k$. La barra inferior anaranjada muestra cómo el evento $B$ se
reparte dentro de cada pedazo: la suma de esos cachitos, ponderada por
$P(A_i)$, es exactamente la fórmula [](#eq-total-prob).

```{code-cell} python
partition_input = PartitionDiagramInput(
    partition_labels=("A_1", "A_2", "A_3"),
    partition_weights=(0.45, 0.35, 0.20),
    overlay_label="B se reparte sobre la partición",
    overlay_fractions=(0.30, 0.55, 0.10),
    title="Partición de Ω y evento B",
    settings=settings,
)
chart_partition_diagram(partition_input)
```

(sec-prob-bayes-data)=
## Bayes con datos: prueba diagnóstica

En una población, $P(D) = 0{,}01$ es la **prevalencia**: la tasa base de la
enfermedad antes de mirar el test. La **sensibilidad** es
$P(+ \mid D)=0{,}99$: si una persona está enferma, el test casi siempre da
positivo. La **especificidad** es $P(- \mid \bar D)=0{,}95$: si una persona no
está enferma, el test casi siempre da negativo. El complemento de la
especificidad, $P(+ \mid \bar D)=0{,}05$, es la tasa de falsos positivos.

En vocabulario bayesiano, la prevalencia es el **prior** o creencia previa; la
sensibilidad y la tasa de falsos positivos son **likelihoods**, probabilidades
de observar el resultado bajo cada estado posible; y $P(D \mid +)$ es el
**posterior**, la creencia actualizada después de ver un positivo.

**Antes de calcular.** Anotá una estimación intuitiva: si el test parece tan
bueno, ¿el positivo te deja cerca de 99%, cerca de 50% o bastante más abajo?
No importa acertar; importa notar cuánto pesa la tasa base.

Pensá en 10.000 personas. 100 enfermos: 99 dan positivo.
9.900 sanos: 495 dan positivo. Total de positivos: $99 + 495 = 594$. La
fracción de verdaderos enfermos dentro de los positivos es
$99 / 594 \approx 0{,}167$.

Aplicamos [](#eq-bayes) con la **probabilidad total** en el denominador. Para
que la cuenta sea legible, la expresamos en varias líneas:

> **Contrato del modelo.** Bayes sirve cuando querés invertir una probabilidad
> condicional: de “qué tan probable es el resultado si la causa es cierta” a
> “qué tan plausible es la causa después de ver el resultado”. Necesitás una
> tasa base y likelihoods comparables. Si omitís la tasa base, el posterior suele
> quedar exagerado.

$$ \begin{aligned}
P(D \mid +) &= \frac{P(+ \mid D)\,P(D)}{P(+)} \\[4pt]
P(+)        &= P(+ \mid D)\,P(D) + P(+ \mid \bar{D})\,P(\bar{D}) \\[4pt]
            &= 0{,}99 \cdot 0{,}01 + 0{,}05 \cdot 0{,}99 \\[4pt]
            &= 0{,}0099 + 0{,}0495 \\[4pt]
            &= 0{,}0594 \\[4pt]
P(D \mid +) &= \frac{0{,}0099}{0{,}0594} \approx 0{,}167
\end{aligned} $$

```{code-cell} python
diagnostic_branches = (
    TotalProbabilityBranch(label="Enfermo", prior=0.01, likelihood=0.99),
    TotalProbabilityBranch(label="Sano", prior=0.99, likelihood=0.05),
)
diagnostic_input = BayesInput(branches=diagnostic_branches)
diagnostic_posteriors = evaluate_bayes(diagnostic_input)
diagnostic_posteriors[0]
```

Antes del árbol conviene mirar las áreas: el círculo «enfermo» es minúsculo frente al universo
sano, y la mayor parte del círculo «test +» nace de falsos positivos sobre los sanos. La fracción
de «enfermo» dentro de «test +» es lo que tira el posterior lejos del $99\%$.

```{code-cell} python
diagnostic_venn = VennTwoSetsInput(
    probability_a=0.01,
    probability_b=0.01 * 0.99 + 0.99 * 0.05,
    probability_intersection=0.01 * 0.99,
    set_a_label="D (enfermo)",
    set_b_label="+ (test positivo)",
    title="Prevalencia y resultado del test",
    settings=settings,
)
chart_venn_two_sets(diagnostic_venn);
```

El mismo árbol que dibujarías a mano resume las cuatro ramas posibles. Cada
rama parte de la prevalencia y se bifurca según el resultado del test; la hoja
lleva la **probabilidad conjunta**, que es justo lo que [](#eq-total-prob) pide sumar para
armar $P(+)$.

```{code-cell} python
tree_input = ProbabilityTreeInput(
    root_label="Población",
    branch_labels=("Enfermo", "Sano"),
    branch_probabilities=(0.01, 0.99),
    leaf_labels=("Test +", "Test −"),
    conditional_probabilities=((0.99, 0.01), (0.05, 0.95)),
    title="Árbol de la prueba diagnóstica",
    settings=settings,
)
chart_probability_tree(tree_input)
```

Aunque el test es excelente, un positivo mueve la creencia del 1% al 16,7%.
La clave está en la **tasa base**: como casi nadie está enfermo, los falsos
positivos pesan mucho.

**Idea para retener.** Bayes no convierte evidencia en certeza: redistribuye
credibilidad usando una tasa base y un mecanismo de observación.

**Chequeo rápido.** Si la prevalencia sube y la calidad del test queda igual,
¿esperás que $P(D \mid +)$ suba o baje? Hacé la predicción antes de mover los
sliders del widget y después verificá cómo reacciona el posterior.

```{code-cell} python
explorer_input = BayesExplorerInput(settings=settings)
build_bayes_explorer(explorer_input)
```

(sec-prob-poll-bayes)=
## Bayes en una encuesta ruidosa

La misma lógica aparece cuando una encuesta no mide una verdad directamente sino una respuesta con ruido. Supongamos que, antes de llamar a una persona, el equipo estima que $52\%$ del barrio apoya una medida. Si alguien realmente la apoya, responde «sí» con probabilidad $0{,}80$; si no la apoya, igual puede decir «sí» por confusión, presión social o interpretación ambigua de la pregunta, con probabilidad $0{,}25$.

**Antes de calcular.** Si una persona responde «sí», ¿creés que la probabilidad de que realmente apoye la medida sube poco, sube mucho o queda casi igual? La respuesta afirmativa pesa, pero su peso depende de cuán ruidosa sea la pregunta.

**En una frase.** Bayes no convierte una respuesta en certeza: convierte una tasa base y un mecanismo de respuesta en una creencia actualizada.

```{code-cell} python
poll_response_branches = (
    TotalProbabilityBranch(label="Apoya", prior=0.52, likelihood=0.80),
    TotalProbabilityBranch(label="No apoya", prior=0.48, likelihood=0.25),
)
poll_response_input = BayesInput(branches=poll_response_branches)
poll_response_posteriors = evaluate_bayes(poll_response_input)
poll_response_posteriors[0]
```

El diagrama hace visible el peso del **ruido**: aunque el círculo «apoya» ocupa cerca de la mitad,
una porción del círculo «responde sí» vive sobre «no apoya». Bayes mide qué fracción del círculo
«responde sí» cae dentro de «apoya».

```{code-cell} python
poll_response_venn = VennTwoSetsInput(
    probability_a=0.52,
    probability_b=0.52 * 0.80 + 0.48 * 0.25,
    probability_intersection=0.52 * 0.80,
    set_a_label="Apoya",
    set_b_label="Responde sí",
    title="Encuesta ruidosa — apoyo real y respuesta",
    settings=settings,
)
chart_venn_two_sets(poll_response_venn);
```

## Chequeo guiado — Encuesta, probabilidad total y Bayes

En la encuesta ruidosa, el apoyo real tiene probabilidad $0{,}52$. Una persona que apoya responde «sí» con probabilidad $0{,}80$; una persona que no apoya responde «sí» con probabilidad $0{,}25$.

**Predicción.** Antes de calcular, decidí si la probabilidad total de observar un «sí» debería quedar más cerca de $0{,}52$, de $0{,}80$ o de $0{,}25$.

**Cómputo.** Calculá primero $P(\text{sí})$ con [](#eq-total-prob). Después calculá $P(\text{apoya} \mid \text{sí})$ con [](#eq-bayes).

**Comunicación.** Escribí una frase para el informe: una respuesta «sí» aumenta la evidencia de apoyo, pero no equivale a apoyo seguro.

**Pista mínima.** El denominador de Bayes es la probabilidad total de obtener una respuesta «sí».

Mirá el solapamiento antes de calcular: el círculo «responde sí» contiene a casi todo el círculo
«apoya», pero también un pedazo de «no apoya». La predicción de $P(\text{apoya} \mid \text{sí})$ tiene
que quedar cerca de la fracción que ocupa el área «apoya» dentro del círculo «sí».

```{code-cell} python
poll_check_venn = VennTwoSetsInput(
    probability_a=0.52,
    probability_b=0.52 * 0.80 + 0.48 * 0.25,
    probability_intersection=0.52 * 0.80,
    set_a_label="Apoya",
    set_b_label="Responde sí",
    title="Chequeo guiado — encuesta ruidosa",
    settings=settings,
)
chart_venn_two_sets(poll_check_venn);
```

```{code-cell} python
expected_yes_probability = sum(branch.prior * branch.likelihood for branch in poll_response_branches)
expected_support_given_yes = poll_response_posteriors[0].posterior

student_answer_yes_probability = 0.536
student_answer_support_given_yes = 0.776
verify_yes_input = NumericAnswerInput(
    student_answer=student_answer_yes_probability,
    expected_answer=expected_yes_probability,
)
verify_support_input = NumericAnswerInput(
    student_answer=student_answer_support_given_yes,
    expected_answer=expected_support_given_yes,
)
verify_numeric_answer(verify_yes_input), verify_numeric_answer(verify_support_input)
```

(sec-prob-inspection)=
## Una pieza pasa la inspección

La línea de producción inspecciona cada pieza con un test que detecta
defectos con probabilidad $0{,}9$ si la pieza está mal y produce un falso
positivo con probabilidad $0{,}05$ si está bien. La verdadera tasa de piezas
defectuosas es $0{,}03$.

Aplicamos [](#eq-bayes) y [](#eq-total-prob) para responder: **dada una alarma, ¿cuál es la
probabilidad de que la pieza esté realmente defectuosa?**

```{code-cell} python
factory_branches = (
    TotalProbabilityBranch(label="Defectuosa", prior=0.03, likelihood=0.90),
    TotalProbabilityBranch(label="Sana", prior=0.97, likelihood=0.05),
)
factory_input = BayesInput(branches=factory_branches)
factory_posteriors = evaluate_bayes(factory_input)
factory_posteriors[0]
```

Las áreas dejan ver por qué el posterior queda lejos del $90\%$ de sensibilidad: las piezas
defectuosas son una minoría, y dentro del círculo «alarma» buena parte viene de piezas sanas con falsa
alarma. La fracción de «defectuosa» dentro de «alarma» es lo que mide la fórmula de Bayes.

```{code-cell} python
factory_venn = VennTwoSetsInput(
    probability_a=0.03,
    probability_b=0.03 * 0.90 + 0.97 * 0.05,
    probability_intersection=0.03 * 0.90,
    set_a_label="Defectuosa",
    set_b_label="Alarma",
    title="Inspección — defectuosas y alarmas",
    settings=settings,
)
chart_venn_two_sets(factory_venn);
```

## Ejercicio 1 — Regla aditiva

Sean $P(A) = 0{,}6$, $P(B) = 0{,}5$ y $P(A \cap B) = 0{,}2$. Calculá
$P(A \cup B)$ usando la fórmula [](#eq-union-prob).

**Predicción.** Antes de calcular, decidí si la unión debería ser menor que
$P(A)+P(B)$ o igual a esa suma. El solapamiento te marca la dirección.

**Cómputo.** Hacé la cuenta sin mirar la celda de verificación.

**Interpretación.** Explicá por qué sería imposible obtener un resultado mayor
que 1 en una unión de eventos.

**Decisión de ingeniería.** Si estos eventos fueran “alarma de calidad” y “revisión manual”,
¿qué advertencia darías a alguien que suma porcentajes sin mirar el solapamiento?

**Pista mínima.** La intersección se resta porque fue contada dos veces.

El dibujo te deja anticipar el tamaño de $P(A \cup B)$ sin la fórmula: contás el área coloreada total
y la comparás con $P(A) + P(B)$. El faltante es exactamente $P(A \cap B)$.

```{code-cell} python
exercise_additive_venn = VennTwoSetsInput(
    probability_a=0.6,
    probability_b=0.5,
    probability_intersection=0.2,
    set_a_label="A",
    set_b_label="B",
    title="Ejercicio 1 — regla aditiva",
    settings=settings,
)
chart_venn_two_sets(exercise_additive_venn);
```

```{code-cell} python
exercise_joint_input = JointEventInput(
    probability_a=0.6,
    probability_b=0.5,
    probability_intersection=0.2,
)
expected_union = joint_event_probabilities(exercise_joint_input).union

student_answer_union = 0.9
verify_input = NumericAnswerInput(
    student_answer=student_answer_union,
    expected_answer=expected_union,
)
verify_numeric_answer(verify_input)
```

## Ejercicio 2 — Bayes a mano

Una caja $C_1$ tiene 3 bolas rojas y 7 blancas. La caja $C_2$ tiene 6 rojas
y 4 blancas. Se elige una caja al azar y se saca una bola: resulta roja.
Calculá $P(C_1 \mid R)$ aplicando la fórmula [](#eq-bayes) con denominador [](#eq-total-prob).

**Predicción.** Antes de calcular, decidí si la respuesta debería quedar por
encima o por debajo de $1/2$. La bola roja favorece a la caja con más rojas, así
que esa intuición te permite detectar errores de dirección.

**Pista mínima.** Construí primero $P(R)$ sumando la contribución de las dos
cajas.

Antes de aplicar la fórmula, mirá el solapamiento entre «se elige $C_1$» y «sale roja». La intersección
es justo lo que va al numerador de $P(C_1 \mid R)$, y el área del círculo «roja» es el denominador.

```{code-cell} python
exercise_box_venn = VennTwoSetsInput(
    probability_a=0.5,
    probability_b=0.45,
    probability_intersection=0.15,
    set_a_label="C_1 (elegida)",
    set_b_label="R (roja)",
    title="Ejercicio 2 — caja y color",
    settings=settings,
)
chart_venn_two_sets(exercise_box_venn);
```

```{code-cell} python
box_branches = (
    TotalProbabilityBranch(label="C1", prior=0.5, likelihood=0.3),
    TotalProbabilityBranch(label="C2", prior=0.5, likelihood=0.6),
)
box_input = BayesInput(branches=box_branches)
expected_posterior = evaluate_bayes(box_input)[0].posterior

student_answer_posterior = 1 / 3
verify_input = NumericAnswerInput(
    student_answer=student_answer_posterior,
    expected_answer=expected_posterior,
)
verify_numeric_answer(verify_input)
```

**Ahora podemos** combinar eventos, condicionar por información nueva y usar
Bayes para actualizar una decisión cuando aparece un test, una alarma o una
respuesta de encuesta.

**Lo que todavía falta** es asignar probabilidad a resultados que no se dejan
enumerar de forma práctica. El dado, la caja y el test viven en conjuntos discretos;
una espera exacta, una altura precisa o un conteo futuro piden un objeto más
flexible.

**La pregunta que empuja el capítulo siguiente** es cómo modelar «tiempo de
espera», «respuestas afirmativas» o «defectos por turno» de modo que ya tengan,
por construcción, una media, una varianza y probabilidades sobre intervalos.
Ese objeto se llama **variable aleatoria**, y su PMF y su densidad son las
herramientas que aparecen a continuación.
