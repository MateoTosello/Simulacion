
import math
import random
import sys


def ruleta():
    valor = random.randint(0, 36)
    return valor


def fibonacci_strategy(initial_bet, cant_tiradas, initial_capital, capital):
    actual_capital = initial_capital
    actual_bet = initial_bet
    valores = [0, initial_bet, initial_bet]
    for i in range(cant_tiradas):
        print(i)
        print("Array: ", valores)
        if valores[1] <= actual_capital:
            valor = ruleta()
            if valor in negro:
                print("Gano")
                actual_capital += valores[1]
                if valores[0] == 0 or valores[0] == initial_bet:
                    valores = [0, initial_bet, initial_bet]
                else:
                    prevant = valores[0]
                    actant = valores[1]
                    act = actant-prevant
                    valores = [prevant-act, act, prevant]
            else:
                print("Perdio")
                actual_capital -= valores[1]
                actant = valores[1]
                posant = valores[2]
                valores = [actant, posant, actant+posant]

            print("Capital: ", actual_capital)
            # if valor in negro:
            #     # if previos_bet > actual_bet or previos_bet < 0 or actual_bet < 0:
            #     #     previos_bet = 0
            #     #     actual_bet = initial_bet
            #     print("gano")
            #     actual_capital += actual_bet
            #     print("previa bet antes: ", previos_bet)
            #     print("actual bet antes: ", actual_bet)
            #     actual_bet -= previos_bet
            #     previos_bet -= actual_bet
            #     print("previa bet: ", previos_bet)
            #     print("actual bet: ", actual_bet)
            #     print("actual capital: ", actual_capital)
            # else:
            # print("perdio")
            # actual_capital -= actual_bet
            # previos_bet = actual_bet
            # actual_bet += previos_bet
            # print("previa bet: ", previos_bet)
            # print("actual bet: ", actual_bet)
            # print("actual capital: ", actual_capital)
        else:
            print("Te quedaste seco")
            return


def simulate_game(strategy, initial_bet, cant_tiradas, cant_corridas, initial_capital, num_elegido, strategy_name):
    for i in range(cant_corridas):

        resultados = strategy(initial_bet, cant_tiradas,
                              initial_capital, num_elegido)


if len(sys.argv) != 11:
    print("Uso: python Tp1.2-Estrategias.py -c <cant_tiradas> -n <corridas> -e <num_elegido> -s <estrategia(m/d/f/o)> -a <capital(i/a)>")
    sys.exit(1)

# Parámetros de la simulación
cant_tiradas = int(sys.argv[2])
cant_corridas = int(sys.argv[4])
num_elegido = int(sys.argv[6])
estrategia = (sys.argv[8])
capital = (sys.argv[10])

negro = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

# Parametros ingresados por la consola

if capital == "a":
    initial_capital = int(input("Ingrese el capital inicial: "))
elif capital == "i":
    initial_capital = math.inf
    print("Capital infinito")

initial_bet = int(input("Ingrese la apuesta inicial: "))

# if (estrategia) == "m":
#     Simulación de la estrategia de Martingala
#     print("Estrategia: Martingala")
#     print()
#     simulate_game(martingala_strategy, initial_bet, cant_tiradas,
#                   cant_corridas, initial_capital, num_elegido, "Martingala")
# elif (estrategia) == "d":
#     Simulación de la estrategia de D'Alembert
#     print("Estrategia: D'Alembert")
#     print()
#     simulate_game(dalembert_strategy, initial_bet, cant_tiradas,
#                   cant_corridas, initial_capital, num_elegido, "D'Alembert")
if (estrategia) == "f":
    # Simulación de la estrategia de Fibonacci
    print("Estrategia: Fibonacci")
    print()
    simulate_game(fibonacci_strategy, initial_bet, cant_tiradas,
                  cant_corridas, initial_capital, num_elegido, "Fibonacci")
# elif (estrategia) == "o":
#     # Simulación de la estrategia de Paroli
#     print("Estrategia: Paroli")
#     print()
#     simulate_game(paroli_strategy, initial_bet, cant_tiradas,
#                   cant_corridas, initial_capital, num_elegido, "Paroli")
