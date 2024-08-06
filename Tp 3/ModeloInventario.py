#En este documento realizaremos la simulación de un modelo de inventario
import os
import random
import array as arr
import sys
import matplotlib.pyplot as plt

#---------------------------------------------------------------------------------------------------------------- 
### Inicializacion
def initialize():
    global tiempo_simulacion, nivel_inventario, tiempo_ultimo_evento, costo_total_ordenes
    global area_mantenimiento, area_faltante, tiempo_sig_evento

    # Inicializar el reloj de simulación
    tiempo_simulacion = 0.0

    # Inicializar las variables de estado
    nivel_inventario = nivel_inicial_inventario
    tiempo_ultimo_evento = 0.0

    # Inicializar los contadores estadísticos
    costo_total_ordenes = 0.0 
    area_mantenimiento = 0.0
    area_faltante = 0.0

    # Inicializar la lista de eventos
    # Dado que no hay ningún pedido pendiente, se elimina el evento de llegada del pedido de la consideración
    tiempo_sig_evento = [0.0] * (cant_eventos + 1)
    tiempo_sig_evento[1] = 1.0e+30
    tiempo_sig_evento[2] = tiempo_simulacion + random.expovariate(media_entre_pedidos_de_clientes)
    tiempo_sig_evento[3] = num_meses
    tiempo_sig_evento[4] = 0.0

#---------------------------------------------------------------------------------------------------------------- 
### Timing
def timing():
    global tiempo_simulacion, tipo_sig_evento
    global tiempo_sig_evento
    min_tiempo_proximo_evento = 1.0e+29
    tipo_sig_evento = 0

    for i in range(1, cant_eventos + 1):
        if(tiempo_sig_evento[i] < min_tiempo_proximo_evento):
            min_tiempo_proximo_evento = tiempo_sig_evento[i]
            tipo_sig_evento = i

    if(tipo_sig_evento == 0):
        txt.write("\nLista de Eventos vacia en tiempo"+str(tiempo_simulacion))
        sys.exit(1)
    
    tiempo_simulacion = min_tiempo_proximo_evento

#---------------------------------------------------------------------------------------------------------------- 
### Actualizar tiempo, avg, estadisticas
def actualizacion_tiempo_promedio_estadisticas():
    global tiempo_simulacion, tiempo_ultimo_evento, nivel_inventario
    global area_faltante, area_mantenimiento

    # Calcular el tiempo transcurrido desde el último evento y actualizar el marcador de tiempo del último evento
    tiempo_desde_ultimo_evento = tiempo_simulacion - tiempo_ultimo_evento
    tiempo_ultimo_evento = tiempo_simulacion

    # Determinar el estado del nivel de inventario durante el intervalo anterior
    if nivel_inventario < 0:
        # Si el nivel de inventario durante el intervalo anterior era negativo, actualizar area_shortage
        area_faltante -= nivel_inventario * tiempo_desde_ultimo_evento
    elif nivel_inventario > 0:
        # Si el nivel de inventario durante el intervalo anterior era positivo, actualizar area_holding
        area_mantenimiento += nivel_inventario * tiempo_desde_ultimo_evento

#---------------------------------------------------------------------------------------------------------------- 
### Llegada de un pedido
def arrivo_orden():
    global cantidad_pedida_proveedor, nivel_inventario, tiempo_sig_evento

    # Incrementar el nivel de inventario por la cantidad pedida
    nivel_inventario += cantidad_pedida_proveedor

    # Dado que no hay ningún pedido pendiente, eliminar el evento de llegada del pedido de la consideración
    tiempo_sig_evento[1] = 1.0e+30

#---------------------------------------------------------------------------------------------------------------- 
### Funcion de evento de una demanda
def demanda():
    global nivel_inventario, tiempo_sig_evento, tiempo_simulacion, media_entre_pedidos_de_clientes, cantidad_pedidos_totales

    # Decrementar el nivel de inventario por un tamaño de demanda generado
    pedido = random_integer(prob_dist_demanda)
    nivel_inventario -= pedido
    cantidad_pedidos_totales += 1 

    # Programar el tiempo de la próxima demanda
    tiempo_sig_evento[2] = tiempo_simulacion + random.expovariate(media_entre_pedidos_de_clientes)

#----------------------------------------------------------------------------------------------------------------    
### Funcion de evaluacion de inventario
def evaluacion():
    global nivel_inventario, smalls, bigs, cantidad_pedida_proveedor, costo_total_ordenes
    global costo_setup, costo_incremental, tiempo_sig_evento, tiempo_simulacion

    # Verificar si el nivel de inventario es menor que smalls
    if nivel_inventario < smalls:
        # El nivel de inventario es menor que smalls, así que hacer un pedido por la cantidad adecuada
        cantidad_pedida_proveedor = bigs - nivel_inventario
        costo_total_ordenes += costo_setup + costo_incremental * cantidad_pedida_proveedor
        
        # Programar la llegada del pedido
        tiempo_sig_evento[1] = tiempo_simulacion + random.uniform(minimo_lag, maximo_lag)
    
    # Independientemente de la decisión de realizar un pedido, programar la próxima evaluación de inventario
    tiempo_sig_evento[4] = tiempo_simulacion + 1.0

#---------------------------------------------------------------------------------------------------------------- 
### Reporte
def reporte(i):
    global costo_total_ordenes, num_meses, costo_mantenimiento, area_mantenimiento #Que es el area de mantenimiento?
    global costo_faltante, area_faltante, smalls, bigs #Que es el area de faltante


    # Calcular y escribir estimaciones de las medidas de rendimiento deseadas
    costo_prom_ordenes = costo_total_ordenes / num_meses
    costo_prom_mantenimiento = costo_mantenimiento * area_mantenimiento / num_meses
    costo_prom_faltante = costo_faltante * area_faltante / num_meses

    txt.write("\nMaximo inventario: " + str(bigs) + "\n")
    txt.write("\nMinimo inventario: " + str(smalls) + "\n")
    txt.write("\nCorrida numero: "+str(i)+"\n")
    txt.write("\nCosto total promedio: " + str(costo_prom_faltante + costo_prom_mantenimiento + costo_prom_ordenes) + "\n")
    txt.write("\nCosto promedio de pedido: " + str(costo_prom_ordenes) + "\n")
    txt.write("\nCosto promedio de mantenimiento: " + str(costo_prom_mantenimiento) + "\n")
    txt.write("\nCosto promedio de faltante: " + str(costo_prom_faltante) + "\n")
    txt.write("---------------------------------------------------------------------------")

#---------------------------------------------------------------------------------------------------------------- 
### Determinar el tamaño de la demanda
def random_integer(prob_distrib):
    # Generar una variable aleatoria U(0,1)
    u = random.random()
    
    # Devolver un número entero aleatorio de acuerdo con la función de distribución (acumulativa) prob_distrib
    for i, prob in enumerate(prob_distrib):
        if u < prob:
            return i + 1
    return len(prob_distrib)


#---------------------------------------------------------------------------------------------------------------- 
### Ejecución del programa
if len(sys.argv) != 25:
    print("Uso: python ModeloInventario.py -a <nivel inicial de inventario> -b <meses de la simulacion> -c <cantidad diferente de politicas> -d <tamaño de pedido maximo de productos por parte del cliente> -e <media de tiempo entre ventas> -f <costo setup> -g <costo incremental> -h <costo de mantenimiento> -i  <costo por producto faltante> -j <minimo lag(minimo en la dist U del tiempo del siguiente evento)> -k <maximo lag (maximo en la dist U del tiempo del siguiente evento)> -l <numero de corridas por politica>")
    sys.exit(1) 

nivel_inicial_inventario = int(sys.argv[2]) #inventario con el que se arranca la simulacion
num_meses = int(sys.argv[4])                #tiempo de simulacion
num_politicas = int(sys.argv[6])            #cantidad de politicas que quiero evaluar (rangos de minimo y maximo de stock)
val_demanda = int(sys.argv[8])              #tamaño de pedido maximo de productos por parte del cliente - trabajamos con 4
media_entre_pedidos_de_clientes = float(sys.argv[10]) # media entre la llegada de dos clientes, media = 0.1 => lambda = 1/0.1 = 10 para la distribucion exponencial
costo_setup = float(sys.argv[12])           #costo base del pedido                                                              K  = 32
costo_incremental = float(sys.argv[14])     #costo agregado por cada item del pedido                                            i  = 3
costo_mantenimiento = float(sys.argv[16])   #costo de mantenimiento de los productos en stock                                   h  = 1
costo_faltante = float(sys.argv[18])        #costo en caso de no tener stock (por cada posibilidad de venta sin concretarse)    pi = 5
minimo_lag = float(sys.argv[20])
maximo_lag = float(sys.argv[22])
num_corridas = int(sys.argv[24])

bigs, smalls, tiempo_sig_evento, cantidad_pedida_proveedor, tipo_sig_evento = 0,0,0,0,0
prob_dist_demanda = [0.166, 0.5, 0.833, 1]
cant_eventos = 4 # Hace referencia a los 4 eventos posibles (demanda, evaluacion de pedido, arribo de pedido)
val_demanda = 4 #tamaño de pedido maximo de productos por parte del cliente -> hardcodeado pero tambien lo pusimos para ingresar
tiempo_proximo_evento = [0.0]*5
area_mantenimiento, area_faltante, tiempo_simulacion, costo_total_ordenes, tiempo_ultimo_evento = 0.0, 0.0, 0.0, 0.0, 0.0

print("Sistema de inventario de un único producto")
print(f"Nivel de inventario inicial: {nivel_inicial_inventario} items")
print(f"Tamaño máximo de prod pedidos por un cliente: {val_demanda}")  # por regla de negocio se pueden pedir hata 4 productos (ejemplo del libro)
print(f"Distribución de probabilidad del tamaño de los pedidos de los clientes: {prob_dist_demanda}")
print(f"Media de tiempo entre pedidos: {media_entre_pedidos_de_clientes:.2f}")
print(f"Rango de demora para la entrega de un pedido por parte del proveedor: {minimo_lag:.2f} to {maximo_lag:.2f} months")
print(f"Tiempo de la simulacion: {num_meses} meses")
print(f"K = {costo_setup:6.1f}, i = {costo_incremental:6.1f}, h = {costo_mantenimiento:6.1f}, pi = {costo_faltante:6.1f}")
print(f"Cantidad de politicas (diferentes maximos y minimos de stock a evaluar): {num_politicas}")
print("--------------------------------------------------------------------------------------------------------------------------")

txt = open("report.txt","w")

# Escritura inicial de los parametros en el reporte
txt.write("Sistema de inventario de un único producto\n")
txt.write(f"Nivel de inventario inicial: {nivel_inicial_inventario} items\n")
txt.write(f"Tamaño maximo de prod pedidos por un cliente: {val_demanda}\n")  #por regla de negocio se pueden pedir hata 4 productos (ejemplo del libro)
txt.write(f"Distribucion de probabilidad del tamaño de los pedidos de los clientes: {prob_dist_demanda}\n")
txt.write(f"Media de tiempo entre pedidos: {media_entre_pedidos_de_clientes:.2f}\n")
txt.write(f"Rango de demora para la entrega de un pedido por parte del proveedor: {minimo_lag:.2f} to {maximo_lag:.2f} months\n")
txt.write(f"Tiempo de la simulacion: {num_meses} meses\n")
txt.write(f"K = {costo_setup:6.1f}, i = {costo_incremental:6.1f}, h = {costo_mantenimiento:6.1f}, pi = {costo_faltante:6.1f}\n")
txt.write(f"Cantidad de politicas (diferentes maximos y minimos de stock a evaluar): {num_politicas}\n\n")
txt.write("--------------------------------------------------------------------------------------------------------------------------")




# Ejecutar la simulación variando la política de inventario
for _ in range(num_politicas):
    print("Ingrese el valor de smalls:")
    smalls = int(input())
    print("Ingrese el valor de bigs:")
    bigs = int(input())

    print(bigs,smalls)

    for i in range(num_corridas):
        print("Corrida: ", i)
        initialize()
        array_nivel_inventario_1_mes = []
        array_nivel_inventario_6_meses = []
        array_nivel_inventario_12_meses = []
        array_nivel_inventario_12_60 = []
        array_nivel_inventario_60_120 = []
        array_tiempo_simulacion_1_mes = []
        array_tiempo_simulacion_6_meses = []
        array_tiempo_simulacion_12_meses = []
        array_tiempo_simulacion_12_60_meses = []
        array_tiempo_simulacion_60_120_meses = []

        cantidad_pedidos_totales = 0
        cont_60, cont_120 = 0,0

        # Ejecutar la simulación hasta que ocurra un evento de fin de simulación (tipo 3)
        while True:
            # Determinar el próximo evento
            timing()
            # Actualizar los acumuladores estadísticos de tiempo promedio
            actualizacion_tiempo_promedio_estadisticas()
            # Invocar la función de evento correspondiente
            if (tipo_sig_evento == 1):
                arrivo_orden()
            elif tipo_sig_evento == 2:
                demanda()
            elif tipo_sig_evento == 4:
                evaluacion()
            elif tipo_sig_evento == 3:
                reporte(i)
                break  # Salir del bucle si es el evento de fin de simulación

            #Aca tengo que hacer las cosas de las graficas 
            if tiempo_simulacion <= 1:
                array_tiempo_simulacion_1_mes.append(tiempo_simulacion)
                array_nivel_inventario_1_mes.append(nivel_inventario)
            if (tiempo_simulacion <= 6):    
                array_tiempo_simulacion_6_meses.append(tiempo_simulacion)
                array_nivel_inventario_6_meses.append(nivel_inventario)
            if (tiempo_simulacion <= 12):
                array_tiempo_simulacion_12_meses.append(tiempo_simulacion)
                array_nivel_inventario_12_meses.append(nivel_inventario)
            elif (tiempo_simulacion > 12 and tiempo_simulacion <= 60 ):
                array_tiempo_simulacion_12_60_meses.append(tiempo_simulacion)
                array_nivel_inventario_12_60.append(nivel_inventario)
            else:
                array_tiempo_simulacion_60_120_meses.append(tiempo_simulacion)
                array_nivel_inventario_60_120.append(nivel_inventario)

            if(tipo_sig_evento == 3):
                break

        # Crear un directorio para guardar las imágenes
        if not os.path.exists("Graficas/politica_"+str(smalls)+", "+str(bigs)+"corrida_"+str(i)):
            os.makedirs("Graficas/politica_"+str(smalls)+", "+str(bigs)+"corrida_"+str(i))

        plt.step(array_tiempo_simulacion_1_mes, array_nivel_inventario_1_mes, where='post')
        plt.title("Grafica de un mes de simulación")
        plt.axhline(smalls, color='red', linestyle='--', linewidth=2, label='Minimo')
        plt.axhline(bigs, color='green', linestyle='--', linewidth=2, label='Maximo')
        plt.xlabel('Tiempo')
        plt.ylabel('Nivel de Inventario')
        plt.savefig("Graficas/politica_"+str(smalls)+", "+str(bigs)+"corrida_"+str(i)+"/1_inventario_politica_"+str(smalls)+", "+str(bigs)+"_mes_1_corrida_"+str(i)+".jpg")
        plt.clf()

        plt.step(array_tiempo_simulacion_6_meses, array_nivel_inventario_6_meses, where='post')
        plt.title("Grafica de 6 meses de simulación")
        plt.axhline(smalls, color='red', linestyle='--', linewidth=2, label='Minimo')
        plt.axhline(bigs, color='green', linestyle='--', linewidth=2, label='Maximo')
        plt.xlabel('Tiempo')
        plt.ylabel('Nivel de Inventario')
        plt.savefig("Graficas/politica_"+str(smalls)+", "+str(bigs)+"corrida_"+str(i)+"/2_inventario_politica_"+str(smalls)+", "+str(bigs)+"_primeros_6_meses_corrida_"+str(i)+".jpg")
        plt.clf()

        plt.step(array_tiempo_simulacion_12_meses, array_nivel_inventario_12_meses, where='post')
        plt.title("Grafica de 12 meses de simulación")
        plt.axhline(smalls, color='red', linestyle='--', linewidth=2, label='Minimo')
        plt.axhline(bigs, color='green', linestyle='--', linewidth=2, label='Maximo')
        plt.xlabel('Tiempo')
        plt.ylabel('Nivel de Inventario')
        plt.savefig("Graficas/politica_"+str(smalls)+", "+str(bigs)+"corrida_"+str(i)+"/3_inventario_politica_"+str(smalls)+", "+str(bigs)+"_primeros_12_meses_corrida_"+str(i)+".jpg")
        plt.clf()

        plt.step(array_tiempo_simulacion_12_60_meses, array_nivel_inventario_12_60, where='post')
        plt.title("Grafica simulación del mes 12 al 60")
        plt.axhline(smalls, color='red', linestyle='--', linewidth=2, label='Minimo')
        plt.axhline(bigs, color='green', linestyle='--', linewidth=2, label='Maximo')
        plt.xlabel('Tiempo')
        plt.ylabel('Nivel de Inventario')
        plt.savefig("Graficas/politica_"+str(smalls)+", "+str(bigs)+"corrida_"+str(i)+"/4_inventario_politica_"+str(smalls)+", "+str(bigs)+"_meses_12_60_corrida_"+str(i)+".jpg")
        plt.clf()

        plt.step(array_tiempo_simulacion_60_120_meses, array_nivel_inventario_60_120, where='post')
        plt.title("Grafica simulación del mes 60 al 120")
        plt.axhline(smalls, color='red', linestyle='--', linewidth=2, label='Minimo')
        plt.axhline(bigs, color='green', linestyle='--', linewidth=2, label='Maximo')
        plt.xlabel('Tiempo')
        plt.ylabel('Nivel de Inventario')
        plt.savefig("Graficas/politica_"+str(smalls)+", "+str(bigs)+"corrida_"+str(i)+"/5_inventario_politica_"+str(smalls)+", "+str(bigs)+"_meses_60_120_corrida_"+str(i)+".jpg")
        plt.clf()

txt.close()

#python ModeloInventario.py -a 20 -b 120 -c 1 -d 4 -e 0.1 -f 32 -g 3 -h 1 -i 5 -j 0.5  -k 1 -l 2
