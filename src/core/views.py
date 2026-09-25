from datetime import UTC

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.forms import CustomAuthenticationForm, CustomUserCreationForm


def index(request: HttpRequest) -> HttpResponse:
    from datetime import datetime

    datos_a_plantilla = {"titulo": "EducaciónIt", "año": datetime.now(UTC).year}
    return render(request, "core/pages/index.html", context=datos_a_plantilla)


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = "core/login.html"
    authentication_form = CustomAuthenticationForm
    next_page = reverse_lazy("core:home")
    success_message = "Inicio de sesión exitoso"


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "core/register.html"
    success_url = reverse_lazy("core:login")
