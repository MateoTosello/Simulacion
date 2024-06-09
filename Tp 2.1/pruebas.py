import math
import random
import sys
from PIL import Image


def glc(semilla, corridas):
    a = 1664525
    c = 1013904223
    m = 2**32  # 4294967296

    resultados = []

    for x in range(corridas):
        subtotal = semilla * a + c
        pseudoaleatorio = subtotal % m
        random = pseudoaleatorio / (m - 1)
        resultados.append(random)
        semilla = pseudoaleatorio
        if pseudoaleatorio == 0:
            print('Límite del Método.')
            break

    return resultados


def metodo_cuadrado(semilla, corridas):
    d = 4
    resultados = []
    res_divididos = []
    x = semilla

    largo_max = 0
    for _ in range(corridas):
        # Elevar al cuadrado y rellenar con ceros si es necesario
        x_cuadrado = str(x ** 2).zfill(2 * d)
        # Extraer D dígitos centrales
        x = int(x_cuadrado[len(x_cuadrado) // 2 -
                d // 2:len(x_cuadrado) // 2 + d // 2])

        if largo_max < len(str(x)):
            largo_max = len(str(x))
        resultados.append(x)

    divisor = 1
    for i in range(largo_max):
        divisor = divisor*10

    for i in range(len(resultados)):
        res_divididos.append(resultados[i]/divisor)

    return resultados


def random_py(semilla, corridas):
    resultados = []
    for i in range(corridas):
        resultados.append(random.random())

    return resultados


def bitmap(resultados, nombre_archivo, semilla):
    # Crear una nueva imagen de 512x512 píxeles
    img = Image.new('RGB', (512, 512), color='black')
    pixels = img.load()

    # Dibujar los resultados en la imagen
    width, height = img.size
    num_results = len(resultados)
    for i in range(num_results):
        x = int((i % width) / (width / 512))
        y = int((i / width) / (height / 512))
        # Asignar color basado en el valor del resultado
        color_value = int(resultados[i] * 255)
        pixels[x, y] = (color_value, color_value, color_value)

    # Guardar la imagen con el nombre de archivo especificado
    img.save(f'{nombre_archivo}_semilla_{semilla}.png')
    print(f'Imagen guardada como {nombre_archivo}_semilla_{semilla}.png')


# def bitmap2(resultados, nombre_archivo, semilla):
#     # Crear una nueva imagen de 512x512 píxeles
#     img = Image.new('RGB', (512, 512), color='black')
#     pixels = img.load()

#     # Dibujar los resultados en la imagen
#     width, height = img.size
#     num_results = len(resultados)
#     for i in range(num_results):
#         x = int((i % width) / (width / 512))
#         y = int((i / width) / (height / 512))
#         # Asignar color basado en el valor del resultado
#         aux = str(resultados[i])
#         prueba = int(aux[0])
#         if (prueba % 2 == 0):
#             pixels[x, y] = (255, 255, 255)
#         else:
#             pixels[x, y] = (0, 0, 0)

#     # Guardar la imagen con el nombre de archivo especificado
#     img.save(f'{nombre_archivo}_semilla_{semilla}.png')
#     print(f'Imagen guardada como {nombre_archivo}_semilla_{semilla}.png')


if len(sys.argv) != 5:
    print("Uso: python glc.py -s <semilla> -n <nro_iteraciones>")
    sys.exit(1)

semilla = int(sys.argv[2])
corridas = int(sys.argv[4])
str_semilla = str(semilla)

resultados = [(0.0000) for x in range(corridas)]
resultados = glc(semilla, corridas)
bitmap(resultados, 'glc', str_semilla)

resultados = [(0.0000) for x in range(corridas)]
semilla = 875302
resultados = metodo_cuadrado(semilla, corridas)
bitmap(resultados, 'mc', str_semilla)

resultados = [(0.0000) for x in range(corridas)]
semilla = 875302
resultados = random_py(semilla, corridas)
bitmap(resultados, 'random_py', str_semilla)
