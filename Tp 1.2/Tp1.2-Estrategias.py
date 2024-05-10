import math
import random
import sys
import numpy as np
import matplotlib.pyplot as plt

# Ruleta


def ruleta():
    valor = random.randint(0, 36)
    return valor


# Estrategias


def martingala_strategy(initial_bet, cant_tiradas, initial_capital, num_elegido):
    actual_capital = initial_capital
    actual_bet = initial_bet
    for i in range(cant_tiradas):
        if actual_bet <= actual_capital:
            valor = ruleta()
            actual_capital -= actual_bet
            if valor == num_elegido:
                actual_capital += actual_bet * 36
                actual_bet = initial_bet
            else:
                actual_bet = actual_bet * 2
        else:
            print("Te quedaste seco")
            return

            # # Final de la funcion
            # return actual_capital


def dalembert_strategy(initial_bet, cant_tiradas, initial_capital, num_elegido):

    actual_capital = initial_capital
    actual_bet = initial_bet
    unidadBase = 10

    for i in range(cant_tiradas):
        if actual_bet <= actual_capital:
            valor = ruleta()
            actual_capital -= actual_bet
            if valor == num_elegido:
                actual_capital += actual_bet * 36
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


def fibonacci_strategy(initial_bet, cant_tiradas, initial_capital, num_elegido):
    actual_capital = initial_capital
    actual_bet = initial_bet
    previos_bet = 0

    for i in range(cant_tiradas):
        if actual_bet <= actual_capital:
            valor = ruleta()
            actual_capital -= actual_bet
            if valor == num_elegido:
                actual_capital += actual_bet * 36
                actual_bet -= previos_bet
                previos_bet -= actual_bet
            else:
                aux = previos_bet
                previos_bet = actual_bet
                actual_bet += aux
        else:
            print("Te quedaste seco")
            return

        # Final de la funcion
        # return actual_capital


def propia_strategy(initial_bet, cant_tiradas, initial_capital, num_elegido):
    actual_capital = initial_capital
    for i in range(cant_tiradas):
        print("Estrategia propia")

        # Final de la funcion
        return actual_capital


def simulate_game(strategy, initial_bet, cant_tiradas, cant_corridas, initial_capital, num_elegido):
    for i in range(cant_corridas):
        strategy(initial_bet, cant_tiradas, initial_capital, num_elegido)


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

print(estrategia)

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
                  cant_tiradas, cant_corridas, initial_capital, num_elegido)
elif (estrategia).lower == "d":
    # Simulación de la estrategia de D'Alembert
    simulate_game(dalembert_strategy, initial_bet,
                  cant_tiradas, cant_corridas, initial_capital, num_elegido)
elif (estrategia).lower == "f":
    # Simulación de la estrategia de Fibonacci
    simulate_game(fibonacci_strategy, initial_bet,
                  cant_tiradas, cant_corridas, initial_capital, num_elegido)
else:
    print("else")
    simulate_game(propia_strategy, initial_bet,
                  cant_tiradas, cant_corridas, initial_capital, num_elegido)
