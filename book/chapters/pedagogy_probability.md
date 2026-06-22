# Deuda pedagógica: Probabilidad

Esta página documenta hallazgos concretos surgidos al revisar el capítulo de
**Probabilidad** contra la rúbrica de [Enfoque pedagógico](pedagogy.md). No son
cambios obligatorios al material, sino tensiones detectadas entre lo que el
libro promete pedagógicamente y lo que efectivamente entrega en la unidad. Cada
punto incluye el principio que está en juego.

## Carga cognitiva y secuenciación

- **Cómputo antes del vocabulario.** El capítulo ejecuta operaciones sobre
  eventos del dado antes de nombrar formalmente espacio muestral, evento y
  resultado. El caso concreto es útil, pero la salida aparece antes de que el
  lector tenga las etiquetas mínimas para interpretarla.
- **Bayes antes del denominador.** La forma simbólica del teorema de Bayes
  aparece antes de la sección de probabilidad total, que explica cómo se arma
  $P(B)$. La fórmula queda apoyada en una pieza que todavía no se enseñó.
- **Vocabulario bayesiano concentrado.** Prevalencia, sensibilidad,
  especificidad, falsos positivos, prior, likelihood y posterior entran en un
  bloque compacto. Un organizador previo [@ausubel1968educational] ayudaría a
  separar qué pertenece al fenómeno y qué pertenece al lenguaje bayesiano.
- **Independencia sólo abstracta.** La sección de independencia da la regla de
  producto y un ejemplo verbal, pero no ofrece cómputo ni gráfico. Para un
  capítulo construido alrededor de diagramas de Venn, ahí se corta la progresión
  concreto → pictórico → abstracto.
- **Definiciones repetidas de Bayes.** La idea "Bayes no convierte evidencia en
  certeza" aparece como **Idea para retener** y luego como **En una frase**. La
  repetición es valiosa si aparece espaciada; en el mismo tramo se vuelve ruido.

## Predicción inconsistente

El capítulo usa bien **Antes de mirar**, **Antes de calcular** y **Predicción**
en regla aditiva, diagnóstico, encuesta, chequeo guiado y ejercicios. Todavía
quedan salidas visuales o numéricas sin pausa generativa previa: el primer
resultado del dado, el Venn de probabilidad condicional, las esperas vistas como
eventos, la tabla de contingencia, Bayes simbólico, la probabilidad total y el
caso de la fábrica.

Como el efecto de generación depende de que el lector intente una respuesta
antes de verla [@slamecka1978generation], conviene aplicar una regla más
uniforme: cada Venn, árbol, tabla o posterior nuevo debería pedir primero una
anticipación concreta.

## Widgets paralelos en lugar de comparativos

El capítulo repite muchas invocaciones de `chart_venn_two_sets` con la misma
estructura: dado, clínica, diagnóstico, encuesta, fábrica y ejercicios. La
repetición muestra consistencia de API, pero pedagógicamente el lector termina
leyendo configuraciones casi idénticas en lugar de comparar escenarios.

Lo mismo ocurre con Bayes: diagnóstico, encuesta y fábrica comparten el patrón
`TotalProbabilityBranch` → `evaluate_bayes` → Venn narrativo. Un explorador
comparativo permitiría ver cómo cambian prior, likelihood y posterior en tres
historias a la vez. El `build_bayes_explorer` actual está fuertemente acoplado
al escenario médico; no generaliza todavía a apoyo electoral o alarmas de
producción.

## Cierres operativos faltantes

La rúbrica de "Cierres de sección" pide cuatro piezas: qué responde, cuándo
usarlo, qué puede salir mal, cómo comunicarlo. Varias secciones terminan en la
figura o en el cómputo sin traducir el resultado a decisión:

- **Regla aditiva.** Falta cerrar con la trampa de sumar sin restar el
  solapamiento y una frase de comunicación.
- **Esperas como eventos.** Se calcula $P(T \mid S)$, pero no se dice qué haría
  Lucía con esa lectura: reforzar personal, avisar al paciente o revisar una
  franja.
- **Tablas de contingencia.** El cociente posterior aparece correctamente, pero
  falta advertencia sobre alarmas y tasas base.
- **Probabilidad total.** El diagrama de partición no cierra con el contrato de
  uso: las ramas deben cubrir todos los casos y no solaparse.
- **Fábrica y ejercicio 2.** Terminan sin **Comunicación** ni **Decisión de
  ingeniería**, a diferencia del chequeo guiado de encuesta.

## Referencias y citaciones internas

El capítulo no tiene citas bibliográficas, aunque trabaja con resultados y
representaciones nombradas. Bayes, Venn y la formalización axiomática de la
probabilidad podrían atribuirse o enlazarse en una nota breve. También conviene
enlazar al [glosario](glossary.md) cuando aparecen evento, partición, prior,
posterior y probabilidad condicional.

Hay una oportunidad técnica adicional: `evaluate_total_probability` existe en
`src/`, pero el capítulo recompone el denominador con una comprensión manual en
un chequeo guiado. Eso rompe la continuidad entre texto, API y contrato del
modelo.

## Cumplimiento de las convenciones del repositorio

`AGENTS.md` establece que cada celda de código sea breve y componga llamadas a
`src/`. La celda inicial de imports es extensa; varias celdas de Venn superan
las seis líneas por configuración repetida, y el primer ejemplo construye
eventos con `frozenset` literales en el capítulo en lugar de una fábrica de
dado en `src/probability`.

Los ejercicios sí usan verificaciones programáticas, lo que está alineado con
la convención del libro. La tensión restante es que las respuestas de estudiante
aparecen hardcodeadas en las celdas, de modo que quien ejecuta sin editar ve
una verificación ya resuelta.

## Visibilidad del código

Aquí la deuda es inversa a la del capítulo de tratamiento de datos. Sólo la
celda de imports está oculta; el resto muestra bloques largos de configuración
de Venn y árboles. El lector ve mucho detalle de presentación y poca llamada
semántica mínima.

La doble codificación [@paivio1991dual] funcionaría mejor si el capítulo
mostrara selectivamente llamadas atómicas como `evaluate_bayes(...)` o
`evaluate_conditional_probability(...)`, y escondiera o abstrajera presets de
visualización repetidos.

## Bucles narrativos abiertos

- **Lucía desaparece.** La clínica abre el capítulo, pero Lucía no vuelve a
  aparecer cuando se calculan probabilidades de esperas largas.
- **Pregunta prospectiva sin cierre.** La apertura pregunta por el próximo
  paciente; el capítulo calcula proporciones históricas pero no enmarca el
  número como respuesta prospectiva con límites claros.
- **Encuesta sin informe.** El "sí" ruidoso se interpreta, pero falta una frase
  de comunicación para el barrio o para quien lee la encuesta.
- **Producción partida en dos.** La tabla de contingencia usa conteos
  observados y la sección bayesiana de fábrica reinicia con parámetros distintos
  sin explicitar el cambio de modelo.
- **Partición genérica.** El diagrama de $A_1,A_2,A_3$ está desconectado de los
  tres escenarios recurrentes, justo cuando podría reforzar aprendizaje situado
  [@lave1991situated].

Estas tensiones no invalidan el capítulo — que ya implementa con solidez la
situación de decisión, recuperación al inicio, Venn como imagen mental, contrato
de Bayes y ejercicios con `verify_*` — pero marcan el siguiente nivel de
refinamiento posible, especialmente útil para iteraciones futuras del material.
