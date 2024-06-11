import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma, norm, nbinom, binom

# Parámetros del método de rechazo para distribución uniforme
a_uniform = 0  # Límite inferior del rango
b_uniform = 1  # Límite superior del rango
c_uniform = 1  # Factor de escala para la distribución uniforme

# Parámetros del método de rechazo para distribución exponencial
lambda_param_exp = 1  # Parámetro lambda para la distribución exponencial
c_exp = lambda_param_exp  # Factor de escala para la distribución exponencial

# Parámetros de la distribución gamma
k_gamma = 2  # Parámetro k para la distribución gamma
theta_gamma = 2  # Parámetro theta para la distribución gamma
# Factor de escala para la distribución gamma
c_gamma = gamma.pdf((k_gamma - 1) * theta_gamma, k_gamma, scale=theta_gamma)

# Parámetros de la distribución normal
mu_normal = 0  # Media de la distribución normal
sigma_normal = 1  # Desviación estándar de la distribución normal

# Parámetros de la distribución Pascal (binomial negativa)
r_pascal = 5  # Número de éxitos
p_pascal = 0.5  # Probabilidad de éxito en cada ensayo

# Parámetros de la distribución binomial
n_binomial = 10  # Número de ensayos
p_binomial = 0.5  # Probabilidad de éxito en cada ensayo

# Función de densidad para la distribución uniforme


def uniform_density(x):
    return 1 / (b_uniform - a_uniform) if a_uniform <= x <= b_uniform else 0

# Función de densidad para la distribución exponencial


def exponential_density(x):
    return lambda_param_exp * np.exp(-lambda_param_exp * x) if x >= 0 else 0

# Función de densidad para la distribución gamma


def gamma_density(x):
    return gamma.pdf(x, k_gamma, scale=theta_gamma)

# Función de densidad para la distribución normal


def normal_density(x):
    return norm.pdf(x, mu_normal, sigma_normal)

# Función de densidad para la distribución Pascal


def pascal_density(x):
    return nbinom.pmf(x, r_pascal, p_pascal)

# Función de densidad para la distribución binomial


def binomial_density(x):
    return nbinom.pmf(x, n_binomial, p_binomial)


# Función para generar números pseudoaleatorios distribuidos uniformemente usando un GLC
def glc_uniform(semilla, tiradas):
    a = 1664525
    c = 1013904223
    m = 2**32
    resultados = []
    x = semilla
    for _ in range(tiradas):
        x = (a * x + c) % m
        pseudo_aleatorio = x / m
        resultados.append(pseudo_aleatorio)
    return resultados

# Función para generar números pseudoaleatorios distribuidos exponencialmente


def glc_exponential(semilla, tiradas):
    a = 1664525
    c = 1013904223
    m = 2**32
    resultados = []
    x = semilla
    for _ in range(tiradas):
        x = (a * x + c) % m
        pseudo_aleatorio = x / m
        # Transformación inversa para obtener una distribución exponencial
        sample = -np.log(1 - pseudo_aleatorio) / lambda_param_exp
        resultados.append(sample)
    return resultados

# Función para generar números pseudoaleatorios distribuidos con distribución gamma


def glc_gamma(semilla, tiradas):
    a = 1664525
    c = 1013904223
    m = 2**32
    resultados = []
    x = semilla
    for _ in range(tiradas):
        x = (a * x + c) % m
        pseudo_aleatorio = x / m
        # Transformación inversa para obtener una distribución gamma
        sample = gamma.ppf(pseudo_aleatorio, k_gamma, scale=theta_gamma)
        resultados.append(sample)
    return resultados

# Función para generar números pseudoaleatorios distribuidos con distribución normal


def glc_normal(semilla, tiradas):
    a = 1664525
    c = 1013904223
    m = 2**32
    resultados = []
    x = semilla
    for _ in range(tiradas):
        x = (a * x + c) % m
        pseudo_aleatorio = x / m
        # Transformación inversa para obtener una distribución normal
        sample = norm.ppf(pseudo_aleatorio, mu_normal, sigma_normal)
        resultados.append(sample)
    return resultados

# Función para generar números pseudoaleatorios distribuidos con distribución Pascal


def glc_pascal(semilla, tiradas):
    a = 1664525
    c = 1013904223
    m = 2**32
    resultados = []
    x = semilla
    for _ in range(tiradas):
        x = (a * x + c) % m
        pseudo_aleatorio = x / m
        # Transformación inversa para obtener una distribución Pascal
        sample = nbinom.ppf(pseudo_aleatorio, r_pascal, p_pascal)
        resultados.append(sample)
    return resultados

# Función para generar números pseudoaleatorios distribuidos con distribución binomial


def glc_binomial(semilla, tiradas):
    a = 1664525
    c = 1013904223516
    m = 2**32
    resultados = []
    x = semilla
    for _ in range(tiradas):
        x = (a * x + c) % m
        pseudo_aleatorio = x / m
        # Transformación inversa para obtener una distribución binomial
        sample = nbinom.ppf(pseudo_aleatorio, n_binomial, p_binomial)
        resultados.append(sample)
    return resultados

# Función para realizar el método de rechazo para la distribución uniforme


def rejection_sampling_uniform(pseudoaleatorios, a, b, c, tiradas):
    samples = []
    num_generated = 0
    while num_generated < tiradas:
        try:
            R1 = next(pseudoaleatorios)
            R2 = next(pseudoaleatorios)
            x = a + (b - a) * R1
            if R2 <= c:
                samples.append(x)
                num_generated += 1
        except StopIteration:
            break
    return np.array(samples)

# Función para realizar el método de rechazo para la distribución exponencial


def rejection_sampling_exponential(pseudoaleatorios, c, tiradas):
    samples = []
    num_generated = 0
    while num_generated < tiradas:
        try:
            R1 = next(pseudoaleatorios)
            R2 = next(pseudoaleatorios)
            x = -np.log(1 - R1) / c
            if R2 <= np.exp(-x):
                samples.append(x)
                num_generated += 1
        except StopIteration:
            break
    return np.array(samples)

# Función para realizar el método de rechazo para la distribución gamma


def rejection_sampling_gamma(pseudoaleatorios, c, tiradas):
    samples = []
    num_generated = 0
    while num_generated < tiradas:
        try:
            R1 = next(pseudoaleatorios)
            R2 = next(pseudoaleatorios)
            x = gamma.ppf(R1, k_gamma, scale=theta_gamma)
            if R2 <= gamma.pdf(x, k_gamma, scale=theta_gamma) / c:
                samples.append(x)
                num_generated += 1
        except StopIteration:
            break
    return np.array(samples)

# Función para realizar el método de rechazo para la distribución normal


def rejection_sampling_normal(pseudoaleatorios, tiradas):
    samples = []
    num_generated = 0
    while num_generated < tiradas:
        try:
            R1 = next(pseudoaleatorios)
            R2 = next(pseudoaleatorios)
            x = norm.ppf(R1, mu_normal, sigma_normal)
            if R2 <= norm.pdf(x, mu_normal, sigma_normal):
                samples.append(x)
                num_generated += 1
        except StopIteration:
            break
    return np.array(samples)

# Función para realizar el método de rechazo para la distribución Pascal


def rejection_sampling_pascal(pseudoaleatorios, c, tiradas):
    samples = []
    num_generated = 0
    while num_generated < tiradas:
        try:
            R1 = next(pseudoaleatorios)
            R2 = next(pseudoaleatorios)
            x = nbinom.ppf(R1, r_pascal, p_pascal)
            if R2 <= nbinom.pmf(x, r_pascal, p_pascal) / c:
                samples.append(x)
                num_generated += 1
        except StopIteration:
            break
    return np.array(samples)

# Función para realizar el método de rechazo para la distribución binomial


def rejection_sampling_binomial(pseudoaleatorios, c, tiradas):
    samples = []
    num_generated = 0
    while num_generated < tiradas:
        try:
            R1 = next(pseudoaleatorios)
            R2 = next(pseudoaleatorios)
            x = nbinom.ppf(R1, n_binomial, p_binomial)
            if R2 <= nbinom.pmf(x, n_binomial, p_binomial) / c:
                samples.append(x)
                num_generated += 1
        except StopIteration:
            break
    return np.array(samples)


# Parámetros de la simulación
tiradas = 10000
semilla_glc = 12345  # Semilla para el GLC

# Generar números pseudoaleatorios para distribución uniforme
pseudoaleatorios_uniform = iter(glc_uniform(semilla_glc, tiradas))

# Generar muestras usando el método de rechazo para distribución uniforme
samples_uniform = rejection_sampling_uniform(
    pseudoaleatorios_uniform, a_uniform, b_uniform, c_uniform, tiradas)

# Generar números pseudoaleatorios para distribución exponencial
pseudoaleatorios_exponential = iter(glc_exponential(semilla_glc, tiradas))

# Generar muestras usando el método de rechazo para distribución exponencial
samples_exponential = rejection_sampling_exponential(
    pseudoaleatorios_exponential, c_exp, tiradas)

# Generar números pseudoaleatorios para distribución gamma
pseudoaleatorios_gamma = iter(glc_gamma(semilla_glc, tiradas))

# Generar muestras usando el método de rechazo para distribución gamma
samples_gamma = rejection_sampling_gamma(
    pseudoaleatorios_gamma, c_gamma, tiradas)

# Generar números pseudoaleatorios para distribución normal
pseudoaleatorios_normal = iter(glc_normal(semilla_glc, tiradas))

# Generar muestras para distribución normal
samples_normal = rejection_sampling_normal(pseudoaleatorios_normal, tiradas)

# Generar números pseudoaleatorios para distribución Pascal
pseudoaleatorios_pascal = iter(glc_pascal(semilla_glc, tiradas))

# Generar muestras para distribución Pascal
samples_pascal = rejection_sampling_pascal(
    pseudoaleatorios_pascal, r_pascal, tiradas)

# Generar números pseudoaleatorios para distribución binomial
pseudoaleatorios_binomial = iter(glc_binomial(semilla_glc, tiradas))

# Generar muestras para distribución binomial
samples_binomial = rejection_sampling_binomial(
    pseudoaleatorios_binomial, n_binomial, tiradas)

# Rango para las funciones de densidad
x_values_uniform = np.linspace(a_uniform, b_uniform, 1000)
# Ajusta el rango según la distribución exponencial
x_values_exponential = np.linspace(0, 10, 1000)
# Ajusta el rango según la distribución gamma
x_values_gamma = np.linspace(0, 20, 1000)
# Ajusta el rango según la distribución normal
x_values_normal = np.linspace(-4, 4, 1000)
x_values_pascal = np.arange(0, 40, 1)  # Rango para la distribución Pascal
x_values_binomial = np.arange(0, 20, 1)  # Rango para la distribución binomial

# Calcular los valores de las funciones de densidad teórica
y_values_uniform = [uniform_density(x) for x in x_values_uniform]
y_values_exponential = [exponential_density(x) for x in x_values_exponential]
y_values_gamma = [gamma_density(x) for x in x_values_gamma]
y_values_normal = [normal_density(x) for x in x_values_normal]
y_values_pascal = [pascal_density(x) for x in x_values_pascal]
y_values_binomial = [binomial_density(x) for x in x_values_binomial]

# Graficar histograma para distribución uniforme
plt.figure()
plt.hist(samples_uniform, bins=50, density=True, alpha=0.6, color='g')
# Agrega la función de densidad teórica
plt.plot(x_values_uniform, y_values_uniform, 'r-', lw=2)
plt.xlabel('Valor de la Variable')
plt.ylabel('Densidad')
plt.title('Distribucion Uniforme - MR')
plt.savefig('Histograma Distribucion Uniforme - MR')
plt.show()

# Graficar histograma para distribución exponencial
plt.figure()
plt.hist(samples_exponential, bins=50, density=True, alpha=0.6, color='b')
plt.plot(x_values_exponential, y_values_exponential, 'r-',
         lw=2)  # Agrega la función de densidad teórica
plt.xlabel('Valor de la Variable')
plt.ylabel('Densidad')
plt.title('Distribucion Exponencial - MR')
plt.savefig('Histograma Distribucion Exponencial - MR')
plt.show()

# Graficar histograma para distribución gamma
plt.figure()
plt.hist(samples_gamma, bins=50, density=True, alpha=0.6, color='m',
         edgecolor='black')  # Añadiendo edgecolor='black'
# Agrega la función de densidad teórica
plt.plot(x_values_gamma, y_values_gamma, 'r-', lw=2)
plt.xlabel('Valor de la Variable')
plt.ylabel('Densidad')
plt.title('Distribucion Gamma - MR')
plt.savefig('Histograma Distribucion Gamma - MR')
plt.show()

# Graficar histograma para distribución normal
plt.figure()
plt.hist(samples_normal, bins=50, density=True, alpha=0.6, color='c')
# Agrega la función de densidad teórica
plt.plot(x_values_normal, y_values_normal, 'r-', lw=2)
plt.xlabel('Valor de la Variable')
plt.ylabel('Densidad')
plt.title('Distribucion Normal - MR')
plt.savefig('Histograma Distribucion Normal - MR')
plt.show()

# Graficar histograma para distribución Pascal
plt.figure()
plt.hist(samples_pascal, bins=30, density=True, alpha=0.6, color='orange')
# Agrega la función de densidad teórica
plt.plot(x_values_pascal, y_values_pascal, 'r-', lw=2)
plt.xlabel('Valor de la Variable')
plt.ylabel('Densidad')
plt.title('Distribucion Pascal - MR')
plt.savefig('Histograma Distribucion Pascal - MR')
plt.show()

# Graficar histograma para distribución binomial
plt.figure()
plt.hist(samples_binomial, bins=20, density=True,
         alpha=0.6, color='purple', edgecolor='black')
# Rango para la distribución binomial
x_values_binomial = np.arange(0, n_binomial + 1, 1)
y_values_binomial = [binomial_density(x) for x in x_values_binomial]
# Agrega la función de densidad teórica
plt.plot(x_values_binomial, y_values_binomial, 'r-', lw=2)
plt.xlabel('Valor de la Variable')
plt.ylabel('Densidad')
plt.title('Distribucion Binomial - MR')
plt.savefig('Histograma Distribucion Binomial - MR')
plt.show()
