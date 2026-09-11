from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from producto.forms import CategoriaForm
from producto.models import Categoria


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "producto/index.html")


def categoria_list(request: HttpRequest) -> HttpResponse:
    categorias = Categoria.objects.all()
    return render(request, "producto/categoria_list.html", {"categorias": categorias})


def categoria_create(request: HttpRequest) -> HttpResponse:
    form = CategoriaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("producto:categoria_list")

    return render(request, "producto/categoria_form.html", {"form": form})
