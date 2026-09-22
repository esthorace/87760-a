from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import TextInput

# class CustomAuthenticationForm(AuthenticationForm):
#     username = forms.CharField(
#         label="Usuario",
#         widget=forms.TextInput(
#             attrs={"class": "form-control", "placeholder": "Ingresa tu nombre de usuario"}
#         ),
#     )
#     password = forms.CharField(
#         label="Contraseña",
#         widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "········"}),
#     )


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = AuthenticationForm
        fields = ("username", "password")
