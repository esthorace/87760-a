from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from producto.forms import CategoriaForm
from producto.models import Categoria


def categoria_list(request: HttpRequest) -> HttpResponse:
    busqueda = request.GET.get("busqueda", "").strip()
    if busqueda:
        categorias = Categoria.objects.filter(nombre__icontains=busqueda)
    else:
        categorias = Categoria.objects.all()

    return render(request, "producto/categoria_list.html", {"categorias": categorias})


def categoria_create(request: HttpRequest) -> HttpResponse:

    match request.method:
        case "POST":
            form = CategoriaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "La categoría fue creada exitosamente")
                return redirect("producto:categoria_list")
        case _:
            form = CategoriaForm()
    return render(request, "producto/categoria_form.html", {"form": form})


def categoria_detail(request: HttpRequest, pk: int) -> HttpResponse:
    categoria = get_object_or_404(Categoria, id=pk)
    return render(request, "producto/categoria_detail.html", {"categoria": categoria})


def categoria_update(request: HttpRequest, pk: int) -> HttpResponse:
    categoria = get_object_or_404(Categoria, id=pk)
    match request.method:
        case "POST":
            form = CategoriaForm(request.POST, instance=categoria)
            if form.is_valid():
                form.save()
                messages.success(request, "La categoría fue editada exitosamente")
                return redirect("producto:categoria_list")
        case _:
            form = CategoriaForm(instance=categoria)

    return render(request, "producto/categoria_form.html", {"form": form})


def categoria_delete(request: HttpRequest, pk: int) -> HttpResponse:
    categoria = get_object_or_404(Categoria, id=pk)
    match request.method:
        case "POST":
            categoria.delete()
            messages.success(request, "La categoría fue eliminada exitosamente")
            return redirect("producto:categoria_list")
        case _:
            return render(request, "producto/categoria_confirm_delete.html", {"categoria": categoria})
