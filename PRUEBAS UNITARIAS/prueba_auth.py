from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class AuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@demo.com', password='12345')

    def test_login_correcto(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertIn(response.status_code, (200, 302))

    def test_login_incorrecto(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'mal'})
        self.assertNotEqual(response.status_code, 302)

    def test_logout(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('logout'))
        self.assertIn(response.status_code, (200, 302))

    def test_registro_exitoso(self):
        response = self.client.post(reverse('registro'), {
            'username': 'nuevo_user',
            'email': 'nuevo@example.com',
            'password1': 'P@ssw0rd123',
            'password2': 'P@ssw0rd123'
        })
        self.assertIn(response.status_code, (200, 302))
        self.assertTrue(User.objects.filter(username='nuevo_user').exists())

    def test_registro_email_duplicado(self):
        User.objects.create_user(username='yaexiste', email='duplicado@example.com', password='12345')
        response = self.client.post(reverse('registro'), {
            'username': 'otro',
            'email': 'duplicado@example.com',
            'password1': '12345',
            'password2': '12345'
        })
        self.assertContains(response, 'email ya registrado', status_code=200)
