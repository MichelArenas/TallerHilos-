"""
6. Ejercicio de Lectores-Escritores (Sistema de Consulta y Actualización de un Registro de Usuarios)

• Descripción: Simular un registro de usuarios con operaciones de lectura y escritura. 
Tres hilos deben consultar (leer) información de usuarios sin afectar a otros lectores. 
Otros dos hilos deben actualizar la información de algunos usuarios (escribir) de forma exclusiva.
Si un escritor está actualizando, los lectores deben esperar.

• Restricción: Implementar threading.Lock para controlar el acceso concurrente al registro
 en escenarios de lectores y escritores.

"""
import threading
import time
import random

# Registro compartido
usuarios = {
    1: "Ana",
    2: "Carlos",
    3: "Laura"
}

# Locks
lock_escritor = threading.Lock()
lock_lectores = threading.Lock()

# Contador de lectores
lectores_activos = 0


# ---------------- LECTOR ----------------
def lector(id_lector):

    global lectores_activos

    # Entrar a leer
    lock_lectores.acquire()

    lectores_activos += 1

    # Primer lector bloquea escritores
    if lectores_activos == 1:
        lock_escritor.acquire()

    lock_lectores.release()

    # Leer información
    print(f"📖 Lector {id_lector} está leyendo...")
    print(usuarios)

    time.sleep(random.randint(1, 3))

    # Salir de lectura
    lock_lectores.acquire()

    lectores_activos -= 1

    # Último lector libera escritores
    if lectores_activos == 0:
        lock_escritor.release()

    lock_lectores.release()

    print(f"✅ Lector {id_lector} terminó.\n")


# ---------------- ESCRITOR ----------------
def escritor(id_escritor):

    # Exclusividad
    lock_escritor.acquire()

    usuario = random.randint(1, 3)

    nuevo_nombre = f"Usuario_Modificado_{id_escritor}"

    usuarios[usuario] = nuevo_nombre

    print(f"✏️ Escritor {id_escritor} actualizó usuario {usuario}")

    time.sleep(2)

    print(f"✅ Escritor {id_escritor} terminó.\n")

    lock_escritor.release()


# Crear hilos
hilos = []

# 3 lectores
for i in range(3):
    hilo = threading.Thread(target=lector, args=(i + 1,))
    hilos.append(hilo)

# 2 escritores
for i in range(2):
    hilo = threading.Thread(target=escritor, args=(i + 1,))
    hilos.append(hilo)

# Iniciar hilos
for hilo in hilos:
    hilo.start()

# Esperar finalización
for hilo in hilos:
    hilo.join()