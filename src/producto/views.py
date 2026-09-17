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

    match request.method:
        case "POST":
            form = CategoriaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("producto:categoria_list")
        case _:
            form = CategoriaForm()
    return render(request, "producto/categoria_form.html", {"form": form})


def categoria_detail(request: HttpRequest, pk: int) -> HttpResponse:
    categoria = Categoria.objects.get(id=pk)
    return render(request, "producto/categoria_detail.html", {"categoria": categoria})


def categoria_update(request: HttpRequest, pk: int) -> HttpResponse:
    categoria = Categoria.objects.get(id=pk)

    match request.method:
        case "POST":
            form = CategoriaForm(request.POST, instance=categoria)
            if form.is_valid():
                form.save()
                return redirect("producto:categoria_list")
        case _:
            form = CategoriaForm(instance=categoria)

    return render(request, "producto/categoria_form.html", {"form": form})


def categoria_delete(request: HttpRequest, pk: int) -> HttpResponse:
    categoria = Categoria.objects.get(id=pk)
    match request.method:
        case "POST":
            categoria.delete()
            return redirect("producto:categoria_list")
        case _:
            return render(request, "producto/categoria_confirm_delete.html", {"categoria": categoria})
