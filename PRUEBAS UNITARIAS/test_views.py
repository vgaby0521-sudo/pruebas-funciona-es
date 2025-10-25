Test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Producto, Carrito, ItemCarrito

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='cliente', password='12345')
        self.producto = Producto.objects.create(
            nombre='Vino Blanco',
            descripcion='Vino blanco español',
            precio=40000,
            stock=15
        )
        self.client.login(username='cliente', password='12345')

    # ---------------------------
    # 1. Prueba de la vista principal
    # ---------------------------
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    # ---------------------------
    # 2. Prueba del detalle de producto
    # ---------------------------
    def test_detalle_producto(self):
        response = self.client.get(reverse('detalle_producto', args=[self.producto.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.producto.nombre)

    # ---------------------------
    # 3. Agregar al carrito - flujo completo
    # ---------------------------
    def test_agregar_al_carrito_producto_nuevo(self):
        """Agrega un producto al carrito por primera vez."""
        response = self.client.post(reverse('agregar_carrito', args=[self.producto.id]), {'cantidad': 1})
        self.assertIn(response.status_code, (200, 302))
        self.assertTrue(Carrito.objects.filter(usuario=self.user).exists())

        carrito = Carrito.objects.get(usuario=self.user)
        item = ItemCarrito.objects.get(carrito=carrito, producto=self.producto)

        self.assertEqual(item.cantidad, 1)
        self.assertEqual(item.producto.nombre, 'Vino Blanco')

    def test_agregar_mismo_producto_incrementa_cantidad(self):
        """Agrega el mismo producto dos veces y verifica que se sume la cantidad."""
        self.client.post(reverse('agregar_carrito', args=[self.producto.id]), {'cantidad': 1})
        self.client.post(reverse('agregar_carrito', args=[self.producto.id]), {'cantidad': 2})

        carrito = Carrito.objects.get(usuario=self.user)
        item = ItemCarrito.objects.get(carrito=carrito, producto=self.producto)

        # Debería haber sumado las cantidades: 1 + 2 = 3
        self.assertEqual(item.cantidad, 3)

    def test_agregar_carrito_cantidad_superior_stock(self):
        """Evita agregar más cantidad que el stock disponible."""
        response = self.client.post(reverse('agregar_carrito', args=[self.producto.id]), {'cantidad': 99})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'cantidad no disponible')

    # ---------------------------
    # 4. Ver contenido del carrito
    # ---------------------------
    def test_ver_carrito_con_productos(self):
        """Verifica que la vista del carrito muestre los productos agregados."""
        self.client.post(reverse('agregar_carrito', args=[self.producto.id]), {'cantidad': 2})
        response = self.client.get(reverse('carrito'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vino Blanco')
        self.assertContains(response, '2')  # cantidad en el HTML