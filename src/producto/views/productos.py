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


class ProductoCreate(CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy("producto:producto_list")


class ProductoUpdate(UpdateView):
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy("producto:producto_list")


class ProductoDetail(DetailView):
    model = Producto


class ProductoDelete(DeleteView):
    model = Producto
    success_url = reverse_lazy("producto:producto_list")
