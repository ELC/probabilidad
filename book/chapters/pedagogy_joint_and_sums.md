# Deuda pedagógica: Sumas y promedios

Esta página documenta hallazgos concretos surgidos al revisar el capítulo de
**Sumas y promedios** contra la rúbrica de [Enfoque pedagógico](pedagogy.md).
No son cambios obligatorios al material, sino tensiones detectadas entre lo que
el libro promete pedagógicamente y lo que efectivamente entrega en la unidad.
Cada punto incluye el principio que está en juego.

## Carga cognitiva y secuenciación

- **Alcance distinto del nombre del archivo.** `joint_and_sums.md` sugiere
  distribuciones conjuntas, marginales, condicionales, covarianza o correlación,
  pero el capítulo explicita que ese contenido queda fuera del recorrido
  inicial. Es una deuda estructural: el nombre promete más de lo que la unidad
  enseña.
- **Promedios antes que sumas.** La apertura promete promedio y total, pero la
  progresión se concentra mucho más en proporciones y promedios. Las sumas
  operativas llegan tarde, en Galton, Binomial como suma de Bernoullis y la
  sección final de sumas independientes.
- **Vocabulario formal concentrado.** En una misma unidad aparecen i.i.d.,
  convergencia en probabilidad, convergencia en distribución, error estándar,
  corrección por continuidad y suma de varianzas. La **Idea para retener** que
  separa LLN y TCL ayuda, pero llega después de varios conceptos densos.
- **Galton interrumpe el puente LLN → TCL.** El tablero cumple la regla de
  incluir un ejemplo ajeno para favorecer transferencia [@gick1983schema], pero
  aparece justo después de la LLN y antes de aplicar el TCL al hilo clínico.
- **Encuesta incompleta respecto del arco prometido.** La encuesta recibe LLN
  como estabilidad de proporciones, pero no muestra la proporción
  asintóticamente Normal que el enfoque pedagógico anuncia.
- **Sumas independientes sin CPA.** La sección final va directo a ecuaciones de
  esperanza, varianza y suma Normal sin caso concreto, gráfico ni widget.

## Predicción inconsistente

El capítulo usa predicción en la simulación de LLN, Galton y ejercicios. La
deuda central está en el TCL: el overlay histograma + Normal, que es una de las
piezas visuales clave del capítulo, se muestra sin pedir antes una anticipación
de forma, simetría o ajuste en colas.

También faltan pausas generativas antes de la trayectoria múltiple de LLN, el
explorador LLN, el error estándar, la aproximación Normal a la Binomial, la
corrección por continuidad y la sección de sumas independientes. El explorador
TCL pregunta por el efecto de cambiar $n$, pero después de que el lector ya vio
el gráfico estático principal.

## Widgets paralelos en lugar de comparativos

`build_lln_explorer` y `build_clt_explorer` trabajan en silos. El primero
explora estabilidad de proporciones; el segundo compara fuentes como Uniforme y
Exponencial. Ninguno muestra en una misma vista cómo se relacionan LLN y TCL
para el mismo fenómeno.

Hay otras comparaciones prometedoras que quedan sólo en texto:

- Galton y TCL clínico comparten la lógica de sumar muchas piezas, pero se
  visualizan con mecanismos distintos y desconectados.
- Conteo Binomial y promedio de Bernoullis no aparecen lado a lado para el
  mismo $n$ y $p$.
- Suma total y promedio muestral no se contrastan en una misma figura, aunque
  el capítulo los anuncia juntos desde la apertura.

Un widget comparativo reforzaría la doble codificación [@paivio1991dual]:
misma simulación, dos lecturas, una para estabilidad del número y otra para
forma de la fluctuación.

## Cierres operativos faltantes

La rúbrica de "Cierres de sección" pide cuatro piezas: qué responde, cuándo
usarlo, qué puede salir mal, cómo comunicarlo. El capítulo tiene contratos
fuertes para LLN y TCL, pero algunos cierres quedan incompletos:

- **TCL.** Las condiciones i.i.d., varianza finita y tamaño muestral suficiente
  aparecen dispersas. Conviene cerrarlas como checklist operativo antes de usar
  la aproximación.
- **LLN.** Explica estabilidad y trampa común, pero falta una frase de
  comunicación para encuesta: por ejemplo, qué significa observar 400
  respuestas frente a un $p$ subyacente.
- **Error estándar.** La regla de la raíz cuadrada se enuncia, pero la decisión
  de duplicar o cuadruplicar muestra queda más clara en ejercicios que en el
  cuerpo teórico.
- **Sumas independientes.** Falta la trampa común de sumar desvíos en lugar de
  varianzas, un ejemplo numérico y una frase de comunicación sobre tiempo total
  o carga total.

## Referencias y citaciones internas

El capítulo trabaja con resultados clásicos sin atribución bibliográfica:
Galton, ley de los grandes números, teorema central del límite, aproximación de
de Moivre-Laplace y, potencialmente, desigualdad de Chebyshev como puente a la
LLN. No hace falta cargar la lectura histórica, pero una nota breve reforzaría
el contrato conceptual de cada resultado.

También hay referencias cruzadas a ecuaciones de capítulos anteriores con
labels cortos. En una build global pueden resolver, pero el estilo no es
consistente con páginas de ejercicios que usan rutas explícitas. Para una guía
pedagógica estable, conviene unificar el patrón de referencias internas.

## Cumplimiento de las convenciones del repositorio

La celda del tablero de Galton es la deuda técnica más clara: construye un
`DataFrame` y encadena Altair directamente en el capítulo. No existe todavía un
`chart_galton` en `src/visualization/`, de modo que la lógica visual no queda
testeable ni reutilizable.

La promesa **symbolic-first** del repositorio también queda parcial: fórmulas
como $\operatorname{Var}(\bar X_n)=\sigma^2/n$, $\operatorname{Var}(X+Y)$ y la
suma de Normales viven sólo en LaTeX del capítulo, no como expresiones
simbólicas reutilizables en `src/symbolic/`.

Los ejercicios embebidos usan `verify_numeric_answer`, lo cual es positivo. La
tensión es que algunas respuestas están hardcodeadas y el segundo ejercicio no
cierra con interpretación, decisión o comunicación como sí hace el primero.

## Visibilidad del código

Todas las celdas ejecutables usan `:tags: [hide-input]`. Eso oculta llamadas
atómicas que serían útiles para aprender la API: `simulate_lln(...)`,
`chart_clt_comparison(...)`, `build_clt_explorer(...)`. También oculta la celda
con lógica inline de Galton, que es justamente donde más convendría visibilizar
o mover la implementación a `src/`.

La estrategia recomendada es selectiva: ocultar imports y armado visual largo,
pero mostrar llamadas pequeñas que conectan concepto, fórmula y herramienta.

## Bucles narrativos abiertos

- **Clínica sólo como promedio.** El capítulo promedia 30 esperas, pero no
  vuelve al total de minutos del turno aunque la apertura promete totales.
- **Encuesta sin TCL de proporción.** La proporción acumulada ilustra LLN, pero
  falta la forma Normal de $\hat p$ que conecta con inferencia.
- **Producción desconectada.** La aproximación Normal a Binomial usa parámetros
  que no se enlazan con la probabilidad de defectos del capítulo anterior.
- **Lucía ausente.** El capítulo habla de equipos de ingeniería, pero los
  personajes recurrentes desaparecen. Eso debilita aprendizaje situado
  [@lave1991situated].
- **Representatividad sin retorno.** El enfoque pedagógico prometía que la
  representatividad reapareciera como condición del TCL; en este capítulo casi
  no se nombra.

Estas tensiones no invalidan el capítulo — que ya implementa con solidez la
situación de decisión, la distinción LLN/TCL, contratos de modelo y cierre hacia
inferencia — pero marcan el siguiente nivel de refinamiento posible,
especialmente útil para iteraciones futuras del material.
