from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from producto.forms import ProductoForm
from producto.models import Producto


class ProductoList(ListView):
    model = Producto
    # template_name = "producto/producto_list.html"
    # context_object_name = "productos"

    def get_queryset(self) -> QuerySet:
        busqueda = self.request.GET.get("busqueda", "").strip()
        if busqueda:
            return Producto.objects.filter(nombre__icontains=busqueda)
        else:
            return Producto.objects.all()


class ProductoCreate(SuccessMessageMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy("producto:producto_list")
    success_message = "El producto se ha creado existosamente"


class ProductoUpdate(SuccessMessageMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy("producto:producto_list")
    success_message = "El producto se ha editado existosamente"


class ProductoDetail(DetailView):
    model = Producto


class ProductoDelete(SuccessMessageMixin, DeleteView):
    model = Producto
    success_url = reverse_lazy("producto:producto_list")
    success_message = "El producto se ha eliminado existosamente"
