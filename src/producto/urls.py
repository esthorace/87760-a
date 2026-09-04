from django.urls import path

from producto import views

app_name = "producto"

urlpatterns = [
    path("", views.index, name="home"),
    path("categoria/list", views.categoria_list, name="categoria_list"),
]
