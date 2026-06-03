from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import MascotaPerdida, MensajeContacto
from .forms import MascotaPerdidaForm

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

# ==========================================
# NUEVO: LÓGICA DE MENSAJERÍA
# ==========================================

class EnviarMensajeView(LoginRequiredMixin, View):
    """Procesa el envío inicial desde la tarjeta de la mascota."""
    def post(self, request, pk):
        mascota = get_object_or_404(MascotaPerdida, pk=pk)
        if mascota.usuario_reporta == request.user:
            messages.error(request, 'No puedes enviarte mensajes a ti mismo.')
            return redirect('mascotas:detalle_mascota', pk=pk)
            
        hoy = timezone.now().date()
        if MensajeContacto.objects.filter(remitente=request.user, fecha_envio__date=hoy).count() >= 5:
            messages.error(request, 'Has alcanzado el límite de 5 mensajes diarios.')
            return redirect('mascotas:detalle_mascota', pk=pk)
            
        texto = request.POST.get('mensaje')
        if texto:
            MensajeContacto.objects.create(
                remitente=request.user,
                destinatario=mascota.usuario_reporta,
                mascota=mascota,
                mensaje=texto
            )
            messages.success(request, '¡Mensaje enviado exitosamente!')
        return redirect('mascotas:detalle_mascota', pk=pk)

# ==========================================
# NUEVO: LÓGICA DE RESPUESTA Y BANDEJA
# ==========================================

class EnviarMensajeView(LoginRequiredMixin, View):
    """Procesa el envío inicial desde la tarjeta de la mascota."""
    def post(self, request, pk):
        mascota = get_object_or_404(MascotaPerdida, pk=pk)
        if mascota.usuario_reporta == request.user:
            messages.error(request, 'No puedes enviarte mensajes a ti mismo.')
            return redirect('mascotas:detalle_mascota', pk=pk)
            
        hoy = timezone.now().date()
        if MensajeContacto.objects.filter(remitente=request.user, fecha_envio__date=hoy).count() >= 5:
            messages.error(request, 'Has alcanzado el límite de 5 mensajes diarios.')
            return redirect('mascotas:detalle_mascota', pk=pk)
            
        texto = request.POST.get('mensaje')
        if texto:
            MensajeContacto.objects.create(
                remitente=request.user,
                destinatario=mascota.usuario_reporta,
                mascota=mascota,
                mensaje=texto
            )
            messages.success(request, '¡Mensaje enviado exitosamente!')
        return redirect('mascotas:detalle_mascota', pk=pk)


# --- REEMPLAZA EL BLOQUE DE MENSAJERÍA AL FINAL DE TU ARCHIVO CON ESTO ---

class EnviarMensajeView(LoginRequiredMixin, View):
    """Procesa el envío inicial desde la tarjeta de la mascota."""
    def post(self, request, pk):
        mascota = get_object_or_404(MascotaPerdida, pk=pk)
        if mascota.usuario_reporta == request.user:
            messages.error(request, 'No puedes enviarte mensajes a ti mismo.')
            return redirect('mascotas:detalle_mascota', pk=pk)
            
        hoy = timezone.now().date()
        if MensajeContacto.objects.filter(remitente=request.user, fecha_envio__date=hoy).count() >= 5:
            messages.error(request, 'Has alcanzado el límite de 5 mensajes diarios.')
            return redirect('mascotas:detalle_mascota', pk=pk)
            
        texto = request.POST.get('mensaje')
        if texto:
            MensajeContacto.objects.create(
                remitente=request.user,
                destinatario=mascota.usuario_reporta,
                mascota=mascota,
                mensaje=texto
            )
            messages.success(request, '¡Mensaje enviado exitosamente!')
        return redirect('mascotas:detalle_mascota', pk=pk)


class ResponderMensajeView(LoginRequiredMixin, View):
    """Permite contestarle al usuario dentro del mismo hilo de chat."""
    def post(self, request, msj_id):
        mensaje_original = get_object_or_404(MensajeContacto, pk=msj_id)
        
        hoy = timezone.now().date()
        if MensajeContacto.objects.filter(remitente=request.user, fecha_envio__date=hoy).count() >= 5:
            messages.error(request, 'Has alcanzado el límite de 5 mensajes diarios.')
            return redirect('mascotas:bandeja_mensajes')
            
        texto = request.POST.get('mensaje')
        if texto:
            destinatario = mensaje_original.destinatario if mensaje_original.remitente == request.user else mensaje_original.remitente
            
            MensajeContacto.objects.create(
                remitente=request.user,
                destinatario=destinatario,
                mascota=mensaje_original.mascota,
                mensaje=texto
            )
            
            # NUEVO: Recordar qué chat debe permanecer abierto tras la recarga
            request.session['chat_abierto_persona'] = destinatario.pk
            request.session['chat_abierto_mascota'] = mensaje_original.mascota.pk
            
            messages.success(request, '¡Respuesta enviada al chat!')
            
        return redirect('mascotas:bandeja_mensajes')


class BandejaMensajesView(LoginRequiredMixin, TemplateView):
    """Bandeja que unifica enviados y recibidos en verdaderos hilos de chat cronológicos."""
    template_name = 'mascotas/bandeja_mensajes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        todos_mensajes = MensajeContacto.objects.filter(
            Q(remitente=user) | Q(destinatario=user)
        ).select_related('remitente', 'destinatario', 'mascota').order_by('fecha_envio')
        
        conversaciones = {}
        for msj in todos_mensajes:
            otra_persona = msj.destinatario if msj.remitente == user else msj.remitente
            llave = f"{otra_persona.pk}_{msj.mascota.pk}"
            
            if llave not in conversaciones:
                conversaciones[llave] = {
                    'otra_persona': otra_persona,
                    'mascota': msj.mascota,
                    'mensajes': [],
                    'ultimo_msj_id': msj.pk
                }
            
            conversaciones[llave]['mensajes'].append(msj)
            conversaciones[llave]['ultimo_msj_id'] = msj.pk

        conversaciones_ordenadas = sorted(
            conversaciones.values(),
            key=lambda x: x['mensajes'][-1].fecha_envio if x['mensajes'] else timezone.now(),
            reverse=True
        )
        
        context['conversaciones'] = conversaciones_ordenadas
        
        # NUEVO: Pasar las variables de sesión al contexto y limpiarlas inmediatamente de la BD
        context['chat_persona'] = self.request.session.pop('chat_abierto_persona', None)
        context['chat_mascota'] = self.request.session.pop('chat_abierto_mascota', None)
        
        return context