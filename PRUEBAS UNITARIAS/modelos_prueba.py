from django.test import TestCase
from django.apps import apps

class ProductoModelTest(TestCase):
    def setUp(self):
        self.Producto = apps.get_model('shop', 'Producto')

    def test_creacion_producto(self):
        producto = self.Producto.objects.create(
            nombre='Vino Tinto',
            descripcion='Botella de vino tinto chileno 750ml',
            precio=35000,
            stock=10
        )
        self.assertEqual(producto.nombre, 'Vino Tinto')
        self.assertTrue(producto.stock > 0)
        self.assertIsNotNone(producto.id)

    def test_str_producto(self):
        producto = self.Producto(nombre='Vino Rosado', precio=25000)
        self.assertIn('Vino', str(producto))
