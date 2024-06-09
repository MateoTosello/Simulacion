import random
from PIL import Image
import array as arr
import statistics
import sys
import math

# compurebo que el programa en CLI se use como se debe#
if len(sys.argv) != 5 or sys.argv[1] != "-s" or sys.argv[3] != "-n":
    print("Uso: python numeros_psa.py -s <semilla> -n <nro_iteraciones>")
    sys.exit(1)
semilla_inicial = int(sys.argv[2])
corridas = int(sys.argv[4])

sem_ini = str(semilla_inicial)


def bitmap(resultados, metodo, semilla):
    x = 0
    y = 0
    tam = int(math.sqrt(len(resultados)))
    img = Image.new('RGB', (tam, tam), "black")
    pixels = img.load()
    for i in range(len(resultados)):
        aux = str(resultados[i])
        prueba = int(aux[2])
        if (prueba % 2 == 0):
            pixels[x, y] = (255, 255, 255)
        if (y+1 >= 512):
            y = 0
            x = x+1
        else:
            y = y+1
    img.save('bitmap_'+metodo+'_semilla_'+semilla+'.png')


def glc(semilla):
    a = 1664525
    c = 1013904223
    m = 2**32
    subtotal = semilla * a + c
    pseudoaleatorio = subtotal % m
    random = pseudoaleatorio / (m - 1)
    return random


def vonNewman(semilla):
    s_str = str(semilla*semilla)
    while len(s_str) != 10:
        s_str = "0"+s_str
    n_rand = (int(s_str[2:6]))
    return n_rand


def merseneTwister(semilla):
    random.seed(semilla)
    return random.random()


resultados = [(0.0000) for x in range(corridas)]
m = 2**32
semilla = glc(semilla_inicial)
for x in range(corridas):
    resultados[x] = semilla
    semilla = glc(semilla*(m - 1))
bitmap(resultados, 'glc', sem_ini)


resultados = [(0.0000) for x in range(corridas)]
semilla = semilla_inicial
for x in range(corridas):
    semilla = merseneTwister(semilla)
    resultados[x] = semilla
bitmap(resultados, 'mt', sem_ini)

resultados = [(0.0000) for x in range(corridas)]
semilla = semilla_inicial
for x in range(corridas):
    semilla = vonNewman(semilla)
    resultados[x] = semilla/10000
bitmap(resultados, 'vn', sem_ini)
