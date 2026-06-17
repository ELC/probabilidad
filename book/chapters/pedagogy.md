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
4. **Intuición.** Un párrafo que explica **por qué** la fórmula tiene sentido
   en lenguaje natural. A esta altura, el lector ya tiene los tres elementos
   anteriores y puede confirmar lo que la fórmula dice.
5. **Exploración interactiva.** Un widget (`build_*_explorer`) que permite
   variar parámetros y ver cómo reacciona el gráfico y los números. Es donde
   la intuición se vuelve estable.

Esta progresión está **implícita** en cada capítulo: no vas a encontrar
secciones tituladas «Concreto» o «Pictórico». En cambio vas a leer encabezados
como «Un experimento concreto», «Una imagen mental» o «La fórmula». La
progresión está, pero no se anuncia.

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

Cada capítulo entra y sale del recorrido con el mismo ritmo de cuatro
movimientos: **mirar atrás** brevemente al capítulo anterior usando los
mismos hilos narrativos (clínica, encuesta, línea de producción),
**mostrar la limitación** que aparece apenas el contexto se mueve un
paso (un paciente nuevo, un turno todavía sin medir, una respuesta más),
**plantear tres preguntas concretas** una por hilo, y recién entonces
**nombrar la herramienta** que las resuelve. Ese pulso se repite tanto
en el párrafo de apertura como en el de cierre.

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

## Cómo recorrer cada capítulo

Una sugerencia de lectura, especialmente para una primera pasada:

1. Leé el **párrafo de apertura** prestando atención a la pregunta que se
   plantea, y anotá, sin pensarlo demasiado, qué responderías ahora mismo.
2. Recorré las secciones de **caso concreto + imagen + fórmula + intuición**
   en orden, sin saltearte el gráfico.
3. Detenete en el **widget interactivo**: cambiá un parámetro a la vez y
   tratá de **predecir** qué va a pasar antes de mirar el gráfico nuevo.
4. Hacé los **ejercicios** sin ejecutar la verificación primero. Después
   compará tu respuesta con la del módulo de `exercises`.
5. Cuando llegues al **párrafo de cierre**, fijate qué pregunta nueva
   queda abierta: esa es la que motiva el capítulo que sigue.

Este ciclo (pregunta → exploración → fórmula → nueva pregunta) es lo que
mantiene el material del libro hilado de principio a fin.
