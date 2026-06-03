from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MascotaPerdida
from .forms import MascotaPerdidaForm

class MascotaListView(ListView):
    """Vista pública para listar todas las mascotas (Read)."""
    model = MascotaPerdida
    template_name = 'mascotas/mascota_list.html'
    context_object_name = 'mascotas'

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