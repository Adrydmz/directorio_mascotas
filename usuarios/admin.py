from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Registra el CustomUser en el panel de administración.
    Añadimos el avatar a las pantallas de visualización.
    """
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('avatar',)}),
    )