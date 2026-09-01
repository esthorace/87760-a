from datetime import UTC

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    from datetime import datetime

    datos_a_plantilla = {"titulo": "EducaciónIt", "año": datetime.now(UTC).year}
    return render(request, "core/index.html", context=datos_a_plantilla)


def saludar(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hola desde Django")


def parametros(request: HttpResponse, nombre: str, apellido: str) -> HttpResponse:
    nombre = nombre.capitalize()
    apellido = apellido.upper()
    return HttpResponse(f"<p><strong>{apellido}</strong>, {nombre}</p>")


def ver_notas(request: HttpRequest) -> HttpResponse:
    lista_notas: list[int] = [10, 9, 5, 3, 8, 5, 7]
    return render(request, "core/notas.html", {"notas": lista_notas})
