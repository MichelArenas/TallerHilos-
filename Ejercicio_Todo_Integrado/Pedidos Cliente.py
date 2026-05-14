import socket

cliente = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

cliente.connect(("localhost", 5000))

print("Conectado al servidor")

productos = ["Mouse", "Teclado", "Monitor", "Laptop"]

print("""
Productos disponibles:
- Mouse
- Teclado
- Monitor
- Laptop
""")



while True:

    producto = input("Producto: ")

    if producto.lower() == "salir":
        break

    if producto not in productos:
        print("Producto inválido")
        continue

    cantidad = input("Cantidad: ")

    mensaje = f"{producto},{cantidad}"

    cliente.send(mensaje.encode())

    print("Pedido enviado")
    

cliente.close()

