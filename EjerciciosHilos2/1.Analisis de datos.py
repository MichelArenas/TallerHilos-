"""
Ya no quiero procesar columnas completas. Cada hilo debe procesar bloques de filas diferentes y
luego combinar las medias globales correctamente.
"""
import threading
import random

# GENERAR DATASET
dataset = [[random.uniform(1, 100) for _ in range(10)] for _ in range(100)]

# CONFIGURACION
num_hilos = 4

lock = threading.Lock()
barrera = threading.Barrier(num_hilos)

# Variables globales
suma_global = 0
cantidad_global = 0

# FUNCION HILO
def procesar_bloque(id_hilo, inicio, fin):

    global suma_global, cantidad_global

    print(f"\nHilo {id_hilo} procesando filas {inicio} hasta {fin}")

    suma_local = 0
    cantidad_local = 0

    # Procesar filas asignadas
    for fila in dataset[inicio:fin]:

        suma_local += sum(fila)
        cantidad_local += len(fila)

    media_local = suma_local / cantidad_local

    print(f"Hilo {id_hilo} -> Media local: {media_local:.2f}")

    # Combinar resultados
    with lock:
        suma_global += suma_local
        cantidad_global += cantidad_local

    print(f"Hilo {id_hilo} esperando en barrera...")
    barrera.wait()

    if id_hilo == 0:
        media_global = suma_global / cantidad_global

        print("\n--- TODOS LOS HILOS TERMINARON ---")
        print(f"Media global: {media_global:.2f}")

# DIVIDIR FILAS
filas_totales = len(dataset)
tam_bloque = filas_totales // num_hilos

# CREAR HILOS
hilos = []

for i in range(num_hilos):

    inicio = i * tam_bloque

    # El último hilo toma las filas sobrantes
    if i == num_hilos - 1:
        fin = filas_totales
    else:
        fin = inicio + tam_bloque

    t = threading.Thread(
        target=procesar_bloque,
        args=(i, inicio, fin)
    )

    hilos.append(t)
    t.start()

# ESPERAR HILOS
for t in hilos:
    t.join()