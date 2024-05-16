import math
import random
import sys
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt

# Ruleta


def ruleta():
    valor = random.randint(0, 36)
    return valor

# Grafica


def grafica_balance(balanceArray, i, strategy_name):

    plt.figure(figsize=(10, 6))

    if balanceArray[0] == 0:
        plt.plot(range(0, len(balanceArray)),
                 balanceArray, label='Flujo de ganancia', color='blue')
        plt.title('Gráfico de flujo de ganancia - Corrida ' + str(i+1) + ' - Tiradas: ' +
                  str(len(balanceArray)-1)+' - Estrategia ' + strategy_name)
        plt.axhline(balanceArray[0], color='red',
                    linestyle='--', linewidth=2, label='Balance cero')
        plt.axhline(balanceArray[-1], color='green',
                    linestyle=':', linewidth=2, label='Balance final')
        plt.ylabel('Ganancia')
    else:
        plt.plot(range(0, len(balanceArray)),
                 balanceArray, label='Flujo de capital', color='blue')
        plt.title('Gráfico de flujo de capital - Corrida ' + str(i+1) + ' - Tiradas: ' +
                  str(len(balanceArray)-1)+' - Estrategia ' + strategy_name)
        plt.axhline(balanceArray[0], color='red',
                    linestyle='--', linewidth=2, label='Capital inicial')
        plt.axhline(balanceArray[-1], color='green',
                    linestyle=':', linewidth=2, label='Capital final')
        plt.ylabel('Capital')

    plt.xlabel('Número de tirada')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, len(balanceArray))
    plt.savefig('balance_corrida_'+str(i+1)+'.png')
    plt.show()


def grafica_resumen_balances(balancesArray, i, strategy_name):
    mpl.style.use("default")
    plt.figure(figsize=(10, 6))
    nro_tiradas_eje_x = [x for x in range(cant_tiradas+1)]
    cant_max_tiradas = len(balancesArray[0])
    for i in range(len(balancesArray)):
        if cant_max_tiradas < len(balancesArray[i]):
            cant_max_tiradas = len(balancesArray[i])
        if balancesArray[0][0] == 0:
            plt.plot(nro_tiradas_eje_x[:len(balancesArray[i])],
                     balancesArray[i], label='Flujo de ganancia corrida '+str(i+1), color='C'+str(i % 10+1))
            plt.axhline(balancesArray[i][-1], color='C'+str(i % 10+1),
                        # , label='Balance final corrida '+str(i+1))
                        linestyle=':', linewidth=2)
        else:
            plt.plot(nro_tiradas_eje_x[:len(balancesArray[i])],
                     balancesArray[i], label='Flujo de capital corrida '+str(i+1), color='C'+str(i % 10+1))
            plt.axhline(balancesArray[i][-1], color='C'+str(i % 10+1),
                        # , label='Capital final corrida '+str(i+1))
                        linestyle=':', linewidth=2)

    if balancesArray[0][0] == 0:
        plt.axhline(0, color='red', linestyle='--',
                    linewidth=2, label='Balance cero')
        plt.ylabel('Ganancia')
        plt.title('Gráfico de flujo de ganancia - Cantidad de Corridas ' + str(i+1) + ' - Tiradas máximas: ' +
                  str(cant_max_tiradas-1)+' - Estrategia ' + str(strategy_name))
    else:
        plt.axhline(balancesArray[0][0], color='red',
                    linestyle='--', linewidth=2, label='Capital inicial')
        plt.ylabel('Capital')
        plt.title('Gráfico de flujo de capital - Cantidad de Corridas ' + str(i+1) + ' - Tiradas máximas: ' +
                  str(cant_max_tiradas-1)+' - Estrategia ' + str(strategy_name))

    plt.xlabel('Número de tirada')
    plt.legend()
    plt.grid(True)
    plt.xlim(0, cant_max_tiradas-1)
    plt.savefig('balance_resumen.png')
    plt.show()


# Diccionario de colores de la ruleta (ruleta europea)
color_mapping = {
    0: 'green', 1: 'red', 2: 'black', 3: 'red', 4: 'black', 5: 'red', 6: 'black', 7: 'red', 8: 'black',
    9: 'red', 10: 'black', 11: 'black', 12: 'red', 13: 'black', 14: 'red', 15: 'black', 16: 'red',
    17: 'black', 18: 'red', 19: 'red', 20: 'black', 21: 'red', 22: 'black', 23: 'red', 24: 'black',
    25: 'red', 26: 'black', 27: 'red', 28: 'black', 29: 'black', 30: 'red', 31: 'black', 32: 'red',
    33: 'black', 34: 'red', 35: 'black', 36: 'red'
}


def contar_colores(valores):
    conteo_colores = {'red': 0, 'black': 0, 'green': 0}
    for valor in valores:
        color = color_mapping.get(valor, 'green')
        conteo_colores[color] += 1
    return conteo_colores


def calcular_frecuencia_relativa(conteo_colores, total):
    frecuencia_relativa = {color: conteo /
                           total for color, conteo in conteo_colores.items()}
    return frecuencia_relativa


def grafica_frec_relativa_colores(valores, i, color_elegido, strategy_name):
    frec_rel_esperada_r_b = 18 / 37
    frec_rel_esperada_g = 1 / 37
    conteo_colores = contar_colores(valores)
    total_valores = len(valores)
    frecuencia_relativa = calcular_frecuencia_relativa(
        conteo_colores, total_valores)

    colores = list(frecuencia_relativa.keys())
    frecuencias = list(frecuencia_relativa.values())

    plt.figure(figsize=(8, 4))

    plt.barh(colores, frecuencias, color=[
             'red', 'black', 'green'], edgecolor='black', alpha=1)

    plt.ylabel('Color')
    plt.xlabel('Frecuencia Relativa')
    plt.title('Histograma de colores en la ruleta - Color elegido: ' + str(color_elegido) +
              ' - Corrida ' + str(i+1) + ' - Tiradas: ' + str(total_valores) + ' - Estrategia ' + strategy_name)
    plt.axvline(frec_rel_esperada_r_b, color="blue",
                linestyle="--", linewidth="2", label='Frecuencia Relativa esperada rojo/negro')
    plt.axvline(frec_rel_esperada_g, color="orange",
                linestyle="--", linewidth="2", label='Frecuencia Relativa esperada verde')
    plt.legend()
    plt.xlim(0, 1)  # La frecuencia relativa está entre 0 y 1
    plt.savefig('frec_relativa_colores_corrida_' + str(i+1) + '.png')
    plt.show()


def grafica_frec_rel(frecRelPorTiradaArray, i, color_elegido, strategy_name):
    frec_rel_esperada = 18/37
    plt.figure(figsize=(15, 8))

    if (color_elegido == 'rojo'):
        plt.bar(range(1, len(frecRelPorTiradaArray)+1),
                frecRelPorTiradaArray, color="red", linewidth=5, label="Frecuencia relativa")
    elif (color_elegido == 'negro'):
        plt.bar(range(1, len(frecRelPorTiradaArray)+1),
                frecRelPorTiradaArray, color="black", linewidth=5, label="Frecuencia relativa")

    plt.axhline(frec_rel_esperada, color='blue', linestyle='--',
                linewidth=2, label='Frecuencia Relativa esperada')
    plt.xlabel('Número de tirada')
    plt.ylabel('Frecuencia relativa')
    plt.title('Gráfico de frecuencia relativa - Corrida '+str(i+1)+' - Tiradas: ' +
              str(len(frecRelPorTiradaArray))+' - Estrategia '+strategy_name)
    plt.legend()
    plt.xlim(0, len(frecRelPorTiradaArray)+1)
    # Guardar la figura en disco
    plt.savefig('frec_rel_corrida_'+str(i+1)+'.png')
    plt.show()  # Mostrar la figura


def grafica_resumen_frec_rel(resumenFrecRel, strategy_name):
    frec_rel_esperada = 18/37
    mpl.style.use("default")
    plt.figure(figsize=(20, 10))
    nro_tiradas_eje_x = [x for x in range(cant_tiradas+1)]
    grosor = 3
    cant_max_tiradas = len(resumenFrecRel[0])
    for i in range(len(resumenFrecRel)):
        if cant_max_tiradas < len(resumenFrecRel[i]):
            cant_max_tiradas = len(resumenFrecRel[i])
        plt.bar(nro_tiradas_eje_x[1:len(resumenFrecRel[i]) + 1],
                resumenFrecRel[i],
                label=f'Frecuencia relativa corrida {i + 1}',
                edgecolor=f'C{i % 10}',  # Color del contorno
                fill=False,  # Solo mostrar contorno
                linewidth=(grosor),  # Ancho del contorno
                )
        grosor -= 0.5
        # plt.bar((nro_tiradas_eje_x[1:len(resumenFrecRel[i])+1]),
        #         resumenFrecRel[i], label='Frecuencia relativa corrida '+str(i+1), color='C'+str(i % 10+1), alpha=(1-(0.15*i)))
    plt.axhline(frec_rel_esperada, color='red', linestyle='--',
                label='Frecuencia Relativa esperada')
    plt.xlabel('Número de tirada')
    plt.ylabel('Frecuencia relativa')
    plt.title('Gráfico de frecuencia relativa - Corrida '+str(i+1)+' - Tiradas: ' +
              str(len(resumenFrecRel[i]))+' - Estrategia '+strategy_name)
    plt.legend()
    plt.xlim(0, cant_max_tiradas+1)
    # Guardar la figura en disco
    plt.savefig('resumen_frec_rel_corrida_'+str(i+1)+'.png')
    plt.show()  # Mostrar la figura

# Estrategias


def martingala_strategy(initial_bet, cant_tiradas, initial_capital, capital):
    balanceArray = []
    betArray = []
    valores = []
    frecRelPorTiradaArray = []
    frec_abs = 0

    if capital == "a":
        balanceArray.append(initial_capital)
    else:
        balanceArray.append(0)
    betArray.append(initial_bet)
    for i in range(cant_tiradas):
        if betArray[i] <= balanceArray[i] or balanceArray[0] == 0:
            valor = ruleta()
            valores.append(valor)
            if valor in color:
                balanceArray.append(balanceArray[i] + betArray[i])
                betArray.append(betArray[0])
                frec_abs += 1
            else:
                balanceArray.append(balanceArray[i] - betArray[i])
                betArray.append(betArray[i] * 2)
        else:
            break

        frecRelPorTiradaArray.append(frec_abs/(i+1))

    return balanceArray, betArray, valores, frecRelPorTiradaArray


def dalembert_strategy(initial_bet, cant_tiradas, initial_capital, capital):
    balanceArray = []
    betArray = []
    valores = []
    frecRelPorTiradaArray = []
    frec_abs = 0

    if capital == "a":
        balanceArray.append(initial_capital)
    else:
        balanceArray.append(0)
    betArray.append(initial_bet)
    unidadBase = initial_bet

    for i in range(cant_tiradas):
        if betArray[i] <= balanceArray[i] or balanceArray[0] == 0:
            valor = ruleta()
            valores.append(valor)
            if valor in color:
                frec_abs += 1
                balanceArray.append(balanceArray[i] + betArray[i])
                # para que no llegue a apuesta 0 en caso de ganar
                if (betArray[i]-unidadBase) < unidadBase:
                    betArray.append(unidadBase)
                else:
                    betArray.append(betArray[i] - unidadBase)

            else:
                balanceArray.append(balanceArray[i] - betArray[i])
                betArray.append(betArray[i] + unidadBase)
        else:
            break

        frecRelPorTiradaArray.append(frec_abs/(i+1))
    return balanceArray, betArray, valores, frecRelPorTiradaArray


def fibonacci_strategy(initial_bet, cant_tiradas, initial_capital, capital):
    balanceArray = []
    betArray = []
    valores = []
    frecRelPorTiradaArray = []
    frec_abs = 0

    if capital == "a":
        balanceArray.append(initial_capital)
    else:
        balanceArray.append(0)
    betArray.append(initial_bet)
    valoresfib = [0, initial_bet, initial_bet]
    for i in range(cant_tiradas):
        if betArray[i] <= balanceArray[i] or balanceArray[0] == 0:
            valor = ruleta()
            valores.append(valor)
            if valor in color:
                frec_abs += 1
                balanceArray.append(balanceArray[i] + valoresfib[1])
                if valoresfib[0] == 0 or valoresfib[0] == initial_bet:
                    valoresfib = [0, initial_bet, initial_bet]
                else:
                    prevant = valoresfib[0]
                    actant = valoresfib[1]
                    act = actant-prevant
                    valoresfib = [prevant-act, act, prevant]
            else:
                balanceArray.append(balanceArray[i] - valoresfib[1])
                actant = valoresfib[1]
                posant = valoresfib[2]
                valoresfib = [actant, posant, actant+posant]
            betArray.append(valoresfib[1])
        else:
            break

        frecRelPorTiradaArray.append(frec_abs/(i+1))

    return balanceArray, betArray, valores, frecRelPorTiradaArray


def paroli_strategy(initial_bet, cant_tiradas, initial_capital, capital):
    balanceArray = []
    betArray = []
    valores = []
    frecRelPorTiradaArray = []
    frec_abs = 0

    if capital == "a":
        balanceArray.append(initial_capital)
    else:
        balanceArray.append(0)
    betArray.append(initial_bet)

    for i in range(cant_tiradas):
        if betArray[i] <= balanceArray[i] or balanceArray[0] == 0:
            valor = ruleta()
            valores.append(valor)
            if valor in color:
                frec_abs += 1
                balanceArray.append(balanceArray[i] + betArray[i])

                betArray.append(betArray[i]*2)

            else:
                balanceArray.append(balanceArray[i] - betArray[i])

                betArray.append(initial_bet)
        else:
            break

        frecRelPorTiradaArray.append(frec_abs/(i+1))

    return balanceArray, betArray, valores, frecRelPorTiradaArray


def simulate_game(strategy, initial_bet, cant_tiradas, cant_corridas, initial_capital, capital, strategy_name, color_elegido):
    balancesArray = []
    resumenFrecRel = []
    for i in range(cant_corridas):
        resultados = strategy(initial_bet, cant_tiradas,
                              initial_capital, capital)

        balanceArray = resultados[0]
        betArray = resultados[1]
        valores = resultados[2]
        frecRelPorTiradaArray = resultados[3]
        balancesArray.append(balanceArray)
        resumenFrecRel.append(frecRelPorTiradaArray)

        grafica_balance(balanceArray, i, strategy_name)
        grafica_frec_relativa_colores(valores, i, color_elegido, strategy_name)
        grafica_frec_rel(frecRelPorTiradaArray, i,
                         color_elegido, strategy_name)
    grafica_resumen_balances(balancesArray, i, strategy_name)
    grafica_resumen_frec_rel(resumenFrecRel,  strategy_name)


# Inicio del programa
if len(sys.argv) != 11:
    print("Uso: python Tp1.2-Estrategias.py -c <cant_tiradas> -n <corridas> -e <color_elegido> -s <estrategia(m/d/f/n)> -a <capital(i/a)>")
    sys.exit(1)

# Parámetros de la simulación
cant_tiradas = int(sys.argv[2])
cant_corridas = int(sys.argv[4])
color_elegido = sys.argv[6]
estrategia = (sys.argv[8])
capital = (sys.argv[10])

if color_elegido == "n":
    color = [2, 4, 6, 8, 10, 11, 13, 15, 17,
             20, 22, 24, 26, 28, 29, 31, 33, 35]
    color_elegido = "negro"
else:
    color = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    color_elegido = "rojo"

# Parametros ingresados por la consola

if capital == "a":
    initial_capital = int(input("Ingrese el capital inicial: "))
else:
    initial_capital = math.inf
    print("Capital infinito")
initial_bet = int(input("Ingrese la apuesta inicial: "))

if (estrategia) == "m":
    # Simulación de la estrategia de Martingala
    simulate_game(martingala_strategy, initial_bet, cant_tiradas,
                  cant_corridas, initial_capital, capital, "Martin Gala", color_elegido)
elif (estrategia) == "d":
    # Simulación de la estrategia de D'Alembert
    simulate_game(dalembert_strategy, initial_bet, cant_tiradas,
                  cant_corridas, initial_capital, capital, "D'Alembert", color_elegido)
elif (estrategia) == "f":
    # Simulación de la estrategia de Fibonacci
    simulate_game(fibonacci_strategy, initial_bet, cant_tiradas,
                  cant_corridas, initial_capital, capital, "Fibonacci", color_elegido)
elif (estrategia) == "o":
    # Simulación de la estrategia de Paroli
    simulate_game(paroli_strategy, initial_bet, cant_tiradas,
                  cant_corridas, initial_capital, capital, "Paroli", color_elegido)
