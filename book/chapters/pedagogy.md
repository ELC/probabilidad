# Enfoque pedagógico

Esta sección explica **cómo está construido** el libro. No usa ningún concepto
nuevo; es una guía para entender por qué cada capítulo recorre las secciones en
el mismo orden y por qué los hilos atraviesan todo el material.

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

## Hilos narrativos

Tres hilos atraviesan el libro y se «picotean» en los capítulos según
corresponda:

- **Hilo A — Sala de espera de una clínica.** Aparece en Tratamiento de datos
  (estadística descriptiva sobre los minutos de espera), en Probabilidad
  (probabilidad condicional de seguir esperando), en Variables aleatorias
  (modelo Exponencial), en Sumas y promedios (TCL aplicado al promedio diario)
  y en Inferencia (IC para la espera media).
- **Hilo B — Encuesta electoral.** Aparece como ejemplo de Bayes en
  Probabilidad, como Binomial en Variables aleatorias, como proporción
  asintóticamente Normal en Sumas y promedios, y como IC + tamaño muestral en
  Inferencia.
- **Hilo C — Línea de producción.** Conteo de defectos en Tratamiento de
  datos; verdadero positivo de un test de calidad en Probabilidad; Binomial y
  Poisson en Variables aleatorias; aproximación Normal en Sumas y promedios;
  test de hipótesis en Inferencia.

Cada capítulo además incluye **al menos un ejemplo independiente** —
desconectado de los hilos — para que el lector vea que las técnicas no están
casadas con un escenario particular: alturas en el capítulo de variables
aleatorias, tablero de Galton en sumas, bootstrap sobre una muestra sintética
en inferencia.

## Preguntas de inicio y síntesis

Cada capítulo arranca con una sección **«Preguntas de inicio»** (3 a 4
preguntas concretas) y termina con dos secciones simétricas:

- **Síntesis y respuestas** — resuelve, una a una, las preguntas planteadas al
  inicio y referencia las ecuaciones numeradas que dieron la respuesta.
- **Próximas preguntas** — formula los interrogantes que el próximo capítulo
  va a abordar. Ese pase es el que da continuidad al recorrido.

Para una guía rápida de notación y términos al pasar entre capítulos, conviene
tener abierto el [glosario](glossary.md).

## Cómo recorrer cada capítulo

Una sugerencia de lectura, especialmente para una primera pasada:

1. Leé las **preguntas de inicio** y anotá, sin pensarlo demasiado, qué
   responderías ahora mismo.
2. Recorré las secciones de **caso concreto + imagen + fórmula + intuición**
   en orden, sin saltearte el gráfico.
3. Detenete en el **widget interactivo**: cambiá un parámetro a la vez y
   tratá de **predecir** qué va a pasar antes de mirar el gráfico nuevo.
4. Hacé los **ejercicios** sin ejecutar la verificación primero. Después
   compará tu respuesta con la del módulo de `exercises`.
5. Volvé a las preguntas de inicio y comparalas con la sección **Síntesis y
   respuestas**: ¿qué cambió en tu intuición?

Este ciclo (pregunta → exploración → fórmula → vuelta a la pregunta) es lo
que mantiene el material del libro hilado de principio a fin.
