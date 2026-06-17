# Glosario

Esta página reúne los símbolos y los términos que aparecen en el libro. La
columna **Aparece en** indica el capítulo y, cuando es útil, la ecuación
numerada donde se introdujo el concepto.

## Símbolos

| Símbolo | Nombre | Aparece en |
| --- | --- | --- |
| $\Omega$ | Espacio muestral (universo de resultados) | Probabilidad |
| $A$, $B$, $C$ | Eventos (subconjuntos de $\Omega$) | Probabilidad |
| $\bar{A}$ | Complemento de $A$ | Probabilidad |
| $A \cup B$ | Unión de eventos | Probabilidad, ec. (2.1)–(2.2) |
| $A \cap B$ | Intersección de eventos | Probabilidad, ec. (2.1) |
| $P(A)$ | Probabilidad del evento $A$ | Probabilidad |
| $P(A \mid B)$ | Probabilidad condicional de $A$ dado $B$ | Probabilidad, ec. (2.3) |
| $\bar{x}$ | Media muestral | Tratamiento de datos, ec. (1.1) |
| $\tilde{x}$ | Mediana muestral | Tratamiento de datos, ec. (1.2) |
| $s$ | Desvío estándar muestral (divisor $n-1$) | Tratamiento de datos, ec. (1.3) |
| $s^2$ | Varianza muestral | Tratamiento de datos, Inferencia |
| $Q_1$, $Q_3$ | Primer y tercer cuartil | Tratamiento de datos, ec. (1.4) |
| $\text{IQR}$ | Rango intercuartil $Q_3 - Q_1$ | Tratamiento de datos, ec. (1.4) |
| $z_i$ | $z$-score muestral de la observación $x_i$ | Tratamiento de datos, ec. (1.5) |
| $X$, $Y$, $T$ | Variables aleatorias | Variables aleatorias |
| $E[X]$, $\mu$ | Esperanza | Variables aleatorias |
| $\mathrm{Var}(X)$, $\sigma^2$ | Varianza poblacional | Variables aleatorias |
| $\sigma$ | Desvío estándar poblacional | Variables aleatorias |
| $f_X(x)$ | Función de densidad (PDF) | Variables aleatorias, ec. (3.2) |
| $F_X(x)$ | Función de distribución acumulada (CDF) | Variables aleatorias |
| $F_X^{-1}(\alpha)$ | Cuantil $\alpha$ | Variables aleatorias, ec. (3.5) |
| $P(X = k)$ | Función de probabilidad puntual (PMF) | Variables aleatorias, ec. (3.1) |
| $\mathcal{N}(\mu, \sigma^2)$ | Distribución Normal | Variables aleatorias, ec. (3.2) |
| $\text{Bin}(n, p)$ | Distribución Binomial | Variables aleatorias, ec. (3.1) |
| $\text{Poisson}(\lambda)$ | Distribución Poisson | Variables aleatorias, ec. (3.7) |
| $\text{Exp}(\lambda)$ | Distribución Exponencial | Variables aleatorias, ec. (3.6) |
| $Z$ | Variable Normal estándar $\mathcal{N}(0,1)$ | Variables aleatorias, ec. (3.4) |
| $\bar{X}_n$ | Media muestral aleatoria | Sumas y promedios, ec. (4.1) |
| $\xrightarrow{P}$ | Convergencia en probabilidad | Sumas y promedios, ec. (4.2) |
| $\xrightarrow{d}$ | Convergencia en distribución | Sumas y promedios, ec. (4.3) |
| $Z_n$ | Promedio estandarizado | Sumas y promedios, ec. (4.3) |
| $\hat{p}$ | Proporción muestral | Inferencia, ec. (5.4) |
| $z_{1-\alpha/2}$ | Cuantil de la Normal estándar | Inferencia, ec. (5.2), (5.4) |
| $t_{n-1,\,1-\alpha/2}$ | Cuantil de la $t$ de Student | Inferencia, ec. (5.3) |
| $\chi^2_{n-1}$ | Distribución chi-cuadrado con $n-1$ grados de libertad | Inferencia, ec. (5.5) |
| $H_0$, $H_1$ | Hipótesis nula y alternativa | Inferencia, ec. (5.7) |
| $\alpha$ | Nivel de significancia / probabilidad de error tipo I | Inferencia, ec. (5.7) |
| $E$ | Margen de error | Inferencia, ec. (5.8), (5.9) |

## Términos

| Término | Significado breve | Aparece en |
| --- | --- | --- |
| Observación | Valor numérico registrado de una unidad de la muestra. | Tratamiento de datos |
| Muestra | Conjunto finito de observaciones; en código vive como `Observations`. | Tratamiento de datos |
| Tabla de frecuencias | Conteo absoluto, relativo y acumulado por intervalos. | Tratamiento de datos |
| Outlier | Observación fuera de $[Q_1 - 1{,}5\,\text{IQR},\ Q_3 + 1{,}5\,\text{IQR}]$. | Tratamiento de datos |
| $z$-score | Distancia a la media expresada en unidades de desvío. | Tratamiento de datos |
| Coeficiente de variación | Cociente $s/\bar{x}$, adimensional. | Tratamiento de datos |
| Evento | Subconjunto del espacio muestral. | Probabilidad |
| Partición | Familia de eventos disjuntos cuya unión es $\Omega$. | Probabilidad, ec. (2.5) |
| Probabilidad total | Descompone $P(B)$ usando una partición. | Probabilidad, ec. (2.5) |
| Teorema de Bayes | Invierte el sentido del condicionamiento. | Probabilidad, ec. (2.4) |
| Prevalencia | $P(D)$ — probabilidad a priori de la enfermedad / clase positiva. | Probabilidad |
| Sensibilidad | $P(+ \mid D)$ del test diagnóstico. | Probabilidad |
| Especificidad | $P(- \mid \bar{D})$ del test diagnóstico. | Probabilidad |
| Variable aleatoria | Función $X: \Omega \to \mathbb{R}$. | Variables aleatorias |
| PMF | *Probability mass function* — distribución discreta. | Variables aleatorias, ec. (3.1) |
| PDF | *Probability density function* — distribución continua. | Variables aleatorias, ec. (3.2) |
| CDF | *Cumulative distribution function*. | Variables aleatorias |
| Cuantil | Valor con probabilidad acumulada $\alpha$ por debajo. | Variables aleatorias, ec. (3.5) |
| Estandarización | Transformación $Z = (X - \mu)/\sigma$. | Variables aleatorias, ec. (3.4) |
| Esperanza | Promedio teórico de la distribución. | Variables aleatorias |
| Varianza | Promedio teórico del cuadrado del desvío. | Variables aleatorias |
| Bernoulli | Variable indicadora con éxito $p$. | Variables aleatorias |
| LLN | Ley de los grandes números: $\bar{X}_n \to \mu$. | Sumas y promedios, ec. (4.2) |
| TCL | Teorema central del límite: $Z_n \to \mathcal{N}(0,1)$. | Sumas y promedios, ec. (4.3) |
| Tablero de Galton | Suma de $\pm 1$ independientes; ilustra el TCL. | Sumas y promedios |
| Aproximación Binomial-Normal | $\text{Bin}(n,p) \approx \mathcal{N}(np, np(1-p))$ para $n$ grande. | Sumas y promedios, ec. (4.4) |
| Pivote | Función de los datos cuya distribución es libre de parámetros. | Inferencia, ec. (5.1) |
| Intervalo de confianza | Procedimiento que cubre $\theta$ con probabilidad $1 - \alpha$. | Inferencia, ec. (5.2) |
| Margen de error | Mitad del ancho del intervalo de confianza. | Inferencia, ec. (5.2), (5.4) |
| Hipótesis nula | Afirmación de control que el test intenta refutar. | Inferencia, ec. (5.7) |
| Hipótesis alternativa | Lo que aceptamos si rechazamos $H_0$. | Inferencia |
| $p$-valor | Probabilidad bajo $H_0$ de un estadístico tan extremo o más. | Inferencia |
| Bootstrap | Remuestreo con reemplazo para estimar distribuciones. | Inferencia |
