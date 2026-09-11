from django.urls import path

from producto import views

app_name = "producto"

urlpatterns = [
    path("", views.index, name="home"),
    path("categoria/list", views.categoria_list, name="categoria_list"),
    path("categoria/create", views.categoria_create, name="categoria_create"),
    path("categoria/detail/<int:pk>", views.categoria_detail, name="categoria_detail"),
    path("categoria/update/<int:pk>", views.categoria_update, name="categoria_update"),
    path("categoria/delete/<int:pk>", views.categoria_delete, name="categoria_delete"),
]
