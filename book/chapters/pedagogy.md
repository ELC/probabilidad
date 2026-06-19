# Enfoque pedagógico

Esta sección explica **cómo está construido** el libro. No usa ningún concepto
nuevo; es una guía para entender por qué cada capítulo recorre las secciones en
el mismo orden y por qué algunos escenarios reaparecen una y otra vez.

## Concreto, pictórico, abstracto (CPA)

El libro adapta la progresión **CPA — Concrete, Pictorial, Abstract** que se
suele asociar al método Singapur en matemática elemental. La idea es **no
arrancar nunca por la fórmula**: primero hay un caso tangible, después hay una
imagen mental, y recién al final aparece la expresión simbólica.

Para que el aula no termine con tres ejemplos juguete, agregamos dos pasos
adicionales que aprovechan que estamos en un cuaderno ejecutable:

1. **Concreto.** Una situación medible — un dado, una sala de espera, una
   encuesta, un turno de la fábrica.
2. **Pictórico.** Un gráfico (histograma, ojiva, boxplot, PMF, PDF, IC) que
   muestra la forma del fenómeno antes de escribir cualquier fórmula.
3. **Abstracto.** La fórmula numerada `(U.k)`, presentada en pasos: «partimos
   de», «sustituimos», «despejamos». Así toda fórmula nueva referencia a
   alguna anterior y nunca aparece de la nada.
4. **Predicción.** Antes de ejecutar un gráfico, una simulación o un widget, el
   texto pide anticipar dirección, forma o magnitud. Ese pequeño compromiso
   mental vuelve más memorable la sorpresa cuando el resultado confirma o
   corrige la intuición.
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
   comunicación.

Esta progresión está **implícita** en cada capítulo: no vas a encontrar
secciones tituladas «Concreto» o «Pictórico». En cambio vas a leer encabezados
como «Un experimento concreto», «Una imagen mental» o «La fórmula». La
progresión está, pero no se anuncia. Lo que sí aparece de manera visible son
pequeñas pausas de aprendizaje: **Situación de decisión**, **Antes de mirar**,
**Intentá antes de ejecutar**, **Chequeo rápido**, **Trampa común**,
**Contrato del modelo**, **Idea para retener**, **Comunicación** y
**Decisión de ingeniería**.

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

En cada uno la idea es la misma: el dibujo viene **antes** que la cuenta.

## Escenarios recurrentes

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
no quedan amarradas a una historia en particular.

## Apertura y transición entre capítulos

Cada capítulo entra con una **Situación de decisión**: quién necesita decidir,
qué pregunta operativa está abierta, qué riesgo aparece si se resume mal y qué
herramienta estadística se vuelve necesaria. Esa entrada convierte el tema en
una necesidad narrativa antes de convertirlo en una lista de definiciones.

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
sino bajar la carga cognitiva y reforzar conexiones espaciadas entre capítulos.

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
(intentar una respuesta antes de verla), la **recuperación activa** (recordar
conceptos previos en un contexto nuevo) y la **retroalimentación inmediata**
(comparar la predicción con una verificación o un gráfico). Los ejercicios, por
eso, no buscan recolectar tareas: buscan que el lector practique, se equivoque
barato y ajuste su modelo mental.

Las verificaciones numéricas se complementan con interpretación y decisión. Un
resultado estadístico no queda cerrado hasta que el lector puede decir qué
significa en la historia, qué supuesto sostiene la conclusión y cómo lo
comunicaría sin convertir incertidumbre en certeza.

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
