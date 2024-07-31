#En este documento realizaremos la simulación de un modelo de inventario
import random
import array as arr
import statistics
import math
import sys
import matplotlib.pyplot as plt

### Ejecución del programa
if len(sys.argv) != 7:
    print("Uso: python ModeloInventario.py -a <nivel inicial de inventario> -b <meses de la simulacion> -c <cantidad diferente de politicas> -d <valores de demanda> -e <media entre pedidos> -f <costo setup> -g <costo incremental> -h <costo de mantenimiento> -i  <costo por producto faltante> -j <minimo lag(minimo en la dist U del tiempo del siguiente evento)> -k <maximo lag (maximo en la dist U del tiempo del siguiente evento)> ")
    sys.exit(1) 

#var = int(sys.argv[2])
nivel_inicial_inventario = int(sys.argv[2]) #inventario con el que se arranca la simulacion
num_meses = int(sys.argv[4])                #tiempo de simulacion
num_politicas = int(sys.argv[6])            #cantidad de politicas que quiero evaluar (rangos de minimo y maximo de stock)
val_demanda = int(sys.argv[8])              #
media_entre_pedidos = float(sys.argv[10])
costo_setup = float(sys.argv[12])           #costo base del pedido
costo_incremental = float(sys.argv[14])     #costo agregado por cada item del pedido
costo_mantenimiento = float(sys.argv[16])   #costo de mantenimiento de los productos en stock
costo_faltante = float(sys.argv[18])        #costo en caso de no tener stock (por cada posibilidad de venta sin concretarse)
minimo_lag = float(sys.argv[20])
maximo_lag = float(sys.argv[22])
num_corridas = int(sys.argv[24])

# El delivery tiene delay, variable aleatoria uniforme entre un mindelay y un maxdelay 
# 
# 
# 
# 
# 
# 
# 
# 
#
# 
# 
# 
# ' 
