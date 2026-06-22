# Deuda pedagógica: Variables aleatorias

Esta página documenta hallazgos concretos surgidos al revisar el capítulo de
**Variables aleatorias** contra la rúbrica de [Enfoque pedagógico](pedagogy.md).
No son cambios obligatorios al material, sino tensiones detectadas entre lo que
el libro promete pedagógicamente y lo que efectivamente entrega en la unidad.
Cada punto incluye el principio que está en juego.

## Carga cognitiva y secuenciación

- **PMF, PDF, CDF y supervivencia en bloque abstracto.** La sección inicial
  introduce cuatro objetos técnicos antes de consolidar una imagen visual. Para
  un lector novel, la distinción discreto/continuo queda cargada de símbolos
  antes de que aparezcan barras, áreas o acumulación.
- **La apertura clínica queda diferida.** El capítulo abre con esperas
  continuas y probabilidad puntual cero, pero el primer modelo desarrollado es
  Bernoulli para encuesta. La Exponencial que responde al hilo clínico llega
  bastante más adelante, después de Bernoulli, Binomial, Geométrica y Normal.
- **Encuesta fragmentada.** La Bernoulli introduce una respuesta sí/no, pero la
  Binomial de encuesta aparece mucho después. El lector debe sostener el hilo
  electoral mientras atraviesa otros modelos.
- **Advertencia discreto/continuo repetida.** La diferencia entre barras y
  áreas aparece varias veces. La repetición es correcta conceptualmente, pero
  sería más eficiente en una comparación visual unificada.
- **Geométrica con orden invertido.** La fórmula y el gráfico aparecen antes de
  una pausa tipo "antes de mirar". La progresión CPA queda desordenada:
  abstracto → pictórico → predicción.

## Predicción inconsistente

El capítulo usa bien **Antes de mirar** o **Predicción** en Binomial,
Exponencial, Poisson, exploradores y varios ejercicios. Todavía quedan
herramientas nuevas sin compromiso previo del lector: Bernoulli, Geométrica,
Normal, probabilidad de cola, cuantiles, estandarización, encuesta Binomial y
el explorador de distribuciones discretas.

Como el efecto de generación [@slamecka1978generation] se apoya en intentar una
respuesta antes de ver el resultado, la regla editorial debería ser más pareja:
si aparece una PMF, PDF, cuantíl, cola o widget nuevo, antes debería haber una
pregunta de dirección, forma u orden de magnitud.

## Widgets paralelos en lugar de comparativos

El capítulo combina varios gráficos estáticos con dos exploradores separados:
uno continuo y otro discreto. Esa separación simplifica la interfaz, pero
debilita comparaciones que el texto sí sugiere:

- Bernoulli, Binomial, Geométrica y Poisson no conviven en un mismo espacio de
  comparación.
- Normal y Exponencial se alternan, pero no se conectan visualmente con el
  problema clínico que abrió el capítulo.
- La sección de conteos y esperas explica verbalmente el vínculo Poisson /
  Exponencial, pero no muestra ambas distribuciones lado a lado con el mismo
  parámetro.

Un comparador visual reforzaría doble codificación [@paivio1991dual]: la
relación entre conteos discretos y tiempos continuos quedaría visible, no sólo
enunciada.

## Cierres operativos faltantes

La rúbrica de "Cierres de sección" pide cuatro piezas: qué responde, cuándo
usarlo, qué puede salir mal, cómo comunicarlo. Varias secciones quedan cortas:

- **Bernoulli.** Cierra prometiendo que será importante para el TCL, pero no
  dice cuándo modelar una respuesta como Bernoulli ni cómo comunicar una
  probabilidad de éxito.
- **Geométrica.** Falta contrato de modelo: intentos independientes, misma
  probabilidad de éxito y conteo hasta el primer éxito.
- **Estandarización.** Termina en fórmula sin una frase operativa que distinga
  un $z$ poblacional de un estadístico muestral.
- **Cuantiles.** La escena de talles es fuerte, pero el cierre muestra sólo el
  número; falta traducirlo a decisión de diseño.
- **Encuesta y Poisson.** Las salidas muestran forma y momentos, pero no
  definen umbrales de alerta ni una comunicación para operaciones.

## Referencias y citaciones internas

El capítulo no usa citas bibliográficas, aunque introduce distribuciones con
nombres propios: Bernoulli, Binomial, Poisson, Normal y Exponencial. No hace
falta convertir el capítulo en historia de la estadística, pero una nota breve
o una cita canónica puede reforzar que esas familias no son convenciones
arbitrarias.

También falta el enlace de ida al [glosario](glossary.md). El glosario sí
apunta a las secciones de variables aleatorias, pero el capítulo no remite al
lector cuando aparecen PMF, PDF, CDF, cuantiles o familias paramétricas.

Hay una deuda de precisión narrativa: el texto describe como "simulación" un
resultado que proviene de un cómputo analítico. Esa palabra puede confundir el
contrato entre modelo, cálculo exacto y experimento computacional.

## Cumplimiento de las convenciones del repositorio

`AGENTS.md` pide celdas breves que compongan llamadas a `src/`. Varias celdas
de gráficos son largas porque construyen `ProbabilityMassInput`,
`DensityChartInput` y parámetros en el propio capítulo. Además, una celda accede
directamente a `.frozen_distribution.cdf`, salteando una función pública de
`distributions` y debilitando el patrón de inputs tipados.

La capa simbólica también queda aplicada de manera irregular. Binomial y Poisson
usan momentos simbólicos, pero Normal y Exponencial recurren a momentos
numéricos aunque existen funciones simbólicas en `src/symbolic/`. La promesa
**symbolic-first** del repositorio quedaría mejor si todas las familias
siguieran el mismo patrón.

## Visibilidad del código

El capítulo muestra casi todas las celdas y oculta principalmente los imports.
Eso expone al lector a bastante boilerplate de visualización, mientras el mapa
de API queda fuera de la vista. Es el patrón inverso al capítulo de tratamiento
de datos: allí se oculta demasiado; aquí se muestra demasiado detalle de armado.

Una alternativa más consistente sería mostrar llamadas atómicas como
`make_binomial(...)`, `evaluate_probability_mass(...)` o `tail_probability...`,
y mover presets largos de gráficos a helpers de `src/visualization`.

## Bucles narrativos abiertos

- **Recuperación inicial blanda.** El capítulo abre con un **Antes de seguir**
  genérico, no con dos o tres preguntas concretas como promete la rúbrica de
  recuperación activa.
- **Situación de decisión despersonalizada.** Se habla de "el equipo", no de
  Lucía, la encuesta o producción. Eso debilita la continuidad de aprendizaje
  situado [@lave1991situated].
- **Clínica diferida.** La escena inicial de esperas no vuelve hasta la
  Exponencial, varias secciones después.
- **Encuesta partida.** Bernoulli aparece temprano, pero la Binomial electoral
  llega tarde y sin puente narrativo.
- **Geométrica como escenario suelto.** Las llamadas son un ejemplo útil, pero
  no pertenecen a los tres hilos recurrentes ni se integran luego.
- **Promesa al TCL sin mini-cierre.** La Bernoulli se anuncia como importante
  para el capítulo siguiente, pero no se cierra con una síntesis explícita que
  prepare esa transferencia.

Estas tensiones no invalidan el capítulo — que ya implementa con solidez varios
contratos de modelo, exploradores, ejercicios con verificación e interpretación,
y un cierre hacia sumas y promedios — pero marcan el siguiente nivel de
refinamiento posible, especialmente útil para iteraciones futuras del material.
