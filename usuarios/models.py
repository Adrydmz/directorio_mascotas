from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado para el sistema.
    Reemplaza el inicio de sesión por defecto de 'username' a 'email'.
    """
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Avatar')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    # Establecemos el correo electrónico como el método principal de autenticación
    USERNAME_FIELD = 'email'
    
    # Al crear un superusuario por consola, nos pedirá estos campos
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        # TRUCO: Si no viene un username, le asignamos el valor del email automáticamente
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email