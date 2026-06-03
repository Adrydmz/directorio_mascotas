from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Autenticación base
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='mascotas:lista_mascotas'), name='logout'),
    path('registro/', views.RegistroUsuarioView.as_view(), name='registro'),
    
    # ----------------------------------------------------------------------
    # NUEVO: Verificación de correo al registrarse (Código 6 dígitos)
    # ----------------------------------------------------------------------
    path('verificar-registro/', views.VerificarRegistroView.as_view(), name='verificar_registro'),
    
    # ----------------------------------------------------------------------
    # NUEVO: Restablecimiento de contraseña (Código 6 dígitos)
    # ----------------------------------------------------------------------
    path('recuperar-password/', views.OlvidePasswordView.as_view(), name='password_reset'),
    path('recuperar-password/verificar/', views.VerificarCodigoPasswordView.as_view(), name='password_reset_verificar'),
    path('recuperar-password/nueva/', views.NuevaPasswordView.as_view(), name='password_reset_nueva'),

    # ----------------------------------------------------------------------
    # CONSERVADO: Cambio de contraseña (usuario logueado que sabe su clave actual)
    # ----------------------------------------------------------------------
    path('cambiar-password/', auth_views.PasswordChangeView.as_view(
        template_name='usuarios/password_change_form.html',
        success_url='/usuarios/cambiar-password/hecho/'
    ), name='password_change'),
    
    path('cambiar-password/hecho/', auth_views.PasswordChangeDoneView.as_view(
        template_name='usuarios/password_change_done.html'
    ), name='password_change_done'),
]