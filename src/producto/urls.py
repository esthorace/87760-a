from django.urls import path
from django.views.generic import TemplateView

from producto.views import categorias, productos, vendedores, ventas

app_name = "producto"

urlpatterns = [
    path("", TemplateView.as_view(template_name="producto/index.html"), name="home"),
]

urlpatterns += [
    path("categoria/list", categorias.categoria_list, name="categoria_list"),
    path("categoria/create", categorias.categoria_create, name="categoria_create"),
    path("categoria/detail/<int:pk>", categorias.categoria_detail, name="categoria_detail"),
    path("categoria/update/<int:pk>", categorias.categoria_update, name="categoria_update"),
    path("categoria/delete/<int:pk>", categorias.categoria_delete, name="categoria_delete"),
]

urlpatterns += [
    path("producto/list", productos.ProductoList.as_view(), name="producto_list"),
    path("producto/create", productos.ProductoCreate.as_view(), name="producto_create"),
    path("producto/detail/<int:pk>", productos.ProductoDetail.as_view(), name="producto_detail"),
    path("producto/update/<int:pk>", productos.ProductoUpdate.as_view(), name="producto_update"),
    path("producto/delete/<int:pk>", productos.ProductoDelete.as_view(), name="producto_delete"),
]

urlpatterns += [
    path("vendedor/list", vendedores.VendedorList.as_view(), name="vendedor_list"),
    path("vendedor/create", vendedores.VendedorCreate.as_view(), name="vendedor_create"),
    path("vendedor/detail/<int:pk>", vendedores.VendedorDetail.as_view(), name="vendedor_detail"),
    path("vendedor/update/<int:pk>", vendedores.VendedorUpdate.as_view(), name="vendedor_update"),
    path("vendedor/delete/<int:pk>", vendedores.VendedorDelete.as_view(), name="vendedor_delete"),
]

urlpatterns += [
    path("venta/list", ventas.VentaList.as_view(), name="venta_list"),
    path("venta/create", ventas.VentaCreate.as_view(), name="venta_create"),
    path("venta/detail/<int:pk>", ventas.VentaDetail.as_view(), name="venta_detail"),
    path("venta/update/<int:pk>", ventas.VentaUpdate.as_view(), name="venta_update"),
    path("venta/delete/<int:pk>", ventas.VentaDelete.as_view(), name="venta_delete"),
]
