import math
from matplotlib import pyplot as plt
import numpy as np
import scipy as gamma


class LGC:
    def __init__(self, seed=1):

        # Parametros GCL
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32
        self.state = seed

    def random(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m


def generador_uniforme_MTI(n, a=0, b=1):
    uniform_numbers = []
    for _ in range(n):
        uniform_numbers.append(a + (b - a) * lcg.random())
    return uniform_numbers


def generador_exponencial_MTI(n, lamda=1):
    exponential_numbers = []
    scale = 1/lamda
    # uniform_numbers es un arreglo de numeros aleatorios con distribucion uniforme
    uniform_numbers = generador_uniforme_MTI(n)
    for u in uniform_numbers:
        exponential_numbers.append(-scale * math.log(1 - u))
    # scale = 1/lamda; math.log -> logaritmo natural
    return exponential_numbers


def generador_normal_MTI(n, media=0, std=1):
    normal_numbers = []
    # se corre la mitad de las veces porque se agregan dos numeros por iteracion
    for _ in range(n // 2):
        u1 = lcg.random()
        u2 = lcg.random()
        z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        z1 = math.sqrt(-2.0 * math.log(u1)) * math.sin(2.0 * math.pi * u2)
        # se agregan dos numeros
        normal_numbers.extend([media + std * z0, media + std * z1])
    return normal_numbers[:n]


def plot_histogram(data, bins=50, title=''):
    plt.hist(data, bins=bins, density=True, alpha=0.7,
             color='skyblue', edgecolor='black')
    plt.title(title)
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.grid(axis='y', alpha=0.75)
    plt.show()

# Definicion de las funciones de densidad


def funcion_densidad_uniforme(x, a, b):
    return 1 / (b - a)


def funcion_densidad_exponencial(x, lamda):
    return lamda * math.exp(-lamda * x)


def funcion_densidad_normal(x, media, std):
    return 1 / (std * math.sqrt(2 * math.pi)) * math.exp(-0.5 * ((x - media) / std) ** 2)


def funcion_densidad_gamma(x, k_gamma, theta_gamma):
    return gamma.pdf(x, k_gamma, theta_gamma)


def funcion_densidad_pascal(x, r_pascal, p_pascal):
    # Calcula la combinación binomial
    binomial_coefficient = math.factorial(
        x + r_pascal - 1) / (math.factorial(x) * math.factorial(r_pascal - 1))

    # Calcula la probabilidad
    probability = binomial_coefficient * \
        (p_pascal ** r_pascal) * ((1 - p_pascal) ** x)

    return probability


def funcion_densidad_binomial():
    return


def plot_histogram_with_pdf(data, y_dist, x_dist, bins=50, title=''):
    plt.hist(data, bins=bins, density=True, alpha=0.7,
             color='skyblue', edgecolor='black')
    x = x_dist
    y = y_dist
    plt.plot(x, y, color='red', linewidth=2)
    plt.title(title)
    plt.xlabel('Valor')
    plt.ylabel('Densidad de Probabilidad')
    plt.legend(['PDF', 'Histograma'])
    plt.grid(axis='y', alpha=0.75)
    plt.savefig(title + ".png")
    plt.show()


lcg = LGC(seed=973160574)
n = 20000

# Ajusta el rango según la distribución
x_values_uniform = np.linspace(0, 1, 1000)
x_values_exponential = np.linspace(0, 10, 1000)
x_values_normal = np.linspace(-4, 4, 1000)

y_values_uniform = [funcion_densidad_uniforme(
    x, 0, 1) for x in x_values_uniform]
y_values_exponential = [funcion_densidad_exponencial(
    x, 1) for x in x_values_exponential]
y_values_normal = [funcion_densidad_normal(x, 0, 1) for x in x_values_normal]

uniform_data = generador_uniforme_MTI(n)
plot_histogram_with_pdf(uniform_data, y_values_uniform, x_values_uniform, 50,
                        title='Histograma de Distribución Uniforme con MTI')

exponential_data = generador_exponencial_MTI(n)
plot_histogram_with_pdf(exponential_data, y_values_exponential, x_values_exponential,
                        bins=20, title='Histograma Distribución Exponencial con MTI')

normal_data = generador_normal_MTI(n)
plot_histogram_with_pdf(normal_data, y_values_normal, x_values_normal,
                        bins=20, title='Histograma Distribución Normal con MTI')
