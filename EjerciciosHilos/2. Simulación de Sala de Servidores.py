"""
2. Ejercicio de Control de Acceso con Semáforos (Simulación de Sala de Servidores)

• Descripción: Simular una sala de servidores a la que solo pueden ingresar
un máximo de tres técnicos al mismo tiempo. Cada técnico debe simular una reparación 
que dure entre 1 y 3 segundos. Al completar la reparación, debe liberar el acceso para 
permitir que otros entren.

• Restricción: Implementar threading.Semaphore para gestionar el acceso controlado a la sala.

"""

import threading
import time
import random

#1. Configurar el semáforo para permitir un máximo de 3 técnicos en la sala
capacidad_sala = 3
semaforo = threading.Semaphore(capacidad_sala)

def ingresar_sala(id_tecnico):
    """
    Funcion que simula a un técnico intentando ingresar a la sala de servidores, 
    realizando una reparación y luego saliendo.

    """
    print(f"Técnico {id_tecnico} esta intentando ingresar a la sala de servidores...")

    # El técnico intenta adquirir el semáforo para ingresar
    with semaforo:  
        print(f"Técnico {id_tecnico} ha ingresado a la sala de servidores.")

        #Simular el tiempo de reparación
        duracion = random.uniform(1,3)
        time.sleep(duracion)

        print(f"Técnico {id_tecnico} ha terminado de reparar en ({duracion:.2f} segundos)")

    print (f"El técnico {id_tecnico} ha salido de la sala de servidores.")


#2. Crear varios hilos para simular a los técnicos intentando ingresar a la sala
tecnicos=[]
for i in range (1,9):
    t=threading.Thread(target=ingresar_sala, args=(i,))
    tecnicos.append(t)
    t.start()
#3. Esperar que todos los hilos (tecnicos) terminen para finalizar el programa
for t in tecnicos:
    t.join()

print("\n---Todos los técnicos han terminado sus reparaciones---")
