from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import MascotaPerdida
from .forms import MascotaPerdidaForm

# Agregamos LoginRequiredMixin aquí para forzar el "Login Directo"
class MascotaListView(LoginRequiredMixin, ListView):
    """Vista protegida para listar todas las mascotas con buscador integrado."""
    model = MascotaPerdida
    template_name = 'mascotas/mascota_list.html'
    context_object_name = 'mascotas'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(especie__icontains=query) |
                Q(raza__icontains=query) |
                Q(ubicacion__icontains=query)
            )
        return queryset

class MascotaDetailView(DetailView):
    """Vista pública para ver los detalles de una mascota específica."""
    model = MascotaPerdida
    template_name = 'mascotas/mascota_detail.html'
    context_object_name = 'mascota'

class MascotaCreateView(LoginRequiredMixin, CreateView):
    """Vista protegida para reportar una mascota (Create)."""
    model = MascotaPerdida
    form_class = MascotaPerdidaForm
    template_name = 'mascotas/mascota_form.html'
    success_url = reverse_lazy('mascotas:lista_mascotas')

    def form_valid(self, form):
        # Asignar automáticamente el usuario autenticado como el creador del reporte
        form.instance.usuario_reporta = self.request.user
        return super().form_valid(form)

class MascotaUpdateView(LoginRequiredMixin, UpdateView):
    """Vista protegida para editar el reporte de una mascota (Update)."""
    model = MascotaPerdida
    form_class = MascotaPerdidaForm
    template_name = 'mascotas/mascota_form.html'
    success_url = reverse_lazy('mascotas:lista_mascotas')

class MascotaDeleteView(LoginRequiredMixin, DeleteView):
    """Vista protegida para eliminar un reporte (Delete)."""
    model = MascotaPerdida
    template_name = 'mascotas/mascota_confirm_delete.html'
    success_url = reverse_lazy('mascotas:lista_mascotas')