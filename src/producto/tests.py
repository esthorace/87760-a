from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from producto.forms import VentaForm
from producto.models import Producto, Vendedor, Venta


class VentaStockTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="vendedor", password="pass")
        self.vendedor = Vendedor.objects.create(user=self.user)
        self.producto = Producto.objects.create(
            nombre="Teclado", precio=100, stock=10
        )

    def test_crear_venta_descuenta_stock(self):
        Venta.objects.create(
            vendedor=self.vendedor, producto=self.producto, cantidad=3
        )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 7)

    def test_no_permite_vender_mas_que_el_stock(self):
        with self.assertRaises(ValidationError):
            Venta.objects.create(
                vendedor=self.vendedor, producto=self.producto, cantidad=11
            )
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 10)
        self.assertEqual(Venta.objects.count(), 0)

    def test_editar_venta_ajusta_stock(self):
        venta = Venta.objects.create(
            vendedor=self.vendedor, producto=self.producto, cantidad=3
        )
        venta.cantidad = 5
        venta.save()
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 5)

    def test_eliminar_venta_reponer_stock(self):
        venta = Venta.objects.create(
            vendedor=self.vendedor, producto=self.producto, cantidad=4
        )
        venta.delete()
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 10)

    def test_formulario_rechaza_cantidad_mayor_al_stock(self):
        form = VentaForm(
            data={
                "vendedor": self.vendedor.pk,
                "producto": self.producto.pk,
                "cantidad": 11,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("producto", form.errors)
