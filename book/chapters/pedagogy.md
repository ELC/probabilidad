# Enfoque pedagógico

Esta sección explica **cómo está construido** el libro. No usa ningún concepto
nuevo; es una guía para entender por qué cada capítulo recorre las secciones en
el mismo orden y por qué algunos escenarios reaparecen una y otra vez. El
diseño se apoya en hallazgos consolidados de la psicología cognitiva y la
educación matemática: aprendizaje situado [@lave1991situated], organizadores
previos [@ausubel1968educational], efecto de generación [@slamecka1978generation]
y práctica de recuperación [@roediger2006test], entre otros.

## Fenómenos de aprendizaje aplicados

Los cuatro fenómenos mencionados en la introducción no son un decorado
teórico: cada uno aterriza en un recurso concreto del libro. Esta sección los
recorre uno a uno explicando el mecanismo y mostrando dónde se ve en
funcionamiento.

### Aprendizaje situado

**Mecanismo.** El conocimiento se consolida mejor cuando se adquiere dentro
del contexto donde después va a usarse: una técnica aprendida en abstracto
queda atada a su aula y rara vez se transfiere [@lave1991situated;
@brown1989situated]. La estrategia es presentar herramientas como respuestas
a problemas reales, no como definiciones autocontenidas.

**Cómo aparece en el libro.** El capítulo de **Tratamiento de datos** no
abre con la definición de media muestral; abre con Lucía mirando ochenta
tiempos de espera anotados en una hoja y necesitando decidir, antes del
cierre del turno, si refuerza una franja o investiga un caso excepcional.
La media, la mediana, el rango y el boxplot aparecen como respuestas a
preguntas que ella formuló primero. Cuando el lector después se encuentra
con $\bar{x}$ en otro contexto, no recupera una fórmula: recupera la
decisión que esa fórmula resolvía.

### Organizadores previos

**Mecanismo.** Antes de introducir información nueva, conviene activar una
estructura conceptual que sirva de "andamio" donde colgar los conceptos
[@ausubel1968educational]. El organizador previo es deliberadamente más
general y abstracto que el material que viene, y le da al lector un mapa
mental antes del territorio.

**Cómo aparece en el libro.** El recuadro **Situación de decisión** que
abre cada capítulo cumple exactamente esa función. Antes de la primera
fórmula, el lector ya tiene en mente quién decide, qué riesgo hay si
resume mal, qué herramienta se vuelve necesaria y qué pregunta queda
abierta. En el capítulo 2, la cita "el riesgo no es calcular mal una
media; es resumir una mañana irregular con un número que esconda justo
lo que importa" ancla **toda** la discusión posterior sobre robustez de la
mediana, sensibilidad del desvío estándar y detección de outliers en un
único esquema interpretativo.

### Efecto de generación

**Mecanismo.** Producir activamente una respuesta — aunque sea
incorrecta — antes de verla mejora la retención respecto de leerla
pasivamente [@slamecka1978generation]. La diferencia es robusta y aparece
incluso cuando la "generación" es modesta: completar una palabra, anticipar
una dirección, estimar un orden de magnitud.

**Cómo aparece en el libro.** Los recuadros **Predicción** y **Antes de
mirar** son su instancia más directa. En el capítulo 2, antes de usar el
widget que muestra cómo cambia la media al incorporar una espera de 20
minutos, el texto pide al lector imaginar primero si el promedio se va a
mover apenas o va a saltar; lo mismo antes de tocar el desvío estándar o
la mediana. El compromiso mental previo convierte el resultado del widget
en confirmación o sorpresa, no en información pasiva.

### Práctica de recuperación

**Mecanismo.** Recordar activamente un concepto desde la memoria — más
todavía si es en un contexto nuevo — consolida la retención más que releerlo
[@roediger2006test; @karpicke2008critical]. El test funciona menos como
evaluación y más como herramienta de aprendizaje.

**Cómo aparece en el libro.** Desde el segundo capítulo, la apertura
incluye dos o tres preguntas cortas que obligan al lector a traer a la
memoria una idea anterior antes de usarla otra vez. En el cierre, las
**Ideas para retener** y los mapas de confusión ("media vs mediana vs
moda" en el capítulo 2) reactivan los conceptos fuera de su contexto
original. La práctica está además **espaciada**: la representatividad
muestral aparece como advertencia al final del capítulo 2, vuelve como
condición de uso del TCL en el capítulo 4 y reaparece como supuesto crítico
del bootstrap en el capítulo de inferencia.

## Tono del libro

El tono busca estar cerca del lector sin perder precisión. Hablamos en segunda
persona, usamos escenas concretas y dejamos que las decisiones de ingeniería
empujen las fórmulas, pero evitamos convertir el material en charla casual. La
voz esperada es: clara, humana, profesional y exigente con los supuestos.

Una buena frase del libro debería cumplir tres condiciones:

- **Ubica una pregunta.** El lector sabe qué problema intenta resolver.
- **Conserva el matiz.** No cambia incertidumbre por certezas cómodas.
- **Suena natural.** Puede leerse en voz alta sin parecer una lista de recetas.

Cuando una expresión coloquial distrae del concepto, conviene suavizarla. Por
ejemplo: «equivocarse sin costo real» comunica mejor que una frase demasiado
casual; «anotados rápidamente» sostiene la escena sin regionalizarla demasiado;
«tomar posición con honestidad» evita sonar evasivo sin prometer más de lo que
los datos permiten.

## Concreto, pictórico, abstracto (CPA)

El libro adapta la progresión **CPA — Concrete, Pictorial, Abstract** que se
suele asociar al método Singapur en matemática elemental [@bruner1966toward].
La idea es **no arrancar nunca por la fórmula**: primero hay un caso tangible,
después hay una imagen mental, y recién al final aparece la expresión
simbólica. Esa secuencia coincide con la recomendación general de moverse de
representaciones concretas a abstractas para reducir carga cognitiva intrínseca
en aprendices novatos [@sweller2011cognitive].

Para que el aula no termine con tres ejemplos juguete, agregamos dos pasos
adicionales que aprovechan que estamos en un cuaderno ejecutable:

1. **Concreto.** Una situación medible — un dado, una sala de espera, una
   encuesta, un turno de la fábrica.
2. **Pictórico.** Un gráfico (histograma, ojiva, boxplot, PMF, PDF, IC) que
   muestra la forma del fenómeno antes de escribir cualquier fórmula. La
   prioridad visual sobre la simbólica es deliberada: la percepción de forma
   precede a la decisión analítica [@tukey1977exploratory].
3. **Abstracto.** La fórmula numerada `(U.k)`, presentada en pasos: «partimos
   de», «sustituimos», «despejamos». Así toda fórmula nueva referencia a
   alguna anterior y nunca aparece de la nada.
4. **Predicción.** Antes de ejecutar un gráfico, una simulación o un widget, el
   texto pide anticipar dirección, forma o magnitud. Ese pequeño compromiso
   mental vuelve más memorable la sorpresa cuando el resultado confirma o
   corrige la intuición. Es una aplicación directa del **efecto de generación**:
   intentar producir una respuesta antes de verla mejora la retención respecto
   de la lectura pasiva [@slamecka1978generation].
5. **Contrato del modelo.** Las herramientas importantes explicitan cuándo
   aplican, qué supuestos piden, qué puede romperlas y cómo interpretar el
   resultado sin exagerarlo.
6. **Intuición.** Un párrafo que explica **por qué** la fórmula tiene sentido
   en lenguaje natural. En secciones densas aparece de forma explícita como
   **Intuición operativa** antes de pasar a la **Forma matemática**.
7. **Exploración interactiva.** Un widget (`build_*_explorer`) que permite
   variar parámetros y ver cómo reacciona el gráfico y los números. Es donde
   la intuición se vuelve estable.
8. **Retención.** Algunas ideas centrales cierran con una **Idea para retener**:
   una frase breve que contrasta conceptos cercanos o resume una trampa común
   sin reemplazar la definición formal.
9. **Verificación, interpretación y decisión.** Cada ejercicio funciona como
   auto-chequeo: el lector intenta una respuesta, ejecuta una verificación,
   traduce el número a una interpretación y ensaya una decisión o una frase de
   comunicación. La verificación inmediata implementa el principio de
   *test-enhanced learning*: testearse a sí mismo consolida más que releer
   [@roediger2006test].

Esta progresión está **implícita** en cada capítulo: no vas a encontrar
secciones tituladas «Concreto» o «Pictórico». En cambio vas a leer encabezados
como «Un experimento concreto», «Una imagen mental» o «La fórmula». La
progresión está, pero no se anuncia. Lo que sí aparece de manera visible son
pequeñas pausas de aprendizaje: **Situación de decisión**, **Antes de mirar**,
**Intentá antes de ejecutar**, **Chequeo rápido**, **Trampa común**,
**Contrato del modelo**, **Idea para retener**, **Comunicación** y
**Decisión de ingeniería**.

## Aprendizaje situado y escenarios recurrentes

Cada concepto aparece dentro de una situación que un ingeniero o ingeniera
podría enfrentar — no como definición desconectada. Esa elección sigue la
tradición del **aprendizaje situado**: el conocimiento se consolida mejor
cuando se adquiere en el contexto donde después va a usarse
[@lave1991situated; @brown1989situated]. Por eso Lucía, la operadora de la
encuesta y la responsable de calidad de la línea de producción no son
decoración: son los anclajes alrededor de los cuales se cuelga el vocabulario
estadístico.

Tres situaciones aparecen una y otra vez en los capítulos sin avisar al lector
que «vuelve el ejemplo X»: la sala de espera de una clínica, una encuesta
electoral y una línea de producción que inspecciona piezas. La idea es que
cada una de las tres se vuelva familiar de manera implícita y que el lector,
al leer un capítulo nuevo, reconozca el escenario antes que la fórmula. La
sala de espera atraviesa todo el libro: empieza como una muestra de minutos,
se modela como Exponencial, su promedio aparece bajo el TCL y termina con un
IC para la espera media. La encuesta entra como Bayes, se vuelve Binomial,
después una proporción asintóticamente Normal y, al final, un IC con su
tamaño muestral. La línea de producción pasa de conteos por turno a una
Bin/Poisson, a una aproximación Normal y a un test de hipótesis.

En paralelo, cada capítulo intercala **al menos un ejemplo deliberadamente
ajeno** a esos tres escenarios — un dado, alturas adultas, el tablero de
Galton, una muestra sintética para bootstrap — para mostrar que las técnicas
no quedan amarradas a una historia en particular. Esa variación deliberada
del contexto fomenta la **transferencia**: aplicar una misma idea a un
problema nuevo es más probable cuando la idea se vio en varios contextos
distintos [@gick1983schema].

## Método Singapur y modelado por barras

El método Singapur se popularizó por su uso de **modelos visuales** (a menudo
diagramas de barras) para resolver problemas. En probabilidad y estadística su
versión natural son:

- **Diagramas de Venn** para uniones, intersecciones y complementos
  (Capítulo de Probabilidad).
- **Histograma + ojiva** para visualizar acumulación
  (Capítulo de Tratamiento de datos).
- **Histograma + curva teórica** para comparar muestras simuladas con la
  Normal del TCL (Capítulo de Sumas y promedios).
- **Líneas paralelas** para mostrar muchos intervalos de confianza generados
  por un mismo procedimiento (Capítulo de Inferencia).

En cada uno la idea es la misma: el dibujo viene **antes** que la cuenta. Esa
prioridad de la imagen sobre el símbolo es coherente con la doble codificación
[@paivio1991dual]: el contenido se retiene mejor cuando se procesa simultáneamente
por canales verbal y visual.

## Apertura y transición entre capítulos

Cada capítulo entra con una **Situación de decisión**: quién necesita decidir,
qué pregunta operativa está abierta, qué riesgo aparece si se resume mal y qué
herramienta estadística se vuelve necesaria. Esa entrada convierte el tema en
una necesidad narrativa antes de convertirlo en una lista de definiciones, y
funciona como **organizador previo** en el sentido de Ausubel: ofrece una
estructura conceptual donde anclar lo que viene [@ausubel1968educational].

Cada capítulo sale del recorrido con el mismo ritmo de tres movimientos:
**Ahora podemos** nombrar qué capacidad nueva ganó el lector, **Lo que todavía
falta** explicita qué límite queda vivo, y **La pregunta que empuja el capítulo
siguiente** muestra por qué la próxima herramienta no aparece de la nada. En el
último capítulo, ese tercer movimiento abre preguntas hacia regresión,
estadística bayesiana y series de tiempo.

Entre apertura y cierre, el capítulo también **mira atrás** brevemente usando
los mismos hilos narrativos (clínica, encuesta, línea de producción), **muestra
la limitación** que aparece apenas el contexto se mueve un paso (un paciente
nuevo, un turno todavía sin medir, una respuesta más), **plantea preguntas
concretas** una por hilo y recién entonces **nombra la herramienta** que las
resuelve.

Desde el segundo capítulo, esa mirada atrás aparece también como una breve
**recuperación activa**: dos o tres preguntas que obligan al lector a traer a la
memoria una idea anterior antes de usarla de nuevo. La intención no es evaluar,
sino bajar la carga cognitiva y reforzar conexiones espaciadas entre capítulos
[@karpicke2008critical].

La consecuencia es que el lector llega a cada nueva técnica con la
pregunta ya hecha, no con un temario anunciado por adelantado. La
herramienta aparece como respuesta natural a un problema que el texto
acaba de plantear; el capítulo siguiente arranca cuando esa respuesta,
a su vez, deja al descubierto una nueva limitación. El último capítulo
cierra el ciclo dejando un cliffhanger hacia regresión, estadística
bayesiana y series de tiempo — temas que continúan la misma maquinaria
de ida y vuelta entre datos y parámetros.

Para una guía rápida de notación y términos al pasar entre capítulos,
conviene tener abierto el [glosario](glossary.md).

## Interactividad sin entrega

El libro no está pensado como courseware ni como una plataforma donde el
estudiante entrega una versión completada. La interactividad cumple otra
función: convertir la lectura en experimentación guiada. Antes de una salida
importante, el lector predice; después ejecuta o inspecciona; finalmente
explica si el resultado cambió su intuición.

Ese ciclo aprovecha tres ideas robustas de aprendizaje: la **generación**
(intentar una respuesta antes de verla, [@slamecka1978generation]), la
**recuperación activa** (recordar conceptos previos en un contexto nuevo,
[@roediger2006test]) y la **retroalimentación inmediata** (comparar la
predicción con una verificación o un gráfico, [@hattie2007power]). Los
ejercicios, por eso, no buscan recolectar tareas: buscan que el lector
practique, se equivoque sin costo real y ajuste su modelo mental.

Las verificaciones numéricas se complementan con interpretación y decisión. Un
resultado estadístico no queda cerrado hasta que el lector puede decir qué
significa en la historia, qué supuesto sostiene la conclusión y cómo lo
comunicaría sin convertir incertidumbre en certeza.

## Cierres de sección

Las secciones densas no deberían terminar apenas aparece la fórmula. Cuando un
concepto introduce una herramienta importante, el cierre ideal deja cuatro
piezas visibles:

- **Qué responde.** La pregunta concreta que esa herramienta permite contestar.
- **Cuándo usarlo.** El tipo de situación donde la herramienta tiene sentido.
- **Qué puede salir mal.** El supuesto, sesgo o confusión que puede romper la
  interpretación.
- **Cómo comunicarlo.** Una frase breve que traduzca el número a una decisión o
  advertencia.

No hace falta escribir esos cuatro rótulos en todas partes. La regla editorial
es que el lector no salga de una sección importante con sólo una cuenta: debe
salir con una pregunta, una condición de uso y una interpretación defendible.

## Recuperación y repetición espaciada

La recuperación activa aparece en tres escalas. Al inicio de cada capítulo, unas
preguntas cortas traen ideas previas antes de usarlas. Dentro de una sección,
las pausas **Antes de mirar** o **Intentá antes de ejecutar** obligan a generar
una predicción. Al final, las **Ideas para retener** y los mapas de confusión
separan conceptos cercanos para que el lector pueda recordarlos fuera del
contexto original.

La repetición no busca copiar definiciones: vuelve sobre la misma idea desde una
decisión nueva. Media y dispersión reaparecen cuando hablamos de error estándar;
Bayes vuelve al discutir evidencia; la representatividad vuelve en inferencia y
bootstrap. Esa **práctica espaciada** consolida la retención a largo plazo más
que la práctica concentrada en un único bloque [@cepeda2006distributed].

## Cómo recorrer cada capítulo

Una sugerencia de lectura, especialmente para una primera pasada:

1. Leé la **Situación de decisión** prestando atención a quién decide, qué
   riesgo aparece y qué pregunta queda abierta. Anotá, sin pensarlo demasiado,
   qué responderías ahora mismo.
2. Recorré las secciones de **caso concreto + imagen + fórmula + intuición**
   en orden, sin saltearte el gráfico.
3. Cuando aparezca **Antes de mirar**, escribí o pensá una predicción concreta:
   dirección, forma, orden de magnitud o comparación.
4. Cuando aparezca un **Contrato del modelo**, leelo como una lista de chequeo:
   cuándo aplica, qué supuesto exige, qué lo puede romper y qué interpretación
   autoriza.
5. Detenete en el **widget interactivo**: cambiá un parámetro a la vez y
   tratá de **predecir** qué va a pasar antes de mirar el gráfico nuevo.
6. Cuando encuentres una **Idea para retener**, usala como tarjeta mental:
   preguntate qué dos conceptos contrasta o qué error frecuente intenta evitar.
7. Hacé los **ejercicios** sin ejecutar la verificación primero. Después
   compará tu respuesta con el módulo de `exercises`, explicá qué significa el
   resultado en la historia y ensayá una recomendación o frase de comunicación.
8. Cuando llegues al **párrafo de cierre**, fijate qué pregunta nueva
   queda abierta: esa es la que motiva el capítulo que sigue.

Este ciclo (decisión → pregunta → predicción → exploración → fórmula →
verificación → retención → transferencia → nueva pregunta) es lo que mantiene
el material del libro hilado de principio a fin.

## Revisiones por capítulo

La aplicación de estos principios se audita capítulo por capítulo. Cada
revisión queda registrada como un capítulo hijo de esta sección y documenta
hallazgos concretos — no cambios obligatorios — entre lo que el libro
promete pedagógicamente y lo que efectivamente entrega en cada unidad:

- [Deuda pedagógica del capítulo 2 — Tratamiento de datos](pedagogy_descriptive_statistics.md)
