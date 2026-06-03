from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm
from .models import CustomUser, CodigoVerificacion

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        # Validación extra: Si no ha verificado su correo, no puede entrar
        if not user.correo_verificado:
            messages.error(self.request, 'Debes verificar tu correo electrónico antes de iniciar sesión.')
            self.request.session['email_verificacion'] = user.email
            return redirect('usuarios:verificar_registro')
        return super().form_valid(form)

class RegistroUsuarioView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'usuarios/registro.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True 
        user.save()
        
        # 1. Generar código en la BD
        codigo_obj = CodigoVerificacion.objects.create(usuario=user, tipo='REGISTRO')
        
        # 2. Enviar correo real
        send_mail(
            'Verifica tu cuenta en Findy',
            f'¡Hola {user.first_name}!\n\nTu código de verificación de 6 dígitos es: {codigo_obj.codigo}\n\nIngrésalo en la página para activar tu cuenta.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        # 3. Guardar en sesión para saber a quién verificar en la siguiente pantalla
        self.request.session['email_verificacion'] = user.email
        messages.success(self.request, '¡Registro exitoso! Te enviamos un código a tu correo.')
        return redirect('usuarios:verificar_registro')

class VerificarRegistroView(View):
    def get(self, request):
        if 'email_verificacion' not in request.session:
            return redirect('usuarios:login')
        return render(request, 'usuarios/verificar_codigo.html', {'titulo': 'Verificar Cuenta'})

    def post(self, request):
        email = request.session.get('email_verificacion')
        codigo_ingresado = request.POST.get('codigo')
        
        try:
            user = CustomUser.objects.get(email=email)
            # Buscar el último código de registro de este usuario
            codigo_bd = CodigoVerificacion.objects.filter(usuario=user, tipo='REGISTRO').last()
            
            if codigo_bd and codigo_bd.codigo == codigo_ingresado:
                user.correo_verificado = True
                user.save()
                codigo_bd.delete() # Se destruye al usarse
                del request.session['email_verificacion']
                messages.success(request, '¡Correo verificado! Ya puedes iniciar sesión.')
                return redirect('usuarios:login')
            else:
                messages.error(request, 'El código es incorrecto. Intenta nuevamente.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Error de usuario.')
        
        return render(request, 'usuarios/verificar_codigo.html', {'titulo': 'Verificar Cuenta'})

# ==========================================
# LÓGICA DE OLVIDÉ MI CONTRASEÑA
# ==========================================

class OlvidePasswordView(View):
    def get(self, request):
        return render(request, 'usuarios/olvide_password.html')
        
    def post(self, request):
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            # Borrar códigos anteriores para que no se acumulen
            CodigoVerificacion.objects.filter(usuario=user, tipo='PASSWORD').delete()
            
            codigo_obj = CodigoVerificacion.objects.create(usuario=user, tipo='PASSWORD')
            
            send_mail(
                'Recuperación de contraseña - Findy',
                f'Hola,\n\nTu código temporal de 6 dígitos para cambiar tu contraseña es: {codigo_obj.codigo}\n\nSi no solicitaste esto, ignora este mensaje.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            request.session['email_recuperacion'] = user.email
            messages.success(request, 'Te hemos enviado un código temporal a tu correo.')
            return redirect('usuarios:password_reset_verificar')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Si el correo existe en nuestro sistema, te enviaremos el código.')
            return redirect('usuarios:login')

class VerificarCodigoPasswordView(View):
    def get(self, request):
        if 'email_recuperacion' not in request.session:
            return redirect('usuarios:login')
        return render(request, 'usuarios/verificar_codigo.html', {'titulo': 'Recuperar Contraseña'})
        
    def post(self, request):
        email = request.session.get('email_recuperacion')
        codigo_ingresado = request.POST.get('codigo')
        
        try:
            user = CustomUser.objects.get(email=email)
            codigo_bd = CodigoVerificacion.objects.filter(usuario=user, tipo='PASSWORD').last()
            
            if codigo_bd and codigo_bd.codigo == codigo_ingresado:
                codigo_bd.delete() # Se destruye al usarse
                request.session['codigo_validado'] = True
                return redirect('usuarios:password_reset_nueva')
            else:
                messages.error(request, 'Código incorrecto.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Error de usuario.')
            
        return render(request, 'usuarios/verificar_codigo.html', {'titulo': 'Recuperar Contraseña'})

class NuevaPasswordView(View):
    def get(self, request):
        if not request.session.get('codigo_validado'):
            return redirect('usuarios:login')
        return render(request, 'usuarios/nueva_password.html')
        
    def post(self, request):
        if not request.session.get('codigo_validado'):
            return redirect('usuarios:login')
            
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password and password == password_confirm:
            email = request.session.get('email_recuperacion')
            user = CustomUser.objects.get(email=email)
            user.set_password(password)
            user.save()
            
            # Limpiamos las sesiones para cerrar la brecha de seguridad
            del request.session['email_recuperacion']
            del request.session['codigo_validado']
            
            messages.success(request, '¡Tu contraseña ha sido actualizada con éxito!')
            return redirect('usuarios:login')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
            
        return render(request, 'usuarios/nueva_password.html')