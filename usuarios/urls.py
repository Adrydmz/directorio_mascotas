from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Autenticación base
    path('registro/', views.RegistroUsuarioView.as_view(), name='registro'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='mascotas:lista_mascotas'), name='logout'),

    # ----------------------------------------------------------------------
    # Cambio de contraseña (cuando el usuario SÍ recuerda su contraseña actual)
    # ----------------------------------------------------------------------
    path('cambiar-password/', auth_views.PasswordChangeView.as_view(
        template_name='usuarios/password_change_form.html',
        success_url='/usuarios/cambiar-password/hecho/'
    ), name='password_change'),
    
    path('cambiar-password/hecho/', auth_views.PasswordChangeDoneView.as_view(
        template_name='usuarios/password_change_done.html'
    ), name='password_change_done'),

    # ----------------------------------------------------------------------
    # Restablecimiento de contraseña (cuando el usuario OLVIDÓ su contraseña)
    # ----------------------------------------------------------------------
    path('recuperar-password/', auth_views.PasswordResetView.as_view(
        template_name='usuarios/password_reset_form.html',
        email_template_name='usuarios/password_reset_email.html',
        success_url='/usuarios/recuperar-password/enviado/'
    ), name='password_reset'),
    
    path('recuperar-password/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='usuarios/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('recuperar-password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='usuarios/password_reset_confirm.html',
        success_url='/usuarios/recuperar-password/completo/'
    ), name='password_reset_confirm'),
    
    path('recuperar-password/completo/', auth_views.PasswordResetCompleteView.as_view(
        template_name='usuarios/password_reset_complete.html'
    ), name='password_reset_complete'),
]