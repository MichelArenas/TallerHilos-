"""
3. Ejercicio de Bloqueos en una Cuenta Bancaria (Gestión de Transacciones)

• Descripción: Implementar una simulación de una cuenta bancaria compartida. 
Dos hilos representarán transacciones de depósito y retiro. Los depósitos suman
una cantidad aleatoria entre 10 y 100 unidades, y los retiros restan una cantidad similar.
El Restricción es evitar inconsistencias en el balance debido a operaciones concurrentes.

• Restricción: Aplicar threading.Lock para bloquear la cuenta mientras una transacción está en curso.
"""

import threading
import time
import random

# Clase que representa la Cuenta Bancaria
class CuentaBancaria:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial
        self.lock = threading.Lock() # El cerrojo para proteger el saldo

    def depositar(self, cantidad):
        print(f"Intentando depositar {cantidad}...")
        # Bloqueamos el acceso antes de modificar el saldo
        with self.lock:
            nuevo_saldo = self.saldo + cantidad
            time.sleep(0.1)  # Simulamos un pequeño retraso de red/procesamiento
            self.saldo = nuevo_saldo
            print(f"Depósito exitoso. Nuevo saldo: {self.saldo}")

    def retirar(self, cantidad):
        print(f"Intentando retirar {cantidad}...")
        # Bloqueamos el acceso antes de modificar el saldo
        with self.lock:
            if self.saldo >= cantidad:
                nuevo_saldo = self.saldo - cantidad
                time.sleep(0.1) # Simulamos retraso
                self.saldo = nuevo_saldo
                print(f"✅ Retiro exitoso. Nuevo saldo: {self.saldo}")
            else:
                print(f"❌ Retiro fallido. Saldo insuficiente ({self.saldo})")

# 3. Función para simular múltiples transacciones
def simular_transacciones(cuenta, tipo):
    for _ in range(5):
        monto = random.randint(10, 100)
        if tipo == "deposito":
            cuenta.depositar(monto)
        else:
            cuenta.retirar(monto)

# --- Ejecución ---
mi_cuenta = CuentaBancaria(100)

# Crear hilos para depósitos y retiros
hilo_deposito = threading.Thread(target=simular_transacciones, args=(mi_cuenta, "deposito"))
hilo_retiro = threading.Thread(target=simular_transacciones, args=(mi_cuenta, "retiro"))

hilo_deposito.start()
hilo_retiro.start()

hilo_deposito.join()
hilo_retiro.join()

print(f"\nPROCESO FINALIZADO. Saldo final en cuenta: {mi_cuenta.saldo}")