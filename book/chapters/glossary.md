# Glosario

Esta página reúne los símbolos y los términos que aparecen en el libro. La
columna **Aparece en** apunta a la subsección donde el concepto se introduce
por primera vez (cuando hay una ecuación numerada que lo define, también se
indica).

## Símbolos

| Símbolo | Nombre | Aparece en |
| --- | --- | --- |
| $\Omega$ | Espacio muestral (universo de resultados) | [Un experimento concreto](#sec-prob-experiment) |
| $A$, $B$, $C$ | Eventos (subconjuntos de $\Omega$) | [Un experimento concreto](#sec-prob-experiment) |
| $\bar{A}$ | Complemento de $A$ | [Un experimento concreto](#sec-prob-experiment), ec. (2.2) |
| $A \cup B$ | Unión de eventos | [La regla aditiva](#sec-prob-additive), ec. (2.1)–(2.2) |
| $A \cap B$ | Intersección de eventos | [La regla aditiva](#sec-prob-additive), ec. (2.1) |
| $P(A)$ | Probabilidad del evento $A$ | [Un experimento concreto](#sec-prob-experiment) |
| $P(A \mid B)$ | Probabilidad condicional de $A$ dado $B$ | [Probabilidad condicional](#sec-prob-conditional), ec. (2.3) |
| $n$ | Tamaño de la muestra | [Una muestra de tiempos de espera](#sec-descriptive-sample) |
| $x_1, \dots, x_n$, $x_i$ | Observaciones individuales de la muestra | [Una muestra de tiempos de espera](#sec-descriptive-sample) |
| $\bar{x}$ | Media muestral | [Tres preguntas que resumen la muestra](#sec-descriptive-summary), ec. (1.1) |
| $\tilde{x}$ | Mediana muestral | [Por qué la mediana resiste lo que la media no](#sec-descriptive-median), ec. (1.2) |
| $\text{SS}$ | Suma de cuadrados $\sum(x_i - \bar{x})^2$ | [Tres preguntas que resumen la muestra](#sec-descriptive-summary) |
| $s$ | Desvío estándar muestral (divisor $n-1$) | [Tres preguntas que resumen la muestra](#sec-descriptive-summary), ec. (1.4) |
| $R$ | Rango muestral $\max_i x_i - \min_i x_i$ | [Tres preguntas que resumen la muestra](#sec-descriptive-summary) |
| $s^2$, $S^2$ | Varianza muestral | [Tres preguntas que resumen la muestra](#sec-descriptive-summary), ec. (1.3) |
| $Q_1$, $Q_3$ | Primer y tercer cuartil | [Posición dentro de la muestra: cuartiles y percentiles](#sec-descriptive-position) |
| $\text{IQR}$ | Rango intercuartil $Q_3 - Q_1$ | [Detección de outliers — la regla de Tukey](#sec-descriptive-tukey), ec. (1.6) |
| $CV$ | Coeficiente de variación $s/\bar{x}$ | [Comparar dispersión en escalas distintas](#sec-descriptive-cv), ec. (1.8) |
| $z_i$ | $z$-score (standard score) muestral de la observación $x_i$ | [Posición relativa: el $z$-score](#sec-descriptive-zscore), ec. (1.5) |
| $z_{\text{obs}}$ | Valor observado del estadístico $Z$ en un test $z$ ($z$-statistic) | [IC para la espera media con $\sigma$ conocido](#sec-inf-mean-known), ec. (5.1) |
| $X$, $Y$, $T$ | Variables aleatorias | [De eventos sueltos a distribuciones](#sec-rv-distribution) |
| $X_i$ | $i$-ésima v.a. en una secuencia i.i.d. | [Repetir bajo las mismas reglas](#sec-sums-iid) |
| $E[X]$, $\mu$ | Esperanza | [Contar defectos con una Binomial](#sec-rv-binomial) |
| $\mathrm{Var}(X)$, $\sigma^2$ | Varianza poblacional | [Contar defectos con una Binomial](#sec-rv-binomial) |
| $\sigma$ | Desvío estándar poblacional | [Contar defectos con una Binomial](#sec-rv-binomial) |
| $p$ | Probabilidad de éxito (Bernoulli / Binomial / Geométrica) | [Una respuesta sí/no: Bernoulli](#sec-rv-bernoulli) |
| $k$ | Valor concreto de una v.a. discreta | [Contar defectos con una Binomial](#sec-rv-binomial) |
| $P(X = k)$ | Función de probabilidad puntual (PMF) | [De eventos sueltos a distribuciones](#sec-rv-distribution) |
| $\text{Bernoulli}(p)$ | Distribución Bernoulli | [Una respuesta sí/no: Bernoulli](#sec-rv-bernoulli), ec. (3.3) |
| $\text{Bin}(n, p)$ | Distribución Binomial | [Contar defectos con una Binomial](#sec-rv-binomial), ec. (3.4) |
| $\text{Geom}(p)$ | Distribución Geométrica | [Esperar hasta el primer éxito: Geométrica](#sec-rv-geometric), ec. (3.5) |
| $f_X(x)$ | Función de densidad (PDF) | [Alturas con la Normal](#sec-rv-normal), ec. (3.2) |
| $\mathcal{N}(\mu, \sigma^2)$ | Distribución Normal | [Alturas con la Normal](#sec-rv-normal), ec. (3.2) |
| $Z$ | Variable Normal estándar $\mathcal{N}(0, 1)$ | [Estandarización](#sec-rv-standardize), ec. (3.4) |
| $F_X(x)$ | Función de distribución acumulada (CDF) | [De eventos sueltos a distribuciones](#sec-rv-distribution), ec. (3.1) |
| $S_X(x)$ | Función de supervivencia / cola derecha | [De eventos sueltos a distribuciones](#sec-rv-distribution), ec. (3.2) |
| $F_X^{-1}(\alpha)$, $x_\alpha$ | Cuantil $\alpha$ | [Cuantiles: invertir la pregunta](#sec-rv-quantiles), ec. (3.5) |
| $\lambda$ | Tasa (Poisson / Exponencial) | [El tiempo de espera como Exponencial](#sec-rv-exponential), ec. (3.9); [Conteos y esperas](#sec-rv-poisson-exponential) |
| $\text{Exp}(\lambda)$ | Distribución Exponencial | [El tiempo de espera como Exponencial](#sec-rv-exponential), ec. (3.9) |
| $\text{Poisson}(\lambda)$ | Distribución Poisson | [Poisson: contar eventos raros](#sec-rv-poisson), ec. (3.11) |
| $\bar{X}_n$ | Media muestral aleatoria | [La proporción observada se estabiliza](#sec-sums-lln), ec. (4.1) |
| $\xrightarrow{P}$ | Convergencia en probabilidad | [La proporción observada se estabiliza](#sec-sums-lln), ec. (4.2) |
| $\xrightarrow{d}$ | Convergencia en distribución | [El TCL formal](#sec-sums-clt), ec. (4.3) |
| $Z_n$ | Promedio estandarizado | [El TCL formal](#sec-sums-clt), ec. (4.3) |
| $SE(\bar X_n)$ | Error estándar del promedio | [El error estándar del promedio](#sec-sums-standard-error), ec. (4.5) |
| $\hat{p}$ | Proporción muestral | [IC para una proporción](#sec-inf-proportion), ec. (5.4) |
| $\alpha$ | Nivel de significancia / probabilidad de error tipo I | [IC para la espera media con $\sigma$ conocido](#sec-inf-mean-known) |
| $z_{1-\alpha/2}$ | Cuantil de la Normal estándar | [IC para la espera media con $\sigma$ conocido](#sec-inf-mean-known), ec. (5.2), (5.4); [El método del pivote](#sec-inf-pivot) |
| $t_{n-1,\,1-\alpha/2}$ | Cuantil de la $t$ de Student | [IC con $\sigma$ desconocido — la $t$ de Student](#sec-inf-mean-unknown), ec. (5.3); [El método del pivote](#sec-inf-pivot) |
| $\chi^2_{n-1}$ | Distribución chi-cuadrado con $n-1$ grados de libertad | [IC para la varianza — la $\chi^2$](#sec-inf-variance), ec. (5.5); [El método del pivote](#sec-inf-pivot) |
| $Q(\mathbf{X};\,\theta)$ | Cantidad pivote: función de datos y parámetro con distribución libre de $\theta$ | [El método del pivote](#sec-inf-pivot), ec. (5.7) |
| $H_0$, $H_1$ | Hipótesis nula y alternativa | [Test de hipótesis sobre la espera media](#sec-inf-test), ec. (5.12) |
| $\mu_0$ | Valor de control bajo $H_0$ | [Test de hipótesis sobre la espera media](#sec-inf-test), ec. (5.12) |
| $T$ (estadístico) | Estadístico del test $t$ | [Test de hipótesis sobre la espera media](#sec-inf-test), ec. (5.12) |
| $E$ | Margen de error | [Tamaño muestral para una precisión dada](#sec-inf-sample-size), ec. (5.13), (5.14) |

## Términos

| Término | Significado breve | Aparece en |
| --- | --- | --- |
| Observación | Valor numérico registrado de una unidad de la muestra. | [Una muestra de tiempos de espera](#sec-descriptive-sample) |
| Muestra | Conjunto finito de observaciones; en código vive como `Observations`. | [Una muestra de tiempos de espera](#sec-descriptive-sample) |
| Representatividad | Grado en que la muestra se parece al proceso o población sobre la que queremos decidir. | [Antes de inferir: cómo se juntaron los datos](#sec-descriptive-sampling) |
| Sesgo | Patrón de recolección o medición que empuja los datos sistemáticamente en una dirección. | [Antes de inferir: cómo se juntaron los datos](#sec-descriptive-sampling) |
| Independencia de observaciones | Condición bajo la cual una observación no arrastra mecánicamente a la siguiente. | [Antes de inferir: cómo se juntaron los datos](#sec-descriptive-sampling) |
| Tabla de frecuencias | Conteo absoluto, relativo y acumulado por intervalos. | [Agrupar la lista antes de resumir](#sec-descriptive-frequency), ec. (1.1) |
| Histograma | Barras que muestran cómo se reparte la frecuencia por intervalos. | [Agrupar la lista antes de resumir](#sec-descriptive-frequency) |
| Ojiva | Curva de frecuencia acumulada por intervalos. | [Agrupar la lista antes de resumir](#sec-descriptive-frequency) |
| Percentil | Valor que deja cierto porcentaje de observaciones por debajo. | [Posición dentro de la muestra: cuartiles y percentiles](#sec-descriptive-position) |
| Suma de cuadrados | $\sum(x_i - \bar{x})^2$, paso intermedio para $s$. | [Tres preguntas que resumen la muestra](#sec-descriptive-summary) |
| Outlier | Observación fuera de $[Q_1 - 1{,}5\,\text{IQR},\ Q_3 + 1{,}5\,\text{IQR}]$. | [Detección de outliers — la regla de Tukey](#sec-descriptive-tukey) |
| $z$-score (*standard score*) | Distancia de una observación a la media, expresada en unidades de desvío estándar. | [Posición relativa: el $z$-score](#sec-descriptive-zscore) |
| $z$-statistic | Valor del estadístico de prueba estandarizado bajo $H_0$ en un test $z$. | [IC para la espera media con $\sigma$ conocido](#sec-inf-mean-known), [Test de hipótesis sobre la espera media](#sec-inf-test) |
| Coeficiente de variación | Cociente $s/\bar{x}$, adimensional. | [Comparar dispersión en escalas distintas](#sec-descriptive-cv), ec. (1.8) |
| Evento | Subconjunto del espacio muestral. | [Un experimento concreto](#sec-prob-experiment) |
| Complemento | Evento formado por todo lo que queda fuera de otro evento. | [Un experimento concreto](#sec-prob-experiment), ec. (2.2) |
| Independencia de eventos | Condición bajo la cual saber que ocurrió un evento no cambia la probabilidad del otro. | [Cuando saber una cosa no cambia la otra](#sec-prob-independence), ec. (2.4) |
| Tabla de contingencia | Tabla que cruza dos eventos o categorías para leer conjuntas, marginales y condicionales. | [Tablas de contingencia: contar antes de dividir](#sec-prob-contingency) |
| Partición | Familia de eventos disjuntos cuya unión es $\Omega$. | [Probabilidad total — armar el denominador](#sec-prob-total), ec. (2.6) |
| Probabilidad total | Descompone $P(B)$ usando una partición. | [Probabilidad total — armar el denominador](#sec-prob-total), ec. (2.6) |
| Teorema de Bayes | Invierte el sentido del condicionamiento. | [Teorema de Bayes (forma simbólica)](#sec-prob-bayes-symbolic), ec. (2.4) |
| Prevalencia | $P(D)$ — probabilidad a priori de la enfermedad / clase positiva. | [Bayes con datos: prueba diagnóstica](#sec-prob-bayes-data) |
| Sensibilidad | $P(+ \mid D)$ del test diagnóstico. | [Bayes con datos: prueba diagnóstica](#sec-prob-bayes-data) |
| Especificidad | $P(- \mid \bar{D})$ del test diagnóstico. | [Bayes con datos: prueba diagnóstica](#sec-prob-bayes-data) |
| Prior / creencia previa | Probabilidad antes de observar la evidencia. | [Bayes con datos: prueba diagnóstica](#sec-prob-bayes-data) |
| Likelihood / verosimilitud | Probabilidad de la evidencia bajo una causa o estado posible. | [Bayes con datos: prueba diagnóstica](#sec-prob-bayes-data) |
| Posterior | Probabilidad actualizada después de observar la evidencia. | [Bayes con datos: prueba diagnóstica](#sec-prob-bayes-data) |
| Variable aleatoria | Función $X: \Omega \to \mathbb{R}$. | [De eventos sueltos a distribuciones](#sec-rv-distribution) |
| PMF | *Probability mass function* — distribución discreta. | [De eventos sueltos a distribuciones](#sec-rv-distribution) |
| Esperanza | Promedio teórico de la distribución. | [Contar defectos con una Binomial](#sec-rv-binomial) |
| Varianza | Promedio teórico del cuadrado del desvío. | [Contar defectos con una Binomial](#sec-rv-binomial) |
| Moda | Valor individual más probable de una distribución. | [Contar defectos con una Binomial](#sec-rv-binomial) |
| Bernoulli | Variable indicadora con éxito $p$. | [Una respuesta sí/no: Bernoulli](#sec-rv-bernoulli), ec. (3.3) |
| Geométrica | Distribución del número de intento en el que aparece el primer éxito. | [Esperar hasta el primer éxito: Geométrica](#sec-rv-geometric), ec. (3.5) |
| PDF | *Probability density function* — distribución continua. | [De eventos sueltos a distribuciones](#sec-rv-distribution) |
| Estandarización | Transformación $Z = (X - \mu)/\sigma$. | [Estandarización](#sec-rv-standardize), ec. (3.4) |
| CDF | *Cumulative distribution function*. | [De eventos sueltos a distribuciones](#sec-rv-distribution), ec. (3.1) |
| Supervivencia | Complemento de la CDF: $P(X>x)$. | [De eventos sueltos a distribuciones](#sec-rv-distribution), ec. (3.2) |
| Cuantil | Valor con probabilidad acumulada $\alpha$ por debajo. | [Cuantiles: invertir la pregunta](#sec-rv-quantiles), ec. (3.5) |
| i.i.d. | Independientes e idénticamente distribuidas. | [Repetir bajo las mismas reglas](#sec-sums-iid) |
| LLN | Ley de los grandes números: $\bar{X}_n \to \mu$. | [La proporción observada se estabiliza](#sec-sums-lln), ec. (4.2) |
| Tablero de Galton | Suma de $\pm 1$ independientes; ilustra el TCL. | [El tablero de Galton](#sec-sums-galton) |
| TCL | Teorema central del límite: $Z_n \to \mathcal{N}(0,1)$. | [El TCL formal](#sec-sums-clt), ec. (4.3) |
| Error estándar | Desvío estándar de un estimador de muestra a muestra. | [El error estándar del promedio](#sec-sums-standard-error), ec. (4.5) |
| Corrección por continuidad | Ajuste de medio punto al aproximar una distribución discreta con una continua. | [Aproximación Binomial → Normal](#sec-sums-binomial-normal), ec. (4.8) |
| Suma de independientes | Regla para sumar esperanzas y, bajo independencia, varianzas. | [Sumar variables independientes](#sec-sums-independent-sums), ec. (4.9)–(4.11) |
| Aproximación Binomial-Normal | $\text{Bin}(n,p) \approx \mathcal{N}(np, np(1-p))$ para $n$ grande. | [Aproximación Binomial → Normal](#sec-sums-binomial-normal), ec. (4.4) |
| Pivote / cantidad pivote | Función de los datos y del parámetro cuya distribución es libre de parámetros desconocidos. | [El método del pivote](#sec-inf-pivot), ec. (5.7) |
| Método del pivote | Receta general que construye un IC eligiendo dos cuantiles de la distribución del pivote y despejando el parámetro. La forma "estadístico ± percentil × dispersión" aparece como caso particular cuando el pivote es afín y la referencia es simétrica. | [El método del pivote](#sec-inf-pivot), ec. (5.7)–(5.11) |
| Intervalo de confianza | Procedimiento que cubre $\theta$ con probabilidad $1 - \alpha$. | [IC para la espera media con $\sigma$ conocido](#sec-inf-mean-known), ec. (5.2); [El método del pivote](#sec-inf-pivot) |
| Grados de libertad | Cantidad de piezas de información independientes que quedan después de estimar restricciones. | [IC con $\sigma$ desconocido — la $t$ de Student](#sec-inf-mean-unknown) |
| Wald | Intervalo asintótico para proporciones basado en aproximación Normal. | [IC para una proporción](#sec-inf-proportion), ec. (5.4) |
| Margen de error | Mitad del ancho del intervalo de confianza. | [IC para la espera media con $\sigma$ conocido](#sec-inf-mean-known), ec. (5.2), (5.4) |
| Hipótesis nula | Afirmación de control que el test intenta refutar. | [Test de hipótesis sobre la espera media](#sec-inf-test), ec. (5.12) |
| Hipótesis alternativa | Lo que aceptamos si rechazamos $H_0$. | [Test de hipótesis sobre la espera media](#sec-inf-test) |
| Test bilateral | Test cuya región extrema se reparte entre dos colas. | [Test de hipótesis sobre la espera media](#sec-inf-test) |
| Test unilateral | Test cuya región extrema queda en una sola dirección. | [Test de hipótesis sobre la espera media](#sec-inf-test) |
| Error tipo I | Rechazar $H_0$ cuando era cierta; falsa alarma. | [Test de hipótesis sobre la espera media](#sec-inf-test) |
| Error tipo II | No rechazar $H_0$ cuando era falsa; no detectar un cambio real. | [Test de hipótesis sobre la espera media](#sec-inf-test) |
| $p$-valor | Probabilidad bajo $H_0$ de un estadístico tan extremo o más. | [Test de hipótesis sobre la espera media](#sec-inf-test) |
| Bootstrap | Remuestreo con reemplazo para estimar distribuciones. | [Bootstrap sin supuestos paramétricos](#sec-inf-bootstrap) |
| Tamaño muestral | $n$ necesario para asegurar un margen de error dado. | [Tamaño muestral para una precisión dada](#sec-inf-sample-size), ec. (5.13), (5.14) |
| Contrato del modelo | Lista breve de cuándo aplica una herramienta, qué supuestos necesita, qué puede romperla y cómo interpretar su salida. | Aparece como pausa de lectura junto a modelos y procedimientos principales. |
| Supuesto | Condición que debe ser razonable para que una fórmula o aproximación sostenga la interpretación prometida. | Aparece en los contratos de modelo. |
| Comunicación de incertidumbre | Traducción de un resultado estadístico a una frase que conserva rango, nivel de confianza, límites y decisión posible. | [Capstone — un memo con incertidumbre](#sec-inf-capstone) |
