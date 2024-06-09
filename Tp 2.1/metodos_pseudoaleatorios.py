import sys
import matplotlib.pyplot as plt
import numpy as np


def glc(corridas):
    semilla = int(input('Ingrese el valor de una semilla: '))
    a = 1664525
    c = 1013904223
    m = 2**32  # 4294967296

    resultados = []

    for x in range(corridas):
        subtotal = semilla * a + c
        pseudoaleatorio = subtotal % m
        random = pseudoaleatorio / (m - 1)
        resultados.append((pseudoaleatorio))
        semilla = pseudoaleatorio
        print(f"Los resultados son: {resultados[x]}")
        if pseudoaleatorio == 0:
            print('Límite del Método.')
            break

    return resultados


def metodo_cuadrado():
    semilla = 8477  # VER
    d = 4
    resultados = []
    x = semilla

    for _ in range(corridas):
        # Elevar al cuadrado y rellenar con ceros si es necesario
        x_cuadrado = str(x ** 2).zfill(2 * d)
        # Extraer D dígitos centrales
        x = int(x_cuadrado[len(x_cuadrado) // 2 -
                d // 2:len(x_cuadrado) // 2 + d // 2])
        resultados.append(x)

    return resultados


if len(sys.argv) != 3:
    print("Uso: python metodos_pseudoakeatorios.py -n <nro_iteraciones>")
    sys.exit(1)
corridas = int(sys.argv[2])

resultados = glc(corridas)

# Convertir la lista de resultados a una matriz 2D (bitmap)
# Suponiendo una dimensión de 100x100 para la matriz bitmap
dimension = int(np.ceil(np.sqrt(len(resultados))))
bitmap = np.zeros((dimension, dimension))

# Llenar la matriz con los resultados
for i in range(len(resultados)):
    row = i // dimension
    col = i % dimension
    bitmap[row, col] = resultados[i]

# Normalizar la matriz para que los valores estén entre 0 y 1
bitmap = bitmap / np.max(bitmap)

# Crear el gráfico bitmap
plt.figure(figsize=(512, 512))
plt.imshow(bitmap, cmap='gray', interpolation='nearest')
plt.title('Bitmap de números pseudoaleatorios generados por el método GCL')
plt.axis('off')  # Ocultar los ejes
plt.show()
