from django.test import SimpleTestCase
from django.urls import reverse, resolve
from shop import views

class UrlsTest(SimpleTestCase):
    def test_url_home_resuelve(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.home)

    def test_url_login_resuelve(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, views.login_view)

    def test_url_carrito_resuelve(self):
        url = reverse('carrito')
        self.assertEqual(resolve(url).func, views.ver_carrito)
