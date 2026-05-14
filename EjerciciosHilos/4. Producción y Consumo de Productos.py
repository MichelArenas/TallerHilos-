"""
4. Ejercicio de Productor-Consumidor con Semáforos (Producción y Consumo de Productos)
• Descripción: Crear un programa donde un grupo de hilos actúan como productores 
que generan productos y los colocan en una cola, mientras que otro grupo actúa como
consumidores que retiran productos de la cola. Cada productor debe producir un producto
cada 2 segundos, y cada consumidor debe consumir un producto cada segundo.

• Restricción: Usar threading.Semaphore para limitar el tamaño máximo de la cola y sincronizar
 la producción y el consumo.

"""

import threading
import random
import time

cola=[]
tamaño_maximo=5

#semaforos
espacios_disponible= threading.Semaphore(tamaño_maximo)
productos_disponibles=threading.Semaphore(0)

#lock para que enetre un hilo a la vez a la cola    
mutex= threading.Lock()

#empezar con la funcion de productor
def productor(id):
    contador=1
    while True:
        #esperar si la cola se llena
        espacios_disponible.acquire()

        #bloquear el acceso a la cola
        mutex.acquire()

        #crear producto
        producto = f"P{id}-Prod{contador}"

        #agregar el producto a la cola
        cola.append(producto)
        print(f"Productor {id} produjo: {producto}")
        print(f"Cola actual: {cola}")

        contador +=1
        #liberar el acceso a la cola

        #Se indica que hay un producto disponible para consumir
        productos_disponibles.release()

        #Esperar dos segundos ya que producen cada dos segundos
        time.sleep(2)

#funcion consumidor
def consumidor(id):
    while True:
        #Esperar si no hay productos disponibles
        productos_disponibles.acquire()

        #bloquear el acceso a la cola
        mutex.acquire()

        #cinsumir un producto de la cola
        producto= cola.pop(0)

        print(f"Consumidor {id} consumió: {producto}")
        print(f"Cola actual: {cola}")

        #liberar la cola
        mutex.release()

        #liberar un espacio en la cola
        espacios_disponible.release()

        #esperar un segundo ya que consumen cada segundo
        time.sleep(1)

#crear hilos productores y consumidores

#Lista de hilos
hilos=[]

#crear productores
for i in range(2):
    hilo=threading.Thread(target=productor, args=(i+1,))
    hilos.append(hilo)

#crear consumidores
for i in range(2):
    hilo=threading.Thread(target=consumidor, args=(i+1,))
    hilos.append(hilo)

#iniciar hilos
for hilo in hilos:
    hilo.start()

#Mantener el programa corriendo
for hilo in hilos:
    hilo.join()
