from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from core import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(template_name="core/logout.html"), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("about/", TemplateView.as_view(template_name="core/pages/about.html"), name="about"),
]

# urls viejas
# urlpatterns += [
#     path("saludar/", views.saludar, name="saludar"),
#     path("parametros/<str:nombre>/<str:apellido>/", views.parametros, name="parametros"),
#     path("notas/", views.ver_notas, name="notas"),
# ]
