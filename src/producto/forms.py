from django import forms

from producto.models import Categoria


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = "__all__"

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre", "")
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener como mínimo 3 caracteres")
        return nombre
