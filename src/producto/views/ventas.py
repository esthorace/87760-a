from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from producto.forms import VentaForm
from producto.models import Venta


class VentaList(LoginRequiredMixin, ListView):
    model = Venta
    # template_name = "producto/venta_list.html"
    # context_object_name = "ventas"

    def get_queryset(self) -> QuerySet:
        busqueda = self.request.GET.get("busqueda", "").strip()
        if busqueda:
            return Venta.objects.filter(
                Q(producto__nombre__icontains=busqueda) | Q(vendedor__user__username__icontains=busqueda)
            )
        else:
            return Venta.objects.all()


class VentaCreate(SuccessMessageMixin, CreateView):
    model = Venta
    form_class = VentaForm
    success_url = reverse_lazy("producto:venta_list")
    success_message = "La venta se ha creado existosamente"


class VentaUpdate(SuccessMessageMixin, UpdateView):
    model = Venta
    form_class = VentaForm
    success_url = reverse_lazy("producto:venta_list")
    success_message = "La venta se ha editado existosamente"


class VentaDetail(DetailView):
    model = Venta


class VentaDelete(SuccessMessageMixin, DeleteView):
    model = Venta
    success_url = reverse_lazy("producto:venta_list")
    success_message = "La venta se ha eliminado existosamente"
