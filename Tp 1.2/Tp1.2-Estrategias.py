import math
import random
import sys
import numpy as np
import matplotlib.pyplot as plt

# Ruleta

def ruleta():
    valor = random.randint(0, 36)
    return valor

# Gráfica


def grafica_balance(balanceArray, i, strategy_name):

    plt.figure(figsize=(10, 6))
    plt.plot(range(0, len(balanceArray)),
             balanceArray, label='Flujo de ganancia', color='blue')
    if balanceArray[0] == 0:
        plt.title('Gráfico de ganancia neta - Corrida ' + str(i+1) + ' - Tiradas: ' +
              str(len(balanceArray)-1)+' - Estrategia ' + strategy_name)
        plt.axhline(balanceArray[0], color='red', linestyle='--',linewidth=2, label='Balance cero')
        plt.axhline(balanceArray[-1], color='green', linestyle=':',linewidth=2, label='Balance final')
    else:
        plt.title('Gráfico de flujo de capital - Corrida ' + str(i+1) + ' - Tiradas: ' +
              str(len(balanceArray)-1)+' - Estrategia ' + strategy_name)
        plt.axhline(balanceArray[0], color='red', linestyle='--',linewidth=2, label='Capital inicial')
        plt.axhline(balanceArray[-1], color='green', linestyle=':',linewidth=2, label='Capital final')
    
    plt.xlabel('Número de tirada')
    plt.ylabel('Cantidad de ganancia')

    plt.legend()
    plt.grid(True)
    # Límites del eje x de tirada 1 a la 10
    plt.xlim(0, len(balanceArray))
    # Guardar la figura en disco
    plt.savefig('balance_corrida_'+str(i+1)+'.png')
    plt.show()  # Mostrar la figura


def grafica_resumen_balances(balancesArray, i, strategy_name):

    plt.figure(figsize=(10, 6))
    nro_tiradas_eje_x = [x for x in range(cant_tiradas+1)]
    cant_max_tiradas = len(balancesArray[0])
    for i in range(len(balancesArray)):
        if cant_max_tiradas < len(balancesArray[i]):
            cant_max_tiradas = len(balancesArray[i])
        plt.plot(nro_tiradas_eje_x[:len(balancesArray[i])],
                 balancesArray[i], label='Flujo de ganancia', color='blue')
    plt.axhline(0, color='red', linestyle='--',
                linewidth=2, label='Balance cero')
    plt.xlabel('Número de tirada')
    plt.ylabel('Cantidad de ganancia')
    plt.title('Gráfico de ganancia neta - Corrida ' + str(i+1) + ' - Tiradas: ' +
              str(len(balancesArray))+' - Estrategia ' + strategy_name)
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
            print("tirada: ", (i+1))
            print("bet: ", betArray[i])
            print("capital: ", balanceArray[i])
            valor = ruleta()
            if valor in negro:
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

    return balanceArray, betArray


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
            if valor in negro:
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
            if valor in negro:
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
            if valor in negro:
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


def simulate_game(strategy, initial_bet, cant_tiradas, cant_corridas, initial_capital, capital, strategy_name):
    balancesArray = []
    for i in range(cant_corridas):
        resultados = strategy(initial_bet, cant_tiradas,
                              initial_capital, capital)

        balanceArray = resultados[0]
        betArray = resultados[1]

        balancesArray.apprend(balanceArray)

        grafica_balance(balanceArray, i, strategy_name)
        grafica_resumen_balances(balancesArray, i, strategy_name)


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

if capital == "a":
    initial_capital = int(input("Ingrese el capital inicial: "))
else:
    initial_capital = math.inf
    print(initial_capital)
initial_bet = int(input("Ingrese la apuesta inicial: "))

if (estrategia) == "m":
    # Simulación de la estrategia de Martingala
    simulate_game(martingala_strategy, initial_bet, cant_tiradas, cant_corridas, initial_capital, capital, "Martin Gala")
elif (estrategia) == "d":
    # Simulación de la estrategia de D'Alembert
    simulate_game(dalembert_strategy, initial_bet, cant_tiradas, cant_corridas, initial_capital, capital, "D'Alembert")
elif (estrategia) == "f":
    # Simulación de la estrategia de Fibonacci
<<<<<<< HEAD
    simulate_game(fibonacci_strategy, initial_bet, cant_tiradas,
                  cant_corridas, initial_capital, capital, "Fibonacci")
else:
    print("else")
    simulate_game(paroli_strategy, initial_bet,
                  cant_tiradas, cant_corridas, initial_capital, capital, "Nosotros")
=======
    simulate_game(fibonacci_strategy, initial_bet, cant_tiradas, cant_corridas, initial_capital, capital, "Fibonacci")
elif (estrategia) == "o":
    simulate_game(paroli_strategy, initial_bet, cant_tiradas, cant_corridas, initial_capital, capital, "Nosotros")
>>>>>>> 2b5261c4bf57be7e141a8cf3c0b58866d72d0a03
