from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Formulario para el registro de nuevos usuarios.
    Extiende el formulario nativo para anclarlo a nuestro CustomUser.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # El email es obligatorio por nuestro modelo, agregamos first y last name como extras
        fields = ('email', 'first_name', 'last_name', 'avatar')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@correo.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }