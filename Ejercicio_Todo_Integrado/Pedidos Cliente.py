import socket
import random
import time

productos = [
    "Mouse",
    "Teclado",
    "Monitor",
    "Laptop"
]

cliente = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

cliente.connect(("localhost", 5000))

cantidad_pedidos = random.randint(1, 5)

for i in range(cantidad_pedidos):

    producto = random.choice(productos)

    cantidad = random.randint(1, 3)

    mensaje = f"{producto},{cantidad}"

    cliente.send(mensaje.encode())

    print(f"Pedido enviado: {mensaje}")

    time.sleep(random.randint(1, 3))

cliente.close()