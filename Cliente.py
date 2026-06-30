import socket
import threading
import time

def escuchar_servidor(cliente):# hilo dedicado a recibir señales del servidor

    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8') # imprime el mensaje
            if mensaje:
                print(f"\n{mensaje}")
                print("> ", end="", flush=True)
            else: # el servidor cierra la conexion si recv() esta vacio
                print("\nConexion cerrada.")
                break
        except: # identifica el cierre forzado 
            break

def iniciar_cliente(): # inicio del socket tcp-ip
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect(('127.0.0.1', 12345))
    except ConnectionRefusedError:
        print("No se pudo conectar al servidor. ¿Está encendido?")
        return

    print(cliente.recv(1024).decode('utf-8')) # el cliente envia sus credenciales para su validacion
    auth = input("Usuario,Contraseña: ")
    cliente.send(auth.encode('utf-8'))
    
    respuesta_auth = cliente.recv(1024).decode('utf-8')
    print(respuesta_auth)


    if "exitosa" in respuesta_auth: # inicio del chat

        hilo = threading.Thread(target=escuchar_servidor, args=(cliente,), daemon=True)
        hilo.start()

        while True: # identifica lo que el usuario escribe en el chat
            msg = input("> ")
            cliente.send(msg.encode('utf-8'))
            
     
            if msg.lower() == '/adios': # cierre del cliente/usuario
                time.sleep(0.5) 
                break
    
    cliente.close()
    print("Has salido del chat.")

if __name__ == "__main__":
    iniciar_cliente()