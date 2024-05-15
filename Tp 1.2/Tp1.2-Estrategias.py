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


def grafica_frec_relativa_colores(valores, i, num_elegido, strategy_name):
    frec_rel_esperada_r_b = (18/37)
    frec_rel_esperada_g = (1/37)
    conteo_colores = contar_colores(valores)
    total_valores = len(valores)
    frecuencia_relativa = calcular_frecuencia_relativa(
        conteo_colores, total_valores)

    colores = list(frecuencia_relativa.keys())
    frecuencias = list(frecuencia_relativa.values())

    plt.figure(figsize=(8, 6))

    plt.bar(colores, frecuencias, color=[
        'red', 'black',  'green'], edgecolor='black', alpha=1)

    plt.xlabel('Color')
    plt.ylabel('Frecuencia Relativa')
    plt.title('Histograma de colores en la ruleta - Color elegido ' + str(num_elegido) + ' - Corrida ' +
              str(i+1) + ' - Tiradas: ' + str(total_valores) + ' - Estrategia ' + strategy_name)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.axhline(frec_rel_esperada_r_b, color="blue",
                linestyle="--", linewidth="2")
    plt.axhline(frec_rel_esperada_g, color="orange",
                linestyle="--", linewidth="2")
    plt.ylim(0, 1)  # La frecuencia relativa está entre 0 y 1
    plt.savefig('frec_relativa_colores_corrida_' + str(i+1) + '.png')
    plt.show()

# def grafica_frec_abs(valores, i, num_elegido, strategy_name):

#     frec_abs_esperada = len(valores) / 37

#     plt.figure(figsize=(8, 6))
#     plt.hist(valores, bins=range(38), color='green',
#              edgecolor='black', alpha=0.7, align='mid')
#     plt.axhline(frec_abs_esperada, color='red', linestyle='--',
#                 linewidth=2, label='Valor Teórico Esperado')
#     plt.xlabel('Resultado')
#     plt.ylabel('Frecuencia Absoluta')
#     plt.title('Histograma lanzamiento de ruleta al número ' + str(num_elegido) + ' - Corrida ' +
#               str(i+1) + ' - Tiradas: ' + str(len(valores))+' - Estrategia '+strategy_name)
#     plt.xticks([x + 0.5 for x in range(37)], [str(x) for x in range(37)])
#     plt.grid(axis='y', linestyle='--', alpha=0.7)
#     plt.legend()
#     plt.savefig('frec_abs_corrida_'+str(i+1)+'.png')
#     plt.show()

# Estrategias


def martingala_strategy(initial_bet, cant_tiradas, initial_capital, capital):
    balanceArray = []
    betArray = []
    valores = []
    if capital == "a":
        balanceArray.append(initial_capital)
    else:
        balanceArray.append(0)
    betArray.append(initial_bet)
    for i in range(cant_tiradas):
        if betArray[i] <= balanceArray[i] or balanceArray[0] == 0:
            print("tirada: ", (i+1))
            print("bet: ", betArray[i])
            print("capital: ", balanceArray[i])
            valor = ruleta()
            valores.append(valor)
            if valor in color:
                print("Gano")
                print()
                balanceArray.append(balanceArray[i] + betArray[i])
                betArray.append(betArray[0])

            else:
                print("Perdio")
                print()
                balanceArray.append(balanceArray[i] - betArray[i])
                betArray.append(betArray[i] * 2)
            print(balanceArray)
        else:
            print("Te quedaste seco")
            break

    return balanceArray, betArray, valores


def dalembert_strategy(initial_bet, cant_tiradas, initial_capital, capital):
    balanceArray = []
    betArray = []
    if capital == "a":
        balanceArray.append(initial_capital)
    else:
        balanceArray.append(0)
    betArray.append(initial_bet)
    unidadBase = initial_bet

    for i in range(cant_tiradas):
        print("Bet: ", betArray[i])
        if betArray[i] <= balanceArray[i]:
            valor = ruleta()
            if valor in color:
                print("Gano")
                balanceArray.append(balanceArray[i] + betArray[i])
                # para que no llegue a apuesta 0 en caso de ganar
                if (betArray[i]-unidadBase) < unidadBase:
                    betArray.append(unidadBase)
                else:
                    betArray.append(betArray[i] - unidadBase)

            else:
                print("Perdio")
                balanceArray.append(balanceArray[i] - betArray[i])
                betArray.append(betArray[i] + unidadBase)
            print(balanceArray)
        else:
            print("Te quedaste seco")
            balanceArray.append(0)
            break

    return balanceArray, betArray


def fibonacci_strategy(initial_bet, cant_tiradas, initial_capital, capital):
    balanceArray = []
    betArray = []
    if capital == "a":
        balanceArray.append(initial_capital)
    else:
        balanceArray.append(0)
    betArray.append(initial_bet)
    valores = [0, initial_bet, initial_bet]
    for i in range(cant_tiradas):
        print(i)
        print("Array: ", valores)
        if valores[1] <= balanceArray[i]:
            valor = ruleta()
            if valor in color:
                print("Gano")
                balanceArray.append(balanceArray[i] + valores[1])
                if valores[0] == 0 or valores[0] == initial_bet:
                    valores = [0, initial_bet, initial_bet]
                else:
                    prevant = valores[0]
                    actant = valores[1]
                    act = actant-prevant
                    valores = [prevant-act, act, prevant]
            else:
                print("Perdio")
                balanceArray.append(balanceArray[i] - valores[1])
                actant = valores[1]
                posant = valores[2]
                valores = [actant, posant, actant+posant]

            print("Capital: ", balanceArray)
        else:
            print("Te quedaste seco")
            balanceArray.append(0)
            break

    return balanceArray, betArray


def paroli_strategy(initial_bet, cant_tiradas, initial_capital, capital):
    balanceArray = []
    betArray = []
    if capital == "a":
        balanceArray.append(initial_capital)
    else:
        balanceArray.append(0)
    betArray.append(initial_bet)
    balanceArray[i] = initial_capital
    betArray[i] = initial_bet

    for i in range(cant_tiradas):
        if betArray[i] <= balanceArray[i]:
            valor = ruleta()
            if valor in color:
                print("Gano")
                balanceArray.append(balanceArray[i] + betArray[i])

                betArray.append(betArray[i]*2)

            else:
                print("Perdio")
                balanceArray.append(balanceArray[i] - betArray[i])

                betArray[i] = initial_bet
            print(balanceArray)
        else:
            print("Te quedaste seco")
            balanceArray.append(0)
            break

    return balanceArray, betArray


def simulate_game(strategy, initial_bet, cant_tiradas, cant_corridas, initial_capital, capital, strategy_name, color_elegido):
    balancesArray = []
    for i in range(cant_corridas):
        resultados = strategy(initial_bet, cant_tiradas,
                              initial_capital, capital)

        balanceArray = resultados[0]
        betArray = resultados[1]
        valores = resultados[2]

        balancesArray.append(balanceArray)

        grafica_balance(balanceArray, i, strategy_name)
        grafica_frec_relativa_colores(valores, i, color_elegido, strategy_name)
    grafica_resumen_balances(balancesArray, i, strategy_name)


# Inicio del programa
if len(sys.argv) != 13:
    print("Uso: python Tp1.2-Estrategias.py -c <cant_tiradas> -n <corridas> -e <color_elegido> -s <estrategia(m/d/f/n)> -a <capital(i/a)> -v <nro_elegido>")
    sys.exit(1)

# Parámetros de la simulación
cant_tiradas = int(sys.argv[2])
cant_corridas = int(sys.argv[4])
color_elegido = sys.argv[6]
estrategia = (sys.argv[8])
capital = (sys.argv[10])
num_elegido = (sys.argv[12])

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
    print(initial_capital)
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
    simulate_game(paroli_strategy, initial_bet, cant_tiradas,
                  cant_corridas, initial_capital, capital, "Paroli", color_elegido)
