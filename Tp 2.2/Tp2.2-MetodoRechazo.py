import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sp
from scipy.stats import chisquare, gamma, norm, nbinom, binom, hypergeom, poisson

# Parámetros del GCL
a = 1103515245
c = 12345
m = 2**31
semilla_glc = 3183856186

# Parámetros de las distribuciones
a_uniform = 0
b_uniform = 1
lambda_param_exp = 1
k_gamma = 2
theta_gamma = 2
mu_normal = 0
sigma_normal = 1
r_pascal = 5
p_pascal = 0.5
n_binomial = 10
p_binomial = 0.5
M_hyp = 50
n_hyp = 10
N_hyp = 20
mu_poisson = 5

# Función GCL


def GCL(seed, num_samples):
    random_numbers = []
    x = seed
    for _ in range(num_samples):
        x = (a * x + c) % m
        random_numbers.append(x / m)
    return np.array(random_numbers)


# Generar números pseudoaleatorios usando GCL
num_samples = 1000
pseudoaleatorios_uniform = GCL(semilla_glc, num_samples)
pseudoaleatorios_exponential = GCL(semilla_glc + 1, num_samples)
pseudoaleatorios_normal = GCL(semilla_glc + 3, num_samples)
pseudoaleatorios_binomial = GCL(semilla_glc + 5, num_samples)
pseudoaleatorios_poisson = GCL(semilla_glc + 7, num_samples)

# Generar muestras para las distribuciones
samples_uniform = pseudoaleatorios_uniform
samples_exponential = [-np.log(1-x) /
                       lambda_param_exp for x in pseudoaleatorios_exponential]
samples_normal = [sp.norm.ppf(x, mu_normal, sigma_normal)
                  for x in pseudoaleatorios_normal]
samples_binomial = [sp.binom.ppf(x, n_binomial, p_binomial)
                    for x in pseudoaleatorios_binomial]
samples_poisson = [sp.poisson.ppf(x, mu_poisson)
                   for x in pseudoaleatorios_poisson]

# Generar muestras usando el método de rechazo para distribución uniforme
samples_uniform = [
    x for x in pseudoaleatorios_uniform if a_uniform <= x <= b_uniform]

# Generar muestras usando GCL para otras distribuciones
pseudoaleatorios_exponential = GCL(semilla_glc + 1, num_samples)
samples_exponential = [-np.log(1-x) /
                       lambda_param_exp for x in pseudoaleatorios_exponential]

pseudoaleatorios_gamma = GCL(semilla_glc + 2, num_samples)
samples_gamma = [gamma.ppf(x, k_gamma, scale=theta_gamma)
                 for x in pseudoaleatorios_gamma]

pseudoaleatorios_normal = GCL(semilla_glc + 3, num_samples)
samples_normal = [norm.ppf(x, mu_normal, sigma_normal)
                  for x in pseudoaleatorios_normal]

pseudoaleatorios_pascal = GCL(semilla_glc + 4, num_samples)
samples_pascal = [nbinom.ppf(x, r_pascal, p_pascal)
                  for x in pseudoaleatorios_pascal]

pseudoaleatorios_binomial = GCL(semilla_glc + 5, num_samples)
samples_binomial = [binom.ppf(x, n_binomial, p_binomial)
                    for x in pseudoaleatorios_binomial]

pseudoaleatorios_hypergeometric = GCL(semilla_glc + 6, num_samples)
samples_hypergeometric = [hypergeom.ppf(
    x, M_hyp, N_hyp, n_hyp) for x in pseudoaleatorios_hypergeometric]

pseudoaleatorios_poisson = GCL(semilla_glc + 7, num_samples)
samples_poisson = [poisson.ppf(x, mu_poisson)
                   for x in pseudoaleatorios_poisson]

# Generar muestras para la distribución empírica discreta
datos_empiricos = [1, 2, 3, 4, 5]
probabilidades_empiricas = [0.2, 0.3, 0.25, 0.15, 0.1]
pseudoaleatorios_discrete_empirical = GCL(semilla_glc + 8, num_samples)
samples_discrete_empirical = np.random.choice(
    datos_empiricos, size=num_samples, p=probabilidades_empiricas)

# Funciones de densidad


def uniform_density(x):
    return 1 / (b_uniform - a_uniform) if a_uniform <= x <= b_uniform else 0


def exponential_density(x):
    return lambda_param_exp * np.exp(-lambda_param_exp * x) if x >= 0 else 0


def gamma_density(x):
    return gamma.pdf(x, k_gamma, scale=theta_gamma)


def normal_density(x):
    return norm.pdf(x, mu_normal, sigma_normal)


def pascal_density(x):
    return nbinom.pmf(x, r_pascal, p_pascal)


def binomial_density(x):
    return binom.pmf(x, n_binomial, p_binomial)


def hypergeometric_density(x):
    return hypergeom.pmf(x, M_hyp, N_hyp, n_hyp)


def poisson_density(x):
    return poisson.pmf(x, mu_poisson)


def discrete_empirical_density(x, datos, probabilidades):
    indice = datos.index(x) if x in datos else None
    return probabilidades[indice] if indice is not None else 0


# Rango para las funciones de densidad
x_values_uniform = np.linspace(a_uniform, b_uniform, 1000)
x_values_exponential = np.linspace(0, 10, 1000)
x_values_gamma = np.linspace(0, 20, 1000)
x_values_normal = np.linspace(-4, 4, 1000)
x_values_pascal = np.arange(0, 40, 1)
x_values_binomial = np.arange(0, n_binomial + 1, 1)
x_values_hypergeometric = np.arange(
    max(0, N_hyp - (M_hyp - n_hyp)), min(n_hyp, N_hyp) + 1, 1)
x_values_poisson = np.arange(0, 3 * mu_poisson, 1)
x_values_discrete_empirical = np.arange(
    min(datos_empiricos), max(datos_empiricos) + 1, 1)

# Calcular los valores de las funciones de densidad teórica
y_values_uniform = [uniform_density(x) for x in x_values_uniform]
y_values_exponential = [exponential_density(x) for x in x_values_exponential]
y_values_gamma = [gamma_density(x) for x in x_values_gamma]
y_values_normal = [normal_density(x) for x in x_values_normal]
y_values_pascal = [pascal_density(x) for x in x_values_pascal]
y_values_binomial = [binomial_density(x) for x in x_values_binomial]
y_values_hypergeometric = [hypergeometric_density(
    x) for x in x_values_hypergeometric]
y_values_poisson = [poisson_density(x) for x in x_values_poisson]
y_values_discrete_empirical = [discrete_empirical_density(
    x, datos_empiricos, probabilidades_empiricas) for x in x_values_discrete_empirical]

# Graficar histogramas y funciones de densidad teórica
fig, axs = plt.subplots(5, 2, figsize=(14, 20))

# Distribución Uniforme
axs[0, 0].hist(samples_uniform, bins=50, density=True,
               alpha=0.6, color='g', label='Muestras')
axs[0, 0].plot(x_values_uniform, y_values_uniform,
               'r-', lw=2, label='Densidad Teórica')
axs[0, 0].set_title('Distribución Uniforme')
axs[0, 0].legend()

# Distribución Exponencial
axs[0, 1].hist(samples_exponential, bins=50, density=True,
               alpha=0.6, color='g', label='Muestras')
axs[0, 1].plot(x_values_exponential, y_values_exponential,
               'r-', lw=2, label='Densidad Teórica')
axs[0, 1].set_title('Distribución Exponencial')
axs[0, 1].legend()

# Distribución Gamma
axs[1, 0].hist(samples_gamma, bins=50, density=True,
               alpha=0.6, color='g', label='Muestras')
axs[1, 0].plot(x_values_gamma, y_values_gamma,
               'r-', lw=2, label='Densidad Teórica')
axs[1, 0].set_title('Distribución Gamma')
axs[1, 0].legend()

# Distribución Normal
axs[1, 1].hist(samples_normal, bins=50, density=True,
               alpha=0.6, color='g', label='Muestras')
axs[1, 1].plot(x_values_normal, y_values_normal,
               'r-', lw=2, label='Densidad Teórica')
axs[1, 1].set_title('Distribución Normal')
axs[1, 1].legend()

# Distribución Pascal
axs[2, 0].hist(samples_pascal, bins=50, density=True,
               alpha=0.6, color='g', label='Muestras')
axs[2, 0].plot(x_values_pascal, y_values_pascal,
               'r-', lw=2, label='Densidad Teórica')
axs[2, 0].set_title('Distribución Pascal')
axs[2, 0].legend()

# Distribución Binomial
axs[2, 1].hist(samples_binomial, bins=50, density=True,
               alpha=0.6, color='g', label='Muestras')
axs[2, 1].plot(x_values_binomial, y_values_binomial,
               'r-', lw=2, label='Densidad Teórica')
axs[2, 1].set_title('Distribución Binomial')
axs[2, 1].legend()

# Distribución Hipergeométrica
axs[3, 0].hist(samples_hypergeometric, bins=50, density=True,
               alpha=0.6, color='g', label='Muestras')
axs[3, 0].plot(x_values_hypergeometric, y_values_hypergeometric,
               'r-', lw=2, label='Densidad Teórica')
axs[3, 0].set_title('Distribución Hipergeométrica')
axs[3, 0].legend()

# Distribución Poisson
axs[3, 1].hist(samples_poisson, bins=50, density=True,
               alpha=0.6, color='g', label='Muestras')
axs[3, 1].plot(x_values_poisson, y_values_poisson,
               'r-', lw=2, label='Densidad Teórica')
axs[3, 1].set_title('Distribución Poisson')
axs[3, 1].legend()

# Distribución Empírica Discreta
axs[4, 0].hist(samples_discrete_empirical, bins=50, density=True,
               alpha=0.6, color='g', label='Muestras')
axs[4, 0].plot(x_values_discrete_empirical,
               y_values_discrete_empirical, 'r-', lw=2, label='Densidad Teórica')
axs[4, 0].set_title('Distribución Empírica Discreta')
axs[4, 0].legend()

# Ocultar el subplot vacío
axs[4, 1].axis('off')

plt.tight_layout()
plt.savefig("MetodoRechazo - Todas las dist")
plt.show()


# Generar muestras para la distribución empírica discreta
datos_empiricos = [1, 2, 3, 4, 5]
probabilidades_empiricas = [0.2, 0.3, 0.25, 0.15, 0.1]
samples_discrete_empirical = np.random.choice(
    datos_empiricos, size=num_samples, p=probabilidades_empiricas)

# Función para realizar la prueba de chi-cuadrado


def chi_square_test(samples, distribution, params, bins=10):
    observed_freq, bin_edges = np.histogram(samples, bins=bins, density=False)
    expected_freq = np.zeros_like(observed_freq)

    for i in range(len(bin_edges) - 1):
        expected_freq[i] = len(samples) * (distribution.cdf(bin_edges[i+1],
                                                            *params) - distribution.cdf(bin_edges[i], *params))

    # Normalizar las frecuencias para que las sumas sean iguales
    observed_freq = observed_freq * \
        (np.sum(expected_freq) / np.sum(observed_freq))

    chi2, p_value = chisquare(observed_freq, f_exp=expected_freq)
    return chi2, p_value


# Parámetros de las distribuciones
params_uniform = (a_uniform, b_uniform - a_uniform)
params_exponential = (1 / lambda_param_exp,)
params_normal = (mu_normal, sigma_normal)
params_binomial = (n_binomial, p_binomial)
params_poisson = (mu_poisson,)

# Nivel de significancia
alpha = 0.05

# Realizar las pruebas de chi-cuadrado
chi2_uniform, p_uniform = chi_square_test(
    samples_uniform, sp.uniform, params_uniform)
chi2_exponential, p_exponential = chi_square_test(
    samples_exponential, sp.expon, params_exponential)
chi2_normal, p_normal = chi_square_test(samples_normal, sp.norm, params_normal)
chi2_binomial, p_binomial = chi_square_test(
    samples_binomial, sp.binom, params_binomial)
chi2_poisson, p_poisson = chi_square_test(
    samples_poisson, sp.poisson, params_poisson)

# Función para interpretar los resultados


def interpret_results(chi2, p_value, alpha):
    if p_value < alpha:
        return f"chi2: {chi2}, p-value: {p_value} -> Rechazar la hipótesis nula. (Distribución incorrecta)"
    else:
        return f"chi2: {chi2}, p-value: {p_value} -> No rechazar la hipótesis nula. (Distribución correcta)"


# Imprimir los resultados con interpretación
print("Test de Chi-cuadrado:")
print(f"Uniforme: {interpret_results(chi2_uniform, p_uniform, alpha)}")
print(f"Exponencial: {interpret_results(
    chi2_exponential, p_exponential, alpha)}")
print(f"Normal: {interpret_results(chi2_normal, p_normal, alpha)}")
print(f"Binomial: {interpret_results(chi2_binomial, p_binomial, alpha)}")
print(f"Poisson: {interpret_results(chi2_poisson, p_poisson, alpha)}")

# Prueba de chi-cuadrado para distribución empírica discreta
observed_freq_empirical, _ = np.histogram(
    samples_discrete_empirical, bins=len(datos_empiricos), density=False)
expected_freq_empirical = np.array(probabilidades_empiricas) * num_samples

# Normalizar las frecuencias para que las sumas sean iguales
observed_freq_empirical = observed_freq_empirical * \
    (np.sum(expected_freq_empirical) / np.sum(observed_freq_empirical))

chi2_empirical, p_empirical = chisquare(
    observed_freq_empirical, f_exp=expected_freq_empirical)

print(f"Empírica Discreta: {interpret_results(
    chi2_empirical, p_empirical, alpha)}")


def runtestUDM(numeros, a):
    tMuestra = np.size(numeros)
    secuencia_con_signos = []
    media = np.mean(numeros)
    n1, n2 = 0, 0
    for i in range(0, tMuestra):
        if numeros[i] > media:
            secuencia_con_signos.append('1')
            n1 += 1
        if numeros[i] < media:
            secuencia_con_signos.append('0')
            n2 += 1
    corridas = 1
    for i in range(0, len(secuencia_con_signos) - 1):
        if secuencia_con_signos[i] != secuencia_con_signos[i + 1]:
            corridas += 1
    mediaC = ((2 * n1 * n2) / (n1 + n2)) + 1
    varianzaC = ((2 * n1 * n2) * (2 * n1 * n2 - tMuestra)) / \
        (pow(tMuestra, 2) * (tMuestra - 1))
    desvio = math.sqrt(varianzaC)
    z = abs((corridas - mediaC) / desvio)
    print(f"Datos de la prueba: Media = {
          mediaC} - Varianza = {varianzaC} - Corridas = {corridas}")

    print(f"El Valor estadistico de prueba es Z = {z}")
    Ztabla = round(sp.norm.ppf(1 - a / 2), 3)
    print("Resultado del test con una confianza del", (1 - (a * 2)) * 100, "%:",
          "No pasa el test" if z > Ztabla else "Pasa el test")


# Parámetro de significancia
alpha = 0.05

# Ejecutar test en las muestras generadas
print("Test de Corridas para la distribución Uniforme:")
runtestUDM(samples_uniform, alpha)

print("\nTest de Corridas para la distribución Exponencial:")
runtestUDM(samples_exponential, alpha)

print("\nTest de Corridas para la distribución Gamma:")
runtestUDM(samples_gamma, alpha)

print("\nTest de Corridas para la distribución Normal:")
runtestUDM(samples_normal, alpha)

print("\nTest de Corridas para la distribución Pascal:")
runtestUDM(samples_pascal, alpha)

print("\nTest de Corridas para la distribución Binomial:")
runtestUDM(samples_binomial, alpha)

print("\nTest de Corridas para la distribución Hipergeométrica:")
runtestUDM(samples_hypergeometric, alpha)

print("\nTest de Corridas para la distribución Poisson:")
runtestUDM(samples_poisson, alpha)
