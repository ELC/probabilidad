# Deuda pedagógica: Tratamiento de datos

Esta página documenta hallazgos concretos surgidos al revisar el capítulo de
**Tratamiento de datos** contra la rúbrica de [Enfoque pedagógico](pedagogy.md).
No son cambios obligatorios al material, sino tensiones detectadas entre lo
que el libro promete pedagógicamente y lo que efectivamente entrega en la
unidad. Cada punto incluye el principio que está en juego.

## Carga cognitiva y secuenciación

- **Resúmenes anticipados.** El objeto `summary` se muestra completo antes de
  haber definido media, mediana, dispersión, percentiles e IQR. Choca con el
  principio CPA: el lector ve la abstracción antes que cualquier pieza
  concreta. Conviene mostrar fragmentos parciales por sección y dejar la
  tabla completa para el cierre.
- **Vocabulario denso al principio.** La sección de fundamentos introduce
  proceso, variabilidad, población, unidad, variable, muestra, parámetro y
  estadístico en pocas páginas. Un organizador previo [@ausubel1968educational]
  funciona mejor si presenta menos anclajes pero más estables; algunos de
  estos términos pueden diferirse hasta que se vuelven operativamente
  necesarios.
- **Anticipos cercanos.** Percentiles, deciles y cuartiles se anuncian en la
  sección de variables discretas como "puntos de corte" y se desarrollan poco
  después en la sección de posición. La anticipación ayuda a conectar con
  frecuencias acumuladas, pero puede sentirse como un cabo abierto si el
  lector todavía no tiene una tarea concreta para usar esos cortes.

## Cumplimiento de las convenciones del repositorio

`AGENTS.md` establece que cada celda de código sea ≤6 líneas y componga
solamente llamadas a `src/`. La revisión detectó celdas con lógica inline
(generación de muestras bimodales con `np.random` directo, cómputo de la tabla
de regla empírica con comprehensions, construcción manual del DataFrame de
personas por delante, comparación y contraejemplo del CV con `np.random`,
`alt.Chart`, `groupby` y `assign`).

## Bucles narrativos abiertos

- **Serie temporal sin gráfico.** La sección sobre orden temporal argumenta
  que conviene mirar la serie antes de colapsar en frecuencias, pero el
  capítulo nunca muestra la serie de los 80 tiempos en orden de llegada.
- **Justificación del tamaño muestral.** El número $n = 80$ aparece sin
  fundamento y la discusión sobre representatividad queda al final del
  capítulo, ya separada del ejemplo.

Estas tensiones no invalidan el capítulo — que ya implementa con solidez la
mayor parte de los principios listados en [Enfoque pedagógico](pedagogy.md)
— pero marcan el siguiente nivel de refinamiento posible, especialmente útil
para iteraciones futuras del material.
