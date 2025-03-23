from django.contrib import admin
from django import forms
from .models import Pack
from productos.models import Producto

class PackAdminForm(forms.ModelForm):
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    def clean_productos(self):
        productos = self.cleaned_data.get('productos')
        if productos.count() != 3:
            raise forms.ValidationError("Debes seleccionar exactamente 3 productos para el pack.")
        return productos

    class Meta:
        model = Pack
        fields = '__all__'

class PackAdmin(admin.ModelAdmin):
    form = PackAdminForm

admin.site.register(Pack, PackAdmin)
