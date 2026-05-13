"""
7. Ejercicio de Cuenta Regresiva con Semáforo Binario (Turnos de Trabajo Alternados)

• Descripción: Crear un programa donde dos hilos representan dos trabajadores alternando turnos
de cuenta regresiva (imprimiendo de 10 a 1). Los trabajadores deben alternar la impresión de los 
números (uno imprime 10, el otro imprime 9, y así sucesivamente).

• Restricción: Usar un semáforo binario para alternar el control entre los hilos en cada paso de 
la cuenta regresiva.

"""

import threading
import time

# Semáforos binarios
sem1 = threading.Semaphore(1)
sem2 = threading.Semaphore(0)

# Variable compartida
contador = 10


# Trabajador 1
def trabajador1():

    global contador

    while contador > 0:

        sem1.acquire()

        print(f" Trabajador 1: {contador}")

        contador -= 1

        time.sleep(1)

        sem2.release()


#Trabajador 2
def trabajador2():

    global contador

    while contador > 0:

        sem2.acquire()

        print(f" Trabajador 2: {contador}")

        contador -= 1

        time.sleep(1)

        sem1.release()


# Crear hilos
hilo1 = threading.Thread(target=trabajador1)
hilo2 = threading.Thread(target=trabajador2)

# Iniciar hilos
hilo1.start()
hilo2.start()

# Esperar finalización
hilo1.join()
hilo2.join()