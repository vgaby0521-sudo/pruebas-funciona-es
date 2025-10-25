from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from shop.models import Producto, Pedido

class FlujoCompraTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='cliente', password='12345')
        self.producto = Producto.objects.create(
            nombre='Vino Reserva',
            descripcion='Vino argentino',
            precio=60000,
            stock=8
        )

    def test_flujo_completo_compra(self):
        login = self.client.login(username='cliente', password='12345')
        self.assertTrue(login)

        # Agregar producto al carrito
        response = self.client.get(reverse('agregar_carrito', args=[self.producto.id]))
        self.assertIn(response.status_code, (200, 302))

        # Ver carrito
        response = self.client.get(reverse('carrito'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.producto.nombre)

        # Checkout
        response = self.client.post(reverse('checkout'))
        self.assertIn(response.status_code, (200, 302))

        # Verificar pedido creado
        self.assertTrue(Pedido.objects.filter(usuario=self.user).exists())

    def test_agregar_cantidad_superior_stock(self):
        self.client.login(username='cliente', password='12345')
        response = self.client.post(reverse('agregar_carrito', args=[self.producto.id]), {'cantidad': 99})
        self.assertContains(response, 'cantidad no disponible', status_code=200)
