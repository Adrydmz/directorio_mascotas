1 .- Analizamos los Requerimientos

Proyecto: Directorio de mascotas perdidas.

Stack Tecnológico: Python 3.12, Django 5.x, PostgreSQL (prohibido SQLite) y Bootstrap 5.

Modelo de Usuario: Implementación obligatoria de CustomUser extendiendo AbstractUser o AbstractBaseUser.

Entidad Principal: El modelo MascotaPerdida.

Campos de Entidad: Nombre, Especie, Raza, Ubicación, Recompensa, Estado encontrada/no encontrada, Fotografía y Fecha de reporte.

Relaciones: ForeignKey hacia CustomUser (Usuario Reporta) y hacia un modelo Avistamiento.

Infraestructura: Despliegue final en Oracle Cloud Infrastructure (OCI) con IP pública.

Seguridad: Uso estricto de variables de entorno para credenciales y configuraciones sensibles.

--------------------------------------------------

2.- Instalacion de requerimientos

Se descargó Python 3.12, Git, PostgreSQL, Visual Studio Code

Diseño de Arquitectura y Estructura de Carpetas
Una vez instaladas las herramientas, abriremos la terminal y ejecutaremos los comandos para crear el entorno de trabajo. El uso de entornos virtuales es una práctica obligatoria para no contaminar el sistema global.

# 1. Creamos la carpeta principal del proyecto
mkdir directorio_mascotas
cd directorio_mascotas

# 2. Inicializamos Git en la carpeta
git init

# 3. Creamos el entorno virtual con Python 3.12
python -m venv venv

# 4. Activamos el entorno virtual 
venv\Scripts\activate

# 5. Creamos el archivo requeriments.txt e insertamos lo siguiente:
Django>=5.0,<5.1
psycopg2-binary>=2.9.9
Pillow>=10.2.0
python-dotenv>=1.0.1
gunicorn>=21.2.0

# 6. Usamos el sig comando, para descargar lo necesario del proyecto:
pip install -r requirements.txt

# Nota *Definimos las versiones exactas para garantizar compatibilidad. psycopg2-binary es el conector de PostgreSQL, Pillow maneja la subida de imágenes, python-dotenv gestiona las variables de entorno, y gunicorn será nuestro servidor para OCI.*

# 7. Creamos el archivo .env e insertamos un template para las variables de entorno que usaremos en el futuro
SECRET_KEY=tu_secret_key_aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=mascotas_db
DB_USER=postgres
DB_PASSWORD=tu_password_aqui
DB_HOST=localhost
DB_PORT=5432

# 8. Ahora necesitamos confirmar que materializamos la estructura base de Django usando los siguientes comandos en terminal.
django-admin startproject core .
python manage.py startapp usuarios
python manage.py startapp mascotas

*Nombramos el proyecto principal como core para mantener la estructura de carpetas estandarizada y limpia. Separamos el proyecto en dos aplicaciones (usuarios y mascotas) siguiendo el principio de responsabilidad única y cumpliendo con el requerimiento de un modelo de usuario personalizado. El punto al final del primer comando es vital para evitar carpetas redundantes*

# 9. Instalamos DBeaver para crear la BD

# 10. Creamos nuestro primer commit porque esta descripcion la agregaremos al repositorio de github.
