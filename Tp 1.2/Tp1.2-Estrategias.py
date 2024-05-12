import math
import random
import sys
import numpy as np
import matplotlib.pyplot as plt

# Ruleta


def ruleta():
    valor = random.randint(0, 36)
    return valor


def grafica_balance(balanceArray, i, strategy_name):

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(balanceArray) + 1),
             balanceArray, label='Flujo de ganancia', color='blue')
    plt.axhline(0, color='red', linestyle='--',
                linewidth=2, label='Balance cero')
    plt.xlabel('Número de tirada')
    plt.ylabel('Cantidad de ganancia')
    plt.title('Gráfico de ganancia neta - Corrida ' + str(i+1) + ' - Tiradas: ' +
              str(len(balanceArray))+' - Estrategia ' + strategy_name)
    plt.legend()
    plt.grid(True)
    # Límites del eje x de tirada 1 a la 10
    plt.xlim(1, len(balanceArray))
    # Guardar la figura en disco
    plt.savefig('balance_corrida_'+str(i+1)+'.png')
    plt.show()  # Mostrar la figura

# Estrategias


def martingala_strategy(initial_bet, cant_tiradas, initial_capital, capital):
    balanceArray = []
    betArray = []
    if capital == "a":
        balanceArray.append(initial_capital)
    else:
        balanceArray.append(0)
    betArray.append(initial_bet)
    for i in range(cant_tiradas):
        if betArray[i] <= balanceArray[i] or balanceArray[0] == 0:
            print("tirada: ", i)
            print("bet: ", betArray[i])
            print("capital: ", balanceArray[i])
            valor = ruleta()
            if valor in negro:
                print("Gano")
                balanceArray.append(balanceArray[i] + betArray[i])
                betArray.append(betArray[0])
            else:
                print("Perdio")
                balanceArray.append(balanceArray[i] - betArray[i])
                betArray.append(betArray[i] * 2)
        else:
            print("Te quedaste seco")
            balanceArray.append(0)
            break

    return balanceArray, betArray

# Martin Gala vieja
#     balanceArray = []
#     betArray = []
#     balanceArray.append(initial_capital)
#     betArray.append(initial_bet)
#     actual_bet = betArray[0]
#     actual_capital = balanceArray[0]
#     actual_capital = initial_capital
#     actual_bet = initial_bet
#     for i in range(cant_tiradas):

#         if actual_bet <= actual_capital:
#             print("tirada: ", i)
#             print("bet: ", actual_bet)
#             print("capital: ", actual_capital)
#             valor = ruleta()
#             actual_capital -= actual_bet
#             if valor in negro:
#                 actual_capital += actual_bet * 2
#                 actual_bet = initial_bet
#             else:
#                 actual_bet = actual_bet * 2

#         else:
#             print("Te quedaste seco")
#             return

#             # # Final de la funcion
#             # return actual_capital


def dalembert_strategy(initial_bet, cant_tiradas, initial_capital, num_elegido):

    actual_capital = initial_capital
    actual_bet = initial_bet
    unidadBase = 10

    for i in range(cant_tiradas):
        if actual_bet <= actual_capital:
            valor = ruleta()
            actual_capital -= actual_bet
            print("tirada: ", i)
            print("bet: ", actual_bet)
            print("capital: ", actual_capital)
            if valor in negro:
                actual_capital += actual_bet * 2
                # para que no llegue a apuesta 0 en caso de ganar
                if (actual_bet-unidadBase) < unidadBase:
                    actual_bet = unidadBase
                else:
                    actual_bet -= unidadBase

            else:
                actual_bet += unidadBase

        else:
            print("Te quedaste seco")
            return

        # Final de la funcion
        return actual_capital


# def fibonacci_logic(balanceArray, betArray):
#     actual_bet = betArray[0]
#     actual_capital = balanceArray[0]
#     previos_bet = 0
#     for i in range(cant_tiradas):
#         if actual_bet <= actual_capital:
#             valor = ruleta()
#             actual_capital -= actual_bet
#             if valor in negro:
#                 actual_capital += actual_bet * 2
#                 if actual_bet < previos_bet:
#                     actual_bet = betArray[0]
#                     previos_bet = 0
#                 else:
#                     actual_bet -= previos_bet
#                     previos_bet -= actual_bet
#             else:
#                 aux = previos_bet
#                 previos_bet = actual_bet
#                 actual_bet += aux
#         else:
#             print("Te quedaste seco")
#             return
        # if betArray[i] <= balanceArray[i]:
        #     valor = ruleta()

        #     print("tirada: ", i, "--------------------------------------------------------------------------")
        #     print("bet: ", betArray[i])
        #     print("capital: ", balanceArray[i+1])
        #     if valor in negro:
        #         print("Ganada")
        #         balanceArray[i+1] = balanceArray[i] + betArray[i]
        #         print("actual", actual_bet)
        #         print("previa", previos_bet)
        #         actual_bet -= previos_bet
        #         previos_bet -= actual_bet
        #         print("actual", actual_bet)
        #         print("previa", previos_bet)
        #     else:
        #         aux = previos_bet
        #         previos_bet = actual_bet
        #         actual_bet += aux
        # else:
        #     print("Te quedaste seco")
        #     return


def fibonacci_strategy(initial_bet, cant_tiradas, initial_capital, capital):
    print("Fibonacci")
    # balanceArray = []
    # betArray = []
    # balanceArray.append(initial_capital)
    # betArray.append(initial_bet)
    # actual_bet = betArray[0]
    # actual_capital = balanceArray[0]
    # print("bet: ", actual_bet)
    # print("capital: ", actual_capital)
    # previos_bet = 0
    # for i in range(cant_tiradas):
    #     print(i)
    #     if actual_bet <= actual_capital:
    #         valor = ruleta()
    #         if valor in negro:
    #             print("gano")
    #             actual_capital += actual_bet
    #             print("previa bet antes: ", previos_bet)
    #             print("actual bet antes: ", actual_bet)
    #             actual_bet -= previos_bet
    #             previos_bet -= actual_bet
    #             print("previa bet: ", previos_bet)
    #             print("actual bet: ", actual_bet)
    #             print("actual capital: ", actual_capital)
    #         else:
    #             print("perdio")
    #             actual_capital -= actual_bet
    #             aux = previos_bet
    #             print("aux: ", aux)
    #             previos_bet = actual_bet
    #             actual_bet += aux
    #             print("previa bet: ", previos_bet)
    #             print("actual bet: ", actual_bet)
    #             print("actual capital: ", actual_capital)

    #         if previos_bet:
    #             print("Entro aca")
    #             actual_bet = betArray[0]
    #             previos_bet = 0
    #     else:
    #         print("Te quedaste seco")
    #         return

    # if capital == "a":
    #     balanceArray[0] = initial_capital
    #     betArray[0] = initial_bet
    #     fibonacci_logic(balanceArray, betArray)
    # actual_capital = initial_capital
    # actual_bet = initial_bet
    # previos_bet = 0

    # Logica Fibbonacci
    # for i in range(cant_tiradas):
    #     if actual_bet <= actual_capital:
    #         valor = ruleta()
    #         actual_capital -= actual_bet
    #         print(
    #             "tirada: ", i, "--------------------------------------------------------------------------")
    #         print("bet: ", actual_bet)
    #         print("capital: ", actual_capital)
    #         if valor in negro:
    #             print("Ganada")
    #             actual_capital += actual_bet * 2
    #             print("actual", actual_bet)
    #             print("previa", previos_bet)
    #             actual_bet -= previos_bet
    #             previos_bet -= actual_bet
    #             print("actual", actual_bet)
    #             print("previa", previos_bet)
    #         else:
    #             aux = previos_bet
    #             previos_bet = actual_bet
    #             actual_bet += aux
    #     else:
    #         print("Te quedaste seco")
    #         return


def propia_strategy(initial_bet, cant_tiradas, initial_capital, capital):
    actual_capital = initial_capital
    for i in range(cant_tiradas):
        print("Estrategia propia")

        # Final de la funcion
        return actual_capital


def simulate_game(strategy, initial_bet, cant_tiradas, cant_corridas, initial_capital, capital, strategy_name):
    for i in range(cant_corridas):
        resultados = strategy(initial_bet, cant_tiradas,
                              initial_capital, capital)

        balanceArray = resultados[0]
        betArray = resultados[1]

        grafica_balance(balanceArray, i, strategy_name)


# Inicio del programa
if len(sys.argv) != 11:
    print("Uso: python Tp1.2-Estrategias.py -c <cant_tiradas> -n <corridas> -e <num_elegido> -s <estrategia(m/d/f/n)> -a <capital(i/a)>")
    sys.exit(1)

# Parámetros de la simulación
cant_tiradas = int(sys.argv[2])
cant_corridas = int(sys.argv[4])
num_elegido = int(sys.argv[6])
estrategia = (sys.argv[8])
capital = (sys.argv[10])

negro = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

# Parametros ingresados por la consola
initial_bet = int(input("Ingrese la apuesta inicial: "))
if capital == "a":
    initial_capital = int(input("Ingrese la capital inicial: "))
else:
    initial_capital = math.inf
    print(initial_capital)

if (estrategia) == "m":
    # Simulación de la estrategia de Martingala
    simulate_game(martingala_strategy, initial_bet,
                  cant_tiradas, cant_corridas, initial_capital, capital, "Martin Gala")
elif (estrategia) == "d":
    # Simulación de la estrategia de D'Alembert
    simulate_game(dalembert_strategy, initial_bet,
                  cant_tiradas, cant_corridas, initial_capital, capital, "D'Alembert")
elif (estrategia) == "f":
    # Simulación de la estrategia de Fibonacci
    simulate_game(fibonacci_strategy, initial_bet, cant_tiradas,
                  cant_corridas, initial_capital, capital, "Fibonacci")
else:
    print("else")
    simulate_game(propia_strategy, initial_bet,
                  cant_tiradas, cant_corridas, initial_capital, capital, "Nosotros")
