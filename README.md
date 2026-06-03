# Bitácora de desarrollo

## 1. Requerimientos del proyecto

- Proyecto: Directorio de mascotas perdidas.
- Stack tecnológico: Python 3.12, Django 5.x, PostgreSQL (prohibido SQLite) y Bootstrap 5.
- Modelo de usuario: CustomUser extendiendo `AbstractUser` o `AbstractBaseUser`.
- Entidad principal: `MascotaPerdida`.
- Campos requeridos: Nombre, Especie, Raza, Ubicación, Recompensa, Estado (encontrada/no encontrada), Fotografía y Fecha de reporte.
- Relaciones: `ForeignKey` hacia `CustomUser` (Usuario Reporta) y hacia un modelo `Avistamiento`.
- Infraestructura: despliegue final en Oracle Cloud Infrastructure (OCI) con IP pública.
- Seguridad: uso estricto de variables de entorno para credenciales y configuraciones sensibles.

---

## 2. Instalación y configuración base

Se descargó Python 3.12, Git, PostgreSQL y Visual Studio Code.

### 2.1. Preparación del entorno

```bash
mkdir directorio_mascotas
cd directorio_mascotas
python -m venv venv
venv\Scripts\activate
```

### 2.2. Inicialización de Git

```bash
git init
```

### 2.3. Dependencias del proyecto

Contenido de `requirements.txt`:

```text
Django>=5.0,<5.1
psycopg2-binary>=2.9.9
Pillow>=10.2.0
python-dotenv>=1.0.1
gunicorn>=21.2.0
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

> Nota: definimos versiones exactas para garantizar compatibilidad. `psycopg2-binary` es el conector para PostgreSQL, `Pillow` maneja la subida de imágenes, `python-dotenv` gestiona variables de entorno y `gunicorn` será el servidor de OCI.

### 2.4. Archivo de entorno

Se creó `.env` con el siguiente template:

```env
SECRET_KEY=tu_secret_key_aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=mascotas_db
DB_USER=postgres
DB_PASSWORD=tu_password_aqui
DB_HOST=localhost
DB_PORT=5432
```

---

## 3. Creación de la estructura Django

### 3.1. Inicio del proyecto y apps

```bash
django-admin startproject core .
python manage.py startapp usuarios
python manage.py startapp mascotas
```

> Se nombró el proyecto principal como `core` para mantener la estructura de carpetas clara y estándar. La separación en dos apps (`usuarios` y `mascotas`) sigue el principio de responsabilidad única.

### 3.2. Herramienta de base de datos

Se instaló DBeaver para gestionar la base de datos PostgreSQL.

---

## 4. Configuración del repositorio Git y primer push

### 4.1. Configuración de usuario Git

```bash
git --version
git config --global user.name "xxx"
git config --global user.email "x@x.xxx"
```

### 4.2. Preparación de `.gitignore`

Se agregó `.gitignore` para excluir archivos locales y de entorno.

### 4.3. Limpieza de `venv` del índice

```bash
git reset
git restore --staged .
git rm -r --cached venv
git status
```

### 4.4. Commit inicial y remoto

```bash
git add .gitignore
git add .
git commit -m "El commit"
git branch -M main
git remote add origin git@github.com:Adrydmz/directorio_mascotas.git
```

### 4.5. Configuración de SSH

```bash
ssh-keygen -t ed25519 -C "x@x.xxx"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub | clip
ssh -T git@github.com
git push -u origin main
```

---

## 5. Configuración de PostgreSQL y migraciones

### 5.1. Primeras migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

Resultado esperado: aplicar migraciones de `admin`, `auth`, `contenttypes` y `sessions`.

### 5.2. Ajustes de configuración

Se modificó `settings.py` para eliminar rastros de SQLite y conectar PostgreSQL usando las variables del `.env`.

### 5.3. Definición del modelo de usuario

Se creó `usuarios/models.py` con un `CustomUser` que usa `email` como identificador y permite avatar opcional.

> Se requirió declarar `AUTH_USER_MODEL` en `settings.py`.

---

## 6. Ajustes de archivos y estructura de recursos

### 6.1. Carpetas estáticas y de media

Se crearon las carpetas `static/` y `media/` en la raíz para evitar warnings y soportar archivos subidos.

### 6.2. Usuario administrador

Se creó el superusuario con el correo personal.

---

## 7. Desarrollo del CRUD de mascotas

### 7.1. Definición de modelos

Se creó el modelo `MascotaPerdida` y el modelo `Avistamiento` dentro de `mascotas`.

### 7.2. Migraciones específicas de la app

```bash
python manage.py makemigrations mascotas
python manage.py migrate
```

### 7.3. Vista de desarrollo local

```bash
python manage.py runserver
```

### 7.4. Formularios y lógica de negocio

Se creó `mascotas/forms.py` para validar los campos y aplicar clases de Bootstrap 5. El campo `usuario_reporta` se asigna automáticamente en la vista.

### 7.5. CRUD completo

Se implementó el CRUD en `mascotas/views.py` con `LoginRequiredMixin` y `form_valid` personalizado para asignar el usuario actual.

### 7.6. Rutas RESTful

Se agregó `mascotas/urls.py` con rutas claras y RESTful que usan `<int:pk>` para identificar registros.

---

## 8. Integración de rutas y plantillas

### 8.1. Enrutado principal

Se actualizó `core/urls.py` para incluir las rutas de `mascotas` y permitir servir archivos media en desarrollo.

### 8.2. Plantillas base

Se creó `templates/base.html` con herencia de plantillas y carga de Bootstrap 5 vía CDN.

### 8.3. Plantillas de mascotas

Se creó la carpeta `mascotas/templates/mascotas` y se añadieron:

- `mascota_list.html`
- `mascota_form.html`
- `mascota_detail.html`
- `mascota_confirm_delete.html`

Se usó `enctype="multipart/form-data"` y `{% csrf_token %}` en los formularios para subir imágenes con seguridad.

---

## 9. Navegación entre lista y detalle

### 9.1. Enlace dinámico de detalle

Se cambió el botón estático:

```html
<a href="#" class="btn btn-outline-primary w-100">Ver Detalles</a>
```

por:

```django
<a href="{% url 'mascotas:detalle_mascota' mascota.pk %}" class="btn btn-outline-primary w-100">Ver Detalles</a>
```

### 9.2. Por qué este cambio

- Conecta la vista de lista con la vista de detalle.
- Completa el ciclo CRUD: ahora el usuario puede ver un registro específico y acceder a editar o eliminar si es el autor.

---

## 10. Implementación de autenticación

### 10.1. Estrategia general

Se decidió usar el sistema nativo de Django (`LoginView`, `LogoutView`) y un formulario de registro personalizado para `CustomUser`.

### 10.2. Formularios y vistas

Se creó `usuarios/forms.py` y `usuarios/views.py`, además de las rutas en `usuarios/urls.py` para:

- `/registro/`
- `/login/`
- `/logout/`

### 10.3. Redirecciones y configuraciones

En `settings.py` se agregó:

```python
LOGIN_URL = 'usuarios:login'
LOGIN_REDIRECT_URL = 'mascotas:lista_mascotas'
LOGOUT_REDIRECT_URL = 'mascotas:lista_mascotas'
```

> `LOGIN_URL` es clave para redirigir automáticamente a usuarios anónimos que intenten acceder a rutas protegidas.

---

## 11. Interfaz de usuario para autenticación

### 11.1. Plantillas de usuario

Se crearon las plantillas dentro de `usuarios/templates/usuarios` para:

- `registro.html`
- `login.html`
- `password_reset_form.html`
- `password_reset_done.html`
- `password_reset_confirm.html`
- `password_reset_complete.html`

### 11.2. Formularios de registro

Se usó `enctype="multipart/form-data"` para permitir subida de avatar opcional.

### 11.3. Menú dinámico

Se actualizó `base.html` para que muestre opciones distintas según si el usuario está autenticado o no.

---

## 12. Recuperación y cambio de contraseña

### 12.1. Decisión técnica

Se reutilizaron las vistas nativas de Django para manejar:

- `PasswordResetView`
- `PasswordChangeView`
- `PasswordResetConfirmView`
- `PasswordResetDoneView`
- `PasswordResetCompleteView`

### 12.2. Backend de email de desarrollo

Se configuró `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` en `core/settings.py` para que los correos se impriman en terminal en lugar de enviarse.

---

## 13. Rutas de restablecimiento de contraseña

Se mapeó el ciclo completo en `usuarios/urls.py` con las plantillas personalizadas y se aseguró que Django reciba los tokens y las redirecciones correctas.

### 13.1. Plantilla de email

Se agregó `password_reset_email.html` como plantilla de texto plano para el enlace seguro de recuperación.

---

## 14. Funcionalidad diferenciadora: búsqueda

### 14.1. Búsqueda por campos

Se implementó un buscador que consulta por `especie`, `raza` o `ubicación`.

### 14.2. Uso de `Q`

Se utilizó `django.db.models.Q` para construir búsquedas con `OR` en múltiples campos.

### 14.3. Método GET

El formulario de búsqueda usa método `GET` para que los resultados sean compartibles por URL.

---

## 15. Live search con JavaScript

Se decidió mejorar la búsqueda con JavaScript puro y `fetch`.

- Se escucha cada tecla del usuario.
- Se envía la petición en segundo plano.
- Se actualizan las tarjetas sin recargar la página.
- Se aplicó `debounce` para evitar muchas consultas simultáneas.

> Esto evita que buscar "Perro" genere varias consultas rápidas a PostgreSQL.

---

## 16. Pruebas funcionales

### 16.1. Objetivos mínimos

Se crearon al menos 5 pruebas funcionales:

- Test de modelo.
- Test de registro.
- Test de login.
- Test de creación de entidad.
- Test de vista protegida.

### 16.2. Enfoque técnico

Se usó `django.test.TestCase` para que Django cree una base de datos de prueba temporal y no afecte la base de datos principal.

### 16.3. Ajuste importante

En `usuarios/tests.py` y `mascotas/tests.py` se detectó el error:

```text
TypeError: UserManager.create_user() missing 1 required positional argument: 'username'
```

> El problema se debía a que `UserManager` de Django aún exige el campo `username` en el código de prueba, aunque en la interfaz se use `email`. La solución fue pasar un `username` simulado en los tests.

### 16.4. Resultado

Los tests pasaron después de corregir el manejo de `username` en los datos de prueba.

---

## 17. Estilos y presentación

### 17.1. CSS personalizado

Se creó `static/css/style.css` y se enlazó en `base.html`.

### 17.2. Diseño visual

Se transformó la interfaz básica en una experiencia más moderna y limpia, con un estilo tipo neumorphism / Googlesque.

### 17.3. Interactividad visual

Se añadió JavaScript para efectos de luz y movimiento, manteniendo la UI responsiva y agradable.

---

## 18. Restricción de acceso al directorio

Se decidió que el directorio solo sea accesible para usuarios autenticados.

- Usuarios anónimos son redirigidos a la pantalla de login.
- Se fortaleció la seguridad en `mascotas/views.py`.

---

## 19. Resumen de comandos clave utilizados

```bash
git --version
git config --global user.name "xxx"
git config --global user.email "x@x.xxx"
git init
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
django-admin startproject core .
python manage.py startapp usuarios
python manage.py startapp mascotas
git reset
git restore --staged .
git rm -r --cached venv
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
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## 20. Observaciones finales

Este documento ahora resume de forma estructurada los avances del proyecto, separa el trabajo por etapas, y mantiene un estilo limpio con títulos coherentes y visibles.
 
