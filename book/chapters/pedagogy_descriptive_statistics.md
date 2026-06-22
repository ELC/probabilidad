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

## Predicción inconsistente

El recurso de **Predicción** está bien usado en media, moda, mediana, desvío
estándar, rango, IQR, percentiles y coeficiente de variación. Todavía queda
intermitente en algunas secciones que introducen herramientas nuevas, como el
boxplot interactivo y el z-score. Como el efecto de generación depende de la
frecuencia y consistencia del intento previo [@slamecka1978generation], esa
intermitencia debilita el contrato implícito con el lector. Conviene aplicar
una regla explícita: si una sección introduce una herramienta y termina con un
gráfico, tabla o lectura operativa, debería abrir con una predicción o un
chequeo previo.

## Widgets paralelos en lugar de comparativos

El capítulo presenta seis exploradores separados (uno por medida) construidos
todos con el mismo `SummaryEvolutionExplorerInput`. Pedagógicamente, el
objetivo declarado es comparar cómo reacciona cada medida al mismo dato
extremo. Seis widgets aislados no permiten esa comparación directa: el lector
agrega 20 minutos en uno y vuelve a agregarlos en otro, repitiendo el
ejercicio en lugar de contrastar. La síntesis ideal es **un único explorador**
que muestre todas las curvas superpuestas frente al mismo input — coherente
con el modelo de comparación dentro de una sola representación visual
[@paivio1991dual].

## Cierres operativos faltantes

La rúbrica de "Cierres de sección" pide cuatro piezas: qué responde, cuándo
usarlo, qué puede salir mal, cómo comunicarlo. Varias secciones del capítulo
terminan en el cómputo y dejan implícitas las otras tres. Casos puntuales:
sesgo y colas no menciona el coeficiente de asimetría de Pearson
[@pearson1895skew]; la regla empírica no muestra un contraejemplo en una
distribución sesgada. El coeficiente de variación ya incorporó una advertencia
fuerte, un contraejemplo visual y una nota técnica desplegable; por eso dejó de
ser una deuda conceptual, aunque aumentó la tensión técnica señalada más abajo.

## Referencias y citaciones internas

El capítulo invoca al menos dos referencias que el texto no entrega:

- La respuesta de un ejercicio dice "en símbolos del glosario" pero el
  capítulo no incluye glosario propio ni link al glosario general.
- La regla de Tukey para outliers se enuncia sin atribución, aunque proviene
  de un trabajo bien identificable [@tukey1977exploratory]. Citarla refuerza
  el principio de "contrato del modelo": el lector ve de dónde sale la
  convención del $1{,}5\,\text{IQR}$.

## Cumplimiento de las convenciones del repositorio

`AGENTS.md` establece que cada celda de código sea ≤6 líneas y componga
solamente llamadas a `src/`. La revisión detectó celdas con lógica inline
(generación de muestras bimodales con `np.random` directo, cómputo de la tabla
de regla empírica con comprehensions, construcción manual del DataFrame de
personas por delante, comparación y contraejemplo del CV con `np.random`,
`alt.Chart`, `groupby` y `assign`).

La verificación programática con `exercises.verify_*` corresponde a las páginas
de ejercicios, no necesariamente a este capítulo teórico. En esta unidad, las
preguntas de boxplot y las predicciones funcionan como auto-chequeo narrativo;
si luego se agrega una página de práctica asociada, ahí sí convendría convertir
parte de esas preguntas en verificaciones automáticas.

## Visibilidad del código

Todas las celdas usan `:tags: [hide-input]`. Si el libro enseña a hacer
estadística *en Python*, ocultar incluso las llamadas atómicas como
`summarize_observations(...)` impide aprender la API. La doble codificación
[@paivio1991dual] sugiere que mostrar selectivamente esas llamadas —
manteniendo ocultos los bloques largos de armado de gráficos — refuerza la
conexión entre concepto, fórmula y herramienta computacional.

## Bucles narrativos abiertos

- **Serie temporal sin gráfico.** La sección sobre orden temporal argumenta
  que conviene mirar la serie antes de colapsar en frecuencias, pero el
  capítulo nunca muestra la serie de los 80 tiempos en orden de llegada.
- **Justificación del tamaño muestral.** El número $n = 80$ aparece sin
  fundamento y la discusión sobre representatividad queda al final del
  capítulo, ya separada del ejemplo.
- **Bimodalidad sin decisión.** El ejemplo unimodal vs bimodal ilustra el
  límite del boxplot, pero no propone qué decisión específica cambiaría
  Lucía si descubriera bimodalidad real en su mañana.

Estas tensiones no invalidan el capítulo — que ya implementa con solidez la
mayor parte de los principios listados en [Enfoque pedagógico](pedagogy.md)
— pero marcan el siguiente nivel de refinamiento posible, especialmente útil
para iteraciones futuras del material.
