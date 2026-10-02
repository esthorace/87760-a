from django import forms

from producto.models import Categoria, Producto, Vendedor, Venta


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = "__all__"

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre", "")
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener como mínimo 3 caracteres")
        return nombre


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"

    def clean_precio(self):
        precio = self.cleaned_data.get("precio")
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio no puede ser menor a 0")
        return precio


class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = "__all__"


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = "__all__"

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get("cantidad")
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a 0")
        return cantidad
