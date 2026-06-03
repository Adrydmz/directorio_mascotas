from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomUserCreationForm

class RegistroUsuarioView(SuccessMessageMixin, CreateView):
    """Vista pública para que nuevos usuarios creen una cuenta."""
    template_name = 'usuarios/registro.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('usuarios:login')
    success_message = "¡Tu cuenta ha sido creada exitosamente! Por favor, inicia sesión."

class CustomLoginView(LoginView):
    """Vista pública para iniciar sesión."""
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True