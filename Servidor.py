import socket
import threading
import mysql.connector
import datetime

# lista d conexiones activas
clientes_activos = {} # Diccionario: {conexion: nombre_usuario}

def conectar_db():
    return mysql.connector.connect(
        host='127.0.0.1', user='root', password='', database='sockets'
    )

def manejar_cliente(conexion, direccion):
    print(f"[NUEVA CONEXIÓN] {direccion} conectado.")
    conexion.send("Bienvenido. Ingresa: usuario,contraseña".encode('utf-8'))
    
    data = conexion.recv(1024).decode('utf-8').split(',')
    
    if len(data) == 2:
        usuario, password = data[0], data[1]
        db = conectar_db()
        cursor = db.cursor()
        query = "SELECT * FROM usuarios WHERE nombre = %s AND password = %s"
        cursor.execute(query, (usuario, password))
        resultado = cursor.fetchone()
        
        if resultado:
            # guardado de usuario
            clientes_activos[conexion] = usuario
            conexion.send("Autenticación exitosa.".encode('utf-8'))
            
            while True:
                msg = conexion.recv(1024).decode('utf-8')
                if not msg: break
                
                if msg.startswith('/todos '):
                    mensaje_a_enviar = msg.replace('/todos ', '')
                    for conn in clientes_activos:
                        conn.send(f"[{usuario} dice a todos]: {mensaje_a_enviar}".encode('utf-8'))
                
                elif msg == '/usuarios':
                    lista = ", ".join(clientes_activos.values())
                    conexion.send(f"Usuarios conectados: {lista}".encode('utf-8'))
                
                elif msg == '/hora':
                    conexion.send(str(datetime.datetime.now()).encode('utf-8'))
                elif msg == '/adios':
                    conexion.send("Adiós!".encode('utf-8'))
                    break
                else:
                    conexion.send("Comando recibido.".encode('utf-8'))
        else:
            conexion.send("Error: Usuario o contraseña incorrectos.".encode('utf-8'))
        
        cursor.close()
        db.close()
    
    # eliminacion de usuario
    if conexion in clientes_activos:
        del clientes_activos[conexion]
    conexion.close()

# config del server
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('127.0.0.1', 12345))
servidor.listen()
print("[SERVIDOR] Escuchando en 127.0.0.1:12345")

while True:
    conn, addr = servidor.accept()
    thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
    thread.start()