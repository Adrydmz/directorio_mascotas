from django.contrib import admin
from .models import MascotaPerdida, Avistamiento

@admin.register(MascotaPerdida)
class MascotaPerdidaAdmin(admin.ModelAdmin):
    """Configuración de visualización en panel para mascotas."""
    list_display = ('nombre', 'especie', 'estado', 'fecha_reporte', 'usuario_reporta')
    list_filter = ('estado', 'especie', 'fecha_reporte')
    search_fields = ('nombre', 'raza', 'ubicacion')

@admin.register(Avistamiento)
class AvistamientoAdmin(admin.ModelAdmin):
    """Configuración de visualización en panel para avistamientos."""
    list_display = ('mascota', 'ubicacion_avistamiento', 'fecha_avistamiento', 'usuario_reporta')
    search_fields = ('ubicacion_avistamiento', 'descripcion')