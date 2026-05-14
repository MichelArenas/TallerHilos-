"""
“Además de calcular la media, cada hilo debe calcular desviación estándar de su sección y sincronizar
ambos resultados usando dos barreras diferentes.”
"""

import threading
import random
import math

# GENERAR DATASET
dataset = [[random.uniform(1, 100) for _ in range(10)] for _ in range(100)]

# CONFIGURACION
num_hilos = 3

lock = threading.Lock()

# DOS BARRERAS
barrera_media = threading.Barrier(num_hilos)
barrera_desviacion = threading.Barrier(num_hilos)

# Resultados globales
medias = []
desviaciones = []

# FUNCION HILO
def procesar_columna(id_hilo, columna):

    print(f"\nHilo {id_hilo} procesando columna {columna}")

    datos_columna = [fila[columna] for fila in dataset]


    # CALCULAR MEDIA

    media = sum(datos_columna) / len(datos_columna)

    with lock:
        medias.append(media)

    print(f"Hilo {id_hilo} -> Media: {media:.2f}")


    # PRIMERA BARRERA

    print(f"Hilo {id_hilo} esperando barrera de medias...")
    barrera_media.wait()


    # CALCULAR DESVIACION

    suma_cuadrados = 0

    for valor in datos_columna:
        suma_cuadrados += (valor - media) ** 2

    desviacion = math.sqrt(suma_cuadrados / len(datos_columna))

    with lock:
        desviaciones.append(desviacion)

    print(f"Hilo {id_hilo} -> Desviación estándar: {desviacion:.2f}")


    # SEGUNDA BARRERA

    print(f"Hilo {id_hilo} esperando barrera de desviaciones...")
    barrera_desviacion.wait()

    if id_hilo == 0:

        print("\n--- TODOS LOS HILOS TERMINARON ---")

        print(f"Suma de medias: {sum(medias):.2f}")

        print(f"Suma de desviaciones: {sum(desviaciones):.2f}")

# CREAR HILOS
hilos = []

for i in range(num_hilos):

    t = threading.Thread(
        target=procesar_columna,
        args=(i, i)
    )

    hilos.append(t)
    t.start()

# ESPERAR HILOS
for t in hilos:
    t.join()
    