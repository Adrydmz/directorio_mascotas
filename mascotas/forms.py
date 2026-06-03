from django import forms
from .models import MascotaPerdida

class MascotaPerdidaForm(forms.ModelForm):
    """
    Formulario basado en el modelo MascotaPerdida.
    Inyectamos las clases de Bootstrap 5 (form-control, form-select) 
    directamente en los widgets para mantener los templates limpios.
    """
    class Meta:
        model = MascotaPerdida
        fields = ['nombre', 'especie', 'raza', 'ubicacion', 'recompensa', 'estado', 'fotografia']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Firulais'}),
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'raza': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Labrador'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Parque Central'}),
            'recompensa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 500.00'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'fotografia': forms.FileInput(attrs={'class': 'form-control'}),
        }