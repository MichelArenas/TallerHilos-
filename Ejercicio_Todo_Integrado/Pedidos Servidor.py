import socket
import random
import time
import threading

cola_pedidos = []

lock_cola = threading.Lock()

# Máximo 10 pedidos en cola
semaforo = threading.Semaphore(10)

# Esperar 3 procesadores
barrera = threading.Barrier(3)

stock = {"Mouse": 10, "Teclado": 8, "Monitor": 5, "Laptop": 3}


def manejar_cliente(conn, addr):

    print(f"Cliente conectado: {addr}")

    while True:

        try:
            mensaje = conn.recv(1024).decode()

            if not mensaje:
                break

            producto, cantidad = mensaje.split(",")

            pedido = (producto, int(cantidad))

            # Esperar espacio en cola
            semaforo.acquire()

            with lock_cola:
                cola_pedidos.append(pedido)

                print(f"Pedido agregado: {pedido}")
                print(f"Pedidos en cola: {len(cola_pedidos)}")

        except:
            break

    conn.close()


def procesador(id_procesador):

    print(f"Procesador {id_procesador} listo")

    barrera.wait()

    while True:

        with lock_cola:

            if len(cola_pedidos) > 0:

                pedido = cola_pedidos.pop(0)

                # Liberar espacio en cola
                semaforo.release()

            else:
                pedido = None

        if pedido:

            producto, cantidad = pedido

            tiempo = random.randint(1, 5)

            print(f"Procesador {id_procesador} atendiendo {pedido}")

            time.sleep(tiempo)

            with lock_cola:

                if stock[producto] >= cantidad:

                    stock[producto] -= cantidad

                    print(f"Pedido despachado: {pedido}")

                else:

                    print(f"Stock insuficiente para {pedido}")

                print(f"Stock actual: {stock}")

        else:

            time.sleep(1)

        # Crear socket del servidor


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("", 5000))
servidor.listen(5)
print("Servidor iniciando")


for i in range(3):

    t = threading.Thread(target=procesador, args=(i,))

    t.daemon = True
    t.start()

while True:

    conn, addr = servidor.accept()

    hilo_cliente = threading.Thread(target=manejar_cliente, args=(conn, addr))

    hilo_cliente.start()
