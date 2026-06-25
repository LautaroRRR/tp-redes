TP Integrador

Como ejecutar el proyecto
Requisitos previos
Tener instalado Python 

Tener instalado XAMPP con la base de datos sockets

Importar el archivo SQL con la tabla usuarios 

Pasos para ejecutar
Configurar Base de Datos: 
Asegurarse de que el servicio MySQL esté corriendo en 127.0.0.1:3306

Iniciar Servidor:

Bash
python Servidor.py
Iniciar Cliente: En una nueva terminal, ejecutar:

Bash
python Cliente.py
Autenticacion: 
Ingresar los datos con el formato usuario,contraseña cuando el sistema lo solicite

Comandos disponibles
/hora: Muestra la fecha y hora actual del servidor

/usuarios: Lista todos los usuarios conectados actualmente

/todos "mensaje": Envia un mensaje a todos los clientes conectados

/adios: Cierra la conexion y sesion

Librerias utilizadas
Generar el archivo de dependencias ejecutando en la terminal:

Bash
pip freeze > requirements.txt