from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    datos_a_plantilla = {"titulo": "EducaciónIt", "año": 2026}
    return render(request, "core/index.html", context=datos_a_plantilla)


def saludar(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hola desde Django")
