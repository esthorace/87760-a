from datetime import UTC

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from core.forms import CustomAuthenticationForm


def index(request: HttpRequest) -> HttpResponse:
    from datetime import datetime

    datos_a_plantilla = {"titulo": "EducaciónIt", "año": datetime.now(UTC).year}
    return render(request, "core/pages/index.html", context=datos_a_plantilla)


class CustomLoginView(LoginView):
    template_name = "core/login.html"
    authentication_form = CustomAuthenticationForm
    next_page = reverse_lazy("core:home")
    # redirect_authenticated_user = True

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        messages.success(self.request, "Inicio de sesión exitoso")
        return super().form_valid(form)
