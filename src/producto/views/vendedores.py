from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from producto.forms import VendedorForm
from producto.models import Vendedor


class VendedorList(LoginRequiredMixin, ListView):
    model = Vendedor
    # template_name = "producto/vendedor_list.html"
    # context_object_name = "vendedores"

    def get_queryset(self) -> QuerySet:
        busqueda = self.request.GET.get("busqueda", "").strip()
        if busqueda:
            return Vendedor.objects.filter(
                Q(user__username__icontains=busqueda) | Q(telefono__icontains=busqueda)
            )
        else:
            return Vendedor.objects.all()


class VendedorCreate(SuccessMessageMixin, CreateView):
    model = Vendedor
    form_class = VendedorForm
    success_url = reverse_lazy("producto:vendedor_list")
    success_message = "El vendedor se ha creado existosamente"


class VendedorUpdate(SuccessMessageMixin, UpdateView):
    model = Vendedor
    form_class = VendedorForm
    success_url = reverse_lazy("producto:vendedor_list")
    success_message = "El vendedor se ha editado existosamente"


class VendedorDetail(DetailView):
    model = Vendedor


class VendedorDelete(SuccessMessageMixin, DeleteView):
    model = Vendedor
    success_url = reverse_lazy("producto:vendedor_list")
    success_message = "El vendedor se ha eliminado existosamente"
