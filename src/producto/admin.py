from django.contrib import admin

from producto.models import Categoria, Producto

admin.site.register(Categoria)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("categoria", "nombre", "precio", "stock")
    list_display_links = ("nombre",)
    list_filter = ("categoria",)
    search_fields = ("nombre",)
