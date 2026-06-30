import socket
import threading
import mysql.connector
import datetime
import time

# lista diccionario de conexiones activas
clientes_activos = {} 

# Conexion con la bd local de los usuarios
def conectar_db():
    return mysql.connector.connect(
        host='127.0.0.1', user='root', password='', database='sockets'
    )

def manejar_cliente(conexion, direccion):
    usuario_nombre = "Desconocido"
    print(f"NUEVA CONEXION {direccion} conectado.")
    
    try:
        conexion.send("Bienvenido. Ingresa: usuario,contraseña".encode('utf-8'))
        data = conexion.recv(1024).decode('utf-8').split(',') # Recepcion de las credenciales del  cliente/usuario

        # valida las credenciales ingresadas con la bd
        if len(data) == 2:
            usuario, password = data[0], data[1]
            db = conectar_db()
            cursor = db.cursor()
            query = "SELECT * FROM usuarios WHERE nombre = %s AND password = %s"
            cursor.execute(query, (usuario, password))
            resultado = cursor.fetchone()
            
            # Registra al usuario/cliente en el diccionario de conexiones activas
            if resultado:
                usuario_nombre = usuario
                clientes_activos[conexion] = usuario_nombre
                conexion.send("Autenticación exitosa.".encode('utf-8'))
                
                # bucle para escuchar comandos del cliente/usuario
                while True:
                    msg = conexion.recv(1024).decode('utf-8')
                    if not msg: break
                    
                    if msg.startswith('/todos '):
                        mensaje_a_enviar = msg.replace('/todos ', '')
                        for conn in clientes_activos:
                            conn.send(f"\n[{usuario_nombre} dice a todos]: {mensaje_a_enviar}".encode('utf-8'))
                    
                    elif msg == '/usuarios':
                        lista = ", ".join(clientes_activos.values())
                        conexion.send(f"Usuarios conectados: {lista}".encode('utf-8'))
                    
                    elif msg == '/hora':
                        conexion.send(str(datetime.datetime.now()).encode('utf-8'))
                    
                    elif msg == '/adios':
                        conexion.send("Adiós!".encode('utf-8'))
                        time.sleep(0.1)
                        break
                    
                    else:
                        conexion.send("Comando no reconocido.".encode('utf-8'))
            else:
                conexion.send("Usuario o contraseña incorrectos.".encode('utf-8'))
            
            cursor.close()
            db.close()
            
    except ConnectionResetError: # identifica el cierre forzado de parte del usuaroi
        print(f"Conexion perdida con {usuario_nombre}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conexion in clientes_activos:
            print(f"DESCONEXION Usuario '{clientes_activos[conexion]}' se ha desconectado.")
            del clientes_activos[conexion]
        else:
            print(f"DESCONEXION Una conexión sin autenticar ({direccion}) se cerró.")
        conexion.close()

# Configuración del servidor socket tcp
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('127.0.0.1', 12345))
servidor.listen()
print("SERVIDOR Escuchando en 127.0.0.1:12345")

# bucle para aceptar conexiones nuevas
while True:
    conn, addr = servidor.accept()
    thread = threading.Thread(target=manejar_cliente, args=(conn, addr)) # uso de multihilo
    thread.start()