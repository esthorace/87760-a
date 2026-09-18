from django.urls import path
from django.views.generic import TemplateView

from producto.views import categorias, productos

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
