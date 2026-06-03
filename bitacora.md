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

# 10. Creamos nuestro primer commit porque esta descripcion la agregaremos al repositorio de github. Pero tuvimos que iniciar sesion primero y usamos los siguientes comandos ya que tuvimos problemas y tuvimos que crear una key

git --version
git config --global user.name "xxx"
git config --global user.email "x@x.xxx"
git reset
git restore --staged .
git rm -r --cached venv
git status
git add .gitignore
git add .
git commit -m "El commit"
git branch -M main
git remote add origin git@github.com:Adrydmz/directorio_mascotas.git
ssh-keygen -t ed25519 -C "x@x.xxx"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub | clip
ssh -T git@github.com
git push -u origin main

# 11. Creamos la BD mascotas_db, usamos estos dos comandos para poner la config de la BD.
(venv) PS G:\Tec\directorio_mascotas> python manage.py makemigrations
No changes detected
(venv) PS G:\Tec\directorio_mascotas> python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
(venv) PS G:\Tec\directorio_mascotas>

# 12. Aqui nos equivocamos porque nos saltamos un paso tuvimos que hacer lo siguiente primero, modificar settings.py 
Hemos reemplazado la configuración base de Django para eliminar cualquier rastro de SQLite y conectar el motor django.db.backends.postgresql directamente a las credenciales extraídas del archivo .env. También definimos explícitamente AUTH_USER_MODEL para que Django sepa que usaremos nuestro propio modelo de usuario.

# 13. Borramos la DB porque nos equivocamos y haremos de nuevo el migrate.

# 14. Creamos usuarios/models.py 
Cumplimos estrictamente con los campos mínimos requeridos en el proyecto: email único, fecha de creación (que se llena automáticamente con auto_now_add=True) y el avatar opcional (permitiendo valores nulos y en blanco). Al definir USERNAME_FIELD = 'email', le decimos a Django que la autenticación se hará por correo.

# 15. Notamos que hubo un "warning" porque nos faltaba crear las carpetas static y media y las creamos en raiz.

# 16. Creamos super usuario con mi correo

# 17. Despues de crear el super usuario creamops la logica de los archivos usuario/models - /admin y mascotas/models - /admin e hicimos el migrate y programos la pagina

(venv) PS G:\Tec\directorio_mascotas> python manage.py makemigrations mascotas
Migrations for 'mascotas':
  mascotas\migrations\0001_initial.py
    - Create model MascotaPerdida
    - Create model Avistamiento
(venv) PS G:\Tec\directorio_mascotas> python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, mascotas, sessions, usuarios
Running migrations:
  Applying mascotas.0001_initial... OK
(venv) PS G:\Tec\directorio_mascotas> python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

# 18 Vamos a crear el archivo que controlará cómo se renderizan los campos cuando un usuario quiera reportar una mascota. Cramos mascotas/forms.py. En lugar de escribir el HTML a mano, le delegamos a Django la creación del formulario validado automáticamente, añadiéndole las clases nativas de Bootstrap 5. Nota que omitimos el campo usuario_reporta porque lo asignaremos de forma automática en la vista por motivos de seguridad.

# 19 Implementamos la lógica del negocio en mascotas/views.py Implementamos el CRUD completo. Usamos LoginRequiredMixin para asegurar que solo los usuarios que han iniciado sesión puedan crear, editar o borrar registros. Sobrescribimos form_valid en la vista de creación para inyectar al usuario actual de forma segura. Ahora necesitamos conectar las vistas que acabamos de crear con direcciones web legibles agregando la logica a mascotas/urls.py, definimos rutas claras y RESTful utilizando el ID (<int:pk>) para identificar registros únicos.

# 20 Finalmente, debemos decirle a todo el proyecto (el directorio core) que incluya las rutas de las mascotas y que, además, permita servir las imágenes subidas durante el entorno de desarrollo, lo hacemos en core/urls.py

# 21 Pasamos a probar que todo funcione bien, para lograrlo implementaremos la herencia de plantillas con un archivo base.html maestro para evitar la duplicación de código. Inyectaremos Bootstrap 5 mediante CDN para tener un diseño profesional y responsivo de inmediato y creamos base.html (Este es el esqueleto de la aplicación. Contiene el menú de navegación y un bloque {% block content %} donde las demás vistas inyectarán su código, cumpliendo el requisito de plantillas con herencia.)

# 22 Creamos en mascotas una carpeta llamada templates y agregamos otra llamada mascotras donde pondremos nuestro html de mascotas mascota_list.html aqui heredamos de base.html y usamos un bucle {% for %} de Django para iterar sobre los registros de la base de datos, mostrándolos en un sistema de tarjetas (cards) de Bootstrap, pasamos a hacer el formulario de mascotas mascota_form.html aqui renderizamos el formulario que configuramos en forms.py. Es vital la inclusión de enctype="multipart/form-data" para cumplir con el requisito de subida de imágenes y {% csrf_token %} para la seguridad OWASP básica

# 23 Teniendo ya la base ahora si probamos la pagina y vemos que funciona bien. (Pero se ve horrible). Vimos que funcionó bien asi que procedemos a hacer los REST que faltan del CRUD.

# 24 Pasamos a mascota_detail.html esta vista mostrará la información completa de la mascota, incluyendo la foto en tamaño grande. Además, implementaremos lógica de seguridad visual: los botones de "Editar" y "Eliminar" solo aparecerán si el usuario que inició sesión es el mismo que creó el reporte.

# 25 Crearemos un panel de confirmacion de eliminar, por si el usuario se equivoca en mascota_confirm_delete.html, cambiamos la linea estatica en mascota_list.html <a href="#" class="btn btn-outline-primary w-100">Ver Detalles</a> por esta <a href="{% url 'mascotas:detalle_mascota' mascota.pk %}" class="btn btn-outline-primary w-100">Ver Detalles</a> 

¿Qué hace exactamente esa línea de código?

La línea original que teníamos en la tarjeta de Bootstrap era estática: <a href="#" ...>. El símbolo # le decía al navegador "no vayas a ningún lado, quédate en esta misma página".

Al cambiarla por <a href="{% url 'mascotas:detalle_mascota' mascota.pk %}" ...>, activamos el motor de plantillas de Django para generar enlaces dinámicos. 

¿Por qué se hizo este cambio?

1. Para conectar la Arquitectura (Navegabilidad)
Antes de este cambio, teníamos la "Vista de Lista" (donde ves todas las mascotas resumidas) y habíamos creado la "Vista de Detalle" (donde ves la foto en grande y toda la información), pero estaban desconectadas. Este cambio es el puente literal entre ambas pantallas.

2. Para completar el ciclo del CRUD
Este botón dinámico es lo que permite al usuario ejecutar la acción de Leer (Read) , navegando desde el directorio general hacia el registro específico en la base de datos PostgreSQL, para luego habilitarle los botones de Actualizar (Update) y Eliminar (Delete) si es el dueño de la publicación.

# 26 Siguiendo nuestra metodología, el siguiente gran bloque es el Paso 27: Implementar autenticación. De acuerdo con la rúbrica, debemos garantizar un sistema robusto que contemple el registro de usuarios, el inicio de sesión y el cierre de sesión, decisión técnica: En lugar de reinventar la rueda, utilizaremos el robusto sistema de autenticación nativo de Django (LoginView y LogoutView). Sin embargo, dado que usamos un modelo CustomUser donde el correo es el identificador, debemos crear un formulario de registro personalizado que herede de UserCreationForm y 

# 27 Creamos usuarios/forms.py Inyectamos clases de Bootstrap 5 directamente en los campos y le indicamos explícitamente a Django que use CustomUser y sus campos requeridos para la creación de la cuenta, creamos la vista también usuarios/views.py, de ahi las urls. aqui mapeamos las rutas /registro/, /login/ y /logout/. Al cerrar sesión, el usuario será redirigido automáticamente a la lista principal de mascotas perdidas. Ahora conectamos las rutas al proyecto y configuramos las redirecciones (modificando core/urls.py) Agregamos a settings.py:

# Configuración de URLs de Autenticación
LOGIN_URL = 'usuarios:login'
LOGIN_REDIRECT_URL = 'mascotas:lista_mascotas'
LOGOUT_REDIRECT_URL = 'mascotas:lista_mascotas'

LOGIN_URL es crucial: si un usuario anónimo intenta acceder a una ruta protegida (como reportar una mascota), los mixins de seguridad de Django lo redirigirán automáticamente a esta dirección

# 28 Teniendo la lógica del backend asegurada, vamos a construir la interfaz gráfica para cumplir con los requerimientos de Registro de usuarios, Inicio de sesión y Cierre de sesión. Decisión técnica: Crearemos estas plantillas utilizando el sistema de herencia de Django anclado a Bootstrap 5. En el registro es vital incluir el atributo enctype="multipart/form-data" en el formulario HTML para habilitar la subida del avatar opcional. Además, actualizaremos nuestro base.html para que el menú de navegación reaccione dinámicamente si el usuario es un visitante o alguien que ya inició sesión.

# 29 Primero creamos las carpetas template/usuarios en usuarios y de ahi haremos registro.html aqui renderizamos el CustomUserCreationForm que construimos previamente. Añadimos un diseño en formato de tarjeta centrado y un enlace de conveniencia para quienes ya tengan cuenta. En la misma carpeta, crea el archivo para que los usuarios ingresen login.html

# 30 Para que el usuario pueda navegar hacia estas nuevas vistas, necesitamos reemplazar el código de nuestro archivo principal, sustituyendo los botones falsos que habíamos puesto por rutas reales, en Django 5, cerrar sesión requiere obligatoriamente una petición POST por seguridad, por lo que transformaremos el enlace de "Cerrar sesión" en un pequeño formulario.

Añadimos la lógica condicional que verifica si el usuario tiene una foto de perfil antes de intentar renderizarla para evitar errores, y configuramos los accesos para que un visitante normal pueda llegar a la página de creación de cuenta.

# 31 Para dar por terminado el Paso 11: Implementar autenticación al 100% y cumplir estrictamente con la rúbrica, nos faltan dos funcionalidades críticas: el Cambio de contraseña y el Restablecimiento de contraseña mediante correo.

# 31.1 Decisión técnica: En vez de programar toda la lógica criptográfica y de generación de tokens desde cero, heredaremos las Vistas Basadas en Clases (CBV) de seguridad nativas de Django (PasswordResetView, PasswordChangeView, etc.). Además, para probar el restablecimiento por correo en nuestra computadora sin tener que configurar un servidor SMTP real de inmediato, configuraremos Django para que "imprima" el correo electrónico simulado directamente la terminal usando console.EmailBackend.

# 32 Modificamos core/settings.py al definir EMAIL_BACKEND apuntando a console.EmailBackend, Django interceptará cualquier correo electrónico que el sistema intente enviar (como el enlace con el token de recuperación) y lo imprimirá como texto plano en tu terminal de VS Code, permitiéndonos probar el flujo sin depender de servicios externos.

# 33 Vamos a mapear todas las vistas necesarias para que Django sepa a dónde dirigir al usuario en cada etapa del proceso de contraseñas. En usuarios/urls.py hemos integrado el ciclo de vida completo dictado por las buenas prácticas de seguridad web: Solicitar cambio, Confirmar envío, Validar Token único y Confirmar éxito. Sobrescribimos la variable template_name en cada una de ellas para poder inyectarles nuestro diseño con Bootstrap 5 en el siguiente paso.

# 34 Para cumplir con el requisito de Restablecimiento de contraseña mediante correo, necesitamos crear la interfaz visual para los cuatro pasos de este proceso.

# 34.1 Decisión técnica: Crearemos estas cuatro plantillas dentro de la carpeta usuarios/templates/usuarios,  heredaremos de base.html y usaremos el diseño de tarjetas (cards) de Bootstrap 5 para mantener la coherencia visual con tu formulario de inicio de sesión y registro. Empezando con password_reset_form.html -> password_reset_done -> password_reset_confirm y password_reset_complete.html.

Por seguridad aqui hicimos nuestro segundo commit :p

# 34.2 Creamos password_reset_email.html este archivo de plantilla no requiere etiquetas HTML, clases de Bootstrap ni heredar de base.html. Su única función es actuar como texto plano donde Django inyecta los tokens criptográficos de un solo uso (uidb64 y token) para garantizar la seguridad de la cuenta al generar el enlace de recuperación.

# 35 Ahora vamos a implementar la funcionalidad de búsqueda (por especie, raza o ubicación) recomendada por tu rúbrica como "Requisito Diferenciador".

Decisión técnica: Para implementar un buscador eficiente sin instalar librerías pesadas de terceros, utilizaremos el objeto Q nativo de Django. Esto nos permite hacer consultas complejas con el operador lógico OR en nuestra base de datos PostgreSQL, buscando coincidencias simultáneas en múltiples campos (nombre, especie, raza o ubicación). Además, usaremos el método GET en el formulario HTML para que las búsquedas se puedan compartir mediante URL.

# 36 Modificamos mascotas/views.py y mascota_list.py

# 37 Se nos ocurrio hacer un live search en vez de la barra normal asi que tomamos la decisión técnica de usar Vanilla JavaScript (el JavaScript puro del navegador) utilizando la API Fetch. Haremos que JavaScript escuche cada vez que tecleas una letra, envíe la petición al servidor en segundo plano, extraiga las tarjetas resultantes y las reemplace en la pantalla sin que la página parpadee. Además, implementaremos una técnica vital de nivel Senior llamada "Debounce": esto hace que el sistema espere unos milisegundos (ej. 300ms) después de tu última tecla antes de buscar. Si no hacemos esto, buscar la palabra "Perro" haría 5 consultas a tu base de datos PostgreSQL, colapsando el servidor.

# 38 Ahora pasaremos a la creación de mínimo 5 pruebas funcionales:

Test de modelo.

Test de registro.

Test de login.

Test de creación de entidad.

Test de vista protegida.

# Decisión técnica: Utilizaremos el framework nativo django.test.TestCase. La gran ventaja de esta herramienta es que Django creará una base de datos en blanco especial para las pruebas, ejecutará nuestras funciones, y luego la destruirá. Así garantizamos que tu base de datos principal de PostgreSQL jamás se ensucie con datos de prueba.

# 39 Modificamos usuarios/tests.py con esto cumplimos con las primeras tres pruebas obligatorias. Probamos la inserción en el modelo de base de datos, verificamos que la vista de registro devuelva un código HTTP 200 (Éxito), y validamos que el motor de autenticación acepte el inicio de sesión y nos pasamos a mascotas/tests.py con esto Completamos las 5 pruebas de la rúbrica validando la creación de la entidad principal y asegurándonos de que nuestro LoginRequiredMixin funciona correctamente bloqueando la ruta a usuarios que no hayan iniciado sesión. Y pasamos a la ejecucion de las pruebas con el comando python manage.py test y todo falló jajajaja como se muestra en la imagen, veremos que pasó.

Si leemos la última línea de cualquiera de los errores en tu consola, dice:
TypeError: UserManager.create_user() missing 1 required positional argument: 'username'

Cuando construimos nuestro CustomUser, decidimos heredar de AbstractUser para no tener que programar el sistema de encriptación desde cero. Sin embargo, el administrador de usuarios por defecto de Django (UserManager) sigue exigiendo internamente el campo username al usar la función create_user() en el código puro (como en nuestras pruebas), a pesar de que para la interfaz web ya le dijimos que el inicio de sesión es con email.

La solución es extremadamente sencilla y limpia: solo necesitamos pasarle un username simulado a nuestros usuarios de prueba en los archivos tests.py.

# 39_2 Listo, los test pasaron, ahora guardaremos el progreso en git.

# 40 Pasamos a agregar los estilos y hacer que la pagina se vea presentable. Creamos en static la carpeta css y style.css y modificamos el base.html para que lo cargue

# 41 Decidimos transformar esa interfaz de un diseño básico a una experiencia Neumórfica / Googlesque (limpia, redondeada, colores pastel) y le inyectaremos luz neón siguiendo el cursor usando Vanilla JavaScript y CSS moderno.
Vamos a decirle a Django que el Directorio ya no es público. Si alguien entra sin cuenta, lo mandará directamente a la pantalla de login.
Modificamos mascotas/views.py 

# 42 Modificamos todo el css, agregamos unos logos, movimos de lugar unas cosas y ya todo bien.