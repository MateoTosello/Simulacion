import random
import sys
import numpy as np
import matplotlib.pyplot as plt
import math

if len(sys.argv) != 7:
    print("Uso: python roulette.py -c <cant_tiradas> -n <corridas> -e <num_elegido>")
    sys.exit(1) 

# numeros = list(range(0,37))
cant_tiradas = int(sys.argv[2])
cant_corridas = int(sys.argv[4])
num_elegido = int(sys.argv[6])

for i in range(cant_corridas):
    frec_abs = 0
    acumulador_promedio = 0
    acumulador_varianza = 0
    valores = []
    promPorTiradaArray = []
    varPorTiradaArray = []
    desvioPorTiradaArray = []
    frecRelPorTiradaArray = []



    for j in range (cant_tiradas):
        valor = random.randint(0,36)
        valores.append(valor)
        # acum = acum + valor
        # promPorTirada = (acum / (j+1))
        # promPorTiradaArray.append(promPorTirada)

        #Promedio
        avg = np.mean(valores)
        promPorTiradaArray.append(avg)

        # Varinza
        var = np.var(valores)
        varPorTiradaArray.append(var)


        #Desvio
        std = np.std(valores)
        desvioPorTiradaArray.append(std)


        if valor == num_elegido:
            frec_abs +=1    

        #FrecuenciaRelativa
        frecRelPorTiradaArray.append(frec_abs/(j+1))

    for n in range(37):
        acumulador_promedio += n
    promedio_esperado = acumulador_promedio / 37

    avg = np.mean(valores)  #promedio
    std = np.std(valores)   #desvio
    var = np.var(valores)   #varianza
        
    
    # print("Valores: ", valores)
    print("Frecuencia absoluta corrida ",i,": ",frec_abs)
    print("Frecuencia relativa corrida ",i,": ",frec_abs/cant_tiradas)
    print("Promedio: ",avg)
    print("Desvio: ",std)
    print("Varianza: ",var)
    print("")

    # Crear la figura y los subgráficos
    fig, axs = plt.subplots(2, 2, figsize=(15, 9))  
    

    #Promedio
    axs[0,0].plot(promPorTiradaArray ,label='Promedio', color='blue')
    axs[0,0].axhline(promedio_esperado, color='red', linestyle='--', linewidth=2, 
    label='Valor Teórico Esperado')
    axs[0,0].set_xlabel('Número de tirada')
    axs[0,0].set_ylabel('Valor obtenido')
    axs[0,0].set_title('Gráfico del promedio del numero ' + str(num_elegido))
    axs[0,0].legend()
    axs[0,0].grid(True)

    #Frecuencia relativa
    frec_rel_esperada = 1/37
    axs[1,0].plot(range(1,cant_tiradas+1),frecRelPorTiradaArray ,label='Frecuencia Relativa', color='blue')
    axs[1,0].axhline(frec_rel_esperada, color='red', linestyle='--', linewidth=2, 
    label='Valor Teórico Esperado')
    axs[1,0].set_xlabel('Número de tirada')
    axs[1,0].set_ylabel('Valor obtenido')
    axs[1,0].set_title('Gráfico de frecuencia relativa del numero ' + str(num_elegido))
    axs[1,0].legend()
    axs[1,0].grid(True)

    #Varianza
    for m in range(37):
        acumulador_varianza += pow((m-promedio_esperado),2)
    varianza_esperada = acumulador_varianza / 37

    axs[0,1].plot(range(1,cant_tiradas+1),varPorTiradaArray ,label='Varianza', color='blue')
    axs[0,1].axhline(varianza_esperada, color='red', linestyle='--', linewidth=2, 
    label='Valor Teórico Esperado')
    axs[0,1].set_xlabel('Número de tirada')
    axs[0,1].set_ylabel('Valor obtenido')
    axs[0,1].set_title('Gráfico de la varianza del numero ' + str(num_elegido))
    axs[0,1].legend()
    axs[0,1].grid(True)


    #Desvio
    desvio_esperado = math.sqrt(varianza_esperada)
    axs[1,1].plot(range(1,cant_tiradas+1),desvioPorTiradaArray ,label='Desvio', color='blue')
    axs[1,1].axhline(desvio_esperado, color='red', linestyle='--', linewidth=2, 
    label='Valor Teórico Esperado')
    axs[1,1].set_xlabel('Número de tirada')
    axs[1,1].set_ylabel('Valor obtenido')
    axs[1,1].set_title('Gráfico del desvio del numero ' + str(num_elegido))
    axs[1,1].legend()
    axs[1,1].grid(True)

    # print(frec_rel_esperada, promedio_esperado, varianza_esperada, desvio_esperado)

    # Ajustar diseño y mostrar gráficos
    plt.tight_layout()

    # Guardar la figura en disco
    plt.savefig('graficas_corrida_nro_'+str(i+1)+'.png')

    # Mostrar la figura
    plt.show()
    
