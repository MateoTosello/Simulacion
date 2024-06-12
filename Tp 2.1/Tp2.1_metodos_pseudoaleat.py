import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare, kstest

# Generador Congruencial Lineal (GCL)
def gcl(a, c, m, seed, n):
    numbers = []
    X = seed
    for _ in range(n):
        X = (a * X + c) % m
        numbers.append(X / m)
    return numbers

# Método de Cuadrados Medios
def cuadrados_medios(seed, n):
    numbers = []
    X = seed
    num_digits = len(str(seed))
    for _ in range(n):
        X2 = str(X * X).zfill(2 * num_digits)
        mid_start = (len(X2) - num_digits) // 2
        X = int(X2[mid_start:mid_start + num_digits])
        numbers.append(X / (10 ** num_digits))
    return numbers

# Generar gráficos de mapas de bits
def plot_bitmaps(numbers, title, test):
    size = int(np.sqrt(len(numbers)))
    numbers = numbers[:size*size]
    matrix = np.reshape(numbers, (size, size))
    plt.figure(figsize=(6, 6))
    plt.imshow(matrix, cmap='gray', interpolation='nearest')
    plt.title(title)
    plt.axis('off') 
    plt.savefig('metodo_'+test+'_'+str(seed)+'.png')
    plt.show()


# Pruebas de aleatoriedad
# Chi-cuadrado
def chi_cuadrado(numbers, bins=10):
    observed, _ = np.histogram(numbers, bins=bins)
    expected = len(numbers) / bins
    chi2, p = chisquare(observed, [expected] * bins)
    return chi2, p

# Paridad
def paridad(numbers):
    bits = ''.join(f'{int(x * (2 ** 32)) & 0xFFFFFFFF:032b}' for x in numbers)
    ones = bits.count('1')
    zeros = bits.count('0')
    total = len(bits)
    p = abs(ones - zeros) / total
    return p

# Póker (Poker Test)
def poker(numbers, m=5):
    # Convertir numeros a string
    str_numbers = [str(int(x * (10**m))).zfill(m) for x in numbers]
    counts = {}
    for num in str_numbers:
        key = ''.join(sorted(num))
        if key in counts:
            counts[key] += 1
        else:
            counts[key] = 1
    frequencies = np.array(list(counts.values()))
    chi2, p = chisquare(frequencies)
    return chi2, p

# Kolmogorov-Smirnov
def kolmogorov_smirnov(numbers):
    d, p = kstest(numbers, 'uniform')
    return d, p

# Evaluación de pruebas
def evaluar_pruebas(resultados_pruebas, alpha=0.05):
    for prueba, (statistic, p_value) in resultados_pruebas.items():
        if p_value > alpha:
            print(f"{prueba}: Aprueba (p-value={p_value:.5f})")
        else:
            print(f"{prueba}: Rechaza (p-value={p_value:.5f})")

# Parámetros y ejecución
seed = 3183856186  #seed CM: 759302 - 3183856186 - 796225369226628988 
# seed = int(time.time())

np.random.seed(seed)

n = 200000

# Parámetros GCL
a = 1664525
c = 1013904223
m = 2**32

gcl_numbers = gcl(a, c, m, seed, n)
cuadrados_numbers = cuadrados_medios(seed, n)
random_numbers = np.random.rand(n)  #numeros aleatorios con biblioteca de python

plot_bitmaps(gcl_numbers, "GCL Bitmap",'GCL')
plot_bitmaps(cuadrados_numbers, "Cuadrados Medios Bitmap",'CM')
plot_bitmaps(random_numbers, "Números Aleatorios", 'Random')

# Pruebas (Valores)
print('\nTests:')
print('Semilla: ',seed)
print("--------------GCL-------------")
print("Chi-Cuadrado:", chi_cuadrado(gcl_numbers))
print("Paridad:", paridad(gcl_numbers))
print("Poker:", poker(gcl_numbers))
print("Kolmogorov-Smirnov:", kolmogorov_smirnov(gcl_numbers))

print("\n-------------Cuadrados Medios Tests----------")
print("Chi-Cuadrado:", chi_cuadrado(cuadrados_numbers))
print("Paridad:", paridad(cuadrados_numbers))
print("Poker:", poker(cuadrados_numbers))
print("Kolmogorov-Smirnov:", kolmogorov_smirnov(cuadrados_numbers))

print("\n------------- Números Aleatorios (python) Tests ----------")
print("Chi-Cuadrado:", chi_cuadrado(random_numbers))
print("Paridad:", paridad(random_numbers))
print("Poker:", poker(random_numbers))
print("Kolmogorov-Smirnov:", kolmogorov_smirnov(random_numbers))

print("\n---------------------------------")
print('\nAprueba-Rechaza:')

# Pruebas (aprobado-rechazado)
resultados_gcl = {
    "Chi-Cuadrado": chi_cuadrado(gcl_numbers),
    "Paridad": (None, paridad(gcl_numbers)),
    "Poker": poker(gcl_numbers),
    "Kolmogorov-Smirnov": kolmogorov_smirnov(gcl_numbers)
}

resultados_cuadrados = {
    "Chi-Cuadrado": chi_cuadrado(cuadrados_numbers),
    "Paridad": (None, paridad(cuadrados_numbers)),
    "Poker": poker(cuadrados_numbers),
    "Kolmogorov-Smirnov": kolmogorov_smirnov(cuadrados_numbers)
}

resultados_random = {
    "Chi-Cuadrado": chi_cuadrado(random_numbers),
    "Paridad": (None, paridad(random_numbers)),
    "Poker": poker(random_numbers),
    "Kolmogorov-Smirnov": kolmogorov_smirnov(random_numbers)
}


print("GCL Tests")
evaluar_pruebas(resultados_gcl)

print("\nCuadrados Medios Tests")
evaluar_pruebas(resultados_cuadrados)

print("\nNúmeros Aleatorios (python) Tests")
evaluar_pruebas(resultados_random)