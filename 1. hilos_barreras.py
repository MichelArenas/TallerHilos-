"""
1. Ejercicio de Sincronización de Hilos con Barreras (Análisis de Datos en Partes)

• Descripción: Crear un programa donde tres hilos procesan 
diferentes columnas de un conjunto de datos (Genere un data
set de 10 atributos numéricos y 100 registros).
Cada hilo calculará la media de su columna. Una vez que todos los hilos
terminan, los resultados deben sumarse.

• Restricción: Usar threading.Barrier para que cada hilo 
espere hasta que los otros hayan terminado de procesar sus
respectivas columnas antes de combinar los resultados.
"""

import threading
import random

#1. generar el dataset (100 registros x 10 atributos numericos)
dataset = [[random.uniform(1,100) for _ in range(10)] for _ in range(100)]

#Lista para almacenar los resultados de cada hilo
resultadosMedia = []
Lock = threading.Lock()

#2. Definir la función que ejecutara cada hilo
def procesar_columna (id_hilo, indice_columna, barrera ):

    """
    Funcion que simula el procesamiento de una columna del dataset por un hilo,
    calcula la media y luego espera en la barrera para sincronizarse con los otros hilos.

    """
    print(f"El hilo: {id_hilo} Se esta procesando en la columna: {indice_columna}...")

    #Extraer la columna y calcular la media
    columna = [fila[indice_columna] for fila in dataset]
    media = sum(columna) / len(columna)

    #Guardar el resultado en la lista de resultados
    with Lock:
        resultadosMedia.append(media)

    print(f"Hilo: {id_hilo} Media calculada: ({media:.2f}) Esperando en la barrera")

    #3. Punto de sincronización 
    barrera.wait()

    #Los hilos despues de la barrera pueden confirmar que pasaron
    if id_hilo == 0:
        print("\n---Todos los hilos han cruzado la barrera---")

#4. Configuracion de hilos y barreras
num_hilos = 3
barreras_Sincronizadas = threading.Barrier(num_hilos)
hilos=[]

#Columnas que se van a procesar
columnas = [0,1,2]

for i in range (num_hilos):
    t = threading.Thread(target=procesar_columna, args=(i, columnas[i], barreras_Sincronizadas))
    hilos.append(t)
    t.start()
#Esperar a que todos los hilos terminen de ejecutarse
for t in hilos:
    t.join()

#5. Sumar los resultados de las medias
sumaTotal = sum(resultadosMedia)
print(f"\nLa suma total de las medias es: {sumaTotal: .2f}")
