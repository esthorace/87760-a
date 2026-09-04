from django.urls import path

from producto import views

app_name = "producto"

urlpatterns = [
    path("", views.index, name="home"),
]
