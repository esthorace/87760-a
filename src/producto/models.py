from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import F, Q


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(
        blank=True, db_default="", verbose_name="descripción"
    )

    class Meta:
        verbose_name = "Categoría de Productos"
        verbose_name_plural = "Categorías de Productos"
        ordering = ("nombre",)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="categoría",
        related_name="productos",
    )
    nombre = models.CharField()
    descripcion = models.TextField(
        blank=True, db_default="", verbose_name="descripción"
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(db_default=0)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ("nombre",)
        indexes = [  # noqa: RUF012
            models.Index(fields=["nombre"], name="idx_producto_nombre"),
        ]
        constraints = (
            models.UniqueConstraint(
                fields=["categoria", "nombre"], name="unique_categoria_producto"
            ),
            models.CheckConstraint(
                condition=Q(precio__gte=0), name="check_precio_mayor_a_cero"
            ),
        )

    def __str__(self) -> str:
        if self.categoria:
            return f"{self.categoria} - {self.nombre}"
        return self.nombre

    def descontar_stock(self, cantidad):
        unidades = int(cantidad)
        if unidades <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        actualizados = Producto.objects.filter(pk=self.pk, stock__gte=unidades).update(
            stock=F("stock") - unidades
        )
        if not actualizados:
            raise ValidationError("El producto no tiene stock suficiente")
        self.refresh_from_db(fields=["stock"])

    def reponer_stock(self, cantidad):
        unidades = int(cantidad)
        if unidades <= 0:
            return
        Producto.objects.filter(pk=self.pk).update(stock=F("stock") + unidades)
        self.refresh_from_db(fields=["stock"])


class Vendedor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    telefono = models.CharField(max_length=15, blank=True, verbose_name="Teléfono")
    imagen_perfil = models.ImageField(
        upload_to="perfiles_vendedores/",
        blank=True,
        null=True,
        verbose_name="Imagen de Perfil",
    )

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = "Vendedor"
        verbose_name_plural = "Vendedores"


class Venta(models.Model):
    vendedor = models.ForeignKey(
        Vendedor, on_delete=models.CASCADE, verbose_name="Vendedor"
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, verbose_name="Producto"
    )
    cantidad = models.FloatField(verbose_name="Cantidad")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de la Venta")

    def __str__(self):
        return f"Venta de {self.producto.nombre} por {self.vendedor.user.username} ({self.cantidad} unidades)"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                venta_anterior = Venta.objects.select_related("producto").get(pk=self.pk)
                venta_anterior.producto.reponer_stock(venta_anterior.cantidad)
            super().save(*args, **kwargs)
            producto = Producto.objects.get(pk=self.producto_id)
            producto.descontar_stock(self.cantidad)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            producto = Producto.objects.get(pk=self.producto_id)
            producto.reponer_stock(self.cantidad)
            return super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
