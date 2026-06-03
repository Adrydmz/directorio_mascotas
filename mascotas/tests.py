from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import MascotaPerdida

User = get_user_model()

class MascotaTests(TestCase):
    def setUp(self):
        """Configuración inicial: creamos el usuario necesario para la llave foránea."""
        self.user = User.objects.create_user(username='admin', email='admin@correo.com', password='Password123!')

    def test_creacion_entidad(self):
        """4. Test de creación de entidad: Verifica que la entidad principal se guarde en BD."""
        mascota = MascotaPerdida.objects.create(
            nombre='Mascota Test',
            especie='PERRO',
            raza='Labrador',
            ubicacion='Centro de la ciudad',
            estado='PERDIDA',
            usuario_reporta=self.user
        )
        # Verificamos que ahora exista exactamente 1 mascota en la base de datos temporal
        self.assertEqual(MascotaPerdida.objects.count(), 1)
        self.assertEqual(mascota.nombre, 'Mascota Test')

    def test_vista_protegida(self):
        """5. Test de vista protegida: Verifica el bloqueo a usuarios anónimos."""
        url_crear = reverse('mascotas:crear_mascota')
        
        # Escenario A: Usuario anónimo intenta entrar -> Debe ser redirigido (Código 302)
        response_anonimo = self.client.get(url_crear)
        self.assertEqual(response_anonimo.status_code, 302)
        
        # Escenario B: Usuario inicia sesión y vuelve a intentar -> Acceso permitido (Código 200)
        self.client.login(email='admin@correo.com', password='Password123!')
        response_autenticado = self.client.get(url_crear)
        self.assertEqual(response_autenticado.status_code, 200)