"""
5. Ejercicio de Sincronización de Hilos para Cálculo Paralelo
 (Cálculo de la Suma de una Gran Matriz)

• Descripción: Dividir una matriz grande de números enteros en cuatro secciones (filas o columnas). 
Cada hilo debe sumar los elementos de una sección y almacenar el resultado parcial. Al finalizar,
una barrera asegura que los cuatro resultados parciales se sumen para obtener el total.

Restricción: Practicar la sincronización con threading.Barrier para reunir los resultados después 
de la suma paralela.

"""

import threading
import random

# Crear matriz
matriz = []

for i in range(8):
    fila = []

    for j in range(8):
        numero = random.randint(1, 10)
        fila.append(numero)

    matriz.append(fila)

# Mostrar matriz
print("MATRIZ:\n")

for fila in matriz:
    print(fila)

# Resultados parciales
resultados = [0, 0, 0, 0]

# Barrera
barrera = threading.Barrier(4)


# Función del hilo
def sumar_seccion(id_hilo, inicio, fin):

    suma = 0

    for i in range(inicio, fin):

        for numero in matriz[i]:
            suma += numero

    resultados[id_hilo] = suma

    print(f"\nHilo {id_hilo + 1} terminó.")
    print(f"Suma parcial: {suma}")

    # Esperar a todos los hilos
    barrera.wait()

    # Solo un hilo calcula el total final
    if id_hilo == 0:

        total = sum(resultados)

        print("\nRESULTADO FINAL")
        print("Resultados parciales:", resultados)
        print("Suma total:", total)


# Crear hilos
hilos = []

hilos.append(threading.Thread(target=sumar_seccion, args=(0, 0, 2)))
hilos.append(threading.Thread(target=sumar_seccion, args=(1, 2, 4)))
hilos.append(threading.Thread(target=sumar_seccion, args=(2, 4, 6)))
hilos.append(threading.Thread(target=sumar_seccion, args=(3, 6, 8)))

# Iniciar hilos
for hilo in hilos:
    hilo.start()

# Esperar hilos
for hilo in hilos:
    hilo.join()