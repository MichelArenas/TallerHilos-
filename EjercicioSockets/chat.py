import socket
import threading

# creamos un socket TCP/IP del lado cliente
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# nos conectamos al servidor (cambiar 'localhost' si está en otra máquina)
server_address = ('10.222.220.208', 9000)
print('Conectando a {} puerto {}'.format(*server_address))
clientSocket.connect(server_address)

# El servidor primero nos pide el nombre. Lo leemos, lo mostramos
# y enviamos lo que el usuario escriba como identificador del chat.
prompt = clientSocket.recv(1024).decode('utf-8')
print(prompt, end='')
nombre = input().strip()
clientSocket.sendall(nombre.encode('utf-8'))

# definimos una función para el hilo de RECEPCIÓN.
# Necesitamos un hilo aparte para recibir, porque el hilo principal se
# queda bloqueado en input() esperando lo que el usuario escribe; sin
# este hilo, los mensajes del otro usuario no se imprimirían hasta que
# nosotros enviáramos algo. Así logramos el flujo bidireccional simultáneo.
def recibir_mensajes(conn):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print('\n[El servidor cerró la conexión]')
                break
            # Imprimimos el mensaje entrante en una nueva línea para no
            # pisar lo que el usuario está escribiendo.
            print('\n' + data.decode('utf-8').rstrip())
            print('> ', end='', flush=True)
    except Exception as e:
        print('\n[Error de recepción]:', e)


# lanzamos el hilo de recepción como daemon: muere cuando termina el programa
hilo_recepcion = threading.Thread(target=recibir_mensajes, args=(clientSocket,), daemon=True)
hilo_recepcion.start()

# Bucle principal: ENVÍO. Lee la entrada del usuario y la manda al servidor.
try:
    while True:
        mensaje = input('> ').strip()
        if not mensaje:
            continue
        if mensaje.lower() == '/salir':
            break
        clientSocket.sendall(mensaje.encode('utf-8'))
except KeyboardInterrupt:
    pass
finally:
    # cerramos el socket al salir
    clientSocket.close()
    print('Conexión cerrada.')