import random
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado para el sistema.
    Reemplaza el inicio de sesión por defecto de 'username' a 'email'.
    """
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Avatar')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    # NUEVO: Para saber si ya puso su código de validación de correo
    correo_verificado = models.BooleanField(default=False, verbose_name='Correo verificado')

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

# NUEVA TABLA: Para manejar los códigos de 6 dígitos temporales
class CodigoVerificacion(models.Model):
    TIPOS = (
        ('REGISTRO', 'Registro'),
        ('PASSWORD', 'Recuperar Contraseña'),
    )
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='codigos')
    codigo = models.CharField(max_length=6, verbose_name='Código de 6 dígitos')
    tipo = models.CharField(max_length=20, choices=TIPOS, verbose_name='Tipo de código')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Si no tiene código al guardarse, genera uno aleatorio de 6 dígitos automáticamente
        if not self.codigo:
            self.codigo = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Código de Verificación'
        verbose_name_plural = 'Códigos de Verificación'

    def __str__(self):
        return f"Código {self.tipo} para {self.usuario.email}"