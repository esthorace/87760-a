from typing import Any

from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().__init__(request, *args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Nombre de usuario"})
        self.fields["password"].widget.attrs.update({"placeholder": "Contraseña"})
