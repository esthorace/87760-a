from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from producto.models import Categoria


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "producto/index.html")


def categoria_list(request: HttpRequest) -> HttpResponse:
    categorias = Categoria.objects.all()
    return render(request, "producto/categoria_list.html", {"categorias": categorias})
