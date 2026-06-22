# Deuda pedagógica: Inferencia estadística

Esta página documenta hallazgos concretos surgidos al revisar el capítulo de
**Inferencia estadística** contra la rúbrica de [Enfoque pedagógico](pedagogy.md).
No son cambios obligatorios al material, sino tensiones detectadas entre lo que
el libro promete pedagógicamente y lo que efectivamente entrega en la unidad.
Cada punto incluye el principio que está en juego.

## Carga cognitiva y secuenciación

- **El pivote aparece antes de definirse.** La primera construcción de intervalo
  usa "pivote" como paso operativo, pero la definición formal de cantidad
  pivote llega bastante después. El lector aplica un término técnico antes de
  tener su andamiaje conceptual.
- **Contrastes infiltrados en intervalos.** En la sección de intervalo para la
  media con $\sigma$ conocida aparecen $z$-statistic y $H_0$ antes de abrir la
  sección de tests. Eso mezcla dos familias de herramientas antes de cerrar la
  primera.
- **Estimador y distribución muestral sin sección propia.** El capítulo usa la
  idea de estimador que fluctúa muestra a muestra, y bootstrap la vuelve
  visual, pero no hay una sección que nombre explícitamente "distribución
  muestral" como objeto central.
- **Cuatro recetas antes de la síntesis.** Media con $\sigma$ conocida, $t$,
  proporción Wald y varianza aparecen antes de la unificación por pivotes. La
  síntesis es fuerte, pero llega después de bastante carga procedural.
- **Potencia ausente.** Se introducen errores tipo I y II, pero no aparece
  potencia, $\beta$ ni el vínculo operativo entre $\alpha$, tamaño muestral y
  efecto detectable.
- **Bootstrap tardío.** El remuestreo llega después de intervalos paramétricos,
  pivotes y tests. Como alternativa visual a la distribución muestral, podría
  reducir carga si apareciera antes de la maquinaria de $p$-valores.

## Predicción inconsistente

El capítulo incluye varias pausas: **Antes de seguir**, **Antes de calcular**,
**Antes de mirar**, **Predicción** e **Intentá antes de ejecutar**. La deuda es
la intermitencia: algunas salidas importantes no piden anticipación previa.

Faltan predicciones antes del gráfico Normal vs $t$, del intervalo $t$ para la
clínica, del intervalo de proporción, de la rama de tamaño muestral para
proporciones, del test de la fábrica y de la conexión intervalo ↔ test. La
sección sobre 95% de confianza pide anticipar cobertura, pero no usa el rótulo
estándar del libro, lo que debilita el contrato de generación
[@slamecka1978generation].

## Widgets paralelos en lugar de comparativos

El capítulo tiene piezas comparativas potentes, pero están distribuidas de
forma desigual:

- `build_mean_ci_explorer` materializa bien las líneas paralelas prometidas
  para inferencia, pero proporción, varianza y $t$ no tienen exploradores
  equivalentes.
- Normal vs $t$ se muestra como gráficos estáticos, no como comparación de
  anchos de intervalo para la misma muestra clínica.
- `build_pivot_inversion_explorer` es el diseño correcto porque unifica Normal,
  $t$ y $\chi^2$, pero llega después de varias recetas ya recorridas.
- Bootstrap queda aislado del intervalo $t$: no hay comparación directa sobre
  los mismos datos.
- No existe todavía un explorador de tests que permita mover $\alpha$, efecto,
  tamaño muestral y observar rechazo, $p$-valor o potencia.

Una vista comparativa reduciría carga extrínseca y reforzaría doble
codificación [@paivio1991dual]: mismo problema, varias herramientas, una sola
lectura visual.

## Cierres operativos faltantes

La rúbrica de "Cierres de sección" pide cuatro piezas: qué responde, cuándo
usarlo, qué puede salir mal, cómo comunicarlo. El capítulo tiene cierres muy
fuertes en interpretación del 95%, pivote y trampas del $p$-valor, pero otras
secciones quedan menos cerradas:

- **Intervalo $t$.** Falta contrato explícito, trampa común e interpretación
  comunicable.
- **Proporción.** La advertencia Wald/Wilson aparece, pero no como contrato de
  modelo ni con frase para una encuesta.
- **Varianza.** La lectura "en una frase" ayuda, pero falta traducirla a
  planificación operativa de regularidad o personal.
- **Bootstrap.** Tiene contrato, pero no una **Idea para retener** ni guía de
  comunicación del intervalo percentílico.
- **Tamaño muestral para proporciones.** No cierra con negociación de costo y
  precisión como sí lo hace la rama de media.
- **Tests.** Las trampas del $p$-valor están bien, pero falta una frase modelo
  para el responsable de calidad de la línea y una lista de supuestos que pueden
  romper la decisión.

## Referencias y citaciones internas

El capítulo no usa citas bibliográficas pese a mencionar resultados y escuelas
con nombres propios o convenciones históricas: $t$ de Student, Wald, Wilson,
bootstrap, Neyman-Pearson, Fisher y advertencias contemporáneas sobre
$p$-valores. Citar esos hitos no debería desplazar la explicación, pero sí
reforzaría que cada procedimiento tiene historia, alcance y contrato de uso.

También hay referencias cruzadas a ecuaciones de otros capítulos con labels
cortos. Conviene unificar el estilo con rutas explícitas cuando las etiquetas
viven fuera del archivo, y enlazar entradas concretas del [glosario](glossary.md)
cuando aparecen pivote, $p$-valor, error tipo I/II y potencia.

## Cumplimiento de las convenciones del repositorio

La celda de bootstrap tiene lógica inline: genera números aleatorios, arma un
`DataFrame` y lo convierte a `DataFrame[Observations]` dentro del capítulo. Esa
lógica debería vivir en `src/` para ser testeable, reusable y coherente con la
regla de celdas breves.

También hay celdas de densidad que ensamblan `DensityChartInput` y grillas en el
notebook. La API existe, pero el patrón repite armado visual en lugar de
ofrecer llamadas de mayor nivel.

Los ejercicios embebidos son desiguales: algunos usan `verify_*`, otros sólo
reutilizan objetos o ejecutan el test sin verificación explícita. Si la unidad
promete verificación, interpretación y decisión, todos los ejercicios del
capítulo deberían cerrar ese ciclo.

## Visibilidad del código

Como en otros capítulos posteriores, se oculta principalmente el bloque de
imports y se muestran las celdas largas. Eso deja invisible el mapa de módulos
del libro y visible el detalle más ruidoso: bootstrap manual, armado de
densidades y objetos intermedios.

La alternativa pedagógica es mostrar llamadas de alto nivel a `inference`,
`sampling` y `widgets`, y mover o esconder la mecánica visual que no enseña el
concepto estadístico.

## Bucles narrativos abiertos

- **Clínica bien cerrada.** Lucía vuelve en el capstone y el capítulo cierra el
  arco de espera media con un memo operativo.
- **Encuesta parcialmente abierta.** Hay intervalo y tamaño muestral para
  proporción, pero falta una decisión explícita sobre si el 50% alcanza para un
  titular o informe.
- **Producción desalineada.** La apertura habla de defectos cerca del límite
  contractual, pero el test principal opera sobre una espera media. El hilo de
  conteos/defectos de capítulos previos no llega limpio al test.
- **Bootstrap desconectado del relato.** Usa una muestra sintética Normal en
  lugar de los datos de Lucía o de la muestra ya usada.
- **Potencia sin respuesta.** La pregunta "¿alcanza para afirmar?" no se cierra
  con potencia ni diseño bajo una alternativa relevante.

Estas tensiones no invalidan el capítulo — que ya implementa con solidez la
situación de decisión, la interpretación frecuentista del 95%, el explorador de
pivotes, las trampas del $p$-valor, el capstone de Lucía y el cierre del libro
hacia temas futuros — pero marcan el siguiente nivel de refinamiento posible,
especialmente útil para iteraciones futuras del material.
