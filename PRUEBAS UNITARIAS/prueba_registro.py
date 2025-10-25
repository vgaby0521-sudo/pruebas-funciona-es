from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Producto

class RegistroBusquedaTest(TestCase):
    def setUp(self):
        self.client = Client()
        Producto.objects.create(nombre='Vino Tinto Premium', descripcion='Seco', precio=50000, stock=8)

    def test_busqueda_producto_existente(self):
        response = self.client.get(reverse('busqueda') + '?q=vino tinto')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vino Tinto')

    def test_busqueda_sin_resultados(self):
        response = self.client.get(reverse('busqueda') + '?q=xyz-no-existe')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'no se encontraron productos')
