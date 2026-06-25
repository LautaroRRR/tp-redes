import socket

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('127.0.0.1', 12345))

    # recibe bienvenida
    print(cliente.recv(1024).decode('utf-8'))
    auth = input("Usuario,Contraseña: ")
    cliente.send(auth.encode('utf-8'))
    print(cliente.recv(1024).decode('utf-8'))

    while True:
        msg = input("> ")
        cliente.send(msg.encode('utf-8'))
        if msg.lower() == '/adios':
            break
        print(f"Servidor: {cliente.recv(1024).decode('utf-8')}")

    cliente.close()

if __name__ == "__main__":
    iniciar_cliente()