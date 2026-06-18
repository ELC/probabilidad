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
| $\bar{A}$ | Complemento de $A$ | [La regla aditiva](#sec-prob-additive) |
| $A \cup B$ | Unión de eventos | [La regla aditiva](#sec-prob-additive), ec. (2.1)–(2.2) |
| $A \cap B$ | Intersección de eventos | [La regla aditiva](#sec-prob-additive), ec. (2.1) |
| $P(A)$ | Probabilidad del evento $A$ | [Un experimento concreto](#sec-prob-experiment) |
| $P(A \mid B)$ | Probabilidad condicional de $A$ dado $B$ | [Probabilidad condicional](#sec-prob-conditional), ec. (2.3) |
| $n$ | Tamaño de la muestra | [Una muestra de tiempos de espera](#sec-descriptive-sample) |
| $x_1, \dots, x_n$, $x_i$ | Observaciones individuales de la muestra | [Una muestra de tiempos de espera](#sec-descriptive-sample) |
| $\bar{x}$ | Media muestral | [Resumir con tres miradas](#sec-descriptive-summary), ec. (1.1) |
| $\tilde{x}$ | Mediana muestral | [Por qué la mediana resiste lo que la media no](#sec-descriptive-median), ec. (1.2) |
| $\text{SS}$ | Suma de cuadrados $\sum(x_i - \bar{x})^2$ | [Resumir con tres miradas](#sec-descriptive-summary) |
| $s$ | Desvío estándar muestral (divisor $n-1$) | [Resumir con tres miradas](#sec-descriptive-summary), ec. (1.3) |
| $s^2$, $S^2$ | Varianza muestral | [Resumir con tres miradas](#sec-descriptive-summary) |
| $Q_1$, $Q_3$ | Primer y tercer cuartil | [Detección de outliers — la regla de Tukey](#sec-descriptive-tukey), ec. (1.4) |
| $\text{IQR}$ | Rango intercuartil $Q_3 - Q_1$ | [Detección de outliers — la regla de Tukey](#sec-descriptive-tukey), ec. (1.4) |
| $z_i$ | $z$-score muestral de la observación $x_i$ | [Posición relativa: el $z$-score](#sec-descriptive-zscore), ec. (1.5) |
| $X$, $Y$, $T$ | Variables aleatorias | [Contar defectos con una Binomial](#sec-rv-binomial) |
| $X_i$ | $i$-ésima v.a. en una secuencia i.i.d. | [La proporción observada se estabiliza](#sec-sums-lln) |
| $E[X]$, $\mu$ | Esperanza | [Contar defectos con una Binomial](#sec-rv-binomial) |
| $\mathrm{Var}(X)$, $\sigma^2$ | Varianza poblacional | [Contar defectos con una Binomial](#sec-rv-binomial) |
| $\sigma$ | Desvío estándar poblacional | [Contar defectos con una Binomial](#sec-rv-binomial) |
| $p$ | Probabilidad de éxito (Bernoulli / Binomial) | [Contar defectos con una Binomial](#sec-rv-binomial) |
| $k$ | Valor concreto de una v.a. discreta | [Contar defectos con una Binomial](#sec-rv-binomial) |
| $P(X = k)$ | Función de probabilidad puntual (PMF) | [Contar defectos con una Binomial](#sec-rv-binomial), ec. (3.1) |
| $\text{Bin}(n, p)$ | Distribución Binomial | [Contar defectos con una Binomial](#sec-rv-binomial), ec. (3.1) |
| $f_X(x)$ | Función de densidad (PDF) | [Alturas con la Normal](#sec-rv-normal), ec. (3.2) |
| $\mathcal{N}(\mu, \sigma^2)$ | Distribución Normal | [Alturas con la Normal](#sec-rv-normal), ec. (3.2) |
| $Z$ | Variable Normal estándar $\mathcal{N}(0, 1)$ | [Estandarización](#sec-rv-standardize), ec. (3.4) |
| $F_X(x)$ | Función de distribución acumulada (CDF) | [Cuantiles: invertir la pregunta](#sec-rv-quantiles) |
| $F_X^{-1}(\alpha)$, $x_\alpha$ | Cuantil $\alpha$ | [Cuantiles: invertir la pregunta](#sec-rv-quantiles), ec. (3.5) |
| $\lambda$ | Tasa (Poisson / Exponencial) | [El tiempo de espera como Exponencial](#sec-rv-exponential), ec. (3.6) |
| $\text{Exp}(\lambda)$ | Distribución Exponencial | [El tiempo de espera como Exponencial](#sec-rv-exponential), ec. (3.6) |
| $\text{Poisson}(\lambda)$ | Distribución Poisson | [Poisson como límite](#sec-rv-poisson), ec. (3.7) |
| $\bar{X}_n$ | Media muestral aleatoria | [La proporción observada se estabiliza](#sec-sums-lln), ec. (4.1) |
| $\xrightarrow{P}$ | Convergencia en probabilidad | [La proporción observada se estabiliza](#sec-sums-lln), ec. (4.2) |
| $\xrightarrow{d}$ | Convergencia en distribución | [El TCL formal](#sec-sums-clt), ec. (4.3) |
| $Z_n$ | Promedio estandarizado | [El TCL formal](#sec-sums-clt), ec. (4.3) |
| $\hat{p}$ | Proporción muestral | [IC para una proporción](#sec-inf-proportion), ec. (5.4) |
| $\alpha$ | Nivel de significancia / probabilidad de error tipo I | [IC para la espera media con $\sigma$ conocido](#sec-inf-mean-known) |
| $z_{1-\alpha/2}$ | Cuantil de la Normal estándar | [IC para la espera media con $\sigma$ conocido](#sec-inf-mean-known), ec. (5.2), (5.4) |
| $t_{n-1,\,1-\alpha/2}$ | Cuantil de la $t$ de Student | [IC con $\sigma$ desconocido — la $t$ de Student](#sec-inf-mean-unknown), ec. (5.3) |
| $\chi^2_{n-1}$ | Distribución chi-cuadrado con $n-1$ grados de libertad | [IC para la varianza — la $\chi^2$](#sec-inf-variance), ec. (5.5) |
| $H_0$, $H_1$ | Hipótesis nula y alternativa | [Test de hipótesis sobre la espera media](#sec-inf-test), ec. (5.7) |
| $\mu_0$ | Valor de control bajo $H_0$ | [Test de hipótesis sobre la espera media](#sec-inf-test), ec. (5.7) |
| $T$ (estadístico) | Estadístico del test $t$ | [Test de hipótesis sobre la espera media](#sec-inf-test), ec. (5.7) |
| $E$ | Margen de error | [Tamaño muestral para una precisión dada](#sec-inf-sample-size), ec. (5.8), (5.9) |

## Términos

| Término | Significado breve | Aparece en |
| --- | --- | --- |
| Observación | Valor numérico registrado de una unidad de la muestra. | [Una muestra de tiempos de espera](#sec-descriptive-sample) |
| Muestra | Conjunto finito de observaciones; en código vive como `Observations`. | [Una muestra de tiempos de espera](#sec-descriptive-sample) |
| Tabla de frecuencias | Conteo absoluto, relativo y acumulado por intervalos. | [Una muestra de tiempos de espera](#sec-descriptive-sample) |
| Suma de cuadrados | $\sum(x_i - \bar{x})^2$, paso intermedio para $s$. | [Resumir con tres miradas](#sec-descriptive-summary) |
| Outlier | Observación fuera de $[Q_1 - 1{,}5\,\text{IQR},\ Q_3 + 1{,}5\,\text{IQR}]$. | [Detección de outliers — la regla de Tukey](#sec-descriptive-tukey) |
| $z$-score | Distancia a la media expresada en unidades de desvío. | [Posición relativa: el $z$-score](#sec-descriptive-zscore) |
| Coeficiente de variación | Cociente $s/\bar{x}$, adimensional. | [Posición relativa: el $z$-score](#sec-descriptive-zscore) |
| Evento | Subconjunto del espacio muestral. | [Un experimento concreto](#sec-prob-experiment) |
| Partición | Familia de eventos disjuntos cuya unión es $\Omega$. | [Probabilidad total — la versión general](#sec-prob-total), ec. (2.5) |
| Probabilidad total | Descompone $P(B)$ usando una partición. | [Probabilidad total — la versión general](#sec-prob-total), ec. (2.5) |
| Teorema de Bayes | Invierte el sentido del condicionamiento. | [Teorema de Bayes (forma simbólica)](#sec-prob-bayes-symbolic), ec. (2.4) |
| Prevalencia | $P(D)$ — probabilidad a priori de la enfermedad / clase positiva. | [Bayes con datos: prueba diagnóstica](#sec-prob-bayes-data) |
| Sensibilidad | $P(+ \mid D)$ del test diagnóstico. | [Bayes con datos: prueba diagnóstica](#sec-prob-bayes-data) |
| Especificidad | $P(- \mid \bar{D})$ del test diagnóstico. | [Bayes con datos: prueba diagnóstica](#sec-prob-bayes-data) |
| Variable aleatoria | Función $X: \Omega \to \mathbb{R}$. | [Contar defectos con una Binomial](#sec-rv-binomial) |
| PMF | *Probability mass function* — distribución discreta. | [Contar defectos con una Binomial](#sec-rv-binomial), ec. (3.1) |
| Esperanza | Promedio teórico de la distribución. | [Contar defectos con una Binomial](#sec-rv-binomial) |
| Varianza | Promedio teórico del cuadrado del desvío. | [Contar defectos con una Binomial](#sec-rv-binomial) |
| Bernoulli | Variable indicadora con éxito $p$. | [Contar defectos con una Binomial](#sec-rv-binomial) |
| PDF | *Probability density function* — distribución continua. | [Alturas con la Normal](#sec-rv-normal), ec. (3.2) |
| Estandarización | Transformación $Z = (X - \mu)/\sigma$. | [Estandarización](#sec-rv-standardize), ec. (3.4) |
| CDF | *Cumulative distribution function*. | [Cuantiles: invertir la pregunta](#sec-rv-quantiles) |
| Cuantil | Valor con probabilidad acumulada $\alpha$ por debajo. | [Cuantiles: invertir la pregunta](#sec-rv-quantiles), ec. (3.5) |
| i.i.d. | Independientes e idénticamente distribuidas. | [La proporción observada se estabiliza](#sec-sums-lln) |
| LLN | Ley de los grandes números: $\bar{X}_n \to \mu$. | [La proporción observada se estabiliza](#sec-sums-lln), ec. (4.2) |
| Tablero de Galton | Suma de $\pm 1$ independientes; ilustra el TCL. | [El tablero de Galton](#sec-sums-galton) |
| TCL | Teorema central del límite: $Z_n \to \mathcal{N}(0,1)$. | [El TCL formal](#sec-sums-clt), ec. (4.3) |
| Aproximación Binomial-Normal | $\text{Bin}(n,p) \approx \mathcal{N}(np, np(1-p))$ para $n$ grande. | [Aproximación Binomial → Normal](#sec-sums-binomial-normal), ec. (4.4) |
| Pivote | Función de los datos cuya distribución es libre de parámetros. | [IC para la espera media con $\sigma$ conocido](#sec-inf-mean-known), ec. (5.1) |
| Intervalo de confianza | Procedimiento que cubre $\theta$ con probabilidad $1 - \alpha$. | [IC para la espera media con $\sigma$ conocido](#sec-inf-mean-known), ec. (5.2) |
| Margen de error | Mitad del ancho del intervalo de confianza. | [IC para la espera media con $\sigma$ conocido](#sec-inf-mean-known), ec. (5.2), (5.4) |
| Hipótesis nula | Afirmación de control que el test intenta refutar. | [Test de hipótesis sobre la espera media](#sec-inf-test), ec. (5.7) |
| Hipótesis alternativa | Lo que aceptamos si rechazamos $H_0$. | [Test de hipótesis sobre la espera media](#sec-inf-test) |
| $p$-valor | Probabilidad bajo $H_0$ de un estadístico tan extremo o más. | [Test de hipótesis sobre la espera media](#sec-inf-test) |
| Bootstrap | Remuestreo con reemplazo para estimar distribuciones. | [Bootstrap sin supuestos paramétricos](#sec-inf-bootstrap) |
| Tamaño muestral | $n$ necesario para asegurar un margen de error dado. | [Tamaño muestral para una precisión dada](#sec-inf-sample-size), ec. (5.8), (5.9) |
| Contrato del modelo | Lista breve de cuándo aplica una herramienta, qué supuestos necesita, qué puede romperla y cómo interpretar su salida. | Aparece como pausa de lectura junto a modelos y procedimientos principales. |
| Supuesto | Condición que debe ser razonable para que una fórmula o aproximación sostenga la interpretación prometida. | Aparece en los contratos de modelo. |
| Comunicación de incertidumbre | Traducción de un resultado estadístico a una frase que conserva rango, nivel de confianza, límites y decisión posible. | [Capstone — un memo con incertidumbre](#capstone-un-memo-con-incertidumbre) |
