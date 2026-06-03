from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

# Obtenemos nuestro CustomUser de forma segura
User = get_user_model()

class UsuarioTests(TestCase):
    def setUp(self):
        """Configuración inicial: se ejecuta antes de cada prueba individual."""
        self.user_data = {
            'username': 'testuser',  
            'email': 'test@correo.com',
            'password': 'SuperPassword123!',
            'first_name': 'Usuario',
            'last_name': 'Prueba'
        }
        # Creamos un usuario en la base de datos temporal
        self.user = User.objects.create_user(**self.user_data)

    def test_modelo_usuario(self):
        """1. Test de modelo: Verifica que CustomUser use email como identificador."""
        self.assertEqual(self.user.email, 'test@correo.com')
        self.assertTrue(self.user.check_password('SuperPassword123!'))
        self.assertTrue(self.user.is_active)

    def test_registro_usuario(self):
        """2. Test de registro: Verifica que la página de registro cargue correctamente."""
        response = self.client.get(reverse('usuarios:registro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/registro.html')

    def test_login_usuario(self):
        """3. Test de login: Verifica que el sistema permita iniciar sesión con credenciales válidas."""
        # Simulamos un inicio de sesión en el cliente de pruebas (Usando el email, como lo pide nuestro sistema)
        login_exitoso = self.client.login(email='test@correo.com', password='SuperPassword123!')
        self.assertTrue(login_exitoso)