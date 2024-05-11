import math
import random
import sys
import numpy as np
import matplotlib.pyplot as plt

#* DEFINICION DE FUNCIONES

# Ruleta
def ruleta():
    valor = random.randint(0, 36)
    return valor

# Parametros
def calcular_parametros(valor,valores,promPorTiradaArray, desvioPorTiradaArray, varPorTiradaArray,frecRelPorTiradaArray, num_elegido,i,frec_abs):
    #Promedio
    avg = np.mean(valores)
    promPorTiradaArray.append(avg)
    # Varianza
    var = np.var(valores)
    varPorTiradaArray.append(var)
    #Desvio
    std = np.std(valores)
    desvioPorTiradaArray.append(std)
    #FrecuenciaAbsoluta
    if valor == num_elegido:
        frec_abs +=1    
    #FrecuenciaRelativa
    frecRelPorTiradaArray.append(frec_abs/(i+1))

    avg = np.mean(valores)  #promedio
    std = np.std(valores)   #desvio
    var = np.var(valores)   #varianza
        
    # print("Valores: ", valores)
    # print("")
    # print("Frecuencia absoluta: ",frec_abs)
    # print("Promedio:","%.2f"%avg)
    # print("Desvio: ","%.2f"%std)
    # print("Varianza: ","%.2f"%var)
    # print("Frecuencia relativa: ","%.2f"%frec_abs/(i+1))
    # print("")
    # print("Promedios Array: ",promPorTiradaArray)
    # print("Desvios Array: ",desvioPorTiradaArray)
    # print("Varianza Array: ",varPorTiradaArray)
    # print("FrecuenciaRelativaArray: ",frecRelPorTiradaArray)

    return promPorTiradaArray, desvioPorTiradaArray, varPorTiradaArray, frecRelPorTiradaArray, avg, std, var

# Estrategias
def martingala_strategy(initial_bet, cant_tiradas, initial_capital, num_elegido):
    actual_capital = initial_capital
    actual_bet = initial_bet
    balance = 0
    
    valores = []
    frec_abs = 0
    promPorTiradaArray = []
    varPorTiradaArray = []
    desvioPorTiradaArray = []
    frecRelPorTiradaArray = []
    balancePorTiradaArray = []
    capitalPorTiradaArray = []
    
    for i in range(cant_tiradas):
        if actual_bet <= actual_capital:
            valor = ruleta()
            actual_capital -= actual_bet
            if valor == num_elegido:
                resultado = "Ganada"
                balance += ((actual_bet * 36) - actual_bet) #suma ganancia neta al balance
                
                actual_capital += actual_bet * 36
                actual_bet = initial_bet
                  
            else:
                resultado = "Perdida"
                balance -= actual_bet #resta perdida al balance
                
                actual_bet = actual_bet * 2
                
            print("Tirada nro: ",i+1)
            print("Resultado: ",resultado)
            print("Capital Actual: ",actual_capital)
            print("Balance Actual: ",balance)
            print("Apuesta Proxima tirada: ",actual_bet)
            print()
            
        else:
            print()
            print("Te quedaste seco")
            break

        valores.append(valor)
        parametros = calcular_parametros(valor,valores,promPorTiradaArray, desvioPorTiradaArray, varPorTiradaArray,frecRelPorTiradaArray,num_elegido,i,frec_abs)
        capitalPorTiradaArray.append(actual_capital)
        balancePorTiradaArray.append(balance)
        

    # if (i == cant_tiradas-1): i+=1
    # print("Luego de ",i," tiradas, el balance es: ",balance)
    return parametros, capitalPorTiradaArray, balancePorTiradaArray, valor, valores, frec_abs
    
def dalembert_strategy(initial_bet, cant_tiradas, initial_capital, num_elegido):

    actual_capital = initial_capital
    actual_bet = initial_bet
    unidadBase = 10
    
    for i in range(cant_tiradas):
        if actual_bet <= actual_capital:
            valor = ruleta()
            actual_capital -= actual_bet
            if valor == num_elegido:
                resultado = "Ganada"
                balance += ((actual_bet * 36) - actual_bet) #suma ganancia neta al balance
                
                actual_capital += actual_bet * 36
                # para que no llegue a apuesta=0 en caso de ganar
                if (actual_bet-unidadBase) < unidadBase:
                    actual_bet = unidadBase
                else:
                    actual_bet -= unidadBase
            else:
                resultado = "Perdida"
                balance -= actual_bet #resta perdida al balance
                
                actual_bet += unidadBase
                            
            # print("Tirada nro: ",i+1)
            # print("Resultado: ",resultado)
            # print("Capital Actual: ",actual_capital)
            # print("Balance Actual: ",balance)
            # print("Apuesta Proxima Tirada: ",actual_bet)
            # print()
        else:
            # print()
            print("Te quedaste seco")
            break
        
    # if (i == cant_tiradas-1): i=cant_tiradas
    # print("Luego de ",i," tiradas, el balance es: ",balance)    
    return

def fibonacci_strategy(initial_bet, cant_tiradas, initial_capital, num_elegido):
    actual_capital = initial_capital
    actual_bet = initial_bet
    previous_bet = 0
    
    for i in range(cant_tiradas):
        if actual_bet <= actual_capital:
            valor = ruleta()
            actual_capital -= actual_bet
            if valor == num_elegido:
                resultado = "Ganada"
                balance += ((actual_bet * 36) - actual_bet) #suma ganancia neta al balance
                
                actual_capital += actual_bet * 36
                actual_bet -= previous_bet
                previous_bet -= actual_bet
                
            else:
                resultado = "Perdida"
                balance -= actual_bet #resta perdida al balance
                
                aux = previous_bet
                previous_bet = actual_bet
                actual_bet += aux
            
            # print("Tirada nro: ",i+1)
            # print("Resultado: ",resultado)
            # print("Capital Actual: ",actual_capital)
            # print("Balance Actual: ",balance)
            # print("Apuesta Proxima tirada: ",actual_bet)
            # print()
        else:
            # print()
            print("Te quedaste seco")
            break
        
    # if (i == cant_tiradas-1): i=cant_tiradas
    # print("Luego de ",i," tiradas, el balance es: ",balance) 
    return

def paroli_strategy(initial_bet, cant_tiradas, initial_capital, num_elegido):
    actual_capital = initial_capital
    actual_bet = initial_bet
    balance = 0
    
    for i in range(cant_tiradas):
        if actual_bet <= actual_capital:
            valor = ruleta()
            actual_capital -= actual_bet
            if valor == num_elegido:
                resultado = "Ganada"
                balance += ((actual_bet * 36) - actual_bet) #suma ganancia neta al balance
                
                actual_capital += actual_bet * 36
                actual_bet =  actual_bet*2
    
            else:
                resultado = "Perdida"
                balance -= actual_bet #resta perdida al balance
                
                actual_bet = initial_bet                
                
            print("Tirada nro: ",i+1)
            print("Resultado: ",resultado)
            print("Capital Actual: ",actual_capital)
            print("Balance Actual: ",balance)
            print("Apuesta Proxima tirada: ",actual_bet)
            print()
            
        else:
            print()
            print("Te quedaste seco")
            break       

    # if (i == cant_tiradas-1): i=cant_tiradas
    # print("Luego de ",i," tiradas, el balance es: ",balance) 
    return


#*--------------------------------------------------------------------------------------------------------
#* DEFINICION DE FUNCIONES DE GRAFICAS

def grafica_promedio(promedio_esperado, promPorTiradaArray, i, strategy_name):
    
    acumulador_promedio = 0
    for p in range(37):
        acumulador_promedio += p
    promedio_esperado = acumulador_promedio / 37
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(promPorTiradaArray) + 1), promPorTiradaArray ,label='Promedio', color='blue')
    plt.axhline(promedio_esperado, color='red', linestyle='--', linewidth=2, label='Valor Teórico Esperado')
    plt.xlabel('Número de tirada')
    plt.ylabel('Valor obtenido')
    plt.title('Gráfico del promedio - Corrida '+str(i+1)+' - Tiradas: '+str(len(promPorTiradaArray))+' - Estrategia '+strategy_name)
    plt.legend()
    plt.grid(True)
    plt.xlim(1, len(promPorTiradaArray))
    plt.savefig('promedio_corrida_'+str(i+1)+'.png') # Guardar la figura en disco
    plt.show() # Mostrar la figura

def grafica_varianza(varianza_esperada, varPorTiradaArray, i, strategy_name):

    plt.plot(range(1, len(varPorTiradaArray) + 1), varPorTiradaArray, label='Varianza', color='blue')
    plt.axhline(varianza_esperada, color='red', linestyle='--', linewidth=2, label='Valor Teórico Esperado')
    plt.xlabel('Número de tirada')
    plt.ylabel('Valor obtenido')
    plt.title('Gráfico de la varianza - Corrida '+str(i+1)+' - Tiradas: '+str(len(varPorTiradaArray))+' - Estrategia '+strategy_name)
    plt.legend()
    plt.grid(True)
    plt.xlim(1, len(varPorTiradaArray))
    plt.savefig('varianza_corrida_'+str(i+1)+'.png') # Guardar la figura en disco
    plt.show() # Mostrar la figura

def grafica_desvio(desvio_esperado, desvioPorTiradaArray, i, strategy_name):
    
    plt.plot(range(1, len(desvioPorTiradaArray) + 1), desvioPorTiradaArray ,label='Desvio', color='blue')
    plt.axhline(desvio_esperado, color='red', linestyle='--', linewidth=2, label='Valor Teórico Esperado')
    plt.xlabel('Número de tirada')
    plt.ylabel('Valor obtenido')
    plt.title('Gráfico del desvio - Corrida '+str(i+1)+' - Tiradas: '+str(len(desvioPorTiradaArray))+' - Estrategia '+strategy_name)
    plt.legend()
    plt.grid(True)
    plt.xlim(1, len(desvioPorTiradaArray))
    plt.savefig('desvio_corrida_'+str(i+1)+'.png') # Guardar la figura en disco
    plt.show() # Mostrar la figura

def grafica_frec_rel(frecRelPorTiradaArray, i, num_elegido, strategy_name):
    frec_rel_esperada = 1/37
    plt.plot(range(1, len(frecRelPorTiradaArray) + 1), frecRelPorTiradaArray ,label='Frecuencia Relativa', color='blue')
    plt.axhline(frec_rel_esperada, color='red', linestyle='--', linewidth=2, label='Valor Teórico Esperado')
    plt.xlabel('Número de tirada')
    plt.ylabel('Valor obtenido')
    plt.title('Gráfico de frecuencia relativa del nro ' +str(num_elegido)+' - Corrida '+str(i+1)+' - Tiradas: '+str(len(frecRelPorTiradaArray))+' - Estrategia '+strategy_name)
    plt.legend()
    plt.grid(True)
    plt.xlim(1, len(frecRelPorTiradaArray))
    plt.savefig('frec_rel_corrida_'+str(i+1)+'.png') # Guardar la figura en disco
    plt.show() # Mostrar la figura

def grafica_frec_abs(valores, i, num_elegido, strategy_name):
    
    frec_abs_esperada = len(valores) / 37

    plt.figure(figsize=(8, 6))
    plt.hist(valores, bins=range(38), color='green', edgecolor='black', alpha=0.7, align='mid')
    plt.axhline(frec_abs_esperada, color='red', linestyle='--', linewidth=2, label='Valor Teórico Esperado')
    plt.xlabel('Resultado')
    plt.ylabel('Frecuencia Absoluta')
    plt.title('Histograma lanzamiento de ruleta al número ' + str(num_elegido)+ ' - Corrida ' + str(i+1)+ ' - Tiradas: ' + str(len(valores))+' - Estrategia '+strategy_name)
    plt.xticks([x + 0.5 for x in range(37)], [str(x) for x in range(37)])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.savefig('frec_abs_corrida_'+str(i+1)+'.png') 
    plt.show()

def grafica_capital(capitalPorTiradaArray, initial_capital, i, strategy_name):
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(capitalPorTiradaArray) + 1), capitalPorTiradaArray, label='Flujo de capital', color='blue')
    plt.axhline(initial_capital, color='red', linestyle='--', linewidth=2, label='Capital inicial')
    plt.xlabel('Número de tirada')
    plt.ylabel('Cantidad de capital')
    plt.title('Gráfico del capital - Corrida '+str(i+1)+' - Tiradas: '+str(len(capitalPorTiradaArray))+' - Estrategia '+strategy_name)
    plt.legend()
    plt.grid(True)
    plt.xlim(1, len(capitalPorTiradaArray))  # Límites del eje x de tirada 1 a la 10
    plt.savefig('capital_corrida_'+str(i+1)+'.png') # Guardar la figura en disco
    plt.show() # Mostrar la figura
    
def grafica_balance(balancePorTiradaArray, i, strategy_name):
        
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(balancePorTiradaArray) + 1), balancePorTiradaArray, label='Flujo de ganancia', color='blue')
    plt.axhline(0, color='red', linestyle='--', linewidth=2, label='Balance cero')
    plt.xlabel('Número de tirada')
    plt.ylabel('Cantidad de ganancia')
    plt.title('Gráfico de ganancia neta - Corrida '+str(i+1)+' - Tiradas: '+str(len(balancePorTiradaArray))+' - Estrategia '+strategy_name)
    plt.legend()
    plt.grid(True)
    plt.xlim(1, len(balancePorTiradaArray))  # Límites del eje x de tirada 1 a la 10
    plt.savefig('balance_corrida_'+str(i+1)+'.png') # Guardar la figura en disco
    plt.show() # Mostrar la figura
    
#*--------------------------------------------------------------------------------------------------------
#* SIMULACION DEL JUEGO

def simulate_game(strategy, initial_bet, cant_tiradas, cant_corridas, initial_capital, num_elegido, strategy_name):
    for i in range(cant_corridas):
       
        resultados = strategy(initial_bet, cant_tiradas, initial_capital, num_elegido)
        
        promPorTiradaArray=(resultados[0])[0]
        desvioPorTiradaArray=(resultados[0])[1]
        varPorTiradaArray=(resultados[0])[2]
        frecRelPorTiradaArray=(resultados[0])[3]
        avg=(resultados[0])[4] #no se usa
        std=(resultados[0])[5] #no se usa
        var=(resultados[0])[6] #no se usa
        capitalPorTiradaArray=resultados[1]
        balancePorTiradaArray=resultados[2]
        valor=resultados[3] #no se usa
        valores=resultados[4]
        
    # graficas
        acumulador_promedio = 0
        for n in range(37):
            acumulador_promedio += n
        promedio_esperado = acumulador_promedio / 37
        
        acumulador_varianza = 0
        for m in range(37):
            acumulador_varianza += pow((m-promedio_esperado),2)
        varianza_esperada = acumulador_varianza / 37
    
        desvio_esperado = math.sqrt(varianza_esperada)
    
        grafica_promedio(promedio_esperado,promPorTiradaArray,i, strategy_name)
        grafica_varianza(varianza_esperada,varPorTiradaArray,i, strategy_name)
        grafica_desvio(desvio_esperado,desvioPorTiradaArray,i, strategy_name)
        grafica_frec_rel(frecRelPorTiradaArray,i,num_elegido, strategy_name)
        grafica_frec_abs(valores,i,num_elegido, strategy_name)
        grafica_capital(capitalPorTiradaArray, initial_capital, i, strategy_name)
        grafica_balance(balancePorTiradaArray,i, strategy_name)
        


#*--------------------------------------------------------------------------------------------------------
#* INICIO DEL PROGRAMA

if len(sys.argv) != 11:
    print("Uso: python Tp1.2-Estrategias.py -c <cant_tiradas> -n <corridas> -e <num_elegido> -s <estrategia(m/d/f/o)> -a <capital(i/a)>")
    sys.exit(1)

# Parámetros de la simulación
cant_tiradas = int(sys.argv[2])
cant_corridas = int(sys.argv[4])
num_elegido = int(sys.argv[6])
estrategia = (sys.argv[8])
capital = (sys.argv[10])


# Parametros ingresados por la consola

if capital == "a":
    initial_capital = int(input("Ingrese el capital inicial: "))
elif capital == "i":
    initial_capital = math.inf
    print("Capital infinito")

initial_bet = int(input("Ingrese la apuesta inicial: "))

if (estrategia) == "m":
    # Simulación de la estrategia de Martingala
    print("Estrategia: Martingala")
    print()
    simulate_game(martingala_strategy, initial_bet, cant_tiradas, cant_corridas, initial_capital, num_elegido,"Martingala")
elif (estrategia)== "d":
    # Simulación de la estrategia de D'Alembert
    print("Estrategia: D'Alembert")
    print()
    simulate_game(dalembert_strategy, initial_bet, cant_tiradas, cant_corridas, initial_capital, num_elegido, "D'Alembert")
elif (estrategia) == "f":
    # Simulación de la estrategia de Fibonacci
    print("Estrategia: Fibonacci")
    print()
    simulate_game(fibonacci_strategy, initial_bet, cant_tiradas, cant_corridas, initial_capital, num_elegido, "Fibonacci")
elif (estrategia) == "o":
    # Simulación de la estrategia de Paroli
    print("Estrategia: Paroli")
    print()
    simulate_game(paroli_strategy, initial_bet, cant_tiradas, cant_corridas, initial_capital, num_elegido, "Paroli")


