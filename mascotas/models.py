from django.db import models
from django.conf import settings

class MascotaPerdida(models.Model):
    """
    Modelo principal para el directorio de mascotas perdidas.
    Cumple con el requisito de CRUD completo y subida de imágenes.
    """
    ESPECIE_CHOICES = [
        ('PERRO', 'Perro'),
        ('GATO', 'Gato'),
        ('AVE', 'Ave'),
        ('OTRO', 'Otro'),
    ]

    ESTADO_CHOICES = [
        ('PERDIDA', 'Perdida'),
        ('ENCONTRADA', 'Encontrada'),
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre de la mascota')
    especie = models.CharField(max_length=20, choices=ESPECIE_CHOICES, verbose_name='Especie')
    raza = models.CharField(max_length=100, verbose_name='Raza')
    ubicacion = models.CharField(max_length=255, verbose_name='Ubicación de extravío')
    recompensa = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Recompensa ofertada')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PERDIDA', verbose_name='Estado')
    fotografia = models.ImageField(upload_to='mascotas/', verbose_name='Fotografía principal')
    fecha_reporte = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de reporte')
    
    usuario_reporta = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='mascotas_reportadas',
        verbose_name='Usuario que reporta'
    )

    class Meta:
        verbose_name = 'Mascota Perdida'
        verbose_name_plural = 'Mascotas Perdidas'
        ordering = ['-fecha_reporte']

    def __str__(self):
        return f"{self.nombre} - {self.especie} ({self.get_estado_display()})"


class Avistamiento(models.Model):
    """
    Modelo adicional para cumplir el requisito de relaciones (ForeignKey).
    Registra cuando alguien ve a una mascota reportada.
    """
    mascota = models.ForeignKey(
        MascotaPerdida, 
        on_delete=models.CASCADE, 
        related_name='avistamientos',
        verbose_name='Mascota avistada'
    )
    usuario_reporta = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name='Usuario que reporta avistamiento'
    )
    ubicacion_avistamiento = models.CharField(max_length=255, verbose_name='Ubicación del avistamiento')
    fecha_avistamiento = models.DateTimeField(auto_now_add=True, verbose_name='Fecha del avistamiento')
    descripcion = models.TextField(verbose_name='Descripción de cómo y dónde se vio')
    foto_evidencia = models.ImageField(upload_to='avistamientos/', null=True, blank=True, verbose_name='Foto de evidencia')

    class Meta:
        verbose_name = 'Avistamiento'
        verbose_name_plural = 'Avistamientos'
        ordering = ['-fecha_avistamiento']

    def __str__(self):
        return f"Avistamiento de {self.mascota.nombre} en {self.ubicacion_avistamiento}"

# NUEVA TABLA: Sistema de Mensajería Directa
class MensajeContacto(models.Model):
    """
    Gestiona los mensajes enviados entre usuarios (máximo 5 por día según requerimientos).
    """
    remitente = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='mensajes_enviados',
        verbose_name='Remitente'
    )
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='mensajes_recibidos',
        verbose_name='Destinatario'
    )
    mascota = models.ForeignKey(
        MascotaPerdida, 
        on_delete=models.CASCADE, 
        related_name='consultas',
        verbose_name='Mascota en cuestión'
    )
    mensaje = models.TextField(max_length=500, verbose_name='Mensaje')
    fecha_envio = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de envío')

    class Meta:
        verbose_name = 'Mensaje de Contacto'
        verbose_name_plural = 'Mensajes de Contacto'
        ordering = ['-fecha_envio'] # Los más recientes primero

    def __str__(self):
        return f"De {self.remitente.email} a {self.destinatario.email} sobre {self.mascota.nombre}"