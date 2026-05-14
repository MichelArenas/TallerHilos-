"""
“Ahora el número de hilos debe ser dinámico. El usuario ingresará cuántos hilos quiere usar y las 
columnas deben repartirse automáticamente entre ellos.”
"""

import threading
import random

# GENERAR DATASET
dataset = [[random.uniform(1, 100) for _ in range(10)] for _ in range(100)]

# ENTRADA DEL USUARIO
num_hilos = int(input("Ingrese la cantidad de hilos: "))

# VARIABLES GLOBALES
resultados = []
lock = threading.Lock()

# Barrera dinámica
barrera = threading.Barrier(num_hilos)

# FUNCION DEL HILO
def procesar_columnas(id_hilo, columnas_asignadas):

    medias_locales = []

    print(f"\nHilo {id_hilo} procesando columnas {columnas_asignadas}")

    for col in columnas_asignadas:

        columna = [fila[col] for fila in dataset]
        media = sum(columna) / len(columna)

        medias_locales.append(media)

        print(f"Hilo {id_hilo} -> Columna {col} -> Media: {media:.2f}")

    # Guardar resultados
    with lock:
        resultados.extend(medias_locales)

    print(f"Hilo {id_hilo} esperando en barrera...")
    barrera.wait()

    if id_hilo == 0:
        print("\n--- TODOS LOS HILOS TERMINARON ---")

# REPARTIR COLUMNAS
columnas_totales = 10
columnas = list(range(columnas_totales))

reparto = [[] for _ in range(num_hilos)]

for i, col in enumerate(columnas):
    reparto[i % num_hilos].append(col)

# CREAR HILOS
hilos = []

for i in range(num_hilos):
    t = threading.Thread(
        target=procesar_columnas,
        args=(i, reparto[i])
    )

    hilos.append(t)
    t.start()

# ESPERAR HILOS
for t in hilos:
    t.join()

# RESULTADO FINAL
suma_total = sum(resultados)

print(f"\nSuma total de medias: {suma_total:.2f}")
